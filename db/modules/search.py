import sqlite3
import sys, os
from embed.embedModel import embedModel
from embed.embedding import embedding
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

async def searchSimilar(target:str ,db, quantity): #, db: sqlite3.Cursor
  settingData = db.execute("""select articleID, titleEb, descriptEb from article""")
  settingData = settingData.fetchall()


  return await embedModel(db,await embedding(target),settingData, quantity)
