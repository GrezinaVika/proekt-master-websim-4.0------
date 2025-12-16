from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.order_items import OrderItemCreate, OrderItemUpdate, OrderItemResponse
from app.services.order_items import OrderItemService
from app.api.dependencies import get_order_item_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/order-items", tags=["order-items"])
@router.get("/", response_model=list[OrderItemResponse])
def get_order_items(
    skip: int = 0,
    limit: int = 100,
    service: OrderItemService = Depends(get_order_item_service)
):
    """Get all order items with pagination"""
    try:
        return service.get_all_order_items(skip, limit)
    except Exception as e:
        logger.error(f"Error getting order items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving order items"
        )

@router.get("/{item_id}", response_model=OrderItemResponse)
def get_order_item(
    item_id: int,
    service: OrderItemService = Depends(get_order_item_service)
):
    """Get single order item by ID"""
    try:
        item = service.get_order_item_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order item not found"
            )
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving order item"
        )

@router.post("/", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
def create_order_item(
    item_data: OrderItemCreate,
    service: OrderItemService = Depends(get_order_item_service)
):
    """Create new order item"""
    try:
        item = service.create_order_item(item_data)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create order item"
            )
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating order item"
        )

@router.put("/{item_id}", response_model=OrderItemResponse)
def update_order_item(
    item_id: int,
    item_data: OrderItemUpdate,
    service: OrderItemService = Depends(get_order_item_service)
):
    """Update existing order item"""
    try:
        item = service.update_order_item(item_id, item_data)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order item not found"
            )
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating order item"
        )

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(
    item_id: int,
    service: OrderItemService = Depends(get_order_item_service)
):
    """Delete order item"""
    try:
        if not service.delete_order_item(item_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order item not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting order item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting order item"
        )
