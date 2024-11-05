from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/rss/add", tags=["users"])
async def insert_rss_domain(domain: Optional[str] = None, db: sqlite3.Cursor = Depends(get_db)):
    if domain:
        return await addRSS(domain, db)
    else:
        raise HTTPException(status_code=400, detail="No domain provided")
