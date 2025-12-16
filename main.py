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

# ==================== LOGGING ====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== FASTAPI SETUP ====================

app = FastAPI(
    title="Restaurant Management System",
    version="1.0.0",
    description="Full-stack ресторан system",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ==================== API ROUTES ====================

try:
    from app.api import (
        dishes, order, tables, order_items,
        waiter_stayistics, cook_statistics, waiter,
        admin, cook, users, roles, migration
    )
    
    api_prefix = "/api"
    app.include_router(dishes.router, prefix=api_prefix)
    app.include_router(order.router, prefix=api_prefix)
    app.include_router(tables.router, prefix=api_prefix)
    app.include_router(order_items.router, prefix=api_prefix)
    app.include_router(waiter_stayistics.router, prefix=api_prefix)
    app.include_router(cook_statistics.router, prefix=api_prefix)
    app.include_router(waiter.router, prefix=api_prefix)
    app.include_router(admin.router, prefix=api_prefix)
    app.include_router(cook.router, prefix=api_prefix)
    app.include_router(users.router, prefix=api_prefix)
    app.include_router(roles.router, prefix=api_prefix)
    app.include_router(migration.router, prefix=api_prefix)
except ImportError as e:
    logger.error(f"Failed to import API modules: {e}")
    raise

# ==================== STARTUP ====================

@app.on_event("startup")
def startup_event() -> None:
    """Initialize on startup"""
    try:
        from app.database.database import init_db
        init_db()
        logger.info("✅ Database initialized")
        logger.info("🚀 System started")
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
async def read_root(request: Request) -> HTMLResponse:
    """Main page"""
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
        logger.error(f"Error rendering root: {e}")
        raise

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request) -> HTMLResponse:
    """Admin page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "Ресторан | Админ", "page": "admin"}
        )
    except Exception as e:
        logger.error(f"Error rendering admin: {e}")
        raise

@app.get("/waiter", response_class=HTMLResponse)
async def waiter_panel(request: Request) -> HTMLResponse:
    """Waiter page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "Ресторан | Официант", "page": "waiter"}
        )
    except Exception as e:
        logger.error(f"Error rendering waiter: {e}")
        raise

@app.get("/cook", response_class=HTMLResponse)
async def cook_panel(request: Request) -> HTMLResponse:
    """Chef page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "Ресторан | Повар", "page": "cook"}
        )
    except Exception as e:
        logger.error(f"Error rendering cook: {e}")
        raise

@app.get("/tables", response_class=HTMLResponse)
async def tables_view(request: Request) -> HTMLResponse:
    """Tables page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "Ресторан | Столы", "page": "tables"}
        )
    except Exception as e:
        logger.error(f"Error rendering tables: {e}")
        raise

@app.get("/menu", response_class=HTMLResponse)
async def menu_view(request: Request) -> HTMLResponse:
    """Menu page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "Ресторан | Меню", "page": "menu"}
        )
    except Exception as e:
        logger.error(f"Error rendering menu: {e}")
        raise

@app.get("/orders", response_class=HTMLResponse)
async def orders_view(request: Request) -> HTMLResponse:
    """Orders page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "Ресторан | Заказы", "page": "orders"}
        )
    except Exception as e:
        logger.error(f"Error rendering orders: {e}")
        raise

@app.get("/statistics", response_class=HTMLResponse)
async def statistics_view(request: Request) -> HTMLResponse:
    """Statistics page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "Ресторан | Статистика", "page": "stats"}
        )
    except Exception as e:
        logger.error(f"Error rendering stats: {e}")
        raise

# ==================== API ENDPOINTS ====================

@app.get("/api/")
async def api_root() -> Dict[str, Any]:
    """API root"""
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
    """Health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/config")
async def get_config() -> Dict[str, Any]:
    """Get config"""
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

# ==================== AUTH ENDPOINTS ====================

@app.post("/api/auth/login")
async def login_for_access_token(
    username: str,
    password: str,
    role: Optional[str] = None
) -> Dict[str, Any]:
    """Login"""
    test_users: Dict[str, Dict[str, Any]] = {
        "ofikNum1": {"id": 1, "username": "ofikNum1", "name": "Официант 1", "role": "waiter", "password": "123321"},
        "adminNum1": {"id": 2, "username": "adminNum1", "name": "Админ", "role": "admin", "password": "123321"},
        "povarNum1": {"id": 3, "username": "povarNum1", "name": "Повар", "role": "chef", "password": "123321"}
    }
    
    if username not in test_users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные данные")
    
    user = test_users[username]
    if user.get("password") != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные данные")
    
    user_copy = user.copy()
    user_copy.pop("password", None)
    return {"access_token": f"token-{username}", "token_type": "bearer", "user": user_copy}

@app.post("/api/auth/register")
async def register_user(username: str, password: str, role: str = "waiter") -> Dict[str, Any]:
    """Register"""
    return {"id": 999, "username": username, "name": f"User {username}", "role": role}

@app.get("/api/users/me")
async def get_current_user_info() -> Dict[str, Any]:
    """Get current user"""
    return {"id": 1, "username": "ofikNum1", "name": "Официант 1", "role": "waiter"}

@app.get("/api/users/{user_id}/stats")
async def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Get user stats"""
    return {"user_id": user_id, "total_orders": 15, "active_orders": 3, "occupied_tables": 2, "total_revenue": 12500.50}

# ==================== ERROR HANDLERS ====================

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse | HTMLResponse:
    """Handle 404"""
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"error": "Not found", "path": request.url.path})
    
    try:
        return templates.TemplateResponse("index.html", {"request": request, "title": "404", "page": "404"})
    except Exception as e:
        logger.error(f"404 error: {e}")
        return JSONResponse(status_code=404, content={"error": "Page not found"})

# ==================== MAIN ====================

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_config=None)