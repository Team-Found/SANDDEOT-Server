from fastapi import APIRouter
from typing import Optional

router = APIRouter()

from models.TalkData import TalkData
from models.MarkdownFormatData import MarkdownFormatData

@router.get("/ai/getAssistant/")
async def get_assistant():
    return {"assistantID": await getAssistant()}

@router.post("/ai/startTalk/")
async def start_talk(item: TalkData):
    print(item)
    return {
        "messages": await startTalk(
            item.threadID, item.assistantID, item.article, item.question, item.selection
        )
    }

@router.get("/ai/getMessageHistory/")
async def get_message_history(threadID: Optional[str] = None):
    return {"messages": await messageHistory(threadID)}

@router.post("/ai/markdownFormat")
async def markdownFormat(item : MarkdownFormatData):
    return {"messages": await send_chatgpt_request(item.content)}