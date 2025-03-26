from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.database.connection import get_db
from infrastructure.repositories.todo_repository_impl import (
    SQLAlchemyTodoRepository,
)
from registry.registry import Registry
from registry.repository import Repository


def get_todo_repository(db: Session = Depends(get_db)):
    """
    TodoRepositoryの依存関係プロバイダ

    SQLAlchemyセッションを取得し、TodoRepositoryインスタンスを作成

    Args:
        db: SQLAlchemyデータベースセッション

    Returns:
        TodoRepositoryインスタンス
    """
    return SQLAlchemyTodoRepository(db)


def get_registry(repository=Depends(get_todo_repository)):
    """
    Registryの依存関係プロバイダ

    リポジトリインスタンスを取得し、Registryインスタンスを作成

    Args:
        repository: リポジトリインスタンス

    Returns:
        Registryインスタンス
    """
    return Registry(repository=repository)
