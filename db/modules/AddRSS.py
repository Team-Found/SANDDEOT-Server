from embed.embedding import embedding
from RSS.htmlToPlaintext import htmlToPlaintext
from RSS.findImgList import findImgList
from RSS.findDomain import findDomain
import aiohttp  # 비동기 HTTP 클라이언트
import aiosqlite
from fastapi import HTTPException
from typing import Dict
import sqlite3
import json
from bs4 import BeautifulSoup
import feedparser
import sys
import os
import time
import queue
import threading
import asyncio
from db.db import get_db

# 큐 생성
task_queue = queue.Queue()


async def process_queue():
    while not task_queue.empty():
        func, entry, rss_id, rss_name = task_queue.get()
        await func(entry, rss_id, rss_name)
        task_queue.task_done()


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# db_modules/add_rss.py


async def fetch_feed(url: str) -> feedparser.FeedParserDict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            return feedparser.parse(content)


async def addRSS(url: str, db: sqlite3.Cursor) -> Dict[str, str]:
    # try:
    # 비동기 HTTP 요청으로 RSS 피드를 가져옵니다.
    feed = await fetch_feed(url)
    # 파비콘 추출
    favicon = (
        feed.feed.image.href
        if "image" in feed.feed
        else await findDomain(url) + "/favicon.ico"
    )

    # 사이트 이름과 URL 추출

    try:
        rssName = feed.feed.title
    except:
        return {"status": "error", "message": "올바른 링크가 아닙니다"}

    rssID = db.execute("""SELECT * FROM rss WHERE rssUrl = ?""", (url,))
    rssID = rssID.fetchall()

    if len(rssID):
        return {
            "status": "success",
            "rssID": rssID[0][0],
            "rssName": rssID[0][1],
            "rssUrl": rssID[0][2],
            "favicon": rssID[0][3],
            "message": "already created",
        }
    else:
        db.execute(
            """INSERT INTO rss (rssName,rssUrl,favicon) VALUES (?, ?, ?)""",
            (rssName, url, favicon),
        )
        db.connection.commit()  # 변경 사항을 데이터베이스에 저장
        rssID = db.execute("""SELECT * FROM rss WHERE rssUrl = ?""", (url,))
        rssID = rssID.fetchall()

    for entry in feed.entries:
        task_queue.put((insertRssArticle, entry, rssID[0][0], rssName))
    # 큐 처리 스레드 시작
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    thread = threading.Thread(target=loop.run_until_complete, args=(process_queue(),))
    thread.start()
    # 즉시 반환
    return {
        "status": "success",
        "rssID": rssID[0][0],
        "rssName": rssID[0][1],
        "rssUrl": rssID[0][2],
        "favicon": rssID[0][3],
        "message": "new created",
    }


async def insertRssArticle(entry, rssID: int, rssName: str = None):
    db_gen = get_db()
    db = next(db_gen)
    title = entry.title
    description = entry.description if "description" in entry else entry.summary
    description = " ".join(str(await htmlToPlaintext(description)).split()[:40])
    if description == None:
        description = title

    writingUrl = entry.link  # 글 링크
    thumbnail = await findImgList(rssName, entry)  # 썸네일과 이미지 리스트 추출
    published = entry.published_parsed if "published_parsed" in entry else None
    # print(published)
    content = None
    if "content" in entry:
        content = entry.content[0]["value"]
    # 동기적으로 데이터베이스에 삽입
    db.execute(
        """
      INSERT INTO article (
          title, descript, date, thumbnail, imgList, titleEb, descriptEb, rssID, content, link, saved
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  """,
        (
            title,
            description,
            time.mktime(published),
            thumbnail["thumbnail"],
            json.dumps(thumbnail["imgList"]),
            await embedding(title),
            await embedding(description),
            rssID,
            content,
            writingUrl,
            0,
        ),
    )
    db.connection.commit()  # 변경 사항을 데이터베이스에 저장
    return f"Article {title} inserted"


# except Exception as e:
#     return {"status": "error", "message": str(e)}
