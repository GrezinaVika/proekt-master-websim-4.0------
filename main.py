# main.py - Restaurant Management System API
import logging
from datetime import datetime
from fastapi import FastAPI, Request, Depends, HTTPException, status, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional, List
import json
import os
import sqlite3

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI(
    title="Restaurant Management System",
    version="1.0.0",
    description="Full-stack система управления рестораном",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    redirect_slashes=False
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

# ==================== DATABASE HELPERS ====================

def get_db():
    """Получение подключения к БД"""
    db_path = "restaurant.db"
    if not os.path.exists(db_path):
        init_database()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Инициализация БД"""
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('waiter', 'chef', 'admin')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица блюд
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            cooking_time INTEGER DEFAULT 15,
            description TEXT,
            available INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица столов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER UNIQUE NOT NULL,
            capacity INTEGER NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('free', 'occupied', 'reserved')) DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица заказов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_id INTEGER NOT NULL,
            waiter_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'cooking', 'ready', 'completed')) DEFAULT 'pending',
            total_amount REAL DEFAULT 0,
            dishes TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(table_id) REFERENCES tables(id),
            FOREIGN KEY(waiter_id) REFERENCES users(id)
        )
    ''')
    
    # Вставляем тестовых пользователей
    cursor.execute('DELETE FROM users')
    cursor.execute(
        'INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)',
        ('ofikNum1', '123321', 'Официант 1', 'waiter')
    )
    cursor.execute(
        'INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)',
        ('adminNum1', '123321', 'Администратор', 'admin')
    )
    cursor.execute(
        'INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)',
        ('povarNum1', '123321', 'Повар 1', 'chef')
    )
    
    # Вставляем тестовые блюда
    cursor.execute('DELETE FROM dishes')
    test_dishes = [
        ('Борщ', 350, 'Основное', 20, 'Классический украинский борщ'),
        ('Стейк', 1200, 'Основное', 25, 'Мраморная говядина на гриле'),
        ('Салат', 450, 'Основное', 15, 'Свежий овощной салат'),
        ('Кофе', 150, 'Напитки', 5, 'Крепкий эспрессо'),
        ('Чизкейк', 300, 'Десерт', 10, 'Нью-йоркский чизкейк'),
        ('Пицца', 650, 'Основное', 30, 'Пицца Маргарита'),
        ('Чай', 100, 'Напитки', 5, 'Черный чай'),
        ('Тирамису', 350, 'Десерт', 10, 'Итальянский десерт'),
    ]
    for dish in test_dishes:
        cursor.execute(
            'INSERT INTO dishes (name, price, category, cooking_time, description) VALUES (?, ?, ?, ?, ?)',
            dish
        )
    
    # Вставляем тестовые столы
    cursor.execute('DELETE FROM tables')
    test_tables = [
        (1, 4, 'У окна', 'free'),
        (2, 6, 'Центр', 'occupied'),
        (3, 2, 'Бар', 'free'),
        (4, 8, 'VIP', 'reserved'),
        (5, 4, 'Терраса', 'free'),
        (6, 4, 'У окна', 'occupied'),
        (7, 2, 'Бар', 'free'),
        (8, 6, 'Центр', 'free'),
    ]
    for table in test_tables:
        cursor.execute(
            'INSERT INTO tables (table_number, capacity, location, status) VALUES (?, ?, ?, ?)',
            table
        )
    
    # Вставляем тестовые заказы
    cursor.execute('DELETE FROM orders')
    cursor.execute(
        'INSERT INTO orders (table_id, waiter_id, status, total_amount, dishes) VALUES (?, ?, ?, ?, ?)',
        (2, 1, 'pending', 1200, json.dumps(['Борщ', 'Чай']))
    )
    cursor.execute(
        'INSERT INTO orders (table_id, waiter_id, status, total_amount, dishes) VALUES (?, ?, ?, ?, ?)',
        (4, 1, 'cooking', 800, json.dumps(['Стейк']))
    )
    cursor.execute(
        'INSERT INTO orders (table_id, waiter_id, status, total_amount, dishes) VALUES (?, ?, ?, ?, ?)',
        (1, 1, 'ready', 450, json.dumps(['Салат']))
    )
    
    conn.commit()
    conn.close()
    logger.info('✅ Database initialized')

# ==================== STARTUP ====================

@app.on_event("startup")
def startup_event():
    """Инициализация приложения при старте"""
    try:
        init_database()
        logger.info("✅ Database ready")
        logger.info("🚀 Restaurant Management System started")
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")

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
        }
    )

# ==================== API HEALTH & CONFIG ====================

@app.get("/api/")
def api_root():
    """Корень API"""
    return {
        "message": "Restaurant Management API",
        "version": "1.0.0",
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
    }

# ==================== AUTH ENDPOINTS ====================

@app.post("/api/auth/login")
async def login_for_access_token(username: str, password: str):
    """Вход в систему"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, name, role FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "access_token": f"fake-jwt-token-{username}",
                "token_type": "bearer",
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "name": user[2],
                    "role": user[3]
                }
            }
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== USER ENDPOINTS ====================

@app.get("/api/users/{user_id}/stats")
async def get_user_stats(user_id: int):
    """Статистика пользователя"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Всего заказов
        cursor.execute('SELECT COUNT(*) FROM orders WHERE waiter_id = ?', (user_id,))
        total_orders = cursor.fetchone()[0]
        
        # Активные заказы
        cursor.execute('SELECT COUNT(*) FROM orders WHERE waiter_id = ? AND status IN ("pending", "cooking")', (user_id,))
        active_orders = cursor.fetchone()[0]
        
        # Занято столов
        cursor.execute('SELECT COUNT(*) FROM tables WHERE status = "occupied"')
        occupied_tables = cursor.fetchone()[0]
        
        # Всего сотрудников
        cursor.execute('SELECT COUNT(*) FROM users')
        total_employees = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "user_id": user_id,
            "total_orders": total_orders,
            "active_orders": active_orders,
            "occupied_tables": occupied_tables,
            "total_employees": total_employees
        }
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== DISHES ENDPOINTS ====================

@app.get("/api/dishes/")
async def get_dishes():
    """Получить все блюда"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, price, category, cooking_time FROM dishes WHERE available = 1')
        dishes = [{
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'category': row[3],
            'cooking_time': row[4]
        } for row in cursor.fetchall()]
        conn.close()
        return dishes
    except Exception as e:
        logger.error(f"Get dishes error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dishes/")
async def create_dish(name: str, price: float, category: str, cooking_time: int = 15, description: str = ""):
    """Создать новое блюдо"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO dishes (name, price, category, cooking_time, description) VALUES (?, ?, ?, ?, ?)',
            (name, price, category, cooking_time, description)
        )
        conn.commit()
        dish_id = cursor.lastrowid
        conn.close()
        return {"id": dish_id, "name": name, "price": price, "category": category}
    except Exception as e:
        logger.error(f"Create dish error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/dishes/{dish_id}")
async def update_dish(dish_id: int, name: str = None, price: float = None, category: str = None, cooking_time: int = None):
    """Обновить блюдо"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        if name:
            cursor.execute('UPDATE dishes SET name = ? WHERE id = ?', (name, dish_id))
        if price is not None:
            cursor.execute('UPDATE dishes SET price = ? WHERE id = ?', (price, dish_id))
        if category:
            cursor.execute('UPDATE dishes SET category = ? WHERE id = ?', (category, dish_id))
        if cooking_time is not None:
            cursor.execute('UPDATE dishes SET cooking_time = ? WHERE id = ?', (cooking_time, dish_id))
        
        conn.commit()
        conn.close()
        return {"success": True, "dish_id": dish_id}
    except Exception as e:
        logger.error(f"Update dish error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/dishes/{dish_id}")
async def delete_dish(dish_id: int):
    """Удалить блюдо"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE dishes SET available = 0 WHERE id = ?', (dish_id,))
        conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e:
        logger.error(f"Delete dish error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== TABLES ENDPOINTS ====================

@app.get("/api/tables/")
async def get_tables():
    """Получить все столы"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, table_number, capacity, location, status FROM tables')
        tables = [{
            'id': row[0],
            'table_number': row[1],
            'capacity': row[2],
            'location': row[3],
            'status': row[4]
        } for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        logger.error(f"Get tables error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ORDERS ENDPOINTS ====================

@app.get("/api/orders/")
async def get_orders():
    """Получить все заказы"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, table_id, waiter_id, status, total_amount, dishes, created_at FROM orders')
        orders = []
        for row in cursor.fetchall():
            orders.append({
                'id': row[0],
                'table_id': row[1],
                'waiter_id': row[2],
                'status': row[3],
                'total_amount': row[4],
                'dishes': json.loads(row[5]) if row[5] else [],
                'created_at': row[6]
            })
        conn.close()
        return orders
    except Exception as e:
        logger.error(f"Get orders error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== EMPLOYEES ENDPOINTS ====================

@app.get("/api/employees/")
async def get_employees():
    """Получить всех сотрудников"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, name, role, created_at FROM users')
        employees = [{
            'id': row[0],
            'username': row[1],
            'name': row[2],
            'role': row[3],
            'created_at': row[4]
        } for row in cursor.fetchall()]
        conn.close()
        return employees
    except Exception as e:
        logger.error(f"Get employees error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/employees/")
async def create_employee(username: str, password: str, name: str, role: str):
    """Создать нового сотрудника"""
    try:
        if role not in ['waiter', 'chef', 'admin']:
            raise HTTPException(status_code=400, detail="Неверная роль")
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Проверка на дубликат
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")
        
        cursor.execute(
            'INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)',
            (username, password, name, role)
        )
        conn.commit()
        employee_id = cursor.lastrowid
        conn.close()
        
        return {
            "id": employee_id,
            "username": username,
            "name": name,
            "role": role,
            "message": "Сотрудник успешно добавлен"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create employee error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/employees/{employee_id}")
async def update_employee(employee_id: int, username: str = None, name: str = None, role: str = None, password: str = None):
    """Обновить информацию о сотруднике"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        if username:
            cursor.execute('UPDATE users SET username = ? WHERE id = ?', (username, employee_id))
        if name:
            cursor.execute('UPDATE users SET name = ? WHERE id = ?', (name, employee_id))
        if role:
            if role not in ['waiter', 'chef', 'admin']:
                raise HTTPException(status_code=400, detail="Неверная роль")
            cursor.execute('UPDATE users SET role = ? WHERE id = ?', (role, employee_id))
        if password:
            cursor.execute('UPDATE users SET password = ? WHERE id = ?', (password, employee_id))
        
        conn.commit()
        conn.close()
        return {"success": True, "employee_id": employee_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update employee error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/employees/{employee_id}")
async def delete_employee(employee_id: int):
    """Удалить сотрудника"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Не даем удалить администратора
        cursor.execute('SELECT role FROM users WHERE id = ?', (employee_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Сотрудник не найден")
        
        if user[0] == 'admin':
            raise HTTPException(status_code=400, detail="Нельзя удалить администратора")
        
        cursor.execute('DELETE FROM users WHERE id = ?', (employee_id,))
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Сотрудник удален"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete employee error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ERROR HANDLERS ====================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Обработчик 404 ошибок"""
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not Found",
                "path": request.url.path,
                "message": "API endpoint not found"
            }
        )
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "404 - Not Found"}
    )

@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    """Обработчик 500 ошибок"""
    logger.error(f"Server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )

# ==================== MAIN ====================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
