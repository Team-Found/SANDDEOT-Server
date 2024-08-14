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
    favicon = feed.feed.image.href if 'image' in feed.feed else await findDomain(url) + '/favicon.ico'
    
    # 사이트 이름과 URL 추출
    
    try:
      siteName = feed.feed.title
    except:
      return {"status": "error", "message": "올바른 링크가 아닙니다"}
    
    siteID = db.execute("""SELECT * FROM site WHERE siteUrl = ?""",(url,))
    siteID = siteID.fetchall()

    if len(siteID):
      return {"status": "success", 
              "siteID": siteID[0][0], 
              "siteName": siteID[0][1], 
              "sitUrl": siteID[0][2], 
              "favicon": siteID[0][3], 
              "message": "already created"}
    else:
      db.execute("""INSERT INTO site (siteName,siteUrl,favicon) VALUES (?, ?, ?)""",(siteName,url,favicon))
      db.connection.commit()  # 변경 사항을 데이터베이스에 저장
      siteID = db.execute("""SELECT * FROM site WHERE siteUrl = ?""",(url,))
      siteID = siteID.fetchall()
    
    # print(siteID)

    for entry in feed.entries:
      title = entry.title
      description = entry.description if 'description' in entry else entry.summary
      description = ' '.join(str(await htmlToPlaintext(description)).split()[:40])

      writingUrl = entry.link  # 글 링크
      thumbnail = await findImgList(siteName, entry)  # 썸네일과 이미지 리스트 추출
      published = entry.published if 'published' in entry else None

      content = None
      if 'content' in entry:
        content = entry.content[0]["value"]
      # 동기적으로 데이터베이스에 삽입
      db.execute("""
          INSERT INTO RSS (
              title, descript, date, thumbnail, imgList, titleEb, descriptEb, siteID, content, link
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
      """, (
          title, description, published,thumbnail["thumbnail"], json.dumps(thumbnail["imgList"]), await embedding(title), await embedding(description), int(siteID[0][0]), content, writingUrl
      ))
      db.connection.commit()  # 변경 사항을 데이터베이스에 저장

    return {"status": "success", 
            "siteID": siteID[0][0], 
            "siteName": siteID[0][1], 
            "sitUrl": siteID[0][2], 
            "favicon": siteID[0][3], 
            "message": "new created"}
  # except Exception as e:
  #     return {"status": "error", "message": str(e)}
