from app.repositories.cook_statistics import CookStatisticsRepository
from app.schemes.cook_statistics import CookStatisticsCreate, CookStatisticsUpdate

class CookStatisticsService:
    def __init__(self, repository: CookStatisticsRepository):
        self.repository = repository
    
    def get_all_statistics(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_statistic_by_id(self, stat_id: int):
        return self.repository.get_by_id(stat_id)
    
    def get_statistic_by_cook(self, cook_id: int):
        return self.repository.get_by_cook(cook_id)
    
    def create_statistic(self, stat_data: CookStatisticsCreate):
        return self.repository.create(stat_data)
    
    def update_statistic(self, stat_id: int, stat_data: CookStatisticsUpdate):
        return self.repository.update(stat_id, stat_data)
    
    def delete_statistic(self, stat_id: int):
        return self.repository.delete(stat_id)
    
    def update_cook_active_orders(self, cook_id: int, change: int):
        return self.repository.update_active_orders(cook_id, change)