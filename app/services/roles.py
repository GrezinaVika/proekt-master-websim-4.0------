from app.repositories.roles import RoleRepository
from app.schemes.roles import RoleCreate, RoleUpdate

class RoleService:
    def __init__(self, repository: RoleRepository):
        self.repository = repository
    
    def get_all_roles(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_role_by_id(self, role_id: int):
        return self.repository.get_by_id(role_id)
    
    def create_role(self, role_data: RoleCreate):
        return self.repository.create(role_data)
    
    def update_role(self, role_id: int, role_data: RoleUpdate):
        return self.repository.update(role_id, role_data)
    
    def delete_role(self, role_id: int):
        return self.repository.delete(role_id)