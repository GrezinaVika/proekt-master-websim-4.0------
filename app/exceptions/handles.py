from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback
from typing import Dict, Any

from .base import RestaurantAPIException
from .database import DatabaseException, DatabaseUnavailableException
from . import (
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    ValidationException,
    BadRequestException,
    ConflictException,
    InternalServerErrorException,
    ServiceUnavailableException,
    TooManyRequestsException
)

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI):
    """Настройка обработчиков исключений для FastAPI приложения"""
    
    @app.exception_handler(RestaurantAPIException)
    async def restaurant_api_exception_handler(request: Request, exc: RestaurantAPIException):
        """Обработчик для кастомных исключений ресторана"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.detail,
                    "type": exc.__class__.__name__,
                    "path": request.url.path,
                    "timestamp": exc.headers.get("timestamp") if exc.headers else None
                }
            },
            headers=exc.headers
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Обработчик для стандартных HTTP исключений"""
        logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": f"HTTP_{exc.status_code}",
                    "message": exc.detail,
                    "type": "HTTPException",
                    "path": request.url.path
                }
            },
            headers=exc.headers
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Обработчик для ошибок валидации запроса"""
        logger.warning(f"Validation error: {exc.errors()}")
        
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "type": "ValidationError",
                    "path": request.url.path,
                    "details": errors
                }
            }
        )
    
    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException):
        """Обработчик для ошибок базы данных"""
        logger.error(f"Database error: {exc.detail}")
        
        # Для продакшена скрываем детали ошибок БД
        is_production = True  # В реальном приложении проверять окружение
        if is_production:
            message = "Database error occurred. Please try again later."
        else:
            message = exc.detail
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": message,
                    "type": exc.__class__.__name__,
                    "path": request.url.path
                }
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Обработчик для всех остальных исключений"""
        logger.error(f"Unhandled exception: {str(exc)}")
        logger.error(traceback.format_exc())
        
        # Для продакшена скрываем детали внутренних ошибок
        is_production = True  # В реальном приложении проверять окружение
        if is_production:
            message = "Internal server error. Please contact support."
        else:
            message = str(exc)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": message,
                    "type": exc.__class__.__name__,
                    "path": request.url.path
                }
            }
        )

class ErrorResponse:
    """Класс для стандартизированных ответов с ошибками"""
    
    @staticmethod
    def not_found(resource: str, resource_id: str = None) -> Dict[str, Any]:
        if resource_id:
            message = f"{resource} with id {resource_id} not found"
        else:
            message = f"{resource} not found"
        
        return {
            "error": {
                "code": "NOT_FOUND",
                "message": message,
                "type": "NotFoundException"
            }
        }
    
    @staticmethod
    def validation_error(errors: list) -> Dict[str, Any]:
        return {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed",
                "type": "ValidationException",
                "details": errors
            }
        }
    
    @staticmethod
    def unauthorized(message: str = "Unauthorized") -> Dict[str, Any]:
        return {
            "error": {
                "code": "UNAUTHORIZED",
                "message": message,
                "type": "UnauthorizedException"
            }
        }
    
    @staticmethod
    def forbidden(message: str = "Forbidden") -> Dict[str, Any]:
        return {
            "error": {
                "code": "FORBIDDEN",
                "message": message,
                "type": "ForbiddenException"
            }
        }
    
    @staticmethod
    def conflict(message: str) -> Dict[str, Any]:
        return {
            "error": {
                "code": "CONFLICT",
                "message": message,
                "type": "ConflictException"
            }
        }
    
    @staticmethod
    def bad_request(message: str) -> Dict[str, Any]:
        return {
            "error": {
                "code": "BAD_REQUEST",
                "message": message,
                "type": "BadRequestException"
            }
        }