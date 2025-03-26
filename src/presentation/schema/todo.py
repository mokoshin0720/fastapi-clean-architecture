from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from domain.todo.aggregate import Todo


class TodoCreate(BaseModel):
    """Todoアイテム作成用リクエストスキーマ"""

    title: str = Field(..., min_length=1, max_length=255, example="牛乳を買う")
    description: Optional[str] = Field(None, example="スーパーで低脂肪乳を購入する")


class TodoUpdate(BaseModel):
    """Todoアイテム更新用リクエストスキーマ"""

    title: Optional[str] = Field(
        None, min_length=1, max_length=255, example="牛乳を買う"
    )
    description: Optional[str] = Field(None, example="スーパーで低脂肪乳を購入する")


class TodoResponse(BaseModel):
    """Todoアイテムレスポンススキーマ"""

    id: UUID
    title: str
    description: Optional[str] = None
    is_completed: bool
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, todo: Todo) -> "TodoResponse":
        """
        Todoエンティティからレスポンススキーマを生成する

        Args:
            todo: Todoエンティティ

        Returns:
            TodoResponse: レスポンススキーマ
        """
        return cls(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            is_completed=todo.completed,
            created_at=todo.created_at.isoformat() if todo.created_at else "",
            updated_at=todo.updated_at.isoformat() if todo.updated_at else "",
        )


class TodoListResponse(BaseModel):
    """Todoアイテムのリストレスポンススキーマ"""

    items: List[TodoResponse]
    count: int

    @classmethod
    def from_entities(cls, todos: List[Todo]) -> "TodoListResponse":
        """
        Todoエンティティのリストからレスポンススキーマを生成する

        Args:
            todos: Todoエンティティのリスト

        Returns:
            TodoListResponse: レスポンススキーマ
        """
        items = [TodoResponse.from_entity(todo) for todo in todos]
        return cls(items=items, count=len(items))
