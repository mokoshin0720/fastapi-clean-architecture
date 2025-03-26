# FastAPI クリーンアーキテクチャ & DDD テンプレート

このプロジェクトは、FastAPI を使用してクリーンアーキテクチャとドメイン駆動設計（DDD）の原則に従った TODO リストアプリケーションのテンプレートです。

## アーキテクチャ

このプロジェクトは次の層で構成されています：

- **ドメイン層**: ビジネスロジックとルールを含みます
  - エンティティ
  - 値オブジェクト
  - リポジトリインターフェース
- **アプリケーション層**: ユースケースとアプリケーションサービスを含みます
  - ユースケース
  - サービス
- **インフラストラクチャ層**: 技術的な実装の詳細を含みます
  - データベース
  - リポジトリ実装
- **プレゼンテーション層**: ユーザーインターフェースを提供します
  - API エンドポイント
  - DTO とリクエスト/レスポンスモデル

## セットアップ

### 前提条件

- Python 3.10 以上
- Poetry

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/fastapi-clean-architecture.git
cd fastapi-clean-architecture

# 依存関係をインストール
poetry install

# 環境変数を設定
cp .env.example .env
# .envファイルを編集して適切な値を設定
```

### 実行

```bash
poetry run uvicorn src.main:app --reload
```

## API エンドポイント

### TODO リスト API

- `GET /api/todos` - すべての TODO アイテムを取得
- `POST /api/todos` - 新しい TODO アイテムを作成

## 開発

```bash
# テストを実行
poetry run pytest

# コードフォーマット
poetry run black .
poetry run isort .

# 静的型チェック
poetry run mypy .
```

## アーキテクチャの利点

- **関心事の分離**: 各層は特定の責任を持ち、コードの理解と保守を容易にします
- **テスト可能性**: ビジネスロジックは外部依存から分離され、テストが容易です
- **柔軟性**: 技術的な実装の詳細は簡単に変更できます
- **スケーラビリティ**: コードベースが大きくなっても管理しやすい構造を提供します
