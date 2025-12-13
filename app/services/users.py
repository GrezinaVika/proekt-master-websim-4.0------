from app.repositories.users import UserRepository
from app.schemes.users import UserCreate, UserUpdate

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_user_by_id(self, user_id: int):
        return self.repository.get_by_id(user_id)
    
    def create_user(self, user_data: UserCreate):
        # Проверка на существующий email
        existing = self.repository.get_by_email(user_data.email)
        if existing:
            return None
        
        # Проверка на существующий username
        existing = self.repository.get_by_username(user_data.username)
        if existing:
            return None
        
        return self.repository.create(user_data)
    
    def update_user(self, user_id: int, user_data: UserUpdate):
        return self.repository.update(user_id, user_data)
    
    def delete_user(self, user_id: int):
        return self.repository.delete(user_id)
    
    def authenticate(self, username: str, password: str):
        return self.repository.authenticate(username, password)