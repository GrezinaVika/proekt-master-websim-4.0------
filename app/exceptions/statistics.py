from .base import (
    NotFoundException,
    ValidationException,
    BadRequestException
)

class StatisticsNotFoundException(NotFoundException):
    """Исключение для статистики, которая не найдена"""
    def __init__(self, stat_id: int = None, user_id: int = None, user_type: str = None):
        if stat_id:
            super().__init__(resource="Statistics", resource_id=str(stat_id))
        elif user_id and user_type:
            super().__init__(
                resource=f"{user_type.capitalize()} statistics", 
                field=f"{user_type}_id", 
                value=str(user_id)
            )
        else:
            super().__init__(resource="Statistics")

class StatisticsValidationException(ValidationException):
    """Исключение для ошибок валидации статистики"""
    def __init__(self, detail: str = "Statistics validation error", errors: dict = None):
        super().__init__(detail=detail, errors=errors)

class InvalidStatisticsDataException(BadRequestException):
    """Исключение для некорректных данных статистики"""
    def __init__(self, detail: str = "Invalid statistics data"):
        super().__init__(detail=detail, error_code="INVALID_STATISTICS_DATA")

class StatisticsCalculationException(BadRequestException):
    """Исключение для ошибок расчета статистики"""
    def __init__(self, detail: str = "Statistics calculation error"):
        super().__init__(detail=detail, error_code="STATISTICS_CALCULATION_ERROR")