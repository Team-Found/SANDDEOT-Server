from fastapi import APIRouter
from typing import Optional

router = APIRouter()

from models.TalkData import TalkData
from models.MarkdownFormatData import MarkdownFormatData

from controllers.ai_controller import ControllerOpenAI

controller = ControllerOpenAI()

@router.get("/ai/getAssistant/")
async def get_assistant():
    return await controller.get_assistant()

@router.post("/ai/startTalk/")
async def start_talk(item: TalkData):
    return await controller.start_talk()

@router.get("/ai/getMessageHistory/")
async def get_message_history(threadID: Optional[str] = None):
    return await controller.get_message_history()

@router.post("/ai/markdownFormat")
async def markdownFormat(item : MarkdownFormatData):
    return await controller.send_chatgpt_request(item.content)