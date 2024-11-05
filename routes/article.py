from fastapi import APIRouter, Depends, HTTPException

import sqlite3
from db.db import get_db

router = APIRouter()

from models.NewArticles import NewArticles
from models.RecommendData import RecommendData

from controllers.article_controller import ControllerArticle
controllerArticle = ControllerArticle()

@router.get("/article/newArticles/", tags=["article"])
async def insert_new_articles(articles: NewArticles, db: sqlite3.Cursor = Depends(get_db)):
    if articles:
        return await controllerArticle.insertNewArticles(articles, db)
    else:
        raise HTTPException(status_code=400, detail="No articles provided")


@router.get("/article/search/", tags=["article"])
async def search_rss(target: str, quantity: int = 4):
    if target:
        return await controllerArticle.search_rss(target, db, quantity)
    else:
        raise HTTPException(status_code=400, detail="No articles provided")

@router.post("/article/recommend/")
async def recommend_article(item: RecommendData, db: sqlite3.Cursor = Depends(get_db)):
    return await controllerArticle.recommend_article(item.data, db, item.quantity)