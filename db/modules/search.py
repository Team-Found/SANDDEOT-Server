import sqlite3
import sys, os
from embed.embedModel import embedModel

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

async def searchSimilar(target:str ,db): #, db: sqlite3.Cursor
  settingData = db.execute("""select rssID, titleEb, descriptEb from RSS LIMIT 10""")
  settingData = settingData.fetchall()
  return await embedModel(target,settingData,4)