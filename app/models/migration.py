# migration.py (остается без изменений)
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database.database import Base

class MigrationHistory(Base):
    __tablename__ = "migration_history"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, unique=True, index=True)
    description = Column(String)
    sql_content = Column(Text, nullable=True)
    applied_at = Column(DateTime)
    status = Column(String)
    applied_by = Column(String, nullable=True)