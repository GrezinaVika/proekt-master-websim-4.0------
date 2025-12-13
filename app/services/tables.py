from app.repositories.tables import TableRepository
from app.schemes.tables import TableCreate, TableUpdate

class TableService:
    def __init__(self, repository: TableRepository):
        self.repository = repository
    
    def get_all_tables(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_table_by_id(self, table_id: int):
        return self.repository.get_by_id(table_id)
    
    def get_table_by_number(self, table_number: int):
        return self.repository.get_by_number(table_number)
    
    def create_table(self, table_data: TableCreate):
        return self.repository.create(table_data)
    
    def update_table(self, table_id: int, table_data: TableUpdate):
        return self.repository.update(table_id, table_data)
    
    def delete_table(self, table_id: int):
        return self.repository.delete(table_id)
    
    def get_available_tables(self):
        return self.repository.get_available_tables()
    
    def update_table_status(self, table_id: int, status: str):
        return self.repository.update_status(table_id, status)