from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.dishes import DishCreate, DishUpdate, DishResponse
from app.services.dishes import DishService
from app.api.dependencies import get_dish_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dishes", tags=["dishes"])

@router.get("/", response_model=list[DishResponse])
def get_dishes(
    skip: int = 0,
    limit: int = 100,
    dish_service: DishService = Depends(get_dish_service)
):
    """Get all dishes with pagination"""
    try:
        return dish_service.get_all_dishes(skip, limit)
    except Exception as e:
        logger.error(f"Error getting dishes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving dishes"
        )

@router.get("/{dish_id}", response_model=DishResponse)
def get_dish(
    dish_id: int,
    dish_service: DishService = Depends(get_dish_service)
):
    """Get single dish by ID"""
    try:
        dish = dish_service.get_dish_by_id(dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dish not found"
            )
        return dish
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dish {dish_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving dish"
        )

@router.post("/", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
def create_dish(
    dish_data: DishCreate,
    dish_service: DishService = Depends(get_dish_service)
):
    """Create new dish"""
    try:
        dish = dish_service.create_dish(dish_data)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create dish"
            )
        return dish
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating dish: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating dish"
        )

@router.put("/{dish_id}", response_model=DishResponse)
def update_dish(
    dish_id: int,
    dish_data: DishUpdate,
    dish_service: DishService = Depends(get_dish_service)
):
    """Update existing dish"""
    try:
        dish = dish_service.update_dish(dish_id, dish_data)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dish not found"
            )
        return dish
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating dish {dish_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating dish"
        )

@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dish(
    dish_id: int,
    dish_service: DishService = Depends(get_dish_service)
):
    """Delete dish"""
    try:
        if not dish_service.delete_dish(dish_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dish not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting dish {dish_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting dish"
        )
