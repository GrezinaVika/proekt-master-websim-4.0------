from sqlalchemy.orm import Session
from app.models.order import OrderModel
from app.schemas import OrderCreate
from datetime import datetime

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, order_id: int):
        """Находит заказ по ID"""
        return self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
    
    def find_all(self):
        """Возвращает все заказы"""
        return self.db.query(OrderModel).all()
    
    def find_by_table(self, table_id: int):
        """Находит заказы по столику"""
        return self.db.query(OrderModel).filter(OrderModel.table_id == table_id).all()
    
    def find_by_status(self, status: str):
        """Находит заказы по статусу"""
        return self.db.query(OrderModel).filter(OrderModel.status == status).all()
    
    def create(self, order_data: OrderCreate, user_id: int):
        """Создает новый заказ"""
        db_order = OrderModel(
            table_id=order_data.table_id,
            waiters_id=user_id,
            status="created",
            total_amount=order_data.total_price if hasattr(order_data, 'total_price') else 0.0,
            created_at=datetime.now()
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def update_status(self, order_id: int, new_status: str):
        """Обновляет статус заказа"""
        order = self.find_by_id(order_id)
        if order:
            order.status = new_status
            self.db.commit()
            self.db.refresh(order)
        return order
    
    def delete(self, order_id: int):
        """Удаляет заказ"""
        order = self.find_by_id(order_id)
        if order:
            self.db.delete(order)
            self.db.commit()
            return True
        return False
