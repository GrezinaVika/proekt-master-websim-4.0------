from sqlalchemy.orm import Session
from app.models.dishes import DishesModel
from app.schemas import DishCreate, DishUpdate

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
    
    def create_dish(self, dish_data: DishCreate):
        db_dish = DishesModel(
            name=dish_data.name,
            description=dish_data.description,
            price=dish_data.price,
            category_id=getattr(dish_data, 'category_id', 1),
            admin_id=1,
            is_available=True
        )
        self.db.add(db_dish)
        self.db.commit()
        self.db.refresh(db_dish)
        return db_dish
    
    def update_dish(self, dish_id: int, dish_data: DishUpdate):
        dish = self.get_dish(dish_id)
        if not dish:
            return None
        
        if dish_data.name:
            dish.name = dish_data.name
        if dish_data.description:
            dish.description = dish_data.description
        if dish_data.price:
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
