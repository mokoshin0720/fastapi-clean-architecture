from domain.todo.repository import TodoRepository
from infra.repositories.todo_repository_impl import SQLAlchemyTodoRepository
from app.database import get_db_instance


class Registry:
    """レジストリ"""

    def __init__(self):
        self.db = get_db_instance()

    def get_todo_repository(self) -> TodoRepository:
        return SQLAlchemyTodoRepository(self.db)
