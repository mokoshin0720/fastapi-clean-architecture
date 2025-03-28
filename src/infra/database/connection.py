import os
from typing import Any, Dict, Generator, Callable, TypeVar
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

# ベースクラス
Base = declarative_base()

# 型変数
T = TypeVar("T")


class DB:
    """
    データベースのコネクションを管理する構造体
    """

    def __init__(self, session: Session):
        self.session = session

    def begin(self) -> "DB":
        """トランザクションを開始する"""
        return DB(self.session.begin_nested())

    def commit(self) -> None:
        """トランザクションをコミットする"""
        self.session.commit()

    def rollback(self) -> None:
        """トランザクションをロールバックする"""
        self.session.rollback()

    def get(self) -> Session:
        """SQLAlchemyのセッションを返す"""
        return self.session

    @contextmanager
    def transaction(self) -> Generator["DB", None, None]:
        """トランザクションを実行する"""
        try:
            yield self
            self.commit()
        except Exception:
            self.rollback()
            raise

    def execute_in_transaction(self, func: Callable[["DB"], T]) -> T:
        """トランザクション内で関数を実行する"""
        try:
            result = func(self)
            self.commit()
            return result
        except Exception:
            self.rollback()
            raise


# シングルトンパターンでDBインスタンスを提供
_db_instance = None


def get_db_instance() -> DB:
    """
    シングルトンパターンでDBインスタンスを取得する
    一度だけセッションを生成し、アプリケーション全体で共有する
    """

    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "todo")

    # データベース接続URL
    database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # エンジンとセッションの作成
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    global _db_instance
    if _db_instance is None:
        session = SessionLocal()
        _db_instance = DB(session)
    return _db_instance
