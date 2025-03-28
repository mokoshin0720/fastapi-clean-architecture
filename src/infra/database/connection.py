import os
from pathlib import Path
from typing import Any, Dict, Generator, Callable, TypeVar
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 環境変数のロード
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# PostgreSQLデータベースURL
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "todo")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# SQLiteの場合、connect_argsを追加
connect_args: Dict[str, Any] = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# エンジンとセッションの作成
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    global _db_instance
    if _db_instance is None:
        session = SessionLocal()
        _db_instance = DB(session)
    return _db_instance
