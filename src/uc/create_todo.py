from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository
from dto.todo import TodoInputDTO


async def create_todo(repository: TodoRepository, input_dto: TodoInputDTO) -> Todo:
    """
    新しいTodoを作成

    Args:
        repository: Todoリポジトリ
        input_dto: 作成するTodoの情報

    Returns:
        作成されたTodoエンティティ
    """
    todo = Todo.create(
        title=input_dto.title,
        description=input_dto.description,
    )

    return await repository.create(todo)
