import sqlite3
import sys, os
from embed.embedModel import embedModel
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

async def searchSimilar(target:str ,db, quantity): #, db: sqlite3.Cursor
  settingData = db.execute("""select rssID, titleEb, descriptEb from RSS""")
  settingData = settingData.fetchall()
  result = await embedModel(target,settingData, quantity)

  articleData = db.execute(f"""select  s.siteID, s.siteName, siteUrl, favicon, rssID ,title, descript, date, thumbnail, imgList, content, link 
                          from RSS r, site s where rssID in ({','.join(map(str,[item[0] for item in result]))}) and r.siteID = s.siteID""")
  
  print(articleData)
  articles_json_list = []
  for index, [siteID, siteName, siteUrl, favicon, rssID, title, descript, date, thumbnail, imgList, content, rssUrl] in enumerate(articleData):
    article_data = {
        "siteID": siteID,
        "siteName": siteName,
        "siteUrl": siteUrl,
        "favicon": favicon,
        "rssID": rssID,
        "title": title,
        "descript": descript,
        "date": date,
        "thumbnail": thumbnail,
        "imgList": imgList,
        "content": content,
        "rssUrl": rssUrl
    }
    # JSON 리스트에 추가
    articles_json_list.append(article_data)


  return json.dumps(articles_json_list)