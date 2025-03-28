from typing import Optional
from uuid import UUID

from domain.todo.aggregate import Todo
from domain.todo.repository import TodoRepository
from infra.database.entites import TodoModel
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
            self.session.query(TodoModel).filter(TodoModel.id == str(todo_id)).first()
        )
        return self._to_entity(model) if model else None

    async def create(self, todo: Todo) -> Todo:
        """新しいTodoエンティティを保存"""
        model = self._to_model(todo)

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

    def _to_model(self, entity: Todo) -> TodoModel:
        """ドメインエンティティからデータベースモデルに変換"""
        return TodoModel(
            id=str(entity.id),
            title=entity.title,
            description=entity.description,
            completed=entity.completed,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
