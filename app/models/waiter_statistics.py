# waiter_statistics.py
from datetime import datetime
from sqlalchemy import DateTime, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base

class WaiterStatisticsModel(Base):
    __tablename__ = "waiter_statistics"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    waiter_id: Mapped[int] = mapped_column(Integer, nullable=False)
    total_orders: Mapped[int] = mapped_column(Integer, default=0)
    occupied_tables: Mapped[int] = mapped_column(Integer, default=0)
    total_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    tips_amount: Mapped[float] = mapped_column(Float, default=0.0)
    hours_worked: Mapped[float] = mapped_column(Float, default=0.0)
    last_updated: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())