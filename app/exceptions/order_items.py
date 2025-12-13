from .base import (
    NotFoundException,
    ValidationException,
    BadRequestException
)

class OrderItemNotFoundException(NotFoundException):
    """Исключение для позиции заказа, которая не найдена"""
    def __init__(self, item_id: int = None):
        if item_id:
            super().__init__(resource="Order item", resource_id=str(item_id))
        else:
            super().__init__(resource="Order item")

class OrderItemValidationException(ValidationException):
    """Исключение для ошибок валидации позиции заказа"""
    def __init__(self, detail: str = "Order item validation error", errors: dict = None):
        super().__init__(detail=detail, errors=errors)

class OrderItemQuantityException(BadRequestException):
    """Исключение для некорректного количества"""
    def __init__(self, quantity: int):
        detail = f"Invalid quantity: {quantity}. Quantity must be positive."
        super().__init__(detail=detail, error_code="INVALID_QUANTITY")

class OrderItemPriceException(ValidationException):
    """Исключение для некорректной цены позиции"""
    def __init__(self, price: float):
        detail = f"Invalid price: {price}. Price must be positive."
        super().__init__(detail=detail)

class OrderItemDishException(ValidationException):
    """Исключение для некорректного блюда в позиции"""
    def __init__(self, dish_id: int):
        detail = f"Dish with id {dish_id} does not exist or is not available"
        super().__init__(detail=detail)