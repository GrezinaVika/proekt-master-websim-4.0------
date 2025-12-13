from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.cook import CookCreate, CookUpdate, CookResponse
from app.services.cook import CookService
from app.api.dependencies import get_cook_service

router = APIRouter(prefix="/cooks", tags=["cooks"])

@router.get("/", response_model=list[CookResponse])
def get_cooks(
    skip: int = 0,
    limit: int = 100,
    service: CookService = Depends(get_cook_service)
):
    return service.get_all_cooks(skip, limit)

@router.get("/{cook_id}", response_model=CookResponse)
def get_cook(
    cook_id: int,
    service: CookService = Depends(get_cook_service)
):
    cook = service.get_cook_by_id(cook_id)
    if not cook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook not found"
        )
    return cook

@router.post("/", response_model=CookResponse, status_code=status.HTTP_201_CREATED)
def create_cook(
    cook_data: CookCreate,
    service: CookService = Depends(get_cook_service)
):
    return service.create_cook(cook_data)

@router.put("/{cook_id}", response_model=CookResponse)
def update_cook(
    cook_id: int,
    cook_data: CookUpdate,
    service: CookService = Depends(get_cook_service)
):
    cook = service.update_cook(cook_id, cook_data)
    if not cook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook not found"
        )
    return cook

@router.delete("/{cook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cook(
    cook_id: int,
    service: CookService = Depends(get_cook_service)
):
    if not service.delete_cook(cook_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook not found"
        )

@router.post("/login")
def login_cook(
    login: str,
    password: str,
    service: CookService = Depends(get_cook_service)
):
    cook = service.authenticate(login, password)
    if not cook:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"message": "Login successful", "cook_id": cook.id}