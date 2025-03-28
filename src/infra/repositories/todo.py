from typing import Optional
from uuid import UUID

from domain.todo.aggregate import Todo
from domain.todo.repository import TodoRepository
import infra.entity as entity
from app.database import DB


class SQLAlchemyTodoRepository(TodoRepository):
    """
    TodoRepositoryインターフェースのSQLAlchemy実装

    ドメインリポジトリインターフェースとデータベースの橋渡しを行います。
    """

    def __init__(self, db: DB):
        self.session = db.get()

    async def get_by_id(self, todo_id: UUID) -> Optional[Todo]:
        """指定されたIDのTodoエンティティを取得"""
        model = (
            self.session.query(entity.Todos)
            .filter(entity.Todos.id == str(todo_id))
            .first()
        )
        return self._to_entity(model) if model else None

    async def create(self, todo: Todo) -> Todo:
        """新しいTodoエンティティを保存"""
        model = self._to_model(todo)

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def _to_entity(self, model: entity.Todos) -> Todo:
        """データベースモデルからドメインエンティティに変換"""
        return Todo(
            id=UUID(model.id),
            title=model.title,
            description=model.description,
            completed=model.completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, input: Todo) -> entity.Todos:
        """ドメインエンティティからデータベースモデルに変換"""
        return entity.Todos(
            id=str(input.id),
            title=input.title,
            description=input.description,
            completed=input.completed,
            created_at=input.created_at,
            updated_at=input.updated_at,
        )
