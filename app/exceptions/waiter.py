from .base import (
    NotFoundException,
    AlreadyExistsException,
    ValidationException,
    BadRequestException
)

class WaiterNotFoundException(NotFoundException):
    """Исключение для официанта, который не найден"""
    def __init__(self, waiter_id: int = None, login: str = None):
        if waiter_id:
            super().__init__(resource="Waiter", resource_id=str(waiter_id))
        elif login:
            super().__init__(resource="Waiter", field="login", value=login)
        else:
            super().__init__(resource="Waiter")

class WaiterAlreadyExistsException(AlreadyExistsException):
    """Исключение для официанта, который уже существует"""
    def __init__(self, login: str):
        super().__init__(resource="Waiter", field="login", value=login)

class WaiterValidationException(ValidationException):
    """Исключение для ошибок валидации официанта"""
    def __init__(self, detail: str = "Waiter validation error", errors: dict = None):
        super().__init__(detail=detail, errors=errors)

class WaiterLoginException(BadRequestException):
    """Исключение для ошибок входа официанта"""
    def __init__(self, detail: str = "Waiter login error"):
        super().__init__(detail=detail, error_code="WAITER_LOGIN_ERROR")

class WaiterShiftException(BadRequestException):
    """Исключение для ошибок смены официанта"""
    def __init__(self, detail: str = "Waiter shift error"):
        super().__init__(detail=detail, error_code="WAITER_SHIFT_ERROR")