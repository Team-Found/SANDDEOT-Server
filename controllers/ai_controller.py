from typing import Optional
from models.MarkdownFormatData import MarkdownFormatData
from models.TalkData import TalkData
from services.openai.ai import getAssistant, messageHistory, send_chatgpt_request, startTalk

class ControllerOpenAI:
    async def get_assistant(self):
        assistant_id = await getAssistant()
        return {"assistantID": assistant_id}

    async def start_talk(self, item: TalkData):
        messages = await startTalk(item.threadID, item.assistantID, item.article, item.question, item.selection)
        return {"messages": messages}
    
    async def get_message_history(self, thread_id: Optional[str] = None):
        messages = await messageHistory(thread_id)
        return {"messages": messages}

    async def markdown_format(self, content):
        messages = await send_chatgpt_request(content)
        return {"messages": messages}

