from pydantic import BaseModel
from typing import Optional


class MarkdownFormatData(BaseModel):
    content : Optional[str] = None