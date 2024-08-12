import sqlite3
import sys, os
import numpy as np
import io
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/LaBSE")

conn = sqlite3.connect(os.path.abspath('db/server.db'))
db = conn.cursor()

settingData = db.execute("""select rssID, title, titleEb from RSS LIMIT 1""").fetchall()
a = np.frombuffer(io.BytesIO(settingData[0][2]).getvalue(), dtype=np.float32)
b = model.encode(settingData[0][1])

print(a==b)