from typing import Optional
from sqlalchemy.orm import Session

from infrastructure.database.connection import DB, get_db_instance


class Repository:
    """リポジトリのレジストリ"""

    def __init__(self, db: DB):
        self.db = db

    @classmethod
    def new_repository(cls) -> tuple["Repository", Optional[Exception]]:
        """リポジトリのレジストリを返す
        内部でPostgreSQLへのコネクションを確立する
        """
        try:
            db = get_db_instance()
            repo = cls(db=db)
            return repo, None
        except Exception as e:
            return cls(db=None), e

    def get_db(self) -> Session:
        """PostgreSQLへのコネクションを返す"""
        return self.db
