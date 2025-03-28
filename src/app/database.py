from typing import Generator, Callable
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from app.config import Config

# ベースクラス
Base = declarative_base()


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

    def execute_in_transaction(self, func: Callable[["DB"], any]) -> any:
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
    config = Config()

    # データベース接続URL
    database_url = f"postgresql://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}"

    # エンジンとセッションの作成
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    global _db_instance
    if _db_instance is None:
        session = SessionLocal()
        _db_instance = DB(session)
    return _db_instance
