# tables.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base

class TablesModel(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    table_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String(50), default="available")
    capacity: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    current_order_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now())