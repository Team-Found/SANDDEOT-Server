from fastapi import APIRouter, Depends, HTTPException

from db.db import get_db
from models.NewArticles import NewArticles
from models.RecommendData import RecommendData

router = APIRouter()

@router.get("/article/newArticles/", tags=["article"])
async def insert_new_articles(
    articles: NewArticles, db: sqlite3.Cursor = Depends(get_db)
):
    if articles:
        return await insertNewArticles(articles, db)
    else:
        raise HTTPException(status_code=400, detail="No articles provided")

@router.get("/article/search/", tags=["article"])
async def search_rss(
    target: str, db: sqlite3.Cursor = Depends(get_db), quantity: int = 4):
    if target:
        return await searchSimilar(target, db, quantity)

@router.post("/article/recommend/")
async def search_rss(item: RecommendData, db: sqlite3.Cursor = Depends(get_db)):
    return await recommend(item.data, db, item.quantity)