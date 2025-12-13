from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
from typing import Callable
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class ExceptionLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования исключений и метрик"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Логируем медленные запросы
            if process_time > 1.0:  # Больше 1 секунды
                logger.warning(
                    f"Slow request: {request.method} {request.url.path} "
                    f"took {process_time:.3f}s"
                )
            
            return response
            
        except Exception as exc:
            process_time = time.time() - start_time
            logger.error(
                f"Exception in request: {request.method} {request.url.path} "
                f"took {process_time:.3f}s - {type(exc).__name__}: {str(exc)}"
            )
            raise

class ErrorContextMiddleware:
    """Middleware для контекста ошибок"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            # Добавляем дополнительную информацию в контекст ошибки
            logger.error(f"Request context: {request.method} {request.url.path}")
            logger.error(f"Headers: {dict(request.headers)}")
            logger.error(f"Query params: {dict(request.query_params)}")
            raise

def setup_error_middleware(app):
    """Настройка middleware для обработки ошибок"""
    app.add_middleware(ExceptionLoggingMiddleware)
    return app