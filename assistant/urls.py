# assistant/urls.py

from django.urls import path
from .views import main_view, local_view, AssistantListView

urlpatterns = [
    path('', main_view, name='main'),  # 첫 번째 페이지: 추천을 해주는 메인 페이지
    path('local/', local_view, name='local-select'),  # 두 번째 페이지: 지역 선택 후 어시스턴트 연결 페이지
    path('api/assistants/', AssistantListView.as_view(), name='assistant-list'),

]