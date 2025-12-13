# waiter.py
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

class WaiterModel(Base):
    __tablename__ = "waiter"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="waiter")
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)