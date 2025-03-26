from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.todo import Todo


class TodoRepository(ABC):
    """
    Todoエンティティのリポジトリインターフェース

    このインターフェースは、永続化の詳細から独立してドメインロジックを
    操作できるようにするために定義されています。
    """

    @abstractmethod
    async def get_all(self) -> List[Todo]:
        """
        すべてのTodoエンティティを取得します

        Returns:
            Todoエンティティのリスト
        """
        pass

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

    @abstractmethod
    async def update(self, todo: Todo) -> Todo:
        """
        既存のTodoエンティティを更新します

        Args:
            todo: 更新するTodoエンティティ

        Returns:
            更新されたTodoエンティティ
        """
        pass

    @abstractmethod
    async def delete(self, todo_id: UUID) -> bool:
        """
        指定されたIDのTodoエンティティを削除します

        Args:
            todo_id: 削除するTodoのID

        Returns:
            削除が成功した場合はTrue、失敗した場合はFalse
        """
        pass
