from app.repositories.orders import OrderRepository
from app.schemes.order import OrderCreate, OrderUpdate

class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository
    
    def get_all_orders(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_order_by_id(self, order_id: int):
        return self.repository.get_by_id(order_id)
    
    def create_order(self, order_data: OrderCreate):
        return self.repository.create(order_data)
    
    def update_order(self, order_id: int, order_data: OrderUpdate):
        return self.repository.update(order_id, order_data)
    
    def delete_order(self, order_id: int):
        return self.repository.delete(order_id)
    
    def get_orders_by_status(self, status: str):
        return self.repository.get_by_status(status)
    
    def get_orders_by_table(self, table_id: int):
        return self.repository.get_by_table(table_id)
    
    def get_orders_by_waiter(self, waiter_id: int):
        return self.repository.get_by_waiter(waiter_id)