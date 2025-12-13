# order_items.py
from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

class OrderItemsModel(Base):
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    menu_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False,default=0.0)