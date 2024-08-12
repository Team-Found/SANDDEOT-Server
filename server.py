#FAST API Import For Set UP
from typing import Union
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import time
import sqlite3
import asyncio

#다른 경로에 있는 모듈 import
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

#모듈 import
from embed.embedModel import embedModel
from db.modules.AddRSS import addRSS
from db.db import get_db

# 데이터베이스 연결
conn = sqlite3.connect('/root/SANDDEOT-Server/db/db.py')
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


# class FindDomain(BaseModel):
#     name: str

@app.get("/insert/rss/")
async def insert_rss_domain(domain: Optional[str] = None, db: sqlite3.Cursor = Depends(get_db)):
    if domain:
        return await addRSS(domain, db)
    else:
        raise HTTPException(status_code=400, detail="No domain provided")
