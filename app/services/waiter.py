from app.repositories.waiter import WaiterRepository
from app.schemes.waiter import WaiterCreate, WaiterUpdate

class WaiterService:
    def __init__(self, repository: WaiterRepository):
        self.repository = repository
    
    def get_all_waiters(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_waiter_by_id(self, waiter_id: int):
        return self.repository.get_by_id(waiter_id)
    
    def create_waiter(self, waiter_data: WaiterCreate):
        return self.repository.create(waiter_data)
    
    def update_waiter(self, waiter_id: int, waiter_data: WaiterUpdate):
        return self.repository.update(waiter_id, waiter_data)
    
    def delete_waiter(self, waiter_id: int):
        return self.repository.delete(waiter_id)
    
    def authenticate(self, login: str, password: str):
        waiter = self.repository.get_by_login(login)
        if waiter and waiter.password == password:  # Внимание: использовать хэширование!
            self.repository.update_last_login(waiter.id)
            return waiter
        return None