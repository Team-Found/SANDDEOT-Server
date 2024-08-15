import sqlite3
import sys, os
from embed.embedModel import embedModel
from embed.embedding import embedding
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

async def searchSimilar(target:str ,db, quantity): #, db: sqlite3.Cursor
  settingData = db.execute("""select articleID, titleEb, descriptEb from article""")
  settingData = settingData.fetchall()


  result = await embedModel(await embedding(target),settingData, quantity)
  articleData = db.execute(f"""select  r.rssID, r.rssName, rssUrl, favicon, articleID ,title, descript, date, thumbnail, imgList, content, link 
                          from article a, rss r where articleID in ({','.join(map(str,[item[0] for item in result]))}) and r.rssID = a.rssID""")
  articles_json_list = []
  for article in articleData:
    rssID, rssName, rssUrl, favicon, articleID, title, descript, date, thumbnail, imgList, content, articleUrl = article

    imgList = json.loads(imgList)

    article_data = {
        "rssID": rssID,
        "rssName": rssName,
        "rssUrl": rssUrl,
        "favicon": favicon,
        "articleID": articleID,
        "title": title,
        "descript": descript,
        "date": date,
        "thumbnail": thumbnail,
        "imgList": imgList,
        "content": content,
        "articleUrl": articleUrl
    }
    # JSON 리스트에 추가
    articles_json_list.append(article_data)


  return json.dumps(articles_json_list)