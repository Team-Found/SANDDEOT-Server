import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
openai_api_key = os.getenv("OPENAI_API_KEY")

# API 키를 사용하여 OpenAI 설정
import openai
openai.api_key = openai_api_key

# 테스트로 간단한 API 요청
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="What is AI?",
    max_tokens=50
)

print(response.choices[0].text.strip())
