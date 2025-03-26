from domain.todo.repository import TodoRepository
from infra.repositories.todo_repository_impl import SQLAlchemyTodoRepository
from registry.repository import Repository


class Registry:
    """レジストリ"""

    def __init__(self, repository: Repository):
        self.repository = repository

    def get_todo_repository(self) -> TodoRepository:
        return SQLAlchemyTodoRepository(self.repository.db)
