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
import re
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
# -------------------------------------------------------------------------------------------------------------------
# 세 번째 페이지: 지역 선택 페이지
def thema_view(request):
    return render(request, 'thema.html')

# -------------------------------------------------------------------------------------------------------------------
# 세 번째 페이지: 독립 선택 페이지
def independence_view(request):
    descriptions = ["문학으로 아픔을 풀어낸 독립운동가", "전장을 누볐던 무장 독립투사", "항일의 빛, 계몽의 사자"]
    assistants_by_description = {}

    # 각 description에 맞는 어시스턴트 데이터를 가져옴
    for description in descriptions:
        assistants_by_description[description] = Assistant.objects.filter(description=description)

    return render(request, 'independence.html', {'assistants_by_description': assistants_by_description})

# -------------------------------------------------------------------------------------------------------------------
# 네 번째 페이지: 독립 선택 페이지
def sommelier_view(request):
    descriptions = ["트랜디한 전통주 와이너리", "막걸리로 즐기는 전통주", "역사가 담긴 한 잔, 안동소주", "파티와 함께하는 이색 전통주"]
    assistants_by_description = {}

    # 각 description에 맞는 어시스턴트 데이터를 갖옴
    for description in descriptions:
        assistants_by_description[description] = Assistant.objects.filter(description=description)

    return render(request, 'sommelier.html', {'assistants_by_description': assistants_by_description})

# -------------------------------------------------------------------------------------------------------------------
# 다섯 번째 페이지: 독립 선택 페이지
def lounge_view(request):
    descriptions = ["Hahoe Village, curved like a lotus flower", "Dosanseowon, a place of Joseon wisdom", "Byeongsan Seowon, like a beautiful folding screen", "Sad love in the moonlight", "Enjoy a fun round of mask dance in Andong"]
    assistants_by_description = {}

    # 각 description에 맞는 어시스턴트 데이터를 갖옴
    for description in descriptions:
        assistants_by_description[description] = Assistant.objects.filter(description=description)

    return render(request, 'lounge.html', {'assistants_by_description': assistants_by_description})

# -------------------------------------------------------------------------------------------------------------------
# 검색 페이지
def search_results_view(request):
    query = request.GET.get('query')
    results = Assistant.objects.filter(name__icontains=query)  # 이름 기준으로 검색
    return render(request, 'search_results.html', {'query': query, 'results': results})

# -------------------------------------------------------------------------------------------------------------------
# 챗봇 페이지 렌더링
def chatbot_view(request, id):
    # 새로운 어시스턴트로 이동할 때 세션에서 스레드 ID 삭제
    request.session.pop('thread_id', None)

    assistant = get_object_or_404(Assistant, id=id)

    # 질문을 리스트로 준비
    questions = [
        assistant.question_1,
        assistant.question_2,
        assistant.question_3,
        assistant.question_4,
        assistant.question_5,
        assistant.question_6,
        assistant.question_7,
        assistant.question_8,
        assistant.question_9,
        assistant.question_10,
    ]

    questions = [q for q in questions if q]  # None 값 제외

    return render(request, 'chatbot.html', {
        'assistant': assistant,
        'id': assistant.id,
        'assistant_id': assistant.assistant_id,
        'document_id': assistant.document_id,
        'assistant_name': assistant.name,
        'questions': questions,
        'welcome_message': assistant.welcome_message
    })


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------------------------------------------------------------------------------------------
# 챗봇 페이지 렌더링
def lounge_chatbot_view(request, id):
    # 새로운 어시스턴트로 이동할 때 세션에서 스레드 ID 삭제
    request.session.pop('thread_id', None)

    assistant = get_object_or_404(Assistant, id=id)

    # 질문을 리스트로 준비
    questions = [
        assistant.question_1,
        assistant.question_2,
        assistant.question_3,
        assistant.question_4,
        assistant.question_5,
        assistant.question_6,
        assistant.question_7,
        assistant.question_8,
        assistant.question_9,
        assistant.question_10,
    ]

    questions = [q for q in questions if q]  # None 값 제외

    return render(request, 'lounge_chatbot.html', {
        'assistant': assistant,
        'id': assistant.id,
        'assistant_id': assistant.assistant_id,
        'document_id': assistant.document_id,
        'assistant_name': assistant.name,
        'questions': questions,
        'welcome_message': assistant.welcome_message
    })


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------------------------------------------------------------------------------------------
# 메모리움 페이지 렌더링
def memorium_chatbot_view(request, id):
    # 새로운 어시스턴트로 이동할 때 세션에서 스레드 ID 삭제
    request.session.pop('thread_id', None)

    assistant = get_object_or_404(Assistant, id=id)

    # 질문을 리스트로 준비
    questions = [
        assistant.question_1,
        assistant.question_2,
        assistant.question_3,
        assistant.question_4,
        assistant.question_5,
        assistant.question_6,
        assistant.question_7,
        assistant.question_8,
        assistant.question_9,
        assistant.question_10,
    ]

    questions = [q for q in questions if q]  # None 값 제외

    return render(request, 'memorium_chatbot.html', {
        'assistant': assistant,
        'id': assistant.id,
        'assistant_id': assistant.assistant_id,
        'document_id': assistant.document_id,
        'assistant_name': assistant.name,
        'questions': questions,
        'welcome_message': assistant.welcome_message
    })


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# -------------------------------------------------------------------------------------------------------------------
# 응답 처리 시 메타데이터 제거
def clean_response(text):
    return re.sub(r'【.*?】', '', text).strip()

class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()  # 상위 클래스 초기화 호출
        self.responses = []

    @override
    def on_text_created(self, text) -> None:
        # clean_text = clean_response(text.value)  # 'text.value'로 문자열을 추출
        # self.responses.append(clean_text)
        pass

    @override
    def on_message_done(self, message) -> None:
        message_content = message.content[0].text.value  # 'text.value'로 문자열 추출
        clean_text = clean_response(message_content)  # 메타데이터 제거 후 추가
        self.responses.append(clean_text)



# Chatbot API (질문을 받아 OpenAI로 처리)
class ChatbotAPIView(APIView):

    def post(self, request, id):
        logger.debug(f"Request Data: {request.data}")

        # assistant_id와 document_id는 DB에서 가져옴
        assistant = get_object_or_404(Assistant, id=id)
        assistant_id = request.data.get('assistant_id')
        document_id = request.data.get('document_id')
        question = request.data.get('question')


        # 기존 스레드를 사용하지 않고, 항상 새로운 스레드를 생성
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
                ],
            )
            thread_id = thread.id  # 새로 생성된 스레드 ID 저장

            event_handler = EventHandler()
            with client.beta.threads.runs.stream(
                    thread_id=thread_id,
                    assistant_id=assistant_id,
                    instructions=f"""
                    당신은 '{assistant.name}'입니다.
                    - 사람과 대화하듯이 억양을 질문에 대한 답변을 해주세요. 특히 '{assistant.name}'이 사람일 경우 그 인물의 성격을 이용하여 답변해주세요.
                    - 첨부된 파일에는 '{assistant.name}'와 관련된 여러 질문(Qn)과 답변(An)이 포함되어 있습니다.
                    - 사용자의 질문과 일치하거나 가장 유사한 질문을 찾아서 그에 대응하는 답변을 정확히 제공합니다.
                    - 이전의 맥락을 무시하고, 파일에 있는 정보만을 바탕으로 답변하세요.
                    """,
                    event_handler=event_handler,
            ) as stream:
                stream.until_done()

            # 스레드 사용 후 자동 삭제
            client.beta.threads.delete(thread_id)

            logger.debug(f"Responses collected: {event_handler.responses}")

            return Response({"response": event_handler.responses}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

