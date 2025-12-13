from sqlalchemy.orm import Session
from app.models.cook import CookModel
from app.schemes.cook import CookCreate, CookUpdate

class CookRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(CookModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, cook_id: int):
        return self.db.query(CookModel).filter(CookModel.id == cook_id).first()
    
    def get_by_login(self, login: str):
        return self.db.query(CookModel).filter(CookModel.login == login).first()
    
    def create(self, cook: CookCreate):
        db_cook = CookModel(
            login=cook.login,
            password=cook.password,
            role=cook.role
        )
        self.db.add(db_cook)
        self.db.commit()
        self.db.refresh(db_cook)
        return db_cook
    
    def update(self, cook_id: int, cook_update: CookUpdate):
        db_cook = self.get_by_id(cook_id)
        if not db_cook:
            return None
        
        update_data = cook_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cook, field, value)
        
        self.db.commit()
        self.db.refresh(db_cook)
        return db_cook
    
    def delete(self, cook_id: int):
        db_cook = self.get_by_id(cook_id)
        if not db_cook:
            return False
        
        self.db.delete(db_cook)
        self.db.commit()
        return True
    
    def update_last_login(self, cook_id: int):
        db_cook = self.get_by_id(cook_id)
        if not db_cook:
            return None
        
        from datetime import datetime
        db_cook.last_login = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_cook)
        return db_cook