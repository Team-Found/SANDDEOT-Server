import os
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
model = "gpt-3.5-turbo"

query = "텍스트를 이미지로 그려주는 모델에 대해 알려줘."

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": query
    }
]

response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    max_tokens=100  # 응답 길이를 적절히 설정하세요.
)

# 응답 출력
print(response.choices[0].message["content"])
