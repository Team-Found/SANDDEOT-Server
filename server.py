#FAST API Import For Set UP
from typing import List
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import time
import sqlite3
import asyncio
from embed.embedModel import embedModel
from db.modules.AddRSS import addRSS
from db.db import get_db
from db.modules.search import searchSimilar
from recommend.recommend import recommend

#다른 경로에 있는 모듈 import
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

conn = sqlite3.connect(os.path.abspath('db/server.db'))
db = conn.cursor()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{any}")
def read_item(any: str):
    print("Input: ", any)
    start = time.time()
    data = embedModel(any)
    end = time.time()
    print("Time taken: ", end - start)
    return {"data": data}




@app.get("/rss/add/")
async def insert_rss_domain(domain: Optional[str] = None, db: sqlite3.Cursor = Depends(get_db)):
    if domain:
        return await addRSS(domain, db)
    else:
        raise HTTPException(status_code=400, detail="No domain provided")

@app.get("/article/search/")
async def search_rss(target:str, db: sqlite3.Cursor = Depends(get_db),quantity:int = 4):
    if target:
        return await searchSimilar(target, db, quantity)

class RecommendData(BaseModel):
    data : List[int]
    quantity : int

@app.post("/article/recommend/")
async def search_rss(item: RecommendData, db: sqlite3.Cursor = Depends(get_db)):
    return await recommend(item.data, db, item.quantity)