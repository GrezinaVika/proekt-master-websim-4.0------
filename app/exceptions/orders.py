from .base import (
    NotFoundException,
    AlreadyExistsException,
    ValidationException,
    ConflictException,
    BadRequestException
)

class OrderNotFoundException(NotFoundException):
    """Исключение для заказа, который не найден"""
    def __init__(self, order_id: int = None):
        if order_id:
            super().__init__(resource="Order", resource_id=str(order_id))
        else:
            super().__init__(resource="Order")

class OrderAlreadyExistsException(AlreadyExistsException):
    """Исключение для заказа, который уже существует"""
    def __init__(self, order_number: str):
        super().__init__(resource="Order", field="order_number", value=order_number)

class OrderValidationException(ValidationException):
    """Исключение для ошибок валидации заказа"""
    def __init__(self, detail: str = "Order validation error", errors: dict = None):
        super().__init__(detail=detail, errors=errors)

class OrderStatusException(ConflictException):
    """Исключение для некорректного статуса заказа"""
    def __init__(self, current_status: str, target_status: str):
        detail = f"Cannot change order status from '{current_status}' to '{target_status}'"
        super().__init__(detail=detail, error_code="INVALID_STATUS_CHANGE")

class OrderEmptyException(BadRequestException):
    """Исключение для пустого заказа"""
    def __init__(self):
        detail = "Order must contain at least one item"
        super().__init__(detail=detail, error_code="EMPTY_ORDER")

class OrderTableException(ValidationException):
    """Исключение для некорректного столика в заказе"""
    def __init__(self, table_id: int):
        detail = f"Table with id {table_id} is not available or does not exist"
        super().__init__(detail=detail)

class OrderTimeException(ConflictException):
    """Исключение для временных ограничений заказа"""
    def __init__(self, detail: str = "Order time constraint violation"):
        super().__init__(detail=detail, error_code="TIME_CONSTRAINT")