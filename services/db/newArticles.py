import sqlite3
from pydantic import BaseModel
from typing import List, Optional
import queue
import threading
import asyncio
import time
from services.db.AddRSS import insertRssArticle
# from db.modules.AddRSS import process_queue

# 큐 생성
task_queue = queue.Queue()


async def process_queue():
    while not task_queue.empty():
        func, entry, rss_id, rss_name = task_queue.get()
        await func(entry, rss_id, rss_name)
        task_queue.task_done()


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


class NewArticles(BaseModel):
    data: List[NewArticle]


async def insertNewArticles(articles: NewArticles, db: sqlite3.Cursor):
    result = []
    for article in articles.data:
        # 이미 해당 link로 글이 등록되어 있는지 확인
        articleID = await getArticleID(article.link, db)
        if articleID is not None:
            article.articleID = articleID
            result.append({"status": "success", "article": article})
            continue
        try:
            # get rssName with rssID
            rssName = db.execute(
                """SELECT rssName FROM rss WHERE rssID = ?""", [article.rssID]
            ).fetchone()[0]
        except Exception as e:
            print(e)
            result.append({"status": "fail", "article": article})
            continue
        article.published_parsed = time.gmtime(article.date)
        task_queue.put((insertRssArticle, article, article.rssID, rssName))
    # 큐 처리 스레드 시작
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    thread = threading.Thread(target=loop.run_until_complete, args=(process_queue(),))
    thread.start()
    return {"result": result}


async def getArticleID(link: str, db: sqlite3.Cursor = None):
    try:
        article = db.execute(
            """SELECT articleID FROM article WHERE link = ?""", [link]
        ).fetchone()
        return article[0] if article else None
    except Exception as e:
        return None
