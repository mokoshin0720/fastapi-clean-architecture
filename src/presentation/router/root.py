from fastapi import APIRouter
from app.registry import Registry
from presentation.router.todo import TodoRouter


class RootRouter:
    def __init__(self, registry: Registry):
        self.api_router = APIRouter()
        self.api_router.add_api_route("/health", self.health_check, methods=["GET"])

        self.api_router.include_router(router=TodoRouter(registry=registry).get_router())

    def get_api_router(self):
        return self.api_router

    async def health_check(self):
        return {"status": "healthy"}
