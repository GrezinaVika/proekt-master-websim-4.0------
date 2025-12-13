from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WaiterBase(BaseModel):
    login: str
    password: str
    role: str = "waiter"

class WaiterCreate(WaiterBase):
    pass

class WaiterUpdate(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

class WaiterResponse(WaiterBase):
    id: int
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True