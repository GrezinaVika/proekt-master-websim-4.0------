from app.repositories.dishes import DishRepository
from app.schemes.dishes import DishCreate, DishUpdate


class DishService:
    def __init__(self, repository: DishRepository):
        self.repository = repository
    
    def get_all_dishes(self, skip: int = 0, limit: int = 100):
        """Get all dishes with pagination"""
        return self.repository.get_all(skip=skip, limit=limit)
    
    def get_dish_by_id(self, dish_id: int):
        """Get single dish by ID"""
        return self.repository.get_by_id(dish_id)
    
    def create_dish(self, dish_data: DishCreate):
        """Create new dish"""
        return self.repository.create(dish_data)
    
    def update_dish(self, dish_id: int, dish_data: DishUpdate):
        """Update existing dish"""
        return self.repository.update(dish_id, dish_data)
    
    def delete_dish(self, dish_id: int):
        """Delete dish"""
        return self.repository.delete(dish_id)
