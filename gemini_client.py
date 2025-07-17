
import os
import google.generativeai as genai
from dotenv import load_dotenv
from file_tools import list_files, create_directory

load_dotenv()

# API 키 설정
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 사용 가능한 도구 정의
tools = {
    "list_files": list_files,
    "create_directory": create_directory,
}

# Gemini 모델 설정 (도구 사용 기능 포함)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools=tools.values(),
)

def get_ai_response(user_query: str):
    """사용자 쿼리를 받아 AI의 응답을 반환하며, 중간에 도구 호출을 처리합니다."""
    chat = model.start_chat()
    response = chat.send_message(user_query)

    # AI가 도구를 사용하라고 응답하는 경우를 처리하는 루프
    while response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        function_name = function_call.name
        args = dict(function_call.args)

        print(f"AI가 도구 호출을 요청했습니다: {function_name}({args})")

        # 요청된 함수를 실제로 실행
        if function_name in tools:
            function_to_call = tools[function_name]
            try:
                function_response = function_to_call(**args)
            except Exception as e:
                function_response = {"error": str(e)}

            print(f"도구 실행 결과: {function_response}")

            # 도구 실행 결과를 다시 AI에게 전달
            response = chat.send_message(
                [
                    {
                        "function_response": {
                            "name": function_name,
                            "response": {"result": function_response},
                        }
                    }
                ]
            )
        else:
            # AI가 정의되지 않은 함수를 호출하려고 할 때
            print(f"오류: AI가 알 수 없는 도구 '{function_name}'를 호출했습니다.")
            break

    # 최종적으로 AI가 텍스트로 응답하면 그 내용을 반환
    return response.text
