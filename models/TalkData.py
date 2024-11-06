from pydantic import BaseModel
from typing import List
from typing import Optional

class TalkData(BaseModel):
    threadID: Optional[str] = None
    assistantID: str
    article: Optional[str] = None
    question: Optional[str] = None
    selection: Optional[str] = None