from sqlalchemy.orm import Session
from app.models.dishes import Dish
from app.schemas import DishCreate

class DishRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, dish_id: int):
        """Находит блюдо по ID"""
        return self.db.query(Dish).filter(Dish.id == dish_id).first()
    
    def find_all(self):
        """Возвращает все блюда"""
        return self.db.query(Dish).all()
    
    def find_by_category(self, category: str):
        """Возвращает блюда по категории"""
        return self.db.query(Dish).filter(Dish.category == category).all()
    
    def find_available(self):
        """Возвращает только доступные блюда"""
        return self.db.query(Dish).filter(Dish.available == True).all()
    
    def create(self, dish_data: DishCreate):
        """Создает новое блюдо"""
        db_dish = Dish(
            name=dish_data.name,
            description=dish_data.description,
            price=dish_data.price,
            category=dish_data.category,
            available=True
        )
        self.db.add(db_dish)
        self.db.commit()
        self.db.refresh(db_dish)
        return db_dish
    
    def update(self, dish_id: int, **kwargs):
        """Обновляет блюдо"""
        dish = self.find_by_id(dish_id)
        if dish:
            for key, value in kwargs.items():
                setattr(dish, key, value)
            self.db.commit()
            self.db.refresh(dish)
        return dish
    
    def delete(self, dish_id: int):
        """Удаляет блюдо"""
        dish = self.find_by_id(dish_id)
        if dish:
            self.db.delete(dish)
            self.db.commit()
            return True
        return False
