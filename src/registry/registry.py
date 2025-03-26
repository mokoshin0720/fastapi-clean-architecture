from registry.repository import Repository


class Registry:
    """レジストリ"""

    def __init__(self, repository: Repository):
        self.repository = repository
