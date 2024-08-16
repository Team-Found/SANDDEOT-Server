# FAST API Import For Set UP
from typing import List
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import time
import sqlite3
import asyncio
from embed.embedModel import embedModel
from db.modules.AddRSS import addRSS
from db.db import get_db
from db.modules.search import searchSimilar
from recommend.recommend import recommend

from db.modules.newArticles import insertNewArticles

# 다른 경로에 있는 모듈 import
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

conn = sqlite3.connect(os.path.abspath("db/server.db"))
db = conn.cursor()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{any}")
def read_item(any: str):
    print("Input: ", any)
    start = time.time()
    data = embedModel(any)
    end = time.time()
    print("Time taken: ", end - start)
    return {"data": data}


@app.get("/rss/add/")
async def insert_rss_domain(
    domain: Optional[str] = None, db: sqlite3.Cursor = Depends(get_db)
):
    if domain:
        return await addRSS(domain, db)
    else:
        raise HTTPException(status_code=400, detail="No domain provided")


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


@app.post("/article/newArticles/")
async def insert_new_articles(
    articles: NewArticles, db: sqlite3.Cursor = Depends(get_db)
):
    if articles:
        return await insertNewArticles(articles, db)
    else:
        raise HTTPException(status_code=400, detail="No articles provided")


@app.get("/article/search/")
async def search_rss(
    target: str, db: sqlite3.Cursor = Depends(get_db), quantity: int = 4
):
    if target:
        return await searchSimilar(target, db, quantity)


class RecommendData(BaseModel):
    data: List[int]
    quantity: int


@app.post("/article/recommend/")
async def search_rss(item: RecommendData, db: sqlite3.Cursor = Depends(get_db)):
    return await recommend(item.data, db, item.quantity)


# @app.get("/assistant/add/")
# async def assistant_add():
#     return assistantAdd()