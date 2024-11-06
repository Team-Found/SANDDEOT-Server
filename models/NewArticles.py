import time
from pydantic import BaseModel
from typing import List
from typing import Optional

class NewArticle(BaseModel):
    articleID: Optional[int] = None
    rssID: int
    title: str
    description: Optional[str] = None
    summary: Optional[str] = None
    date: int  # unix timestamp
    content: List[dict]
    link: str
    media_thumbnail: Optional[str] = None
    published_parsed: Optional[time.struct_time] = None  # 선택적 속성 추가

    class Config:
        arbitrary_types_allowed = True

class NewArticles(BaseModel):
    data: List[NewArticle]