from pydantic import BaseModel
from typing import Optional


class markdownFormatData(BaseModel):
    content : Optional[str] = None