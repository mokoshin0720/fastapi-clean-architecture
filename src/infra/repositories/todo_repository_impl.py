from typing import Optional
from uuid import UUID

from domain.todo.aggregate import Todo
from domain.todo.repository import TodoRepository
from infra.database.models import TodoModel
from infra.database.connection import DB


class SQLAlchemyTodoRepository(TodoRepository):
    """
    TodoRepositoryインターフェースのSQLAlchemy実装

    ドメインリポジトリインターフェースとデータベースの橋渡しを行います。
    """

    def __init__(self, db: DB):
        self.db = db
        self.session = db.get()

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
            completed=todo.completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def _to_entity(self, model: TodoModel) -> Todo:
        """データベースモデルからドメインエンティティに変換"""
        return Todo(
            id=UUID(model.id),
            title=model.title,
            description=model.description,
            completed=model.completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
