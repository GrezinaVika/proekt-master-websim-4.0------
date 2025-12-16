"""Restaurant Management System - Main Application"""
import logging
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ==================== LOGGING CONFIGURATION ====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== FASTAPI INITIALIZATION ====================

app = FastAPI(
    title="Restaurant Management System",
    version="1.0.0",
    description="Full-stack restaurant management system",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# ==================== MIDDLEWARE CONFIGURATION ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== STATIC FILES AND TEMPLATES ====================

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ==================== API ROUTES IMPORT ====================

try:
    from app.api import (
        dishes, order, tables, order_items,
        waiter_stayistics, cook_statistics, waiter,
        admin, cook, users, roles, migration
    )
except ImportError as e:
    logger.error(f"Failed to import API modules: {e}")
    raise

# ==================== API ROUTER REGISTRATION ====================

api_prefix = "/api"
routers = [
    (dishes.router, "dishes"),
    (order.router, "orders"),
    (tables.router, "tables"),
    (order_items.router, "order_items"),
    (waiter_stayistics.router, "waiter_statistics"),
    (cook_statistics.router, "cook_statistics"),
    (waiter.router, "waiter"),
    (admin.router, "admin"),
    (cook.router, "cook"),
    (users.router, "users"),
    (roles.router, "roles"),
    (migration.router, "migration")
]

for router, name in routers:
    try:
        app.include_router(router, prefix=api_prefix)
        logger.debug(f"Registered router: {name}")
    except Exception as e:
        logger.warning(f"Failed to register router {name}: {e}")

# ==================== STARTUP EVENT ====================

@app.on_event("startup")
async def startup_event() -> None:
    """Initialize database on application startup"""
    try:
        from app.database.database import init_db
        init_db()
        logger.info("✅ Database initialized")
        logger.info("🚀 Restaurant Management System started")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise

# ==================== DOCUMENTATION REDIRECTS ====================

@app.get("/docs", include_in_schema=False)
async def redirect_to_api_docs() -> RedirectResponse:
    """Redirect /docs to /api/docs"""
    return RedirectResponse(url="/api/docs")


@app.get("/redoc", include_in_schema=False)
async def redirect_to_api_redoc() -> RedirectResponse:
    """Redirect /redoc to /api/redoc"""
    return RedirectResponse(url="/api/redoc")


@app.get("/openapi.json", include_in_schema=False)
async def redirect_to_openapi() -> RedirectResponse:
    """Redirect /openapi.json to /api/openapi.json"""
    return RedirectResponse(url="/api/openapi.json")

# ==================== FRONTEND ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request) -> str:
    """Main application page"""
    try:
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
    except Exception as e:
        logger.error(f"Error rendering root page: {e}")
        raise


@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request) -> str:
    """Admin panel page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Ресторан | Админ панель",
                "page": "admin",
                "api_docs_url": "/docs"
            }
        )
    except Exception as e:
        logger.error(f"Error rendering admin page: {e}")
        raise


@app.get("/waiter", response_class=HTMLResponse)
async def waiter_panel(request: Request) -> str:
    """Waiter panel page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Ресторан | Панель официанта",
                "page": "waiter",
                "api_docs_url": "/docs"
            }
        )
    except Exception as e:
        logger.error(f"Error rendering waiter page: {e}")
        raise


@app.get("/cook", response_class=HTMLResponse)
async def cook_panel(request: Request) -> str:
    """Chef panel page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Ресторан | Панель повара",
                "page": "cook",
                "api_docs_url": "/docs"
            }
        )
    except Exception as e:
        logger.error(f"Error rendering cook page: {e}")
        raise


@app.get("/tables", response_class=HTMLResponse)
async def tables_view(request: Request) -> str:
    """Tables management page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Ресторан | Столики",
                "page": "tables",
                "api_docs_url": "/docs"
            }
        )
    except Exception as e:
        logger.error(f"Error rendering tables page: {e}")
        raise


@app.get("/menu", response_class=HTMLResponse)
async def menu_view(request: Request) -> str:
    """Menu page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Ресторан | Меню",
                "page": "menu",
                "api_docs_url": "/docs"
            }
        )
    except Exception as e:
        logger.error(f"Error rendering menu page: {e}")
        raise


@app.get("/orders", response_class=HTMLResponse)
async def orders_view(request: Request) -> str:
    """Orders management page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Ресторан | Заказы",
                "page": "orders",
                "api_docs_url": "/docs"
            }
        )
    except Exception as e:
        logger.error(f"Error rendering orders page: {e}")
        raise


@app.get("/statistics", response_class=HTMLResponse)
async def statistics_view(request: Request) -> str:
    """Statistics page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Ресторан | Статистика",
                "page": "statistics",
                "api_docs_url": "/docs"
            }
        )
    except Exception as e:
        logger.error(f"Error rendering statistics page: {e}")
        raise

# ==================== API ENDPOINTS ====================

@app.get("/api/")
async def api_root() -> Dict[str, Any]:
    """API root endpoint"""
    return {
        "message": "Restaurant Management API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth/...",
            "users": "/api/users/...",
            "dishes": "/api/dishes/...",
            "tables": "/api/tables/...",
            "orders": "/api/orders/..."
        },
        "docs": "/api/docs",
        "docs_alt": "/docs",
        "redoc": "/api/redoc",
        "redoc_alt": "/redoc",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/health")
async def health_check() -> Dict[str, str]:
    """API health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/config")
async def get_config() -> Dict[str, Any]:
    """Get frontend configuration"""
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

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/api/auth/login")
async def login_for_access_token(
    username: str,
    password: str,
    role: Optional[str] = None
) -> Dict[str, Any]:
    """User login endpoint (demo implementation)"""
    test_users: Dict[str, Dict[str, Any]] = {
        "ofikNum1": {
            "id": 1,
            "username": "ofikNum1",
            "name": "Официант 1",
            "role": "waiter",
            "password": "123321"
        },
        "adminNum1": {
            "id": 2,
            "username": "adminNum1",
            "name": "Администратор",
            "role": "admin",
            "password": "123321"
        },
        "povarNum1": {
            "id": 3,
            "username": "povarNum1",
            "name": "Повар 1",
            "role": "chef",
            "password": "123321"
        }
    }

    if username not in test_users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )

    user = test_users[username]
    if user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )

    user_copy = user.copy()
    user_copy.pop("password")
    return {
        "access_token": f"fake-jwt-token-{username}",
        "token_type": "bearer",
        "user": user_copy
    }


@app.post("/api/auth/register")
async def register_user(
    username: str,
    password: str,
    role: str = "waiter"
) -> Dict[str, Any]:
    """User registration endpoint (demo implementation)"""
    return {
        "id": 999,
        "username": username,
        "name": f"Новый {role}",
        "role": role,
        "message": "Пользователь зарегистрирован (демо)"
    }


@app.get("/api/users/me")
async def get_current_user_info() -> Dict[str, Any]:
    """Get current user info (demo)"""
    return {
        "id": 1,
        "username": "ofikNum1",
        "name": "Официант 1",
        "role": "waiter"
    }


@app.get("/api/users/{user_id}/stats")
async def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Get user statistics (demo)"""
    return {
        "user_id": user_id,
        "total_orders": 15,
        "active_orders": 3,
        "occupied_tables": 2,
        "total_revenue": 12500.50
    }

# ==================== ERROR HANDLERS ====================

@app.exception_handler(404)
async def not_found_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse | HTMLResponse:
    """Handle 404 errors"""
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=404,
            content={
                "message": "API endpoint not found",
                "path": request.url.path,
                "available_endpoints": [
                    "/api/docs",
                    "/api/health",
                    "/api/config",
                    "/api/auth/login",
                    "/api/auth/register",
                    "/api/users/me",
                    "/api/users/{id}/stats",
                    "/api/dishes/",
                    "/api/tables/",
                    "/api/orders/"
                ]
            }
        )

    # Return main page for non-API requests (SPA)
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Страница не найдена",
                "page": "404"
            }
        )
    except Exception as e:
        logger.error(f"Error handling 404: {e}")
        return JSONResponse(
            status_code=404,
            content={"error": "Page not found"}
        )


@app.exception_handler(500)
async def internal_error_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle 500 errors"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
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