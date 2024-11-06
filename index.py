from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import ai, article, rss

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}

app.include_router(ai.router)
app.include_router(article.router)
app.include_router(rss.router)