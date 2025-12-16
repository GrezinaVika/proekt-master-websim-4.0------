from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.tables import TableCreate, TableUpdate, TableResponse
from app.services.tables import TableService
from app.api.dependencies import get_table_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tables", tags=["tables"])
@router.get("/", response_model=list[TableResponse])
def get_tables(
    skip: int = 0,
    limit: int = 100,
    table_service: TableService = Depends(get_table_service)
):
    """Get all tables with pagination"""
    try:
        return table_service.get_all_tables(skip, limit)
    except Exception as e:
        logger.error(f"Error getting tables: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving tables"
        )

@router.get("/{table_id}", response_model=TableResponse)
def get_table(
    table_id: int,
    table_service: TableService = Depends(get_table_service)
):
    """Get single table by ID"""
    try:
        table = table_service.get_table_by_id(table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found"
            )
        return table
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting table {table_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving table"
        )

@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(
    table_data: TableCreate,
    table_service: TableService = Depends(get_table_service)
):
    """Create new table"""
    try:
        table = table_service.create_table(table_data)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create table"
            )
        return table
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating table"
        )

@router.put("/{table_id}", response_model=TableResponse)
def update_table(
    table_id: int,
    table_data: TableUpdate,
    table_service: TableService = Depends(get_table_service)
):
    """Update existing table"""
    try:
        table = table_service.update_table(table_id, table_data)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found"
            )
        return table
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating table {table_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating table"
        )

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(
    table_id: int,
    table_service: TableService = Depends(get_table_service)
):
    """Delete table"""
    try:
        if not table_service.delete_table(table_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting table {table_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting table"
        )
