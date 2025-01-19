# 대한민국 지역문화 챗봇 시스템

## 프로젝트 소개
대한민국 각 지역의 문화유산, 역사적 인물, 관광 명소, 전통 등을 사용자에게 전달하기 위한 챗봇 기반 정보 제공 시스템입니다. 
OpenAI API를 활용하여 사용자의 질문에 맞는 정보를 검색하고 제공하며, 사용자 친화적인 인터페이스를 갖춘 웹 애플리케이션으로 개발되었습니다.

![프로젝트 화면](./portfolio_images/project_overview.png)

## 주요 기능
1. **지역문화 정보 제공**
   - 대한민국의 지역별 문화유산, 독립운동가, 전통술 등에 대한 상세 정보 제공.

2. **챗봇 시스템 연동**
   - OpenAI GPT-4 API를 활용하여 자연스러운 대화 기반 정보 제공.

3. **관리자 기능**
   - 관리자 페이지에서 어시스턴트 및 문서 ID를 관리하고, 새로운 정보를 추가할 수 있는 기능 제공.

4. **대화 세션 관리**
   - 대화 흐름을 유지하며, 사용자가 새로운 질문을 할 때 기존 세션 초기화.

5. **배포 및 운영**
   - NGINX와 Gunicorn을 이용해 Vultr 서버에서 배포 및 운영.

![챗봇 예시](./portfolio_images/chatbot_example1.png)

## 기술 스택
- **프레임워크 및 언어**: Django, Django REST Framework
- **API 연동**: OpenAI API
- **프론트엔드**: HTML, CSS, jQuery, AJAX
- **배포 및 운영**: NGINX, Gunicorn, Vultr
- **버전 관리**: Git

## 프로젝트 구조
```
region-culture-chatbot/
├── chatbot/                 # 챗봇 관련 로직 및 API
├── core/                    # 프로젝트 설정 및 공통 기능
├── frontend/                # 프론트엔드 리소스 (HTML, CSS, JS)
├── static/                  # 정적 파일
├── templates/               # 템플릿 파일
├── manage.py                # Django 관리 스크립트
└── requirements.txt         # 프로젝트 의존성 목록
```

## 설치 및 실행
### 1. 의존성 설치
```
pip install -r requirements.txt
```

### 2. 데이터베이스 마이그레이션
```
python manage.py makemigrations
python manage.py migrate
```

### 3. 서버 실행
```
python manage.py runserver
```

### 4. 챗봇 사용
로컬 서버(`http://127.0.0.1:8000/`)에 접속하여 챗봇 기능을 체험하세요.

## 주요 성과
- 독립운동 챗봇과 보드게임 연동으로 "교육+오락" 서비스 제공.
- **성과**:
  - 보드게임 학생창업 300 선정.
  - 경북 콘텐츠진흥원 엑셀러레이터 사업 선정.
  - 2024 코엑스 에듀테크 페어 박람회 참여.

## 기여 방법
1. 본 저장소를 포크합니다.
2. 새로운 브랜치를 생성합니다.
   ```
   git checkout -b feature/새로운기능
   ```
3. 변경 사항을 커밋합니다.
   ```
   git commit -m "Add 새로운 기능"
   ```
4. 브랜치에 푸시합니다.
   ```
   git push origin feature/새로운기능
   ```
5. Pull Request를 생성합니다.

## 라이선스
이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 배포됩니다.

---

### 문의
프로젝트와 관련된 문의 사항은 [jhs789654123@gmail.com]로 연락주세요.
