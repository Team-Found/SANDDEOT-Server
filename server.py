#FAST API Import For Set UP
from typing import Union
from fastapi import FastAPI
import time

app = FastAPI()

#다른 경로에 있는 모듈 import
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

#모듈 import
from db import main
from embed.embedModel import embedModel

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


@app.get("/sql")
def test():
    a = 0;
    return {"data": a}