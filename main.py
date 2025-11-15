# import base64
# import requests
# import json
#
# # ⚠️ 이 값들은 RapidAPI 계정 및 API 문서에서 확인하여 대체해야 합니다.
# # 1. 엔드포인트 URL
# URL = "http://localhost:3001/api/python"
#
# # 2. 필수 헤더 정보
# HEADERS = {
#     'content-type': "application/json; charset=utf-8",
#     # 'X-RapidAPI-Key': "YOUR_RAPIDAPI_KEY",
#     # 'X-RapidAPI-Host': "easy-compiler-api.p.rapidapi.com"
# }
#
# # 3. 요청 본문 (Payload) - Python 3 실행 예시
# # 'Hello World'를 출력하는 간단한 Python 코드
# PYTHON_CODE = """
# for i in range(10):
#     print(i)
# """
#
# base64_code = base64.b64encode(PYTHON_CODE.encode('utf-8')).decode('utf-8')
#
# PAYLOAD = {
#     "language": "python3",  # 언어 지정
#     "code": base64_code,  # 실행할 Python 코드
#     "input": ""  # 표준 입력 (필요 시 여기에 데이터를 넣습니다)
# }
#
# try:
#     # 4. API 호출
#     response = requests.request("POST", URL, data=json.dumps(PAYLOAD), headers=HEADERS)
#
#     # 5. 결과 출력
#     if response.status_code == 200:
#         result = response.json()
#         print("--- API 실행 결과 ---")
#         print(f"출력 (Stdout):\n{result.get('stdout', 'N/A')}")
#         print(f"에러 (Stderr):\n{result.get('stderr', 'N/A')}")
#         print(f"상태 :\n{result.get('statusMes', 'N/A')}")
#     else:
#         print(f"요청 실패: 상태 코드 {response.status_code}")
#         print(response.text)
#
# except Exception as e:
#     print(f"오류 발생: {e}")

import time
local_time = time.localtime()
formatted_time = time.strftime("%Y%m%d_%H%M%S", local_time)
print(f"현재 시간(초): {formatted_time}")