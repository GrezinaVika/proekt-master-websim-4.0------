from sqlalchemy.orm import Session
from app.models import Table
from app.schemas import TableCreate, TableUpdate

class TableService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_table(self, table_id: int):
        return self.db.query(Table).filter(Table.id == table_id).first()
    
    def get_all_tables(self):
        """Получает все столики"""
        return self.db.query(Table).all()
    
    def get_free_tables(self):
        """Получает только свободные столики"""
        return self.db.query(Table).filter(Table.status == "free").all()
    
    def create_table(self, table_data: TableCreate):
        db_table = Table(
            table_number=table_data.table_number,
            seats=table_data.seats,
            status="free"
        )
        self.db.add(db_table)
        self.db.commit()
        self.db.refresh(db_table)
        return db_table
    
    def update_table(self, table_id: int, table_data: TableUpdate):
        table = self.get_table(table_id)
        if not table:
            return None
        
        if table_data.status:
            table.status = table_data.status
        if table_data.seats:
            table.seats = table_data.seats
        
        self.db.commit()
        self.db.refresh(table)
        return table
    
    def delete_table(self, table_id: int):
        table = self.get_table(table_id)
        if table:
            self.db.delete(table)
            self.db.commit()
            return True
        return False
