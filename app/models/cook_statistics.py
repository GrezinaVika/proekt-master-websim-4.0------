# cook_statistics.py
from datetime import datetime
from sqlalchemy import DateTime, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base

class CookStatisticsModel(Base):
    __tablename__ = "cook_statistics"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    cook_id: Mapped[int] = mapped_column(Integer, nullable=False)
    active_orders: Mapped[int] = mapped_column(Integer, default=0)
    completed_orders: Mapped[int] = mapped_column(Integer, default=0)
    average_cooking_time: Mapped[float] = mapped_column(Float, default=0.0)
    last_updated: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())