import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from infra.database.connection import init_db
from presentation.router.root import RootRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


# FastAPIアプリケーションのインスタンスを作成
app = FastAPI(
    title="FastAPI クリーンアーキテクチャ & DDD テンプレート",
    description="FastAPIを使用したクリーンアーキテクチャとDDDのテンプレート",
    version="0.1.0",
    lifespan=lifespan,
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
router = RootRouter().get_api_router()
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
