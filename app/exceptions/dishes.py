from .base import (
    NotFoundException,
    AlreadyExistsException,
    ValidationException,
    ConflictException
)

class DishNotFoundException(NotFoundException):
    """Исключение для блюда, которое не найдено"""
    def __init__(self, dish_id: int = None, name: str = None):
        if dish_id:
            super().__init__(resource="Dish", resource_id=str(dish_id))
        elif name:
            super().__init__(resource="Dish", field="name", value=name)
        else:
            super().__init__(resource="Dish")

class DishAlreadyExistsException(AlreadyExistsException):
    """Исключение для блюда, которое уже существует"""
    def __init__(self, name: str):
        super().__init__(resource="Dish", field="name", value=name)

class DishValidationException(ValidationException):
    """Исключение для ошибок валидации блюда"""
    def __init__(self, detail: str = "Dish validation error", errors: dict = None):
        super().__init__(detail=detail, errors=errors)

class DishInUseException(ConflictException):
    """Исключение при попытке удалить блюдо, которое используется в заказах"""
    def __init__(self, dish_id: int):
        detail = f"Dish with id {dish_id} is in use in active orders and cannot be deleted"
        super().__init__(detail=detail, error_code="DISH_IN_USE")

class DishPriceException(ValidationException):
    """Исключение для некорректной цены блюда"""
    def __init__(self, price: float):
        detail = f"Invalid price: {price}. Price must be positive."
        super().__init__(detail=detail)

class DishCategoryException(ValidationException):
    """Исключение для некорректной категории блюда"""
    def __init__(self, category_id: int):
        detail = f"Category with id {category_id} does not exist"
        super().__init__(detail=detail)