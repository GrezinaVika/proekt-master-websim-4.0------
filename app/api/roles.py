from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.roles import RoleCreate, RoleUpdate, RoleResponse
from app.services.roles import RoleService
from app.api.dependencies import get_role_service

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=list[RoleResponse])
def get_roles(
    skip: int = 0,
    limit: int = 100,
    service: RoleService = Depends(get_role_service)
):
    return service.get_all_roles(skip, limit)

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    role = service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    role_data: RoleCreate,
    service: RoleService = Depends(get_role_service)
):
    existing = service.get_all_roles()
    for role in existing:
        if role.name == role_data.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role with this name already exists"
            )
    return service.create_role(role_data)

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    service: RoleService = Depends(get_role_service)
):
    role = service.update_role(role_id, role_data)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    if not service.delete_role(role_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )