# FastAPI クリーンアーキテクチャ & DDD テンプレート

このプロジェクトは、FastAPI を使用してクリーンアーキテクチャとドメイン駆動設計（DDD）の原則に従った TODO リストアプリケーションのテンプレートです。

## アーキテクチャ

このプロジェクトは以下のクリーンアーキテクチャの原則に従って構築されています：

### レイヤー構造

- **ドメイン層** (`src/domain/`): ビジネスルールとドメインモデルを含む中心的な層

  - 集約（Aggregate）、エンティティ、値オブジェクト、リポジトリインターフェースなどを定義
  - 例: `domain/todo/aggregate.py` - TODO アイテムのドメインモデル

- **ユースケース層** (`src/usecase/`): アプリケーションの具体的なユースケースを実装

  - ドメイン層のオブジェクトを操作するためのビジネスロジック
  - 例: `usecase/create_todo.py`, `usecase/get_todo_by_id.py`

- **コントローラー層** (`src/controller/`): HTTP リクエストの受け取りと応答を担当

  - API エンドポイントの定義とルーティング
  - リクエスト/レスポンスのスキーマ定義
  - 例: `controller/router/`, `controller/schema/`

- **インフラストラクチャ層** (`src/infra/`): 外部サービスとの連携を担当
  - データベースへのアクセス
  - リポジトリの実装
  - 例: `infra/repositories/`, `infra/entity.py`

### 依存関係の方向

内側の層（ドメイン）は外側の層（インフラ）に依存せず、外側の層が内側の層に依存します。これにより、ドメインロジックを外部の実装詳細から分離し、テスト容易性と保守性を向上させています。

### 依存性注入

依存オブジェクト（リポジトリなど）は上位のレイヤーから下位のレイヤーに注入されます。`app/registry.py` を通じて依存関係を管理し、疎結合なアーキテクチャを実現しています。

## セットアップ

### 前提条件

- [aqua](https://aquaproj.github.io/)でパッケージ管理をしているため、インストールをしておく

## サーバー起動方法

```
aqua i # 必要なパッケージをインストール
task setup
task dev
```

## API エンドポイント

### TODO リスト API

- `GET /api/todos` - すべての TODO アイテムを取得
- `POST /api/todos` - 新しい TODO アイテムを作成

## DB 操作

データベースに変更を加える手順：

1. `migration/schema.sql` ファイルでテーブル定義を修正する
2. `task codegen` コマンドを実行して、SQLAlchemy 用のモデルを自動生成する

これにより、`src/infra/entity.py` ファイルが更新され、データベーススキーマの変更がコードに反映されます。
