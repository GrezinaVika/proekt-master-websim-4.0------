from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.waiter_statistics import WaiterStatisticsModel
from app.schemes.waiter_statistics import WaiterStatisticsCreate, WaiterStatisticsUpdate

class WaiterStatisticsRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(WaiterStatisticsModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, stat_id: int):
        return self.db.query(WaiterStatisticsModel).filter(WaiterStatisticsModel.id == stat_id).first()
    
    def get_by_waiter(self, waiter_id: int):
        return self.db.query(WaiterStatisticsModel).filter(WaiterStatisticsModel.waiter_id == waiter_id).first()
    
    def create(self, stat: WaiterStatisticsCreate):
        db_stat = WaiterStatisticsModel(
            waiter_id=stat.waiter_id,
            total_orders=stat.total_orders,
            occupied_tables=stat.occupied_tables,
            total_revenue=stat.total_revenue,
            tips_amount=stat.tips_amount,
            hours_worked=stat.hours_worked
        )
        self.db.add(db_stat)
        self.db.commit()
        self.db.refresh(db_stat)
        return db_stat
    
    def update(self, stat_id: int, stat_update: WaiterStatisticsUpdate):
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
    
    def increment_orders(self, waiter_id: int, revenue: float = 0.0, tips: float = 0.0):
        db_stat = self.get_by_waiter(waiter_id)
        if not db_stat:
            return None
        
        db_stat.total_orders += 1
        db_stat.total_revenue += revenue
        db_stat.tips_amount += tips
        db_stat.last_updated = func.now()
        
        self.db.commit()
        self.db.refresh(db_stat)
        return db_stat
    
    def update_hours_worked(self, waiter_id: int, hours: float):
        db_stat = self.get_by_waiter(waiter_id)
        if not db_stat:
            return None
        
        db_stat.hours_worked += hours
        db_stat.last_updated = func.now()
        
        self.db.commit()
        self.db.refresh(db_stat)
        return db_stat