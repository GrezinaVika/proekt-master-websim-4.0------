from pydantic import BaseModel
from typing import Optional

class OrderItemBase(BaseModel):
    order_id: int
    menu_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    menu_id: Optional[int] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

class OrderItemResponse(OrderItemBase):
    id: int
    
    class Config:
        from_attributes = True