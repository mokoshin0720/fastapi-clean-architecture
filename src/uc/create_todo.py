from domain.todo.aggregate import Todo
from presentation.schema.todo import TodoCreate
from registry.registry import Registry


class CreateTodo:
    """
    新しいTodoを作成するユースケース
    """

    def __init__(self, registry: Registry):
        """
        コンストラクタ

        Args:
            registry: レジストリ
        """
        self.todo_repository = registry.get_todo_repository()

    async def do(self, input_dto: TodoCreate) -> Todo:
        """
        新しいTodoを作成

        Args:
            input_dto: 作成するTodoの情報

        Returns:
            作成されたTodoエンティティ
        """
        todo = Todo.create(
            title=input_dto.title,
            description=input_dto.description,
        )

        return await self.todo_repository.create(todo)
