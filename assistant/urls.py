# assistant/urls.py

from django.urls import path
from .views import (
    main_view,
    local_view,
    chatbot_view,
    thema_view,
    independence_view,
    search_results_view,
    AssistantListView,
    ChatbotAPIView,
    )

urlpatterns = [
    path('', main_view, name='main-select'),  # 첫 번째 페이지: 추천을 해주는 메인 페이지
    path('local/', local_view, name='local-select'),  # 두 번째 페이지: 지역 선택 후 어시스턴트 연결 페이지
    path('chatbot/<int:id>/', chatbot_view, name='chatbot'),
    path('thema/', thema_view, name='thema-select'),
    path('independence/', independence_view, name='independence-select'),
    path('search/', search_results_view, name='search-results'),  # 검색 결과 페이지


    path('api/assistants/', AssistantListView.as_view(), name='assistant-list'),
    path('api/chatbot/<int:id>/', ChatbotAPIView.as_view(), name='chatbot-api'),  # 새로운 챗봇 API

]