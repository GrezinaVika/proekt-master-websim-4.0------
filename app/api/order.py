from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.order import OrderCreate, OrderUpdate, OrderResponse
from app.services.order import OrderService
from app.api.dependencies import get_order_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=list[OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    order_service: OrderService = Depends(get_order_service)
):
    return order_service.get_all_orders(skip, limit)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    order_service: OrderService = Depends(get_order_service)
):
    order = order_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    order_service: OrderService = Depends(get_order_service)
):
    return order_service.create_order(order_data)

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    order_service: OrderService = Depends(get_order_service)
):
    order = order_service.update_order(order_id, order_data)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    order_service: OrderService = Depends(get_order_service)
):
    if not order_service.delete_order(order_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

@router.get("/status/{status}", response_model=list[OrderResponse])
def get_orders_by_status(
    status: str,
    order_service: OrderService = Depends(get_order_service)
):
    return order_service.get_orders_by_status(status)

@router.get("/table/{table_id}", response_model=list[OrderResponse])
def get_orders_by_table(
    table_id: int,
    order_service: OrderService = Depends(get_order_service)
):
    return order_service.get_orders_by_table(table_id)

@router.get("/waiter/{waiter_id}", response_model=list[OrderResponse])
def get_orders_by_waiter(
    waiter_id: int,
    order_service: OrderService = Depends(get_order_service)
):
    return order_service.get_orders_by_waiter(waiter_id)