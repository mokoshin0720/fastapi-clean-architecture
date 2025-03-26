from typing import Generic, TypeVar, Type, List, Optional, Any, Dict, Union

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.infrastructure.database.connection import DB, Base

# エンティティとモデルのための型変数
T = TypeVar("T", bound=Base)
E = TypeVar("E")  # エンティティ型


class RepositoryBase(Generic[T, E]):
    """
    リポジトリパターンの基底クラス
    すべてのリポジトリはこのクラスを継承することで、
    基本的なCRUD操作を実装できる
    """

    def __init__(self, db: DB, model_class: Type[T]):
        """
        初期化

        Args:
            db: データベース抽象化クラス
            model_class: リポジトリが扱うモデルクラス
        """
        self.db = db
        self.model_class = model_class

    def find_all(self) -> List[E]:
        """
        すべてのエンティティを取得

        Returns:
            エンティティのリスト
        """
        stmt = select(self.model_class)
        models = self.db.get().execute(stmt).scalars().all()
        return [self._to_entity(model) for model in models]

    def find_by_id(self, id: Any) -> Optional[E]:
        """
        IDによるエンティティ取得

        Args:
            id: エンティティのID

        Returns:
            エンティティ、存在しない場合はNone
        """
        model = self.db.get().get(self.model_class, id)
        return self._to_entity(model) if model else None

    def find_by(self, **kwargs) -> List[E]:
        """
        条件によるエンティティ検索

        Args:
            **kwargs: フィルター条件

        Returns:
            条件に一致するエンティティのリスト
        """
        stmt = select(self.model_class).filter_by(**kwargs)
        models = self.db.get().execute(stmt).scalars().all()
        return [self._to_entity(model) for model in models]

    def create(self, entity: E) -> E:
        """
        エンティティの作成

        Args:
            entity: 作成するエンティティ

        Returns:
            作成されたエンティティ
        """
        model = self._to_model(entity)
        self.db.get().add(model)
        self.db.get().flush()
        return self._to_entity(model)

    def update(self, entity: E) -> E:
        """
        エンティティの更新

        Args:
            entity: 更新するエンティティ

        Returns:
            更新されたエンティティ
        """
        model = self._to_model(entity)
        model = self.db.get().merge(model)
        self.db.get().flush()
        return self._to_entity(model)

    def delete(self, entity: Union[E, int]) -> None:
        """
        エンティティの削除

        Args:
            entity: 削除するエンティティまたはエンティティのID
        """
        if isinstance(entity, int):
            model = self.db.get().get(self.model_class, entity)
            if model:
                self.db.get().delete(model)
        else:
            model = self._to_model(entity)
            self.db.get().delete(model)
        self.db.get().flush()

    def _to_entity(self, model: T) -> E:
        """
        モデルからエンティティへの変換
        サブクラスでオーバーライドする必要がある

        Args:
            model: 変換するモデル

        Returns:
            変換されたエンティティ
        """
        raise NotImplementedError("サブクラスで実装する必要があります")

    def _to_model(self, entity: E) -> T:
        """
        エンティティからモデルへの変換
        サブクラスでオーバーライドする必要がある

        Args:
            entity: 変換するエンティティ

        Returns:
            変換されたモデル
        """
        raise NotImplementedError("サブクラスで実装する必要があります")
