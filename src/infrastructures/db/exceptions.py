class RepositoryError(Exception):
    """Базовое исключение репозитория."""
    pass


class RepositoryConflictError(RepositoryError):
    """Ошибка возникающая при нарушении ограничений целостности (например, unique)."""
    pass