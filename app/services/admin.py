from app.repositories.admin import AdminRepository
from app.schemes.admin import AdminCreate, AdminUpdate

class AdminService:
    def __init__(self, repository: AdminRepository):
        self.repository = repository
    
    def get_all_admins(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_admin_by_id(self, admin_id: int):
        return self.repository.get_by_id(admin_id)
    
    def create_admin(self, admin_data: AdminCreate):
        return self.repository.create(admin_data)
    
    def update_admin(self, admin_id: int, admin_data: AdminUpdate):
        return self.repository.update(admin_id, admin_data)
    
    def delete_admin(self, admin_id: int):
        return self.repository.delete(admin_id)
    
    def authenticate(self, login: str, password: str):
        admin = self.repository.get_by_login(login)
        if admin and admin.password == password:  # Внимание: использовать хэширование!
            self.repository.update_last_login(admin.id)
            return admin
        return None