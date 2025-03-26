from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


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


class TodoListResponse(BaseModel):
    """Todoアイテムのリストレスポンススキーマ"""

    items: List[TodoResponse]
    count: int
