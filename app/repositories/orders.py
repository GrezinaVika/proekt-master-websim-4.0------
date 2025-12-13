from sqlalchemy.orm import Session
from app.models.order import OrderModel
from app.schemes.order import OrderCreate, OrderUpdate

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(OrderModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, order_id: int):
        return self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
    
    def create(self, order: OrderCreate):
        db_order = OrderModel(
            table_id=order.table_id,
            cook_id=order.cook_id,
            waiters_id=order.waiters_id,
            status=order.status
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def update(self, order_id: int, order_update: OrderUpdate):
        db_order = self.get_by_id(order_id)
        if not db_order:
            return None
        
        update_data = order_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def delete(self, order_id: int):
        db_order = self.get_by_id(order_id)
        if not db_order:
            return False
        
        self.db.delete(db_order)
        self.db.commit()
        return True
    
    def get_by_status(self, status: str):
        return self.db.query(OrderModel).filter(OrderModel.status == status).all()
    
    def get_by_table(self, table_id: int):
        return self.db.query(OrderModel).filter(OrderModel.table_id == table_id).all()
    
    def get_by_waiter(self, waiter_id: int):
        return self.db.query(OrderModel).filter(OrderModel.waiters_id == waiter_id).all()