from app.repositories.migration import MigrationRepository
from app.schemes.migration import MigrationCreate, MigrationUpdate

class MigrationService:
    def __init__(self, repository: MigrationRepository):
        self.repository = repository
    
    def get_all_migrations(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_migration_by_id(self, migration_id: int):
        return self.repository.get_by_id(migration_id)
    
    def create_migration(self, migration_data: MigrationCreate):
        return self.repository.create(migration_data)
    
    def update_migration(self, migration_id: int, migration_data: MigrationUpdate):
        return self.repository.update(migration_id, migration_data)
    
    def delete_migration(self, migration_id: int):
        return self.repository.delete(migration_id)
    
    def mark_as_success(self, migration_id: int):
        return self.repository.update_status(migration_id, "success")
    
    def mark_as_failed(self, migration_id: int):
        return self.repository.update_status(migration_id, "failed")