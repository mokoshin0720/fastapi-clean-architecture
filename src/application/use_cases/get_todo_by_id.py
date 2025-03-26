from typing import Optional
from uuid import UUID

from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository


async def get_todo_by_id(repository: TodoRepository, todo_id: UUID) -> Optional[Todo]:
    """
    指定されたIDのTodoを取得

    Args:
        repository: Todoリポジトリ
        todo_id: 取得するTodoのID

    Returns:
        見つかった場合はTodoエンティティ、見つからない場合はNone
    """
    return await repository.get_by_id(todo_id)
