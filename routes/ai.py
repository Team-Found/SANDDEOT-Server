from fastapi import APIRouter
from typing import Optional

router = APIRouter()

from models.TalkData import TalkData
from models.MarkdownFormatData import MarkdownFormatData

from controllers.ai_controller import ControllerOpenAI

controller = ControllerOpenAI()

@router.get("/ai/getAssistant/", tags=["openAI"])
async def get_assistant():
    return await controller.get_assistant()

@router.post("/ai/startTalk/", tags=["openAI"])
async def start_talk(item: TalkData):
    return await controller.start_talk(item)

@router.get("/ai/getMessageHistory/", tags=["openAI"])
async def get_message_history(threadID: Optional[str] = None):
    return await controller.get_message_history(threadID)

@router.post("/ai/markdownFormat", tags=["openAI"])
async def markdownFormat(item : MarkdownFormatData):
    return await controller.markdown_format(item.content)