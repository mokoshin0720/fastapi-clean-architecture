from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from app.registry import Registry
import usecase
from controller.schema.todo import (
    CreateTodoRequest,
    TodoResponse,
)


class TodoRouter:
    def __init__(self, registry: Registry):
        self.router = APIRouter(prefix="/todos", tags=["todos"])
        self._register_routes()
        self.registry = registry

    def get_router(self):
        return self.router

    def _register_routes(self):
        self.router.add_api_route(
            "/{todo_id}",
            self.get_todo,
            methods=["GET"],
            response_model=TodoResponse,
            summary="特定のTODOアイテムを取得",
            description="指定されたIDのTODOアイテムを取得します。存在しない場合は404エラーを返します。",
        )
        self.router.add_api_route(
            "",
            self.create_todo,
            methods=["POST"],
            response_model=TodoResponse,
            status_code=status.HTTP_201_CREATED,
            summary="新しいTODOアイテムを作成",
            description="提供された情報から新しいTODOアイテムを作成します。",
        )

    async def get_todo(
        self,
        todo_id: UUID,
    ):
        todo = await usecase.GetTodoById(registry=self.registry).do(todo_id=todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {todo_id} のTODOアイテムは見つかりませんでした",
            )

        return TodoResponse.from_entity(todo)

    async def create_todo(
        self,
        todo_create: CreateTodoRequest,
    ):
        input_dto = CreateTodoRequest(
            title=todo_create.title,
            description=todo_create.description,
        )

        todo = await usecase.CreateTodo(registry=self.registry).do(input_dto)

        return TodoResponse.from_entity(todo)
