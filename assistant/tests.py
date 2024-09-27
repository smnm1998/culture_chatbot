<!DOCTYPE html>
<html lang="ko-KR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ assistant.name }} Chat</title>
    <link rel="stylesheet" href="//fonts.googleapis.com/earlyaccess/nanummyeongjo.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    {% load static %}
    <link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css">
    <link rel="stylesheet" href="{% static 'css/assistant/chatbot.css' %}">

</head>
<body>
    <div class="page-container">
        <header class="menu-bar">
            <button id="menuButton"><a href="{% url 'main-select' %}"><img src="{% static 'image/assistant/logo.png' %}" alt="Menu" class="size-12"></a></button>
{#            <button id="userButton"><img src="{% static 'image/assistant/user-circle.svg' %}" alt="User" class="size-12"></button>#}
        </header>

        <div class="chat-container" id="chatContainer">
            <div id="messageList" class="message-list">
                <div class="message-container ai-message">
                    <div class="message-content">
                        <p id="welcomeMessage"></p>
                    </div>
                    <hr class="msg-hr">
                    <div class="message-actions">
                        <button class="action-button like-btn" data-like-img="{% static 'image/assistant/like.svg' %}"><img src="{% static 'image/assistant/like.svg' %}" alt="좋아요"></button>
                        <button class="action-button unlike-btn" data-unlike-img="{% static 'image/assistant/unlike.svg' %}"><img src="{% static 'image/assistant/unlike.svg' %}" alt="싫어요"></button>
                        <button class="action-button action-button-cp copy-btn" data-copy-img="{% static 'image/assistant/copy.svg' %}" onclick="handleCopy(this)">
                            <img src="{% static 'image/assistant/copy.svg' %}" alt="복사">
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Swiper 슬라이더 -->
        <div class="swiper-container">
            <div class="swiper-wrapper">
            </div>
        </div>

        <div class="input-container">
            <div class="input-wrapper">
                <input id="messageInput" type="text" placeholder="무엇이든 물어보세요...">
                <input type="hidden" id="assistant_id" value="some_assistant_id">
                <input type="hidden" id="document_id" value="some_document_id">
                <button id="sendButton" class="send-button">
                    <img src="{% static 'image/assistant/message-send.svg' %}" alt="Send">
                </button>
            </div>
        </div>
    </div>

<!-- Swiper JS -->
<script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
<script>
    $(document).ready(function () {
        const apiBaseUrl = '/api/chatbot/{{ assistant.id }}/';

        // 세션 스토리지에서 배열 인덱스를 가져오는 함수
        function getArrayIndexFromSession() {
            return sessionStorage.getItem('arrayIndex') || 1; // 기본값은 1 (첫 번째 배열)
        }

        // 세션 스토리지에서 배열 인덱스를 가져옴
        const arrayIndex = parseInt(getArrayIndexFromSession()) - 1; // 배열은 0부터 시작

        // 섹션에 따른 인사말 배열
        const welcomeMessages = [
            "{{ assistant.name }}입니다! 무엇을 도와드릴까요?",
            "{{ assistant.name }}(이)라네. 어떤 것이 궁금해 찾아 왔나?"
        ];

        // 인사말 설정
        $('#welcomeMessage').text(welcomeMessages[arrayIndex]);

        // 섹션에 맞는 태그 배열
        const sectionTags = [
            ['{{ assistant.name }}(는)은 무엇인가요??', '{{ assistant.name }}의 대표 인물은 어떤 분인가요?', '{{ assistant.name }}의 특징은 무엇인가요?', '{{ assistant.name }}에 어울리는 것은 무엇인가요?'],
            ['당신은 누구신가요?', '어떤 이야기를 남기셨나요?', '또다른 활동은 어떤게 있나요?', '어디서 주로 활동하셨나요?', '가장 지키고자 했던 가치는 무엇인가요?' ],
        ];

        // Swiper 초기화
        var swiper = new Swiper('.swiper-container', {
            slidesPerView: 'auto',  // 한 화면에 1.7개의 슬라이드가 보이도록 설정
            spaceBetween: 15,    // 슬라이드 간의 간격을 설정
            freeMode: true,      // 슬라이드를 자유롭게 움직일 수 있도록 설정
            watchOverflow: true, // 슬라이드가 넘치면 스크롤 방지
        });

        // Swiper의 태그 업데이트 함수
        function updateSwiperTags(arrayIndex) {
            const swiperWrapper = $('.swiper-wrapper');
            swiperWrapper.empty(); // 기존 태그들 지우기

            const tags = sectionTags[arrayIndex]; // 배열에서 태그 가져오기
            tags.forEach(tag => {
                const slide = $(`<div class="swiper-slide">
                        <button class="tag-button">${tag}</button>
                    </div>`);
                swiperWrapper.append(slide);
            });

            swiper.update(); // Swiper 업데이트
        }

        // Swiper의 태그 업데이트 실행
        updateSwiperTags(arrayIndex);

        // 태그 버튼 클릭 시 바로 어시스턴트에 전송
        $('.swiper-wrapper').on('click', '.tag-button', function () {
            const tagText = $(this).text().trim();
            appendMessage(tagText, 'user'); // 사용자 메시지 추가
            sendMessageToBot(tagText); // 봇에게 메시지 전송
        });

        // 메시지 전송 버튼 클릭 이벤트
        $('#sendButton').on('click', function () {
            const message = $('#messageInput').val().trim();
            if (message) {
                appendMessage(message, 'user');
                $('#messageInput').val('');  // 메시지 입력 필드 비우기
                sendMessageToBot(message);   // 봇에게 메시지 보내기
            }
        });

        // 메시지를 화면에 추가하는 함수
        function appendMessage(text, sender) {
            const messageContainer = $('<div>', { class: 'message-container' });
            const messageContent = $('<div>', { class: 'message-content' });
            const messageText = $('<p>').text(text);

            messageContent.append(messageText);
            messageContainer.append(messageContent);

            // AI 메시지의 경우 action 버튼 추가
            if (sender === 'ai') {
                messageContainer.addClass('ai-message');
                appendActions(messageContainer, text);
            } else {
                messageContainer.addClass('user-message');
            }

            $('#messageList').append(messageContainer);
            scrollToBottom();  // 메시지가 추가되면 화면을 맨 아래로 스크롤
        }

        // 스크롤을 맨 아래로 이동시키는 함수
        function scrollToBottom() {
            const chatContainer = $('#chatContainer');
            chatContainer.scrollTop(chatContainer[0].scrollHeight);
        }

        // 봇에게 메시지를 전송하는 함수
        function sendMessageToBot(message) {
            const eventSource = new EventSource(`${apiBaseUrl}?question=${encodeURIComponent(message)}`);
            let fullResponse = '';
            const aiMessageContainer = $('<div>', { class: 'message-container ai-message' }).append(
                $('<div>', { class: 'message-content' }).append($('<p>'))
            );
            $('#messageList').append(aiMessageContainer);
            const messageContent = aiMessageContainer.find('p');

            eventSource.onmessage = function (event) {
                const text = event.data;
                if (text) {
                    fullResponse += text;
                    typeText(messageContent, text);  // 타이핑 효과로 메시지 추가
                }
            };

            eventSource.onerror = function () {
                eventSource.close();
                if (fullResponse) {
                    appendActions(aiMessageContainer, fullResponse);
                } else {
                    appendMessage('챗봇 답변을 가져오는 중 오류가 발생했습니다.', 'ai');
                }
            };

            eventSource.onclose = function () {
                appendActions(aiMessageContainer, fullResponse);
            };
        }

        // 텍스트를 한 글자씩 출력하는 타이핑 효과 함수
        function typeText(element, text, index = 0) {
            if (index < text.length) {
                element.text(element.text() + text.charAt(index));  // 한 글자씩 추가
                setTimeout(function () {
                    typeText(element, text, index + 1);
                }, 50);  // 타이핑 효과를 위한 딜레이
            }
        }

        // AI 메시지에 action 버튼과 구분선을 추가하는 함수
        function appendActions(container, text) {
            const likeImg = $('.like-btn').data('like-img');
            const unlikeImg = $('.unlike-btn').data('unlike-img');
            const copyImg = $('.copy-btn').data('copy-img');

            const actionsContainer = $(`<div>
                    <hr class="msg-hr">
                    <div class="message-actions">
                        <button class="action-button"><img src="${likeImg}" alt="좋아요"></button>
                        <button class="action-button"><img src="${unlikeImg}" alt="싫어요"></button>
                        <button class="action-button action-button-cp" onclick="handleCopy(this)">
                            <img src="${copyImg}" alt="복사">
                        </button>
                    </div>
                </div>`);

            container.append(actionsContainer);  // 컨테이너에 요소 추가
        }

        window.handleCopy = function (button) {
            const messageText = $(button).closest('.message-container').find('.message-content p').text();

            if (messageText) {
                navigator.clipboard.writeText(messageText).then(() => {
                    console.log("Text copied to clipboard:", messageText); // 복사 성공 로그
                }).catch(err => {
                    console.error('복사 오류:', err);
                });
            } else {
                console.error('No text found to copy.');
            }
        };
    });
</script>

</body>
</html>



















# from django.test import TestCase
#
# # Create your tests here.
# from typing_extensions import override
# from openai import AssistantEventHandler, OpenAI
#
# client = OpenAI(api_key="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")
#
#
#
#
#
# # 이벤트 핸들러 정의 (스트리밍 응답 처리)
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
#
# # 어시스턴트와 파일 ID를 받아 스레드를 만들고 질문 처리
# def ask_question_with_streaming(assistant_id, file_id, question):
#     # 스레드 생성 및 파일 첨부
#     thread = client.beta.threads.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": question,
#                 "attachments": [
#                     {"file_id": file_id, "tools": [{"type": "file_search"}]}
#                 ]
#             }
#         ]
#     )
#
#     # 스트리밍을 통한 응답 처리
#     with client.beta.threads.runs.stream(
#         thread_id=thread.id,
#         assistant_id=assistant_id,
#         instructions="Please use the attached file to answer the user's question. 답변을 대화하듯이 말해주세요",
#         event_handler=EventHandler(),
#     ) as stream:
#         stream.until_done()
#
# # 어시스턴트 ID와 파일 ID 설정
#
# assistant_id = "asst_A2FxkYEYcOq3Bd2FH8h6o7er"  # 어시스턴트의 ID
# file_id = "file-s3zWpiqz0ayTtgrfILOFcKP2"  # 업로드된 파일의 ID
#
# # 질문 설정
# question = "어디서 주로 활동하셨나요"
#
# # 질문을 보내고 스트리밍으로 응답 받기
# ask_question_with_streaming(assistant_id, file_id, question)
#
#









