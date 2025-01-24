
# from dotenv import load_dotenv
# from openai import OpenAI
# import os
#
# # .env 파일 로드 (기존 환경 변수 덮어쓰기 허용)
# load_dotenv(override=True)
# print(os.getenv("OPENAI_API_KEY"))
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#
# try:
#     file_info = client.files.retrieve(file_id="file-s3zWpiqz0ayTtgrfILOFcKP2")
#     print(f"File Info: {file_info}")
# except Exception as e:
#     print(f"Error retrieving file: {e}")
#




#
# # 전체 환경 변수 출력
# for key, value in os.environ.items():
#     if "OPENAI_API_KEY" in key:
#         print(f"{key}: {value}")




