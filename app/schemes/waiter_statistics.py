from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class WaiterStatisticsBase(BaseModel):
    waiter_id: int
    total_orders: int = 0
    occupied_tables: int = 0
    total_revenue: float = 0.0
    tips_amount: float = 0.0
    hours_worked: float = 0.0

class WaiterStatisticsCreate(WaiterStatisticsBase):
    pass

class WaiterStatisticsUpdate(BaseModel):
    total_orders: Optional[int] = None
    occupied_tables: Optional[int] = None
    total_revenue: Optional[float] = None
    tips_amount: Optional[float] = None
    hours_worked: Optional[float] = None

class WaiterStatisticsResponse(WaiterStatisticsBase):
    id: int
    last_updated: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True