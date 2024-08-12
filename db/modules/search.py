import sqlite3
import sys, os
from embed.embedModel import embedModel
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

async def searchSimilar(target:str ,db): #, db: sqlite3.Cursor
  settingData = db.execute("""select rssID, titleEb, descriptEb from RSS""")
  settingData = settingData.fetchall()
  result = await embedModel(target,settingData,4)
  print(result[0])
  print(result[0][0])
  print(','.join(map(str,[item[0] for item in result])))
  articleData = db.execute(f"""select rssID, siteID, title, descript, date, thumbnail, imgList, content, link from RSS where rssID in ({','.join(map(str,[item[0] for item in result]))})""").fetchall()
  print(articleData)
  return ([item2 for item2 in [item for item in articleData]])
