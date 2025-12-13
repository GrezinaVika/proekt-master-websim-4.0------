from sqlalchemy.orm import Session
from app.models.order_items import OrderItemsModel
from app.schemes.order_items import OrderItemCreate, OrderItemUpdate

class OrderItemRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(OrderItemsModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, item_id: int):
        return self.db.query(OrderItemsModel).filter(OrderItemsModel.id == item_id).first()
    
    def get_by_order(self, order_id: int):
        return self.db.query(OrderItemsModel).filter(OrderItemsModel.order_id == order_id).all()
    
    def create(self, order_item: OrderItemCreate):
        db_item = OrderItemsModel(
            order_id=order_item.order_id,
            menu_id=order_item.menu_id,
            quantity=order_item.quantity,
            price=order_item.price
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def update(self, item_id: int, item_update: OrderItemUpdate):
        db_item = self.get_by_id(item_id)
        if not db_item:
            return None
        
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def delete(self, item_id: int):
        db_item = self.get_by_id(item_id)
        if not db_item:
            return False
        
        self.db.delete(db_item)
        self.db.commit()
        return True
    
    def get_by_menu(self, menu_id: int):
        return self.db.query(OrderItemsModel).filter(OrderItemsModel.menu_id == menu_id).all()