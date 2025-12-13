from .base import (
    NotFoundException,
    AlreadyExistsException,
    ValidationException,
    UnauthorizedException,
    ForbiddenException
)

class UserNotFoundException(NotFoundException):
    """Исключение для пользователя, который не найден"""
    def __init__(self, user_id: int = None, username: str = None, email: str = None):
        if user_id:
            super().__init__(resource="User", resource_id=str(user_id))
        elif username:
            super().__init__(resource="User", field="username", value=username)
        elif email:
            super().__init__(resource="User", field="email", value=email)
        else:
            super().__init__(resource="User")

class UserAlreadyExistsException(AlreadyExistsException):
    """Исключение для пользователя, который уже существует"""
    def __init__(self, field: str, value: str):
        super().__init__(resource="User", field=field, value=value)

class UserValidationException(ValidationException):
    """Исключение для ошибок валидации пользователя"""
    def __init__(self, detail: str = "User validation error", errors: dict = None):
        super().__init__(detail=detail, errors=errors)

class AuthenticationException(UnauthorizedException):
    """Исключение для ошибок аутентификации"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail=detail, error_code="AUTH_FAILED")

class InvalidCredentialsException(UnauthorizedException):
    """Исключение для неверных учетных данных"""
    def __init__(self):
        detail = "Invalid username or password"
        super().__init__(detail=detail, error_code="INVALID_CREDENTIALS")

class InactiveUserException(ForbiddenException):
    """Исключение для неактивного пользователя"""
    def __init__(self, user_id: int):
        detail = f"User with id {user_id} is inactive"
        super().__init__(detail=detail, error_code="USER_INACTIVE")

class InsufficientPermissionsException(ForbiddenException):
    """Исключение для недостаточных прав"""
    def __init__(self, required_permission: str = None):
        if required_permission:
            detail = f"Insufficient permissions. Required: {required_permission}"
        else:
            detail = "Insufficient permissions"
        super().__init__(detail=detail, error_code="INSUFFICIENT_PERMISSIONS")