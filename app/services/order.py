from app.repositories.orders import OrderRepository
from app.schemes.order import OrderCreate, OrderUpdate


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository
    
    def get_all_orders(self, skip: int = 0, limit: int = 100):
        """Get all orders with pagination"""
        return self.repository.get_all(skip=skip, limit=limit)
    
    def get_order_by_id(self, order_id: int):
        """Get single order by ID"""
        return self.repository.get_by_id(order_id)
    
    def create_order(self, order_data: OrderCreate):
        """Create new order"""
        return self.repository.create(order_data)
    
    def update_order(self, order_id: int, order_data: OrderUpdate):
        """Update existing order"""
        return self.repository.update(order_id, order_data)
    
    def delete_order(self, order_id: int):
        """Delete order"""
        return self.repository.delete(order_id)
