from sqlalchemy.orm import Session
from app.models.dishes import DishesModel

class DishService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_dish(self, dish_id: int):
        return self.db.query(DishesModel).filter(DishesModel.id == dish_id).first()
    
    def get_all_dishes(self):
        """Получает все блюда из меню"""
        return self.db.query(DishesModel).all()
    
    def get_dishes_by_category(self, category: str):
        """Получает блюда по категории"""
        return self.db.query(DishesModel).filter(DishesModel.category_id == category).all()
    
    def create_dish(self, dish_data):
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
    
    def update_dish(self, dish_id: int, dish_data):
        dish = self.get_dish(dish_id)
        if not dish:
            return None
        
        if hasattr(dish_data, 'name') and dish_data.name:
            dish.name = dish_data.name
        if hasattr(dish_data, 'description') and dish_data.description:
            dish.description = dish_data.description
        if hasattr(dish_data, 'price') and dish_data.price:
            dish.price = dish_data.price
        if hasattr(dish_data, 'is_available') and dish_data.is_available is not None:
            dish.is_available = dish_data.is_available
        
        self.db.commit()
        self.db.refresh(dish)
        return dish
    
    def delete_dish(self, dish_id: int):
        dish = self.get_dish(dish_id)
        if dish:
            self.db.delete(dish)
            self.db.commit()
            return True
        return False
