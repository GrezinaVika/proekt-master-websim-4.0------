from .base import (
    InternalServerErrorException,
    ServiceUnavailableException
)

class DatabaseException(InternalServerErrorException):
    """Базовое исключение для ошибок базы данных"""
    def __init__(self, detail: str = "Database error"):
        super().__init__(detail=detail, error_code="DATABASE_ERROR")

class ConnectionException(DatabaseException):
    """Исключение для ошибок подключения к БД"""
    def __init__(self):
        detail = "Database connection error"
        super().__init__(detail=detail)

class QueryException(DatabaseException):
    """Исключение для ошибок выполнения запроса"""
    def __init__(self, query: str = None):
        if query:
            detail = f"Query execution error: {query}"
        else:
            detail = "Query execution error"
        super().__init__(detail=detail)

class ConstraintViolationException(DatabaseException):
    """Исключение для нарушений ограничений БД"""
    def __init__(self, constraint: str = None):
        if constraint:
            detail = f"Constraint violation: {constraint}"
        else:
            detail = "Database constraint violation"
        super().__init__(detail=detail)

class TransactionException(DatabaseException):
    """Исключение для ошибок транзакции"""
    def __init__(self, detail: str = "Transaction error"):
        super().__init__(detail=detail)

class MigrationException(DatabaseException):
    """Исключение для ошибок миграции"""
    def __init__(self, detail: str = "Migration error"):
        super().__init__(detail=detail, error_code="MIGRATION_ERROR")

class DatabaseUnavailableException(ServiceUnavailableException):
    """Исключение, когда БД недоступна"""
    def __init__(self):
        detail = "Database is temporarily unavailable"
        super().__init__(detail=detail, error_code="DATABASE_UNAVAILABLE")