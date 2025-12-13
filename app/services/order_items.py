from app.repositories.order_items import OrderItemRepository
from app.schemes.order_items import OrderItemCreate, OrderItemUpdate

class OrderItemService:
    def __init__(self, repository: OrderItemRepository):
        self.repository = repository
    
    def get_all_order_items(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_order_item_by_id(self, item_id: int):
        return self.repository.get_by_id(item_id)
    
    def create_order_item(self, item_data: OrderItemCreate):
        return self.repository.create(item_data)
    
    def update_order_item(self, item_id: int, item_data: OrderItemUpdate):
        return self.repository.update(item_id, item_data)
    
    def delete_order_item(self, item_id: int):
        return self.repository.delete(item_id)
    
    def get_items_by_order(self, order_id: int):
        return self.repository.get_by_order(order_id)
    
    def get_items_by_menu(self, menu_id: int):
        return self.repository.get_by_menu(menu_id)