from sqlalchemy.orm import Session
from app.models.dishes import DishesModel
from app.schemes.dishes import DishCreate, DishUpdate

class DishRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(DishesModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, dish_id: int):
        return self.db.query(DishesModel).filter(DishesModel.id == dish_id).first()
    
    def create(self, dish: DishCreate):
        db_dish = DishesModel(**dish.model_dump())
        self.db.add(db_dish)
        self.db.commit()
        self.db.refresh(db_dish)
        return db_dish
    
    def update(self, dish_id: int, dish_update: DishUpdate):
        db_dish = self.get_by_id(dish_id)
        if not db_dish:
            return None
        
        update_data = dish_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_dish, field, value)
        
        self.db.commit()
        self.db.refresh(db_dish)
        return db_dish
    
    def delete(self, dish_id: int):
        db_dish = self.get_by_id(dish_id)
        if not db_dish:
            return False
        
        self.db.delete(db_dish)
        self.db.commit()
        return True