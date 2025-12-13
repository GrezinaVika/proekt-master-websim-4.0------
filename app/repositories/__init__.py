# app/repositories/__init__.py
from .dishes import DishRepository
from .orders import OrderRepository
from .tables import TableRepository
from .categories import CategoryRepository
from .order_items import OrderItemRepository
from .waiter_statistics import WaiterStatisticsRepository
from .cook_statistics import CookStatisticsRepository
from .waiter import WaiterRepository
from .admin import AdminRepository
from .cook import CookRepository
from .users import UserRepository
from .roles import RoleRepository
from .migration import MigrationRepository

__all__ = [
    "DishRepository",
    "OrderRepository",
    "TableRepository",
    "CategoryRepository",
    "OrderItemRepository",
    "WaiterStatisticsRepository",
    "CookStatisticsRepository",
    "WaiterRepository",
    "AdminRepository",
    "CookRepository",
    "UserRepository",
    "RoleRepository",
    "MigrationRepository",
]