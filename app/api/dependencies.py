from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.database import get_db

# Импортируем репозитории
from app.repositories.dishes import DishRepository
from app.repositories.orders import OrderRepository
from app.repositories.tables import TableRepository
from app.repositories.order_items import OrderItemRepository
from app.repositories.waiter_statistics import WaiterStatisticsRepository
from app.repositories.cook_statistics import CookStatisticsRepository
from app.repositories.waiter import WaiterRepository
from app.repositories.admin import AdminRepository
from app.repositories.cook import CookRepository
from app.repositories.users import UserRepository
from app.repositories.roles import RoleRepository
from app.repositories.migration import MigrationRepository

# Импортируем сервисы
from app.services.dishes import DishService
from app.services.order import OrderService
from app.services.tables import TableService
from app.services.order_items import OrderItemService
from app.services.waiter_statistics import WaiterStatisticsService
from app.services.cook_statistics import CookStatisticsService
from app.services.waiter import WaiterService
from app.services.admin import AdminService
from app.services.cook import CookService
from app.services.users import UserService
from app.services.roles import RoleService
from app.services.migration import MigrationService

# Dependency для репозиториев
def get_dish_repository(db: Session = Depends(get_db)):
    return DishRepository(db)

def get_order_repository(db: Session = Depends(get_db)):
    return OrderRepository(db)

def get_table_repository(db: Session = Depends(get_db)):
    return TableRepository(db)

def get_order_item_repository(db: Session = Depends(get_db)):
    return OrderItemRepository(db)

def get_waiter_statistics_repository(db: Session = Depends(get_db)):
    return WaiterStatisticsRepository(db)

def get_cook_statistics_repository(db: Session = Depends(get_db)):
    return CookStatisticsRepository(db)

def get_waiter_repository(db: Session = Depends(get_db)):
    return WaiterRepository(db)

def get_admin_repository(db: Session = Depends(get_db)):
    return AdminRepository(db)

def get_cook_repository(db: Session = Depends(get_db)):
    return CookRepository(db)

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_role_repository(db: Session = Depends(get_db)):
    return RoleRepository(db)

def get_migration_repository(db: Session = Depends(get_db)):
    return MigrationRepository(db)

# Dependency для сервисов
def get_dish_service(repo: DishRepository = Depends(get_dish_repository)):
    return DishService(repo)

def get_order_service(repo: OrderRepository = Depends(get_order_repository)):
    return OrderService(repo)

def get_table_service(repo: TableRepository = Depends(get_table_repository)):
    return TableService(repo)

def get_order_item_service(repo: OrderItemRepository = Depends(get_order_item_repository)):
    return OrderItemService(repo)

def get_waiter_statistics_service(repo: WaiterStatisticsRepository = Depends(get_waiter_statistics_repository)):
    return WaiterStatisticsService(repo)

def get_cook_statistics_service(repo: CookStatisticsRepository = Depends(get_cook_statistics_repository)):
    return CookStatisticsService(repo)

def get_waiter_service(repo: WaiterRepository = Depends(get_waiter_repository)):
    return WaiterService(repo)

def get_admin_service(repo: AdminRepository = Depends(get_admin_repository)):
    return AdminService(repo)

def get_cook_service(repo: CookRepository = Depends(get_cook_repository)):
    return CookService(repo)

def get_user_service(repo: UserRepository = Depends(get_user_repository)):
    return UserService(repo)

def get_role_service(repo: RoleRepository = Depends(get_role_repository)):
    return RoleService(repo)

def get_migration_service(repo: MigrationRepository = Depends(get_migration_repository)):
    return MigrationService(repo)