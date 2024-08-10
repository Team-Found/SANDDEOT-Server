from typing import Union
from fastapi import FastAPI
import time
from embedModel import embedModel


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
