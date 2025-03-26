from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends

from registry.registry import Registry
from dto.todo import TodoInputDTO, TodoOutputDTO
from presentation.api.dependencies import get_registry

import uc

from presentation.api.schemas import (
    TodoCreate,
    TodoResponse,
)

# APIルーターの作成
api_router = APIRouter()

# TODOエンドポイント
todo_router = APIRouter(prefix="/todos", tags=["todos"])


@todo_router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="特定のTODOアイテムを取得",
    description="指定されたIDのTODOアイテムを取得します。存在しない場合は404エラーを返します。",
)
async def get_todo(
    todo_id: UUID,
    registry: Registry = Depends(get_registry),
):
    todo = await uc.get_todo_by_id(repository=registry.repository, todo_id=todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {todo_id} のTODOアイテムは見つかりませんでした",
        )

    return TodoOutputDTO.from_entity(todo)


@todo_router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="新しいTODOアイテムを作成",
    description="提供された情報から新しいTODOアイテムを作成します。",
)
async def create_todo(
    todo_create: TodoCreate,
    registry: Registry = Depends(get_registry),
):
    input_dto = TodoInputDTO(
        title=todo_create.title,
        description=todo_create.description,
    )

    todo = await uc.CreateTodo(registry=registry).do(input_dto)

    return TodoOutputDTO.from_entity(todo)


# すべてのルーターを登録
api_router.include_router(todo_router)
