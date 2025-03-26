from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Todo:
    """
    Todoエンティティクラス
    ドメインロジックを含むビジネスオブジェクト
    """

    id: Optional[int]
    title: str
    description: Optional[str]
    completed: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

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
            completed=False,
            created_at=now,
            updated_at=now,
        )

    def mark_as_completed(self) -> None:
        """
        Todoを完了状態にする
        """
        self.completed = True
        self.updated_at = datetime.utcnow()

    def update_title(self, new_title: str) -> None:
        """
        Todoのタイトルを更新する

        Args:
            new_title: 新しいタイトル
        """
        if not new_title:
            raise ValueError("タイトルは空にできません")

        self.title = new_title
        self.updated_at = datetime.utcnow()

    def update_description(self, new_description: Optional[str]) -> None:
        """
        Todoの説明を更新する

        Args:
            new_description: 新しい説明
        """
        self.description = new_description
        self.updated_at = datetime.utcnow()

    def toggle_completion(self) -> None:
        """
        Todoの完了状態を切り替える
        """
        self.completed = not self.completed
        self.updated_at = datetime.utcnow()
