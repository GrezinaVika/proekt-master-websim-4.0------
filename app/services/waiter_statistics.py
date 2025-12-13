from app.repositories.waiter_statistics import WaiterStatisticsRepository
from app.schemes.waiter_statistics import WaiterStatisticsCreate, WaiterStatisticsUpdate

class WaiterStatisticsService:
    def __init__(self, repository: WaiterStatisticsRepository):
        self.repository = repository
    
    def get_all_statistics(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    
    def get_statistic_by_id(self, stat_id: int):
        return self.repository.get_by_id(stat_id)
    
    def get_statistic_by_waiter(self, waiter_id: int):
        return self.repository.get_by_waiter(waiter_id)
    
    def create_statistic(self, stat_data: WaiterStatisticsCreate):
        return self.repository.create(stat_data)
    
    def update_statistic(self, stat_id: int, stat_data: WaiterStatisticsUpdate):
        return self.repository.update(stat_id, stat_data)
    
    def delete_statistic(self, stat_id: int):
        return self.repository.delete(stat_id)
    
    def add_order_to_statistic(self, waiter_id: int, revenue: float = 0.0, tips: float = 0.0):
        return self.repository.increment_orders(waiter_id, revenue, tips)
    
    def update_waiter_hours(self, waiter_id: int, hours: float):
        return self.repository.update_hours_worked(waiter_id, hours)