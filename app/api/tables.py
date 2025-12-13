from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.tables import TableCreate, TableUpdate, TableResponse
from app.services.tables import TableService
from app.api.dependencies import get_table_service

router = APIRouter(prefix="/tables", tags=["tables"])

@router.get("/", response_model=list[TableResponse])
def get_tables(
    skip: int = 0,
    limit: int = 100,
    table_service: TableService = Depends(get_table_service)
):
    return table_service.get_all_tables(skip, limit)

@router.get("/{table_id}", response_model=TableResponse)
def get_table(
    table_id: int,
    table_service: TableService = Depends(get_table_service)
):
    table = table_service.get_table_by_id(table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    return table

@router.get("/number/{table_number}", response_model=TableResponse)
def get_table_by_number(
    table_number: int,
    table_service: TableService = Depends(get_table_service)
):
    table = table_service.get_table_by_number(table_number)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    return table

@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(
    table_data: TableCreate,
    table_service: TableService = Depends(get_table_service)
):
    # Проверяем, существует ли столик с таким номером
    existing = table_service.get_table_by_number(table_data.table_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Table with number {table_data.table_number} already exists"
        )
    return table_service.create_table(table_data)

@router.put("/{table_id}", response_model=TableResponse)
def update_table(
    table_id: int,
    table_data: TableUpdate,
    table_service: TableService = Depends(get_table_service)
):
    table = table_service.update_table(table_id, table_data)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    return table

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(
    table_id: int,
    table_service: TableService = Depends(get_table_service)
):
    if not table_service.delete_table(table_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )

@router.get("/available/", response_model=list[TableResponse])
def get_available_tables(
    table_service: TableService = Depends(get_table_service)
):
    return table_service.get_available_tables()

@router.patch("/{table_id}/status/{status}", response_model=TableResponse)
def update_table_status(
    table_id: int,
    status: str,
    table_service: TableService = Depends(get_table_service)
):
    table = table_service.update_table_status(table_id, status)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    return table