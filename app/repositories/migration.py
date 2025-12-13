from sqlalchemy.orm import Session
from datetime import datetime
from app.models.migration import MigrationHistory
from app.schemes.migration import MigrationCreate, MigrationUpdate

class MigrationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(MigrationHistory).offset(skip).limit(limit).all()
    
    def get_by_id(self, migration_id: int):
        return self.db.query(MigrationHistory).filter(MigrationHistory.id == migration_id).first()
    
    def get_by_version(self, version: str):
        return self.db.query(MigrationHistory).filter(MigrationHistory.version == version).first()
    
    def create(self, migration: MigrationCreate):
        db_migration = MigrationHistory(
            version=migration.version,
            description=migration.description,
            sql_content=migration.sql_content,
            status=migration.status,
            applied_by=migration.applied_by,
            applied_at=datetime.utcnow() if migration.status == "success" else None
        )
        self.db.add(db_migration)
        self.db.commit()
        self.db.refresh(db_migration)
        return db_migration
    
    def update(self, migration_id: int, migration_update: MigrationUpdate):
        db_migration = self.get_by_id(migration_id)
        if not db_migration:
            return None
        
        update_data = migration_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "status" and value == "success" and not db_migration.applied_at:
                db_migration.applied_at = datetime.utcnow()
            setattr(db_migration, field, value)
        
        self.db.commit()
        self.db.refresh(db_migration)
        return db_migration
    
    def delete(self, migration_id: int):
        db_migration = self.get_by_id(migration_id)
        if not db_migration:
            return False
        
        self.db.delete(db_migration)
        self.db.commit()
        return True
    
    def update_status(self, migration_id: int, status: str):
        db_migration = self.get_by_id(migration_id)
        if not db_migration:
            return None
        
        db_migration.status = status
        if status == "success" and not db_migration.applied_at:
            db_migration.applied_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_migration)
        return db_migration