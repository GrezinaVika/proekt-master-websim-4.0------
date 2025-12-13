from sqlalchemy.orm import Session
from app.models.cook_statistics import CookStatisticsModel
from app.schemes.cook_statistics import CookStatisticsCreate, CookStatisticsUpdate

class CookStatisticsRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(CookStatisticsModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, stat_id: int):
        return self.db.query(CookStatisticsModel).filter(CookStatisticsModel.id == stat_id).first()
    
    def get_by_cook(self, cook_id: int):
        return self.db.query(CookStatisticsModel).filter(CookStatisticsModel.cook_id == cook_id).first()
    
    def create(self, stat: CookStatisticsCreate):
        db_stat = CookStatisticsModel(
            cook_id=stat.cook_id,
            active_orders=stat.active_orders
        )
        self.db.add(db_stat)
        self.db.commit()
        self.db.refresh(db_stat)
        return db_stat
    
    def update(self, stat_id: int, stat_update: CookStatisticsUpdate):
        db_stat = self.get_by_id(stat_id)
        if not db_stat:
            return None
        
        update_data = stat_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_stat, field, value)
        
        self.db.commit()
        self.db.refresh(db_stat)
        return db_stat
    
    def delete(self, stat_id: int):
        db_stat = self.get_by_id(stat_id)
        if not db_stat:
            return False
        
        self.db.delete(db_stat)
        self.db.commit()
        return True
    
    def update_active_orders(self, cook_id: int, change: int):
        db_stat = self.get_by_cook(cook_id)
        if not db_stat:
            return None
        
        db_stat.active_orders = max(0, db_stat.active_orders + change)
        self.db.commit()
        self.db.refresh(db_stat)
        return db_stat