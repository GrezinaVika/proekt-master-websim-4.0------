from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.categories import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.categories import CategoryService
from app.api.dependencies import get_category_service

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    category_service: CategoryService = Depends(get_category_service)
):
    return category_service.get_all_categories(skip, limit)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service)
):
    category = category_service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service)
):
    return category_service.create_category(category_data)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service)
):
    category = category_service.update_category(category_id, category_data)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service)
):
    if not category_service.delete_category(category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )