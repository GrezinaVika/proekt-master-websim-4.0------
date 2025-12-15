from sqlalchemy.orm import Session
from app.models import Order, OrderItem
from app.schemas import OrderCreate
from datetime import datetime

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, order_id: int):
        """Находит заказ по ID"""
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def find_all(self):
        """Возвращает все заказы"""
        return self.db.query(Order).all()
    
    def find_by_table(self, table_id: int):
        """Находит заказы по столику"""
        return self.db.query(Order).filter(Order.table_id == table_id).all()
    
    def find_by_status(self, status: str):
        """Находит заказы по статусу"""
        return self.db.query(Order).filter(Order.status == status).all()
    
    def create(self, order_data: OrderCreate, user_id: int):
        """Создает новый заказ"""
        db_order = Order(
            table_id=order_data.table_id,
            user_id=user_id,
            status="pending",
            total_price=order_data.total_price,
            created_at=datetime.now()
        )
        self.db.add(db_order)
        self.db.flush()
        
        # Добавляем элементы заказа
        for item in order_data.items:
            order_item = OrderItem(
                order_id=db_order.id,
                dish_id=item.dish_id,
                quantity=item.quantity,
                price=item.price
            )
            self.db.add(order_item)
        
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
