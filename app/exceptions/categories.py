from .base import (
    NotFoundException,
    AlreadyExistsException,
    ValidationException,
    ConflictException
)

class CategoryNotFoundException(NotFoundException):
    """Исключение для категории, которая не найдена"""
    def __init__(self, category_id: int = None, name: str = None):
        if category_id:
            super().__init__(resource="Category", resource_id=str(category_id))
        elif name:
            super().__init__(resource="Category", field="name", value=name)
        else:
            super().__init__(resource="Category")

class CategoryAlreadyExistsException(AlreadyExistsException):
    """Исключение для категории, которая уже существует"""
    def __init__(self, name: str):
        super().__init__(resource="Category", field="name", value=name)

class CategoryValidationException(ValidationException):
    """Исключение для ошибок валидации категории"""
    def __init__(self, detail: str = "Category validation error", errors: dict = None):
        super().__init__(detail=detail, errors=errors)

class CategoryInUseException(ConflictException):
    """Исключение при попытке удалить категорию, которая используется"""
    def __init__(self, category_id: int):
        detail = f"Category with id {category_id} is in use by dishes and cannot be deleted"
        super().__init__(detail=detail, error_code="CATEGORY_IN_USE")