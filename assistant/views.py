from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Province, CityCountyTown, Assistant
from .serializers import ProvinceSerializer, AssistantSerializer, CityCountyTownSerializer
from django.http import StreamingHttpResponse, JsonResponse
import time
import openai
import os




# 첫 번째 페이지: 추천 페이지
def main_view(request):
    return render(request, 'main.html')  # main.html 템플릿 렌더링

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


# 챗봇 페이지 렌더링
def chatbot(request, id):
    assistant = get_object_or_404(Assistant, id=id)
    return render(request, 'chatbot.html', {'assistant': assistant})

# GPT-4 실시간 스트림 응답 처리
def gpt_response_stream(request, id):
    assistant = get_object_or_404(Assistant, id=id)
    assistant_id = assistant.assistant_variable  # MySQL에서 저장된 어시스턴트 변수 가져오기

    print(f"Assistant ID: {assistant_id}")  # 어시스턴트 ID 출력

    question = request.GET.get('question', '').strip()
    print(f"Received question: {question}")  # 사용자 질문 출력

    def stream():
        if question:
            try:
                print("Calling OpenAI API...")  # OpenAI API 호출 전 출력
                # OpenAI API를 통해 어시스턴트 호출
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": f"당신은 {assistant.name} 어시스턴트입니다."},
                        {"role": "user", "content": question},
                    ],
                    stream=True
                )
                print("API call successful")  # API 호출 성공 시 출력

                for chunk in response:
                    chunk_message = chunk['choices'][0]['delta'].get('content', '')
                    if chunk_message:
                        print(f"Chunk message: {chunk_message}")  # 받아온 chunk 메시지 출력
                        for char in chunk_message:
                            yield f"data: {char}\n\n"
                            time.sleep(0.05)
                yield 'event: DONE\ndata: \n\n'
            except openai.OpenAIError as e:
                print(f"OpenAI Error: {e}")  # 오류 발생 시 오류 내용 출력
                yield f"data: Error: {str(e)}\n\n"
        else:
            print("No question provided")  # 질문이 없을 경우 출력
            yield 'data: No question provided\n\n'

    return StreamingHttpResponse(stream(), content_type='text/event-stream')
