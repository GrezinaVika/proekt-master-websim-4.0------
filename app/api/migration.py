from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.migration import MigrationCreate, MigrationUpdate, MigrationResponse
from app.services.migration import MigrationService
from app.api.dependencies import get_migration_service

router = APIRouter(prefix="/migrations", tags=["migrations"])

@router.get("/", response_model=list[MigrationResponse])
def get_migrations(
    skip: int = 0,
    limit: int = 100,
    service: MigrationService = Depends(get_migration_service)
):
    return service.get_all_migrations(skip, limit)

@router.get("/{migration_id}", response_model=MigrationResponse)
def get_migration(
    migration_id: int,
    service: MigrationService = Depends(get_migration_service)
):
    migration = service.get_migration_by_id(migration_id)
    if not migration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Migration not found"
        )
    return migration

@router.get("/version/{version}", response_model=MigrationResponse)
def get_migration_by_version(
    version: str,
    service: MigrationService = Depends(get_migration_service)
):
    migrations = service.get_all_migrations()
    for migration in migrations:
        if migration.version == version:
            return migration
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Migration not found"
    )

@router.post("/", response_model=MigrationResponse, status_code=status.HTTP_201_CREATED)
def create_migration(
    migration_data: MigrationCreate,
    service: MigrationService = Depends(get_migration_service)
):
    return service.create_migration(migration_data)

@router.put("/{migration_id}", response_model=MigrationResponse)
def update_migration(
    migration_id: int,
    migration_data: MigrationUpdate,
    service: MigrationService = Depends(get_migration_service)
):
    migration = service.update_migration(migration_id, migration_data)
    if not migration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Migration not found"
        )
    return migration

@router.delete("/{migration_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_migration(
    migration_id: int,
    service: MigrationService = Depends(get_migration_service)
):
    if not service.delete_migration(migration_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Migration not found"
        )

@router.patch("/{migration_id}/success", response_model=MigrationResponse)
def mark_migration_success(
    migration_id: int,
    service: MigrationService = Depends(get_migration_service)
):
    migration = service.mark_as_success(migration_id)
    if not migration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Migration not found"
        )
    return migration

@router.patch("/{migration_id}/failed", response_model=MigrationResponse)
def mark_migration_failed(
    migration_id: int,
    service: MigrationService = Depends(get_migration_service)
):
    migration = service.mark_as_failed(migration_id)
    if not migration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Migration not found"
        )
    return migration