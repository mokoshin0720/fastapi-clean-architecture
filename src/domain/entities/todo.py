from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Todo:
    """
    Todoエンティティクラス

    ドメインのコアとなるエンティティで、Todoアイテムを表現します。
    """

    id: UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, title: str, description: Optional[str] = None) -> "Todo":
        """
        新しいTodoエンティティを作成するファクトリメソッド

        Args:
            title: Todoのタイトル
            description: Todoの詳細説明（オプション）

        Returns:
            新しく作成されたTodoエンティティ
        """
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            title=title,
            description=description,
            is_completed=False,
            created_at=now,
            updated_at=now,
        )

    def complete(self) -> None:
        """Todoを完了状態にマークします"""
        self.is_completed = True
        self.updated_at = datetime.utcnow()

    def uncomplete(self) -> None:
        """Todoの完了状態を解除します"""
        self.is_completed = False
        self.updated_at = datetime.utcnow()

    def update(
        self, title: Optional[str] = None, description: Optional[str] = None
    ) -> None:
        """
        Todoの情報を更新します

        Args:
            title: 新しいタイトル
            description: 新しい説明
        """
        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        self.updated_at = datetime.utcnow()
