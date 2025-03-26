import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 環境変数のロード
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# データベースURL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# SQLiteの場合、connect_argsを追加
connect_args: Dict[str, Any] = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# エンジンとセッションの作成
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラス
Base = declarative_base()


def get_db():
    """
    データベースセッションを取得するジェネレータ

    使用例:
    ```
    db = next(get_db())
    try:
        # データベース操作
    finally:
        db.close()
    ```

    または、FastAPIの依存関係注入機能と併用:
    ```
    @app.get("/items/")
    def read_items(db: Session = Depends(get_db)):
        # データベース操作
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    データベースの初期化
    アプリケーション起動時に呼び出される
    """
    # すべてのテーブルを作成
    Base.metadata.create_all(bind=engine)
