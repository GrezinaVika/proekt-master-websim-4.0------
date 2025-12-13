from .base import (
    NotFoundException,
    AlreadyExistsException,
    ValidationException,
    BadRequestException
)

class CookNotFoundException(NotFoundException):
    """Исключение для повара, который не найден"""
    def __init__(self, cook_id: int = None, login: str = None):
        if cook_id:
            super().__init__(resource="Cook", resource_id=str(cook_id))
        elif login:
            super().__init__(resource="Cook", field="login", value=login)
        else:
            super().__init__(resource="Cook")

class CookAlreadyExistsException(AlreadyExistsException):
    """Исключение для повара, который уже существует"""
    def __init__(self, login: str):
        super().__init__(resource="Cook", field="login", value=login)

class CookValidationException(ValidationException):
    """Исключение для ошибок валидации повара"""
    def __init__(self, detail: str = "Cook validation error", errors: dict = None):
        super().__init__(detail=detail, errors=errors)

class CookLoginException(BadRequestException):
    """Исключение для ошибок входа повара"""
    def __init__(self, detail: str = "Cook login error"):
        super().__init__(detail=detail, error_code="COOK_LOGIN_ERROR")

class CookBusyException(BadRequestException):
    """Исключение, когда повар слишком занят"""
    def __init__(self, cook_id: int, active_orders: int):
        detail = f"Cook with id {cook_id} is busy with {active_orders} active orders"
        super().__init__(detail=detail, error_code="COOK_BUSY")