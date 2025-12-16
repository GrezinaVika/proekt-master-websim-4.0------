from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.order import OrderCreate, OrderUpdate, OrderResponse
from app.services.order import OrderService
from app.api.dependencies import get_order_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.get("/", response_model=list[OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    order_service: OrderService = Depends(get_order_service)
):
    """Get all orders with pagination"""
    try:
        return order_service.get_all_orders(skip, limit)
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving orders"
        )

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    order_service: OrderService = Depends(get_order_service)
):
    """Get single order by ID"""
    try:
        order = order_service.get_order_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving order"
        )

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    order_service: OrderService = Depends(get_order_service)
):
    """Create new order"""
    try:
        order = order_service.create_order(order_data)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create order"
            )
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating order"
        )

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    order_service: OrderService = Depends(get_order_service)
):
    """Update existing order"""
    try:
        order = order_service.update_order(order_id, order_data)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating order"
        )

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    order_service: OrderService = Depends(get_order_service)
):
    """Delete order"""
    try:
        if not order_service.delete_order(order_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting order {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting order"
        )
