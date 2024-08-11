from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# db_modules/add_rss.py
import json
import feedparser
import sqlite3
from typing import Dict
from fastapi import HTTPException
from RSS.findDomain import findDomain
from RSS.findImgList import findImgList
from RSS.htmlToPlaintext import htmlToPlaintext
from embed.embedding import embedding

def addRSS(url: str, db: sqlite3.Cursor) -> Dict[str, str]:
    # try:
    #TODO: 이미있는 사이트는 받지않기
    # 없으면 반환
    # 도메인 부족해도 채워주기

    feed = feedparser.parse(url)
    
    # 파비콘 추출
    if 'image' in feed.feed:
        favicon = feed.feed.image.href
    else:
        favicon = findDomain(url) + '/favicon.ico'
    
    # 사이트 이름과 URL 추출
    siteName = feed.feed.title
    siteUrl = feed.feed.link

    for entry in feed.entries:
        title = entry.title
        description = entry.description if 'description' in entry else entry.summary
        description = ' '.join(str(htmlToPlaintext(description)).split()[:40])

        writingUrl = entry.link  # 글 링크
        thumbnail = findImgList(siteName, entry)  # 썸네일과 이미지 리스트 추출
        published = entry.published if 'published' in entry else None

        db.execute("""
            INSERT INTO RSS (
                title, descript, date, siteName, siteUrl, thumbnail, imgList, titleEb, descriptEb
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, description, published, siteName, siteUrl, thumbnail["thumbnail"], json.dumps(thumbnail["imgList"]), embedding(title), embedding(description)
        ))
        db.connection.commit()  # 변경 사항을 데이터베이스에 저장

    return {"siteName": siteName, "siteFavicon": favicon, "title": title, "description": description}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Database error: {e}")
