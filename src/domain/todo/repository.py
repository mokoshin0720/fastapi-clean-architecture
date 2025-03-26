from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.todo.aggregate import Todo


class TodoRepository(ABC):
    """
    Todoエンティティのリポジトリインターフェース

    このインターフェースは、永続化の詳細から独立してドメインロジックを
    操作できるようにするために定義されています。
    """

    @abstractmethod
    async def get_by_id(self, todo_id: UUID) -> Optional[Todo]:
        """
        指定されたIDのTodoエンティティを取得します

        Args:
            todo_id: 取得するTodoのID

        Returns:
            見つかった場合はTodoエンティティ、見つからない場合はNone
        """
        pass

    @abstractmethod
    async def create(self, todo: Todo) -> Todo:
        """
        新しいTodoエンティティを保存します

        Args:
            todo: 保存するTodoエンティティ

        Returns:
            保存されたTodoエンティティ
        """
        pass
