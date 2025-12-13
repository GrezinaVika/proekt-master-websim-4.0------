from pydantic import BaseModel
from typing import Optional

class DishBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[int] = None
    admin_id: Optional[int] = None

class DishCreate(DishBase):
    pass

class DishUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

class DishResponse(DishBase):
    id: int
    
    class Config:
        from_attributes = True