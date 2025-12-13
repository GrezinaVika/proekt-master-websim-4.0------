from app.repositories.cook import CookRepository
from app.schemes.cook import CookCreate, CookUpdate

class CookService:
    def __init__(self, repository: CookRepository):
        self.repository = repository
    
    def get_all_cooks(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_cook_by_id(self, cook_id: int):
        return self.repository.get_by_id(cook_id)
    
    def create_cook(self, cook_data: CookCreate):
        return self.repository.create(cook_data)
    
    def update_cook(self, cook_id: int, cook_data: CookUpdate):
        return self.repository.update(cook_id, cook_data)
    
    def delete_cook(self, cook_id: int):
        return self.repository.delete(cook_id)
    
    def authenticate(self, login: str, password: str):
        cook = self.repository.get_by_login(login)
        if cook and cook.password == password:  # Внимание: использовать хэширование!
            self.repository.update_last_login(cook.id)
            return cook
        return None