from sqlalchemy.orm import Session
from app.models.tables import TablesModel
from app.schemas import TableCreate

class TableRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, table_id: int):
        """Находит стол по ID"""
        return self.db.query(TablesModel).filter(TablesModel.id == table_id).first()
    
    def find_all(self):
        """Возвращает все столы"""
        return self.db.query(TablesModel).all()
    
    def find_free(self):
        """Возвращает только свободные столы"""
        return self.db.query(TablesModel).filter(TablesModel.status == "available").all()
    
    def find_occupied(self):
        """Возвращает только занятые столы"""
        return self.db.query(TablesModel).filter(TablesModel.status == "occupied").all()
    
    def create(self, table_data: TableCreate):
        """Создает новый стол"""
        db_table = TablesModel(
            table_number=table_data.table_number,
            capacity=getattr(table_data, 'seats', 4),
            status="available"
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
