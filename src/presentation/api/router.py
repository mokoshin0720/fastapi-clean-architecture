from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.todo_use_cases import TodoInputDTO, TodoUseCase
from src.presentation.api.dependencies import get_todo_use_case
from src.presentation.api.schemas import (
    TodoCreate,
    TodoListResponse,
    TodoResponse,
    TodoUpdate,
)

# APIルーターの作成
api_router = APIRouter()

# TODOエンドポイント
todo_router = APIRouter(prefix="/todos", tags=["todos"])


@todo_router.get(
    "",
    response_model=TodoListResponse,
    summary="すべてのTODOアイテムを取得",
    description="データベースに保存されているすべてのTODOアイテムを取得します。",
)
async def get_todos(
    use_case: TodoUseCase = Depends(get_todo_use_case),
):
    """
    すべてのTODOアイテムを取得するエンドポイント
    """
    todos = await use_case.get_all_todos()
    return TodoListResponse(items=todos, count=len(todos))


@todo_router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="特定のTODOアイテムを取得",
    description="指定されたIDのTODOアイテムを取得します。存在しない場合は404エラーを返します。",
)
async def get_todo(
    todo_id: UUID,
    use_case: TodoUseCase = Depends(get_todo_use_case),
):
    """
    特定のTODOアイテムを取得するエンドポイント
    """
    todo = await use_case.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {todo_id} のTODOアイテムは見つかりませんでした",
        )
    return todo


@todo_router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="新しいTODOアイテムを作成",
    description="提供された情報から新しいTODOアイテムを作成します。",
)
async def create_todo(
    todo_create: TodoCreate,
    use_case: TodoUseCase = Depends(get_todo_use_case),
):
    """
    新しいTODOアイテムを作成するエンドポイント
    """
    input_dto = TodoInputDTO(
        title=todo_create.title,
        description=todo_create.description,
    )

    created_todo = await use_case.create_todo(input_dto)
    return created_todo


@todo_router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="TODOアイテムを更新",
    description="指定されたIDのTODOアイテムを更新します。存在しない場合は404エラーを返します。",
)
async def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    use_case: TodoUseCase = Depends(get_todo_use_case),
):
    """
    TODOアイテムを更新するエンドポイント
    """
    if not any([todo_update.title, todo_update.description is not None]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="更新するフィールドが指定されていません",
        )

    input_dto = TodoInputDTO(
        title=todo_update.title if todo_update.title else "",
        description=todo_update.description,
    )

    updated_todo = await use_case.update_todo(todo_id, input_dto)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {todo_id} のTODOアイテムは見つかりませんでした",
        )

    return updated_todo


@todo_router.patch(
    "/{todo_id}/complete",
    response_model=TodoResponse,
    summary="TODOアイテムを完了としてマーク",
    description="指定されたIDのTODOアイテムを完了状態にします。存在しない場合は404エラーを返します。",
)
async def complete_todo(
    todo_id: UUID,
    use_case: TodoUseCase = Depends(get_todo_use_case),
):
    """
    TODOアイテムを完了としてマークするエンドポイント
    """
    completed_todo = await use_case.complete_todo(todo_id)
    if not completed_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {todo_id} のTODOアイテムは見つかりませんでした",
        )

    return completed_todo


@todo_router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="TODOアイテムを削除",
    description="指定されたIDのTODOアイテムを削除します。",
)
async def delete_todo(
    todo_id: UUID,
    use_case: TodoUseCase = Depends(get_todo_use_case),
):
    """
    TODOアイテムを削除するエンドポイント
    """
    await use_case.delete_todo(todo_id)
    return None


# すべてのルーターを登録
api_router.include_router(todo_router)
