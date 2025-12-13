from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CookStatisticsBase(BaseModel):
    cook_id: int
    active_orders: int = 0

class CookStatisticsCreate(CookStatisticsBase):
    pass

class CookStatisticsUpdate(BaseModel):
    active_orders: Optional[int] = None

class CookStatisticsResponse(CookStatisticsBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True