import os
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

model = "gpt-3.5-turbo"
instruction = """
내가 메시지를 보낼때 다음과 같은 양식으로 질문할 것이다.

1. {text : "내용"}
앞으로 모든 응답들은 이 text에 담긴 내용에 관련된 질문을 답변하게 된다
이 내용을 보냈을 때는 ok라고 응답해라

2.
{
    chatID : 0,
    question : "질문"
}

앞으로 chatID가 같은 question과 너의 응답내용을 참고하여 
{
    chatID : 0
    answer : "답변내용"
}
해당 양식으로 답변해야한다.

가장 중요하게 지켜아할 점은
chatID가 다른 질문에 대해서는 절대로 어떤 경우가 있어도 영향을 받지 않는다
"""

assistant = client.beta.assistants.create(
    name="user-assistant",
    instructions=instruction,
    model="gpt-4-1106-preview",
    # tools=[{"type":"retrieval"}]
)

# response = openai.ChatCompletion.create(
#     model=model,
#     messages=messages,
#     max_tokens=100  # 응답 길이를 적절히 설정하세요.
# )

# # 응답 출력
# print(response.choices[0].message["content"])
