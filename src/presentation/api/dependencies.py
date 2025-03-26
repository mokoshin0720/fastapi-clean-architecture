from fastapi import Depends
from sqlalchemy.orm import Session

from application.use_cases.todo_use_cases import TodoUseCase
from infrastructure.database.connection import get_db
from infrastructure.repositories.todo_repository_impl import (
    SQLAlchemyTodoRepository,
)


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


def get_todo_use_case(repository=Depends(get_todo_repository)):
    """
    TodoUseCaseの依存関係プロバイダ

    TodoRepositoryを取得し、TodoUseCaseインスタンスを作成

    Args:
        repository: TodoRepositoryインスタンス

    Returns:
        TodoUseCaseインスタンス
    """
    return TodoUseCase(repository)
