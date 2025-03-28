from typing import Optional
from uuid import UUID

from domain.todo.aggregate import Todo
from app.registry import Registry


class GetTodoById:
    """
    指定されたIDのTodoを取得するユースケース
    """

    def __init__(self, registry: Registry):
        self.todo_repository = registry.get_todo_repository()

    async def do(self, todo_id: UUID) -> Optional[Todo]:
        """
        指定されたIDのTodoを取得

        Args:
            todo_id: 取得するTodoのID

        Returns:
            見つかった場合はTodoエンティティ、見つからない場合はNone
        """
        return await self.todo_repository.get_by_id(todo_id)
