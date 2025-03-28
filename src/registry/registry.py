from domain.todo.repository import TodoRepository
from infra.repositories.todo_repository_impl import SQLAlchemyTodoRepository
from registry.repository import Repository
from infra.database.connection import get_db_instance


class Registry:
    """レジストリ"""

    def __init__(self):
        self.repository = Repository(get_db_instance())

    def get_todo_repository(self) -> TodoRepository:
        return SQLAlchemyTodoRepository(self.repository.db)
