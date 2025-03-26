import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.database.connection import init_db
from presentation.api.router import api_router

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI(
    title="FastAPI クリーンアーキテクチャ & DDD テンプレート",
    description="FastAPIを使用したクリーンアーキテクチャとDDDのテンプレート",
    version="0.1.0",
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターの設定
api_prefix = os.getenv("API_PREFIX", "/api")
app.include_router(api_router, prefix=api_prefix)


# スタートアップイベント
@app.on_event("startup")
async def startup_event():
    init_db()


# 健康チェックエンドポイント
@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
