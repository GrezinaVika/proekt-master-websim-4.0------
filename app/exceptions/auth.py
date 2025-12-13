from .base import (
    UnauthorizedException,
    ForbiddenException,
    BadRequestException
)

class TokenException(UnauthorizedException):
    """Базовое исключение для ошибок токена"""
    def __init__(self, detail: str = "Token error"):
        super().__init__(detail=detail, error_code="TOKEN_ERROR")

class InvalidTokenException(TokenException):
    """Исключение для невалидного токена"""
    def __init__(self):
        detail = "Invalid token"
        super().__init__(detail=detail)

class ExpiredTokenException(TokenException):
    """Исключение для просроченного токена"""
    def __init__(self):
        detail = "Token has expired"
        super().__init__(detail=detail)

class MissingTokenException(TokenException):
    """Исключение для отсутствующего токена"""
    def __init__(self):
        detail = "Token is missing"
        super().__init__(detail=detail)

class InvalidTokenTypeException(TokenException):
    """Исключение для неверного типа токена"""
    def __init__(self, expected: str, actual: str):
        detail = f"Invalid token type. Expected: {expected}, got: {actual}"
        super().__init__(detail=detail)

class OAuthException(BadRequestException):
    """Исключение для ошибок OAuth"""
    def __init__(self, detail: str = "OAuth error"):
        super().__init__(detail=detail, error_code="OAUTH_ERROR")

class RegistrationException(BadRequestException):
    """Исключение для ошибок регистрации"""
    def __init__(self, detail: str = "Registration error"):
        super().__init__(detail=detail, error_code="REGISTRATION_ERROR")