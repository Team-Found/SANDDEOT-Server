from embed.embedding import embedding
from RSS.htmlToPlaintext import htmlToPlaintext
from RSS.findImgList import findImgList
from RSS.findDomain import findDomain
import aiohttp  # 비동기 HTTP 클라이언트
from fastapi import HTTPException
from typing import Dict
import sqlite3
import json
from bs4 import BeautifulSoup
import feedparser
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# db_modules/add_rss.py


async def fetch_feed(url: str) -> feedparser.FeedParserDict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            return feedparser.parse(content)

async def addRSS(url: str, db: sqlite3.Cursor) -> Dict[str, str]:
  try:
    # 비동기 HTTP 요청으로 RSS 피드를 가져옵니다.
    feed = await fetch_feed(url)

    # 파비콘 추출
    favicon = feed.feed.image.href if 'image' in feed.feed else await findDomain(url) + '/favicon.ico'
    
    # 사이트 이름과 URL 추출
    siteName = feed.feed.title
    siteUrl = feed.feed.link

    for entry in feed.entries:
        title = entry.title
        description = entry.description if 'description' in entry else entry.summary
        description = ' '.join(str(await htmlToPlaintext(description)).split()[:40])

        writingUrl = entry.link  # 글 링크
        thumbnail = await findImgList(siteName, entry)  # 썸네일과 이미지 리스트 추출
        published = entry.published if 'published' in entry else None

        # 동기적으로 데이터베이스에 삽입
        db.execute("""
            INSERT INTO RSS (
                title, descript, date, siteName, siteUrl, thumbnail, imgList, titleEb, descriptEb
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, description, published, siteName, siteUrl, thumbnail["thumbnail"], json.dumps(thumbnail["imgList"]), await embedding(title), await embedding(description)
        ))
        db.connection.commit()  # 변경 사항을 데이터베이스에 저장

    return {"status": "success", "domain": url}
  except Exception as e:
      return {"status": "error", "message": str(e)}
