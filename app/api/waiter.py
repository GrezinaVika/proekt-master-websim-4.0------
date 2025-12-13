from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.waiter import WaiterCreate, WaiterUpdate, WaiterResponse
from app.services.waiter import WaiterService
from app.api.dependencies import get_waiter_service

router = APIRouter(prefix="/waiters", tags=["waiters"])

@router.get("/", response_model=list[WaiterResponse])
def get_waiters(
    skip: int = 0,
    limit: int = 100,
    service: WaiterService = Depends(get_waiter_service)
):
    return service.get_all_waiters(skip, limit)

@router.get("/{waiter_id}", response_model=WaiterResponse)
def get_waiter(
    waiter_id: int,
    service: WaiterService = Depends(get_waiter_service)
):
    waiter = service.get_waiter_by_id(waiter_id)
    if not waiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waiter not found"
        )
    return waiter

@router.post("/", response_model=WaiterResponse, status_code=status.HTTP_201_CREATED)
def create_waiter(
    waiter_data: WaiterCreate,
    service: WaiterService = Depends(get_waiter_service)
):
    # В реальном приложении нужно проверять уникальность логина
    return service.create_waiter(waiter_data)

@router.put("/{waiter_id}", response_model=WaiterResponse)
def update_waiter(
    waiter_id: int,
    waiter_data: WaiterUpdate,
    service: WaiterService = Depends(get_waiter_service)
):
    waiter = service.update_waiter(waiter_id, waiter_data)
    if not waiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waiter not found"
        )
    return waiter

@router.delete("/{waiter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_waiter(
    waiter_id: int,
    service: WaiterService = Depends(get_waiter_service)
):
    if not service.delete_waiter(waiter_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waiter not found"
        )

@router.post("/login")
def login_waiter(
    login: str,
    password: str,
    service: WaiterService = Depends(get_waiter_service)
):
    waiter = service.authenticate(login, password)
    if not waiter:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"message": "Login successful", "waiter_id": waiter.id}