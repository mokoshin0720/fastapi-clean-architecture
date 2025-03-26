from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.todo import Todo
from src.domain.repositories.todo_repository import TodoRepository
from src.infrastructure.database.models import TodoModel


class SQLAlchemyTodoRepository(TodoRepository):
    """
    TodoRepositoryインターフェースのSQLAlchemy実装

    ドメインリポジトリインターフェースとデータベースの橋渡しを行います。
    """

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self) -> List[Todo]:
        """すべてのTodoエンティティを取得"""
        models = self.session.query(TodoModel).all()
        return [self._to_entity(model) for model in models]

    async def get_by_id(self, todo_id: UUID) -> Optional[Todo]:
        """指定されたIDのTodoエンティティを取得"""
        model = (
            self.session.query(TodoModel).filter(TodoModel.id == str(todo_id)).first()
        )
        return self._to_entity(model) if model else None

    async def create(self, todo: Todo) -> Todo:
        """新しいTodoエンティティを保存"""
        model = TodoModel(
            id=str(todo.id),
            title=todo.title,
            description=todo.description,
            is_completed=todo.is_completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    async def update(self, todo: Todo) -> Todo:
        """既存のTodoエンティティを更新"""
        model = (
            self.session.query(TodoModel).filter(TodoModel.id == str(todo.id)).first()
        )

        if model:
            model.title = todo.title
            model.description = todo.description
            model.is_completed = todo.is_completed
            model.updated_at = todo.updated_at

            self.session.commit()
            self.session.refresh(model)

        return self._to_entity(model)

    async def delete(self, todo_id: UUID) -> bool:
        """指定されたIDのTodoエンティティを削除"""
        model = (
            self.session.query(TodoModel).filter(TodoModel.id == str(todo_id)).first()
        )

        if not model:
            return False

        self.session.delete(model)
        self.session.commit()

        return True

    def _to_entity(self, model: TodoModel) -> Todo:
        """データベースモデルからドメインエンティティに変換"""
        return Todo(
            id=UUID(model.id),
            title=model.title,
            description=model.description,
            is_completed=model.is_completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
