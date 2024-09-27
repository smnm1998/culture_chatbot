


















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









