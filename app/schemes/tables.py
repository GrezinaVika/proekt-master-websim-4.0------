from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TableBase(BaseModel):
    table_number: int
    capacity: int = 2
    location: Optional[str] = None
    description: Optional[str] = None
    status: str = "available"

class TableCreate(TableBase):
    pass

class TableUpdate(BaseModel):
    table_number: Optional[int] = None
    capacity: Optional[int] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    is_available: Optional[bool] = None

class TableResponse(TableBase):
    id: int
    is_available: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True