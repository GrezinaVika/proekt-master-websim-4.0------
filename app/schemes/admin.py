from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AdminBase(BaseModel):
    login: str
    password: str
    role: str = "admin"

class AdminCreate(AdminBase):
    pass

class AdminUpdate(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

class AdminResponse(AdminBase):
    id: int
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True