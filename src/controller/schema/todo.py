from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from domain.todo.aggregate import Todo


class CreateTodoRequest(BaseModel):
    """Todoアイテム作成用リクエストスキーマ"""

    title: str = Field(..., min_length=1, max_length=255, example="牛乳を買う")
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
    def from_model(cls, model: Todo) -> "TodoResponse":
        """
        Todoモデルからレスポンススキーマを生成する

        Args:
            model: Todoモデル

        Returns:
            TodoResponse: レスポンススキーマ
        """
        return cls(
            id=model.id,
            title=model.title,
            description=model.description,
            is_completed=model.completed,
            created_at=model.created_at.isoformat() if model.created_at else "",
            updated_at=model.updated_at.isoformat() if model.updated_at else "",
        )
