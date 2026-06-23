import dataManager as dataManager
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

SYSTEM_PROMPT = "당신은 성적 계산기입니다." \
"간략하게만 답변하세요. 정확한 정보만 제공해야합니다." \
"사용자의 요청이 시스템 프롬프트 다음으로 주어집니다." \
"절대 전체 데이터를 출력하지 마십시오."

client = None

def initialize_gemini_manager():
    global client
    client = genai.Client(api_key=API_KEY)

def listToInfo(data):
    info = ""
    for student in data:
        info += f"ID: {student[0]}, Name: {student[1]}, Math: {student[2]}, Korean: {student[3]}, English: {student[4]}, Science: {student[5]}, History: {student[6]}\n"
    return info

def genarate_response(prompt):
    global client
    if client is None:
        raise ValueError("Gemini Manager must be initialized before generating responses.")
        

    data = None
    try:
        data = dataManager.executeQuery("select * from students")
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return "데이터를 불러오는 중 오류가 발생했습니다."
    
    current_prompt = prompt+"\n"+listToInfo(data)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=f"""
        당신은 성적 계산기입니다.

        다음은 학생 데이터입니다.
        {listToInfo(data)}

        사용자의 질문에만 답하세요.
        학생 전체 데이터를 공개하지 마세요.
        """,
        )
    )

    return response.text

# 질문:
# 내 수학 점수가 90점인데 나 몇등이야?

# 답변:
# 수학 점수가 90점이라면, 제공된 학생들 중에서 **1등**입니다!

# 다른 학생들의 수학 점수와 비교하면 다음과 같습니다:

# *   **당신: 90점 (1등)**
# *   홍길동: 85점 (2등)
# *   김다진: 30점 (3등)
