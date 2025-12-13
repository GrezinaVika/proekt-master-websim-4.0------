from .base import (
    NotFoundException,
    AlreadyExistsException,
    ValidationException,
    ConflictException,
    BadRequestException
)

class TableNotFoundException(NotFoundException):
    """Исключение для столика, который не найден"""
    def __init__(self, table_id: int = None, table_number: int = None):
        if table_id:
            super().__init__(resource="Table", resource_id=str(table_id))
        elif table_number:
            super().__init__(resource="Table", field="table_number", value=str(table_number))
        else:
            super().__init__(resource="Table")

class TableAlreadyExistsException(AlreadyExistsException):
    """Исключение для столика, который уже существует"""
    def __init__(self, table_number: int):
        super().__init__(resource="Table", field="table_number", value=str(table_number))

class TableValidationException(ValidationException):
    """Исключение для ошибок валидации столика"""
    def __init__(self, detail: str = "Table validation error", errors: dict = None):
        super().__init__(detail=detail, errors=errors)

class TableOccupiedException(ConflictException):
    """Исключение при попытке занять уже занятый столик"""
    def __init__(self, table_id: int):
        detail = f"Table with id {table_id} is already occupied"
        super().__init__(detail=detail, error_code="TABLE_OCCUPIED")

class TableNotAvailableException(BadRequestException):
    """Исключение при попытке использовать недоступный столик"""
    def __init__(self, table_id: int):
        detail = f"Table with id {table_id} is not available"
        super().__init__(detail=detail, error_code="TABLE_NOT_AVAILABLE")

class TableCapacityException(ValidationException):
    """Исключение для некорректной вместимости столика"""
    def __init__(self, capacity: int, min_capacity: int = 1, max_capacity: int = 12):
        detail = f"Capacity {capacity} is invalid. Must be between {min_capacity} and {max_capacity}"
        super().__init__(detail=detail)