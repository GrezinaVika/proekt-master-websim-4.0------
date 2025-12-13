# main.py
from fastapi import FastAPI
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Restaurant Management API",
    version="1.0.0",
    description="API for managing restaurant operations",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Импортируем и подключаем роуты
from app.api import dishes
from app.api import order
from app.api import tables
from app.api import categories
from app.api import order_items
from app.api import waiter_stayistics
from app.api import cook_statistics
from app.api import waiter
from app.api import admin
from app.api import cook
from app.api import users
from app.api import roles
from app.api import migration

app.include_router(dishes.router)
app.include_router(order.router)
app.include_router(tables.router)
app.include_router(categories.router)
app.include_router(order_items.router)
app.include_router(waiter_stayistics.router)
app.include_router(cook_statistics.router)
app.include_router(waiter.router)
app.include_router(admin.router)
app.include_router(cook.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(migration.router)

@app.on_event("startup")
def startup_event():
    from app.database.database import init_db
    init_db()
    print("✅ Database initialized")

@app.get("/")
def read_root():
    return {
        "message": "Restaurant Management API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)