from .base import (
    NotFoundException,
    AlreadyExistsException,
    ValidationException,
    ForbiddenException
)

class AdminNotFoundException(NotFoundException):
    """Исключение для администратора, который не найден"""
    def __init__(self, admin_id: int = None, login: str = None):
        if admin_id:
            super().__init__(resource="Admin", resource_id=str(admin_id))
        elif login:
            super().__init__(resource="Admin", field="login", value=login)
        else:
            super().__init__(resource="Admin")

class AdminAlreadyExistsException(AlreadyExistsException):
    """Исключение для администратора, который уже существует"""
    def __init__(self, login: str):
        super().__init__(resource="Admin", field="login", value=login)

class AdminValidationException(ValidationException):
    """Исключение для ошибок валидации администратора"""
    def __init__(self, detail: str = "Admin validation error", errors: dict = None):
        super().__init__(detail=detail, errors=errors)

class AdminPermissionException(ForbiddenException):
    """Исключение для недостаточных прав администратора"""
    def __init__(self, required_permission: str = None):
        if required_permission:
            detail = f"Admin requires permission: {required_permission}"
        else:
            detail = "Admin permission required"
        super().__init__(detail=detail, error_code="ADMIN_PERMISSION_REQUIRED")