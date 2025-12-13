from sqlalchemy.orm import Session
from app.models.waiter import WaiterModel
from app.schemes.waiter import WaiterCreate, WaiterUpdate

class WaiterRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(WaiterModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, waiter_id: int):
        return self.db.query(WaiterModel).filter(WaiterModel.id == waiter_id).first()
    
    def get_by_login(self, login: str):
        return self.db.query(WaiterModel).filter(WaiterModel.login == login).first()
    
    def create(self, waiter: WaiterCreate):
        db_waiter = WaiterModel(
            login=waiter.login,
            password=waiter.password,
            role=waiter.role
        )
        self.db.add(db_waiter)
        self.db.commit()
        self.db.refresh(db_waiter)
        return db_waiter
    
    def update(self, waiter_id: int, waiter_update: WaiterUpdate):
        db_waiter = self.get_by_id(waiter_id)
        if not db_waiter:
            return None
        
        update_data = waiter_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_waiter, field, value)
        
        self.db.commit()
        self.db.refresh(db_waiter)
        return db_waiter
    
    def delete(self, waiter_id: int):
        db_waiter = self.get_by_id(waiter_id)
        if not db_waiter:
            return False
        
        self.db.delete(db_waiter)
        self.db.commit()
        return True
    
    def update_last_login(self, waiter_id: int):
        db_waiter = self.get_by_id(waiter_id)
        if not db_waiter:
            return None
        
        from datetime import datetime
        db_waiter.last_login = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_waiter)
        return db_waiter