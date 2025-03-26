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

    class Config:
        """Pydanticの設定"""

        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "牛乳を買う",
                "description": "スーパーで低脂肪乳を購入する",
                "is_completed": False,
                "created_at": "2023-01-01T12:00:00",
                "updated_at": "2023-01-01T12:00:00",
            }
        }


class TodoListResponse(BaseModel):
    """Todoアイテムのリストレスポンススキーマ"""

    items: List[TodoResponse]
    count: int
