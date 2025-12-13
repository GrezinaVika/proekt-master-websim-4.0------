from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    table_id: int
    cook_id: Optional[int] = None
    waiters_id: Optional[int] = None
    status: str = "Создан"

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    table_id: Optional[int] = None
    cook_id: Optional[int] = None
    waiters_id: Optional[int] = None
    status: Optional[str] = None

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True