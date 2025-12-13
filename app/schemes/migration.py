from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MigrationBase(BaseModel):
    version: str
    description: Optional[str] = None
    sql_content: Optional[str] = None
    status: str = "pending"
    applied_by: Optional[str] = None

class MigrationCreate(MigrationBase):
    pass

class MigrationUpdate(BaseModel):
    version: Optional[str] = None
    description: Optional[str] = None
    sql_content: Optional[str] = None
    status: Optional[str] = None
    applied_by: Optional[str] = None

class MigrationResponse(MigrationBase):
    id: int
    applied_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True