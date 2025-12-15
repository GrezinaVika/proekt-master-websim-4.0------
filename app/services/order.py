from sqlalchemy.orm import Session
from app.models.order import OrderModel
from app.models.tables import TablesModel
from datetime import datetime

class OrderService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(self, order_data, user_id: int):
        """Создает новый заказ"""
        db_order = OrderModel(
            table_id=getattr(order_data, 'table_id', 1),
            waiters_id=user_id,
            status="created",
            total_amount=getattr(order_data, 'total_price', 0.0),
            created_at=datetime.now()
        )
        self.db.add(db_order)
        self.db.flush()
        
        # Обновляем статус стола
        table = self.db.query(TablesModel).filter(TablesModel.id == order_data.table_id).first()
        if table:
            table.status = "occupied"
            table.current_order_id = db_order.id
        
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def get_order(self, order_id: int):
        return self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
    
    def get_all_orders(self):
        return self.db.query(OrderModel).all()
    
    def update_order_status(self, order_id: int, new_status: str):
        """Обновляет статус заказа"""
        order = self.get_order(order_id)
        if not order:
            return None
        
        order.status = new_status
        
        # Если заказ завершен, освобождаем стол
        if new_status == "completed":
            table = self.db.query(TablesModel).filter(TablesModel.id == order.table_id).first()
            if table:
                table.status = "available"
                table.current_order_id = None
        
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def delete_order(self, order_id: int):
        order = self.get_order(order_id)
        if order:
            self.db.delete(order)
            self.db.commit()
            return True
        return False
