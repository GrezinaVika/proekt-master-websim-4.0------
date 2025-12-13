from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.order_items import OrderItemCreate, OrderItemUpdate, OrderItemResponse
from app.services.order_items import OrderItemService
from app.api.dependencies import get_order_item_service

router = APIRouter(prefix="/order-items", tags=["order-items"])

@router.get("/", response_model=list[OrderItemResponse])
def get_order_items(
    skip: int = 0,
    limit: int = 100,
    service: OrderItemService = Depends(get_order_item_service)
):
    return service.get_all_order_items(skip, limit)

@router.get("/{item_id}", response_model=OrderItemResponse)
def get_order_item(
    item_id: int,
    service: OrderItemService = Depends(get_order_item_service)
):
    item = service.get_order_item_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found"
        )
    return item

@router.post("/", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
def create_order_item(
    item_data: OrderItemCreate,
    service: OrderItemService = Depends(get_order_item_service)
):
    return service.create_order_item(item_data)

@router.put("/{item_id}", response_model=OrderItemResponse)
def update_order_item(
    item_id: int,
    item_data: OrderItemUpdate,
    service: OrderItemService = Depends(get_order_item_service)
):
    item = service.update_order_item(item_id, item_data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found"
        )
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(
    item_id: int,
    service: OrderItemService = Depends(get_order_item_service)
):
    if not service.delete_order_item(item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found"
        )

@router.get("/order/{order_id}", response_model=list[OrderItemResponse])
def get_items_by_order(
    order_id: int,
    service: OrderItemService = Depends(get_order_item_service)
):
    return service.get_items_by_order(order_id)

@router.get("/menu/{menu_id}", response_model=list[OrderItemResponse])
def get_items_by_menu(
    menu_id: int,
    service: OrderItemService = Depends(get_order_item_service)
):
    return service.get_items_by_menu(menu_id)