import os
from dotenv import load_dotenv
import openai
import time

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

instruction = """
너는 본문의 글에 대한 질문을 답변하는 인공지능 챗봇이다. 본문 내에서 답을 찾아서 적절한 답변을 하여도 좋고, 웹 검색이나 지식 베이스를 참고하여 답변해도 좋다. 답변의 길이는 500자를 넘지 않도록 하자.

1. 시스템은 대화의 시작 시점에 다음과 같이 본문 내용을 HTML로 전달할 것이다.
{text : "<h1>글 제목</h1><p>본문 내용</p>...(이어서 계속)"}
앞으로 모든 응답들은 이 text에 담긴 내용에 관련된 질문을 답변하게 된다
이 내용을 보냈을 때는 ok라고 응답해라

2. 사용자는 다음과 같은 형식으로 질문을 전달할 것이다.
{
    question : "질문내용",
    selection : "선택된 텍스트"
}

{
    answer : "답변내용"
}
해당 양식으로 답변해야한다.
"""


# model = "gpt-3.5-turbo"
async def getAssistant():
    assistant = client.beta.assistants.create(
        name="user-assistant",
        model="gpt-4o",
        instructions=instruction,
        # tools=[{"type": "retrieval"}],
    )
    return assistant


async def getThread():
    thread = client.beta.threads.create()
    return thread


async def startTalk(threadID, assistantID, article, question: str, selection):
    if article == None:
        return "No article provided"
    if question == None:
        return "No question provided"
    if not threadID:
        threadID = await getThread()
        ## 스레드 첫 시작
        client.beta.threads.messages.create(
            thread_id=threadID,
            role="system",
            content={"HTML": article},
        )

    # 사용자의 질문 메시지
    client.beta.threads.messages.create(
        thread_id=threadID,
        role="user",
        content={"question": question, "selection": selection},
    )

    run = client.beta.threads.create_and_run_poll(
        thread_id=threadID, assistant_id=assistantID
    )

    # 응답 대기 무한루프
    while run.status != "completed":
        # run = client.beta.threads.polls.get(poll_id=run.id)
        print(run.status)
        time.sleep(1)

    # 응답 메시지
    messages = client.beta.threads.messages.list(thread_id=threadID)

    print(messages)
    return messages


# response = openai.ChatCompletion.create(
#     model=model,
#     messages=messages,
#     max_tokens=100  # 응답 길이를 적절히 설정하세요.
# )

# # 응답 출력
# print(response.choices[0].message["content"])
