from typing import Union
from fastapi import FastAPI

from embedModel import embedModel


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{any}")
def read_item(any: str):
    return {"data": embedModel(any)}