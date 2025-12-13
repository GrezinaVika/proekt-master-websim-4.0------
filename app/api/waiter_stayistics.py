from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.waiter_statistics import (
    WaiterStatisticsCreate, 
    WaiterStatisticsUpdate, 
    WaiterStatisticsResponse
)
from app.services.waiter_statistics import WaiterStatisticsService
from app.api.dependencies import get_waiter_statistics_service

router = APIRouter(prefix="/waiter-statistics", tags=["waiter-statistics"])

@router.get("/", response_model=list[WaiterStatisticsResponse])
def get_all_statistics(
    skip: int = 0,
    limit: int = 100,
    service: WaiterStatisticsService = Depends(get_waiter_statistics_service)
):
    return service.get_all_statistics(skip, limit)

@router.get("/{stat_id}", response_model=WaiterStatisticsResponse)
def get_statistic(
    stat_id: int,
    service: WaiterStatisticsService = Depends(get_waiter_statistics_service)
):
    stat = service.get_statistic_by_id(stat_id)
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Statistics not found"
        )
    return stat

@router.get("/waiter/{waiter_id}", response_model=WaiterStatisticsResponse)
def get_statistic_by_waiter(
    waiter_id: int,
    service: WaiterStatisticsService = Depends(get_waiter_statistics_service)
):
    stat = service.get_statistic_by_waiter(waiter_id)
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Statistics for this waiter not found"
        )
    return stat

@router.post("/", response_model=WaiterStatisticsResponse, status_code=status.HTTP_201_CREATED)
def create_statistic(
    stat_data: WaiterStatisticsCreate,
    service: WaiterStatisticsService = Depends(get_waiter_statistics_service)
):
    # Проверяем, существует ли уже статистика для этого официанта
    existing = service.get_statistic_by_waiter(stat_data.waiter_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statistics for waiter {stat_data.waiter_id} already exists"
        )
    return service.create_statistic(stat_data)

@router.put("/{stat_id}", response_model=WaiterStatisticsResponse)
def update_statistic(
    stat_id: int,
    stat_data: WaiterStatisticsUpdate,
    service: WaiterStatisticsService = Depends(get_waiter_statistics_service)
):
    stat = service.update_statistic(stat_id, stat_data)
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Statistics not found"
        )
    return stat

@router.patch("/waiter/{waiter_id}/add-order", response_model=WaiterStatisticsResponse)
def add_order_to_statistic(
    waiter_id: int,
    revenue: float = 0.0,
    tips: float = 0.0,
    service: WaiterStatisticsService = Depends(get_waiter_statistics_service)
):
    stat = service.add_order_to_statistic(waiter_id, revenue, tips)
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Statistics not found"
        )
    return stat

@router.delete("/{stat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_statistic(
    stat_id: int,
    service: WaiterStatisticsService = Depends(get_waiter_statistics_service)
):
    if not service.delete_statistic(stat_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Statistics not found"
        )