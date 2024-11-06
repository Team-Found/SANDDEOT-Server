import sqlite3
from db.db import get_db
from fastapi import Depends, HTTPException
from models import NewArticles, RecommendData
from services.db.newArticles import insertNewArticles
from services.db.search import searchSimilar
from services.recommend.recommend import recommend

class ControllerArticle:
    async def insert_new_articles(self,articles: NewArticles, db: sqlite3.Cursor = Depends(get_db)):
        return await insertNewArticles(articles, db)
    
    async def search_rss(self,target: str, db: sqlite3.Cursor = Depends(get_db), quantity: int = 4):
        return await searchSimilar(target, db, quantity)

    async def recommend_article(self,data, db: sqlite3.Cursor = Depends(get_db), quantity: int = 4):
        return await recommend(data, db, quantity)