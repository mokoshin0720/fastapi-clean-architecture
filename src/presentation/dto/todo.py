from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.entities.todo import Todo


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
