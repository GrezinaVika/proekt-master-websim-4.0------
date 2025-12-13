# app/database/database.py
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# SQLite база данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./restaurant.db"

# Создаем движок SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True  # Показывает SQL запросы в консоли
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Включаем поддержку внешних ключей для SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def get_db():
    """Зависимость для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Инициализация базы данных - создание таблиц"""
    # Импортируем все модели, чтобы они зарегистрировались у Base
    from app.database.database import Base
    from app.models.admin import AdminModel
    from app.models.categories import CategoriesModel
    from app.models.cook_statistics import CookStatisticsModel
    from app.models.cook import CookModel
    from app.models.dishes import DishesModel
    from app.models.migration import MigrationHistory
    from app.models.order_items import OrderItemsModel
    from app.models.order import OrderModel
    from app.models.roles import Role
    from app.models.tables import TablesModel
    from app.models.users import User
    from app.models.waiter import WaiterModel
    from app.models.waiter_statistics import WaiterStatisticsModel
    
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    print(f"✅ Создано таблиц: {len(Base.metadata.tables)}")
    
    # Выводим список созданных таблиц
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("📊 Созданные таблицы:")
    for table in tables:
        print(f"  - {table}")