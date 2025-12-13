from sqlalchemy.orm import Session
from app.models.tables import TablesModel
from app.schemes.tables import TableCreate, TableUpdate

class TableRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(TablesModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, table_id: int):
        return self.db.query(TablesModel).filter(TablesModel.id == table_id).first()
    
    def get_by_number(self, table_number: int):
        return self.db.query(TablesModel).filter(TablesModel.table_number == table_number).first()
    
    def create(self, table: TableCreate):
        db_table = TablesModel(
            table_number=table.table_number,
            capacity=table.capacity,
            location=table.location,
            description=table.description,
            status=table.status,
            is_available=True
        )
        self.db.add(db_table)
        self.db.commit()
        self.db.refresh(db_table)
        return db_table
    
    def update(self, table_id: int, table_update: TableUpdate):
        db_table = self.get_by_id(table_id)
        if not db_table:
            return None
        
        update_data = table_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_table, field, value)
        
        self.db.commit()
        self.db.refresh(db_table)
        return db_table
    
    def delete(self, table_id: int):
        db_table = self.get_by_id(table_id)
        if not db_table:
            return False
        
        self.db.delete(db_table)
        self.db.commit()
        return True
    
    def get_available_tables(self):
        return self.db.query(TablesModel).filter(
            TablesModel.is_available == True,
            TablesModel.status == "available"
        ).all()
    
    def update_status(self, table_id: int, status: str):
        db_table = self.get_by_id(table_id)
        if not db_table:
            return None
        
        db_table.status = status
        db_table.is_available = (status == "available")
        self.db.commit()
        self.db.refresh(db_table)
        return db_table