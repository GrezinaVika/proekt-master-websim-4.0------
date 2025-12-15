from sqlalchemy.orm import Session
from app.models.dishes import DishesModel

class DishRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, dish_id: int):
        """Находит блюдо по ID"""
        return self.db.query(DishesModel).filter(DishesModel.id == dish_id).first()
    
    def find_all(self):
        """Возвращает все блюда"""
        return self.db.query(DishesModel).all()
    
    def find_by_category(self, category: str):
        """Возвращает блюда по категории"""
        return self.db.query(DishesModel).filter(DishesModel.category_id == category).all()
    
    def find_available(self):
        """Возвращает только доступные блюда"""
        return self.db.query(DishesModel).filter(DishesModel.is_available == True).all()
    
    def create(self, dish_data):
        """Создает новое блюдо"""
        db_dish = DishesModel(
            name=getattr(dish_data, 'name', 'Unknown'),
            description=getattr(dish_data, 'description', ''),
            price=getattr(dish_data, 'price', 0.0),
            category_id=getattr(dish_data, 'category_id', 1),
            admin_id=1,
            is_available=True
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
