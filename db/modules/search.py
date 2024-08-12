import sqlite3
import os

conn = sqlite3.connect(os.path.abspath('db/server.db'))
db = conn.cursor()

settingData = db.execute("""select rssID, titleEb, descriptEb from RSS""")
settingData = settingData.fetchall()
print(settingData[0][1])
# async def searchSimilar(target: list[str]): #, db: sqlite3.Cursor
