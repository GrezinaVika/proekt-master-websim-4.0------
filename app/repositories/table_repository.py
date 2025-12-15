from sqlalchemy.orm import Session
from app.models.tables import Table
from app.schemas import TableCreate

class TableRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, table_id: int):
        """Находит стол по ID"""
        return self.db.query(Table).filter(Table.id == table_id).first()
    
    def find_all(self):
        """Возвращает все столы"""
        return self.db.query(Table).all()
    
    def find_free(self):
        """Возвращает только свободные столы"""
        return self.db.query(Table).filter(Table.status == "free").all()
    
    def find_occupied(self):
        """Возвращает только занятые столы"""
        return self.db.query(Table).filter(Table.status == "occupied").all()
    
    def create(self, table_data: TableCreate):
        """Создает новый стол"""
        db_table = Table(
            table_number=table_data.table_number,
            seats=table_data.seats,
            status="free"
        )
        self.db.add(db_table)
        self.db.commit()
        self.db.refresh(db_table)
        return db_table
    
    def update_status(self, table_id: int, status: str):
        """Обновляет статус стола"""
        table = self.find_by_id(table_id)
        if table:
            table.status = status
            self.db.commit()
            self.db.refresh(table)
        return table
    
    def delete(self, table_id: int):
        """Удаляет стол"""
        table = self.find_by_id(table_id)
        if table:
            self.db.delete(table)
            self.db.commit()
            return True
        return False
