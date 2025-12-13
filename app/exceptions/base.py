from fastapi import HTTPException, status
from typing import Optional, Dict, Any

class RestaurantAPIException(HTTPException):
    """Базовое исключение для API ресторана"""
    def __init__(
        self, 
        detail: str, 
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: Optional[Dict[str, str]] = None,
        error_code: Optional[str] = None
    ):
        super().__init__(
            status_code=status_code, 
            detail=detail,
            headers=headers
        )
        self.error_code = error_code or f"ERR_{status_code}"

class NotFoundException(RestaurantAPIException):
    """Исключение для случаев, когда объект не найден"""
    def __init__(
        self, 
        resource: str, 
        resource_id: Optional[str] = None,
        field: Optional[str] = None,
        value: Optional[str] = None
    ):
        if field and value:
            detail = f"{resource} with {field} '{value}' not found"
        elif resource_id:
            detail = f"{resource} with id {resource_id} not found"
        else:
            detail = f"{resource} not found"
        
        super().__init__(
            detail=detail, 
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND"
        )
        self.resource = resource
        self.resource_id = resource_id

class AlreadyExistsException(RestaurantAPIException):
    """Исключение для случаев, когда объект уже существует"""
    def __init__(
        self, 
        resource: str, 
        field: str,
        value: str
    ):
        detail = f"{resource} with {field} '{value}' already exists"
        super().__init__(
            detail=detail, 
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="RESOURCE_EXISTS"
        )
        self.resource = resource
        self.field = field
        self.value = value

class UnauthorizedException(RestaurantAPIException):
    """Исключение для случаев неавторизованного доступа"""
    def __init__(
        self, 
        detail: str = "Invalid credentials",
        error_code: Optional[str] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=error_code or "UNAUTHORIZED"
        )

class ForbiddenException(RestaurantAPIException):
    """Исключение для случаев запрещенного доступа"""
    def __init__(
        self, 
        detail: str = "Access forbidden",
        error_code: Optional[str] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=error_code or "FORBIDDEN"
        )

class ValidationException(RestaurantAPIException):
    """Исключение для ошибок валидации"""
    def __init__(
        self, 
        detail: str = "Validation error",
        errors: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR"
        )
        self.errors = errors or {}

class BadRequestException(RestaurantAPIException):
    """Исключение для некорректных запросов"""
    def __init__(
        self, 
        detail: str = "Bad request",
        error_code: Optional[str] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code or "BAD_REQUEST"
        )

class ConflictException(RestaurantAPIException):
    """Исключение для конфликтующих операций"""
    def __init__(
        self, 
        detail: str = "Conflict",
        error_code: Optional[str] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=status.HTTP_409_CONFLICT,
            error_code=error_code or "CONFLICT"
        )

class InternalServerErrorException(RestaurantAPIException):
    """Исключение для внутренних ошибок сервера"""
    def __init__(
        self, 
        detail: str = "Internal server error",
        error_code: Optional[str] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code or "INTERNAL_ERROR"
        )

class ServiceUnavailableException(RestaurantAPIException):
    """Исключение для временной недоступности сервиса"""
    def __init__(
        self, 
        detail: str = "Service temporarily unavailable",
        error_code: Optional[str] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code=error_code or "SERVICE_UNAVAILABLE"
        )

class TooManyRequestsException(RestaurantAPIException):
    """Исключение для превышения лимита запросов"""
    def __init__(
        self, 
        detail: str = "Too many requests",
        retry_after: Optional[int] = None
    ):
        headers = {}
        if retry_after:
            headers["Retry-After"] = str(retry_after)
        
        super().__init__(
            detail=detail, 
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            headers=headers,
            error_code="RATE_LIMIT_EXCEEDED"
        )