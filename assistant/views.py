from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Province, CityCountyTown, Assistant
from .serializers import ProvinceSerializer, AssistantSerializer, CityCountyTownSerializer
from django.http import StreamingHttpResponse, JsonResponse
import time
# import openai
import os

from typing_extensions import override
from openai import OpenAI, AssistantEventHandler
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import logging
logger = logging.getLogger(__name__)


# -------------------------------------------------------------
# 첫 번째 페이지: 추천 페이지
def main_view(request):
    descriptions = ["라운지(여행공간)와 함께하는 안동 여행", "데이트 코스로 제격", "로컬 음식에 담긴 이야기"]
    assistants_by_description = {}

    # 각 description에 맞는 어시스턴트 데이터를 가져옴
    for description in descriptions:
        assistants_by_description[description] = Assistant.objects.filter(description=description)

    return render(request, 'main.html', {'assistants_by_description': assistants_by_description})

# -------------------------------------------------------------
# 두 번째 페이지: 지역 선택 페이지
def local_view(request):
    return render(request, 'local.html')

# 도 목록 API
class ProvinceListView(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

# 시/군/읍 목록 API
class CityCountyTownListView(generics.ListAPIView):
    serializer_class = CityCountyTownSerializer

    def get_queryset(self):
        province_name = self.request.query_params.get('province')
        if province_name:
            return CityCountyTown.objects.filter(province__name=province_name)
        return CityCountyTown.objects.none()

# 어시스턴트 목록 API
class AssistantListView(generics.ListAPIView):
    serializer_class = AssistantSerializer

    def get_queryset(self):
        province_name = self.request.query_params.get('province')
        city_name = self.request.query_params.get('city_county_town')
        if province_name and city_name:
            return Assistant.objects.filter(city_county_town__name=city_name, city_county_town__province__name=province_name)
        return Assistant.objects.none()
# -------------------------------------------------------------
# Chatbot 클래스 기반 뷰
def chatbot_view(request, id):
    assistant = get_object_or_404(Assistant, id=id)

    return render(request, 'chatbot.html', {
        'id': assistant.id,
        'assistant_id': assistant.assistant_id,
        'document_id': assistant.document_id,
        'assistant_name': assistant.name
    })

# 챗봇 페이지 렌더링
# openai.api_key = os.getenv("OPENAI_API_KEY")
# OpenAI 클라이언트 설정
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 이벤트 핸들러 정의 (스트리밍 응답 처리)
# class EventHandler(AssistantEventHandler):
#     @override
#     def on_text_created(self, text) -> None:
#         print(f"\nassistant > {text}", end="", flush=True)
#
#     @override
#     def on_tool_call_created(self, tool_call):
#         print(f"\nassistant > {tool_call.type}\n", flush=True)
#
#     @override
#     def on_message_done(self, message) -> None:
#         message_content = message.content[0].text
#         annotations = message_content.annotations
#         citations = []
#         for index, annotation in enumerate(annotations):
#             message_content.value = message_content.value.replace(
#                 annotation.text, f"[{index}]"
#             )
#             if file_citation := getattr(annotation, "file_citation", None):
#                 cited_file = client.files.retrieve(file_citation.file_id)
#                 citations.append(f"[{index}] {cited_file.filename}")
#
#         print(message_content.value)
#         print("\n".join(citations))

class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()  # 상위 클래스 초기화 호출
        self.responses = []

    @override
    def on_text_created(self, text) -> None:
        self.responses.append(text)

    @override
    def on_message_done(self, message) -> None:
        message_content = message.content[0].text
        self.responses.append(message_content)



# Chatbot API (질문을 받아 OpenAI로 처리)
class ChatbotAPIView(APIView):

    def post(self, request, id):
        logger.debug(f"Request Data: {request.data}")

        # assistant_id와 document_id는 DB에서 가져옴
        assistant_id = request.data.get('assistant_id')  # 프론트엔드에서 전달된 값 또는 DB에서 가져오기
        document_id = request.data.get('document_id')  # 프론트엔드에서 전달된 값 또는 DB에서 가져오기
        question = request.data.get('question')  # 사용자가 입력한 질문

        # 로그로 데이터 확인
        logger.debug(f"Assistant ID: {assistant_id}, Document ID: {document_id}, Question: {question}")

        # 데이터가 없는 경우에 대한 오류 처리 추가
        if not assistant_id or not document_id or not question:
            return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)


        # 이벤트 핸들러 생성
        event_handler = EventHandler()

        # 스레드 생성 및 스트리밍 처리
        try:
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": question,
                        "attachments": [
                            {"file_id": document_id, "tools": [{"type": "file_search"}]}
                        ]
                    }
                ]
            )

            with client.beta.threads.runs.stream(
                    thread_id=thread.id,
                    assistant_id=assistant_id,
                    instructions="Please use the attached file to answer the user's question.",
                    event_handler=event_handler,
            ) as stream:
                stream.until_done()

            # 응답이 제대로 수집되었는지 로그로 확인
            logger.debug(f"Responses collected: {event_handler.responses}")

            # 여기서는 실시간 출력이 콘솔로 이루어지므로 따로 응답을 반환하지 않음
            return Response({"response": event_handler.responses}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")  # 에러 로그 추가
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # GPT-4 실시간 스트림 응답 처리
# def gpt_response_stream(request, id):
#     assistant = get_object_or_404(Assistant, id=id)
#     assistant_id = assistant.assistant_variable  # MySQL에서 저장된 어시스턴트 변수 가져오기
#
#     print(f"Assistant ID: {assistant_id}")  # 어시스턴트 ID 출력
#
#     question = request.GET.get('question', '').strip()
#     print(f"Received question: {question}")  # 사용자 질문 출력
#
#     def stream():
#         if question:
#             try:
#                 print("Calling OpenAI API...")  # OpenAI API 호출 전 출력
#                 # OpenAI API를 통해 어시스턴트 호출
#
#                 system_message = (
#                     f"당신은 {assistant.name} 입니다. "
#                     f"만약 사용자가 당신이 누구인지 묻는다면, 인공지능이라고 하지 말고, 주제에 맞는 역할로 답해주세요. "
#                     f"예를 들어, 당신이 역사적 인물이라면 그 인물의 말투와 성격에 맞추어 답변을 제공하세요. "
#                     f"상황에 따라 겸손하거나 진중한 말투로 이야기하며, 적절히 예의를 갖추어 답변하세요."
#                 )
#
#                 # OpenAI API를 통해 어시스턴트 호출
#                 response = openai.ChatCompletion.create(
#                     model="gpt-4",
#                     messages=[
#                         {"role": "system", "content": system_message},
#                         {"role": "user", "content": question},
#                     ],
#                     stream=True
#                 )
#                 print("API call successful")  # API 호출 성공 시 출력
#
#                 for chunk in response:
#                     chunk_message = chunk['choices'][0]['delta'].get('content', '')
#                     if chunk_message:
#                         print(f"Chunk message: {chunk_message}")  # 받아온 chunk 메시지 출력
#                         for char in chunk_message:
#                             yield f"data: {char}\n\n"
#                             time.sleep(0.05)
#                 yield 'event: DONE\ndata: \n\n'
#             except openai.OpenAIError as e:
#                 print(f"OpenAI Error: {e}")  # 오류 발생 시 오류 내용 출력
#                 yield f"data: Error: {str(e)}\n\n"
#         else:
#             print("No question provided")  # 질문이 없을 경우 출력
#             yield 'data: No question provided\n\n'
#
#     return StreamingHttpResponse(stream(), content_type='text/event-stream')

# 세 번째 페이지: 지역 선택 페이지
def thema_view(request):
    return render(request, 'thema.html')

# 세 번째 페이지: 독립 선택 페이지
def independence_view(request):
    descriptions = ["문학으로 아픔을 풀어낸 독립운동가", "전장을 누볐던 무장 독립투사", "항일의 빛, 계몽의 사자"]
    assistants_by_description = {}

    # 각 description에 맞는 어시스턴트 데이터를 가져옴
    for description in descriptions:
        assistants_by_description[description] = Assistant.objects.filter(description=description)

    return render(request, 'independence.html', {'assistants_by_description': assistants_by_description})

def search_results_view(request):
    query = request.GET.get('query')
    results = Assistant.objects.filter(name__icontains=query)  # 이름 기준으로 검색
    return render(request, 'search_results.html', {'query': query, 'results': results})
