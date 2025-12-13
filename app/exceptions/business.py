from .base import (
    BadRequestException,
    ConflictException,
    ValidationException
)

class BusinessRuleException(BadRequestException):
    """Исключение для нарушений бизнес-правил"""
    def __init__(self, rule: str, detail: str = None):
        if detail:
            full_detail = f"Business rule violation: {rule} - {detail}"
        else:
            full_detail = f"Business rule violation: {rule}"
        super().__init__(detail=full_detail, error_code="BUSINESS_RULE_VIOLATION")
        self.rule = rule

class RestaurantClosedException(BusinessRuleException):
    """Исключение, когда ресторан закрыт"""
    def __init__(self, opening_time: str, closing_time: str):
        detail = f"Restaurant is closed. Open from {opening_time} to {closing_time}"
        super().__init__(rule="restaurant_hours", detail=detail)

class CapacityExceededException(BusinessRuleException):
    """Исключение при превышении вместимости"""
    def __init__(self, capacity: int, requested: int):
        detail = f"Capacity exceeded: {capacity} available, {requested} requested"
        super().__init__(rule="capacity_limit", detail=detail)

class MinimumOrderException(BusinessRuleException):
    """Исключение для минимальной суммы заказа"""
    def __init__(self, minimum: float, current: float):
        detail = f"Minimum order amount is {minimum}. Current: {current}"
        super().__init__(rule="minimum_order", detail=detail)

class ReservationConflictException(ConflictException):
    """Исключение для конфликтов бронирования"""
    def __init__(self, table_id: int, time_slot: str):
        detail = f"Table {table_id} is already reserved for time slot {time_slot}"
        super().__init__(detail=detail, error_code="RESERVATION_CONFLICT")

class PaymentException(BadRequestException):
    """Исключение для ошибок оплаты"""
    def __init__(self, detail: str = "Payment error"):
        super().__init__(detail=detail, error_code="PAYMENT_ERROR")