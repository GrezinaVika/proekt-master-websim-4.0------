from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CookBase(BaseModel):
    login: str
    password: str
    role: str = "cook"

class CookCreate(CookBase):
    pass

class CookUpdate(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

class CookResponse(CookBase):
    id: int
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True