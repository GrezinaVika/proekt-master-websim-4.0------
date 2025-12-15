from sqlalchemy.orm import Session
from app.models.tables import TablesModel
from app.schemas import TableCreate, TableUpdate

class TableService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_table(self, table_id: int):
        return self.db.query(TablesModel).filter(TablesModel.id == table_id).first()
    
    def get_all_tables(self):
        """Получает все столики"""
        return self.db.query(TablesModel).all()
    
    def get_free_tables(self):
        """Получает только свободные столики"""
        return self.db.query(TablesModel).filter(TablesModel.status == "available").all()
    
    def create_table(self, table_data: TableCreate):
        db_table = TablesModel(
            table_number=table_data.table_number,
            capacity=getattr(table_data, 'seats', 4),
            status="available"
        )
        self.db.add(db_table)
        self.db.commit()
        self.db.refresh(db_table)
        return db_table
    
    def update_table(self, table_id: int, table_data: TableUpdate):
        table = self.get_table(table_id)
        if not table:
            return None
        
        if hasattr(table_data, 'status') and table_data.status:
            table.status = table_data.status
        if hasattr(table_data, 'seats') and table_data.seats:
            table.capacity = table_data.seats
        
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
