from typing import List, Optional, Dict, Any
from datetime import datetime

from src.domain.todo.aggregate import Todo
from src.infrastructure.database.models import TodoModel
from src.infrastructure.database.connection import DB
from src.infrastructure.database.repository_base import RepositoryBase


class TodoRepository(RepositoryBase[TodoModel, Todo]):
    """
    Todoエンティティのリポジトリ実装
    """

    def __init__(self, db: DB):
        """
        初期化

        Args:
            db: データベース抽象化クラス
        """
        super().__init__(db, TodoModel)

    def _to_entity(self, model: TodoModel) -> Todo:
        """
        モデルからエンティティへの変換

        Args:
            model: 変換するモデル

        Returns:
            変換されたエンティティ
        """
        if model is None:
            return None

        return Todo(
            id=model.id,
            title=model.title,
            description=model.description,
            completed=model.completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Todo) -> TodoModel:
        """
        エンティティからモデルへの変換

        Args:
            entity: 変換するエンティティ

        Returns:
            変換されたモデル
        """
        # 既存のモデルを取得または新規作成
        if entity.id is not None:
            model = self.db.get().get(TodoModel, entity.id)
            if model is None:
                model = TodoModel(id=entity.id)
        else:
            model = TodoModel()

        # プロパティの設定
        model.title = entity.title
        model.description = entity.description
        model.completed = entity.completed

        # 作成日時と更新日時の設定
        now = datetime.utcnow()
        if entity.created_at is None:
            model.created_at = now
        else:
            model.created_at = entity.created_at

        model.updated_at = entity.updated_at or now

        return model

    def find_completed(self) -> List[Todo]:
        """
        完了済みのTodoを検索

        Returns:
            完了済みTodoのリスト
        """
        return self.find_by(completed=True)

    def find_pending(self) -> List[Todo]:
        """
        未完了のTodoを検索

        Returns:
            未完了Todoのリスト
        """
        return self.find_by(completed=False)
