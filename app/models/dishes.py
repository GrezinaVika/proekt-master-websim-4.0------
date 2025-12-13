# dishes.py
from typing import Optional
from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

class DishesModel(Base):
    __tablename__ = "dishes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    admin_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_available: Mapped[bool] = mapped_column(default=True)
    cooking_time: Mapped[int] = mapped_column(Integer, default=15)