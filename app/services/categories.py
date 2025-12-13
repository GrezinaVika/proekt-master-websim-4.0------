from app.repositories.categories import CategoryRepository
from app.schemes.categories import CategoryCreate, CategoryUpdate

class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def get_all_categories(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_category_by_id(self, category_id: int):
        return self.repository.get_by_id(category_id)
    
    def create_category(self, category_data: CategoryCreate):
        return self.repository.create(category_data)
    
    def update_category(self, category_id: int, category_data: CategoryUpdate):
        return self.repository.update(category_id, category_data)
    
    def delete_category(self, category_id: int):
        return self.repository.delete(category_id)