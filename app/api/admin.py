from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.admin import AdminCreate, AdminUpdate, AdminResponse
from app.services.admin import AdminService
from app.api.dependencies import get_admin_service

router = APIRouter(prefix="/admins", tags=["admins"])

@router.get("/", response_model=list[AdminResponse])
def get_admins(
    skip: int = 0,
    limit: int = 100,
    service: AdminService = Depends(get_admin_service)
):
    return service.get_all_admins(skip, limit)

@router.get("/{admin_id}", response_model=AdminResponse)
def get_admin(
    admin_id: int,
    service: AdminService = Depends(get_admin_service)
):
    admin = service.get_admin_by_id(admin_id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    return admin

@router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def create_admin(
    admin_data: AdminCreate,
    service: AdminService = Depends(get_admin_service)
):
    return service.create_admin(admin_data)

@router.put("/{admin_id}", response_model=AdminResponse)
def update_admin(
    admin_id: int,
    admin_data: AdminUpdate,
    service: AdminService = Depends(get_admin_service)
):
    admin = service.update_admin(admin_id, admin_data)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    return admin

@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
    admin_id: int,
    service: AdminService = Depends(get_admin_service)
):
    if not service.delete_admin(admin_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )

@router.post("/login")
def login_admin(
    login: str,
    password: str,
    service: AdminService = Depends(get_admin_service)
):
    admin = service.authenticate(login, password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"message": "Login successful", "admin_id": admin.id}