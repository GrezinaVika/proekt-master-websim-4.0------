from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_items import OrderItem
from app.models.tables import Table
from app.schemas import OrderCreate, OrderUpdate
from datetime import datetime

class OrderService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(self, order_data: OrderCreate, user_id: int):
        """Создает новый заказ"""
        # Создаем основной заказ
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
        
        # Обновляем статус стола
        table = self.db.query(Table).filter(Table.id == order_data.table_id).first()
        if table:
            table.status = "occupied"
        
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def get_order(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def get_all_orders(self):
        return self.db.query(Order).all()
    
    def update_order_status(self, order_id: int, new_status: str):
        """Обновляет статус заказа"""
        order = self.get_order(order_id)
        if not order:
            return None
        
        order.status = new_status
        
        # Если заказ завершен, освобождаем стол
        if new_status == "completed":
            table = self.db.query(Table).filter(Table.id == order.table_id).first()
            if table:
                table.status = "free"
        
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
