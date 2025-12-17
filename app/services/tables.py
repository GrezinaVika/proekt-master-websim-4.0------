from app.repositories.tables import TableRepository
from app.schemes.tables import TableCreate, TableUpdate


class TableService:
    def __init__(self, repository: TableRepository):
        self.repository = repository
    
    def get_all_tables(self, skip: int = 0, limit: int = 100):
        """Get all tables with pagination"""
        return self.repository.get_all(skip=skip, limit=limit)
    
    def get_table_by_id(self, table_id: int):
        """Get single table by ID"""
        return self.repository.get_by_id(table_id)
    
    def create_table(self, table_data: TableCreate):
        """Create new table"""
        return self.repository.create(table_data)
    
    def update_table(self, table_id: int, table_data: TableUpdate):
        """Update existing table"""
        return self.repository.update(table_id, table_data)
    
    def delete_table(self, table_id: int):
        """Delete table"""
        return self.repository.delete(table_id)
