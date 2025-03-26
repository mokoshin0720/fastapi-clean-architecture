from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository


@dataclass
class TodoInputDTO:
    """Todo作成・更新用のデータ転送オブジェクト"""

    title: str
    description: Optional[str] = None


@dataclass
class TodoOutputDTO:
    """Todoの出力用データ転送オブジェクト"""

    id: UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: Todo) -> "TodoOutputDTO":
        """エンティティからDTOを作成"""
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            is_completed=entity.is_completed,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat(),
        )


class TodoUseCase:
    """
    Todoに関するユースケース

    アプリケーション層の責務を担い、ドメインロジックの調整と
    プレゼンテーション層へのインターフェースを提供します。
    """

    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def get_all_todos(self) -> List[TodoOutputDTO]:
        """
        すべてのTodoを取得

        Returns:
            TodoOutputDTOのリスト
        """
        todos = await self.repository.get_all()
        return [TodoOutputDTO.from_entity(todo) for todo in todos]

    async def get_todo_by_id(self, todo_id: UUID) -> Optional[TodoOutputDTO]:
        """
        指定されたIDのTodoを取得

        Args:
            todo_id: 取得するTodoのID

        Returns:
            見つかった場合はTodoOutputDTO、見つからない場合はNone
        """
        todo = await self.repository.get_by_id(todo_id)
        return TodoOutputDTO.from_entity(todo) if todo else None

    async def create_todo(self, input_dto: TodoInputDTO) -> TodoOutputDTO:
        """
        新しいTodoを作成

        Args:
            input_dto: 作成するTodoの情報

        Returns:
            作成されたTodoのDTO
        """
        todo = Todo.create(
            title=input_dto.title,
            description=input_dto.description,
        )

        created_todo = await self.repository.create(todo)
        return TodoOutputDTO.from_entity(created_todo)

    async def update_todo(
        self, todo_id: UUID, input_dto: TodoInputDTO
    ) -> Optional[TodoOutputDTO]:
        """
        既存のTodoを更新

        Args:
            todo_id: 更新するTodoのID
            input_dto: 更新するTodoの情報

        Returns:
            更新されたTodoのDTO、見つからない場合はNone
        """
        todo = await self.repository.get_by_id(todo_id)
        if not todo:
            return None

        todo.update(
            title=input_dto.title,
            description=input_dto.description,
        )

        updated_todo = await self.repository.update(todo)
        return TodoOutputDTO.from_entity(updated_todo)

    async def complete_todo(self, todo_id: UUID) -> Optional[TodoOutputDTO]:
        """
        Todoを完了状態にする

        Args:
            todo_id: 完了にするTodoのID

        Returns:
            更新されたTodoのDTO、見つからない場合はNone
        """
        todo = await self.repository.get_by_id(todo_id)
        if not todo:
            return None

        todo.complete()
        updated_todo = await self.repository.update(todo)
        return TodoOutputDTO.from_entity(updated_todo)

    async def delete_todo(self, todo_id: UUID) -> bool:
        """
        Todoを削除

        Args:
            todo_id: 削除するTodoのID

        Returns:
            削除が成功した場合はTrue、失敗した場合はFalse
        """
        return await self.repository.delete(todo_id)
