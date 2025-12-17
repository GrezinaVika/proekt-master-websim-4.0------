# main.py
import logging
from datetime import datetime
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Инициализация FastAPI
app = FastAPI(
    title="Restaurant Management System",
    version="1.0.0",
    description="Full-stack система управления рестораном",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключаем шаблоны
templates = Jinja2Templates(directory="app/templates")

# Импортируем и подключаем API роуты
from app.api import dishes
from app.api import order
from app.api import tables
from app.api import categories
from app.api import order_items
from app.api import waiter_statistics
from app.api import cook_statistics
from app.api import waiter
from app.api import admin
from app.api import cook
from app.api import users
from app.api import roles
from app.api import migration

# Подключаем API роуты с префиксом /api
api_prefix = "/api"
app.include_router(dishes.router, prefix=api_prefix)
app.include_router(order.router, prefix=api_prefix)
app.include_router(tables.router, prefix=api_prefix)
app.include_router(categories.router, prefix=api_prefix)
app.include_router(order_items.router, prefix=api_prefix)
app.include_router(waiter_statistics.router, prefix=api_prefix)
app.include_router(cook_statistics.router, prefix=api_prefix)
app.include_router(waiter.router, prefix=api_prefix)
app.include_router(admin.router, prefix=api_prefix)
app.include_router(cook.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)
app.include_router(roles.router, prefix=api_prefix)
app.include_router(migration.router, prefix=api_prefix)

@app.on_event("startup")
def startup_event():
    """Инициализация приложения при старте"""
    from app.database.database import init_db
    init_db()
    logging.info("✅ Database initialized")
    logging.info("🚀 Restaurant Management System started")

# ==================== ДОПОЛНИТЕЛЬНЫЕ ПУТИ ДОКУМЕНТАЦИИ ====================

@app.get("/docs", include_in_schema=False)
async def redirect_to_api_docs():
    """Перенаправление с /docs на /api/docs"""
    return RedirectResponse(url="/api/docs")

@app.get("/redoc", include_in_schema=False)
async def redirect_to_api_redoc():
    """Перенаправление с /redoc на /api/redoc"""
    return RedirectResponse(url="/api/redoc")

@app.get("/openapi.json", include_in_schema=False)
async def redirect_to_openapi():
    """Перенаправление на OpenAPI спецификацию"""
    return RedirectResponse(url="/api/openapi.json")

# ==================== FRONTEND ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Главная страница приложения"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Ресторан | Главная",
            "version": "1.0.0",
            "year": datetime.now().year,
            "api_docs_url": "/docs",
            "api_redoc_url": "/redoc"
        }
    )

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    """Панель администратора"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Ресторан | Админ панель",
            "page": "admin",
            "api_docs_url": "/docs"
        }
    )

@app.get("/waiter", response_class=HTMLResponse)
async def waiter_panel(request: Request):
    """Панель официанта"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Ресторан | Панель официанта",
            "page": "waiter",
            "api_docs_url": "/docs"
        }
    )

@app.get("/cook", response_class=HTMLResponse)
async def cook_panel(request: Request):
    """Панель повара"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Ресторан | Панель повара",
            "page": "cook",
            "api_docs_url": "/docs"
        }
    )

@app.get("/tables", response_class=HTMLResponse)
async def tables_view(request: Request):
    """Управление столиками"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Ресторан | Столики",
            "page": "tables",
            "api_docs_url": "/docs"
        }
    )

@app.get("/menu", response_class=HTMLResponse)
async def menu_view(request: Request):
    """Меню ресторана"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Ресторан | Меню",
            "page": "menu",
            "api_docs_url": "/docs"
        }
    )

@app.get("/orders", response_class=HTMLResponse)
async def orders_view(request: Request):
    """Управление заказами"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Ресторан | Заказы",
            "page": "orders",
            "api_docs_url": "/docs"
        }
    )

@app.get("/statistics", response_class=HTMLResponse)
async def statistics_view(request: Request):
    """Статистика"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Ресторан | Статистика",
            "page": "statistics",
            "api_docs_url": "/docs"
        }
    )

# ==================== ВСПОМОГАТЕЛЬНЫЕ API МАРШРУТЫ ====================

@app.get("/api/")
def api_root():
    """Корень API"""
    return {
        "message": "Restaurant Management API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth/...",
            "users": "/api/users/...",
            "dishes": "/api/dishes/...",
            "tables": "/api/tables/...",
            "orders": "/api/orders/...",
        },
        "docs": "/api/docs",
        "docs_alt": "/docs",
        "redoc": "/api/redoc",
        "redoc_alt": "/redoc",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/health")
def health_check():
    """Проверка здоровья API"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/config")
async def get_config():
    """Получение конфигурации для фронтенда"""
    return {
        "api_url": "/api",
        "app_name": "Restaurant Management System",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "features": {
            "admin": True,
            "waiter": True,
            "cook": True,
            "tables": True,
            "menu": True,
            "orders": True,
            "statistics": True
        }
    }

# Временные эндпоинты для тестирования фронтенда
@app.post("/api/auth/login")
async def login_for_access_token(username: str, password: str, role: Optional[str] = None):
    """Вход в систему (временная реализация)"""
    # Эмуляция аутентификации
    test_users = {
        "ofikNum1": {"id": 1, "username": "ofikNum1", "name": "Официант 1", "role": "waiter", "password": "123321"},
        "adminNum1": {"id": 2, "username": "adminNum1", "name": "Администратор", "role": "admin", "password": "123321"},
        "povarNum1": {"id": 3, "username": "povarNum1", "name": "Повар 1", "role": "chef", "password": "123321"}
    }
    
    if username in test_users and test_users[username]["password"] == password:
        user = test_users[username].copy()
        user.pop("password")
        return {
            "access_token": f"fake-jwt-token-{username}",
            "token_type": "bearer",
            "user": user
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные учетные данные"
    )

@app.post("/api/auth/register")
async def register_user(username: str, password: str, role: str = "waiter"):
    """Регистрация пользователя (временная реализация)"""
    return {
        "id": 999,
        "username": username,
        "name": f"Новый {role}",
        "role": role,
        "message": "Пользователь зарегистрирован (демо)"
    }

@app.get("/api/users/me")
async def get_current_user_info():
    """Получение информации о текущем пользователе (демо)"""
    # В реальном приложении здесь была бы проверка токена
    return {
        "id": 1,
        "username": "ofikNum1",
        "name": "Официант 1",
        "role": "waiter"
    }

@app.get("/api/users/{user_id}/stats")
async def get_user_stats(user_id: int):
    """Статистика пользователя (демо)"""
    return {
        "user_id": user_id,
        "total_orders": 15,
        "active_orders": 3,
        "occupied_tables": 2,
        "total_revenue": 12500.50
    }

# ==================== ERROR HANDLERS ====================

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc):
    """Обработчик 404 ошибок"""
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=404,
            content={
                "message": "API endpoint not found", 
                "path": request.url.path,
                "available_endpoints": [
                    "/api/docs",
                    "/api/auth/login",
                    "/api/auth/register",
                    "/api/users/me",
                    "/api/users/{id}/stats",
                    "/api/dishes/",
                    "/api/tables/",
                    "/api/orders/",
                    "/api/health",
                    "/api/config"
                ]
            }
        )
    
    # Для не-API запросов возвращаем главную страницу (SPA)
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Страница не найдена",
            "page": "404"
        }
    )

# ==================== MAIN ====================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None
    )
