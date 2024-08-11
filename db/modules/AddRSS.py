#다른 경로에 있는 모듈 import
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from db.main import db

import feedparser
from bs4 import BeautifulSoup
from ...RSS.findDomain import findDomain
from ...RSS.findImgList import findImgList
from ...RSS.htmlToPlaintext import htmlToPlaintext



for url in target_feeds.values():
    rss_url = url
    feed = feedparser.parse(rss_url)

    # 파비콘을 추출하는 코드
    if 'image' in feed.feed:
      print(feed.feed.image.href)
    else:
      print(findDomain(rss_url)+'favicon.ico')

    # 사이트 이름 추출
    siteName = feed.feed.title
    print('사이트이름' + siteName)

    for entry in feed.entries:
      print(entry.guid) #RSSArticleID
      print("Title:", entry.title) #글이름

      if 'description' in entry:
        description = entry.description
      elif 'summary' in entry:
        description = entry.summary
      print("desc:", htmlToPlaintext(description))


      writingUrl = entry.link #글 링크
      print('글링크' +writingUrl)

      thumbnail = findImgList(siteName,entry)
      print(f"썸네일 {thumbnail}")

      published = entry.get('published', 'No publish date found')
      if published == 'No publish date found':
        published_parsed = entry.get('published_parsed', None)
      if published_parsed:
          from time import strftime
          published = strftime('%Y-%m-%d %H:%M:%S', published_parsed)
  
      try:
        print("Published:", entry.published)
      except:
          pass
      print()