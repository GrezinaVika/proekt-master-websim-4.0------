from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.cook_statistics import (
    CookStatisticsCreate, 
    CookStatisticsUpdate, 
    CookStatisticsResponse
)
from app.services.cook_statistics import CookStatisticsService
from app.api.dependencies import get_cook_statistics_service

router = APIRouter(prefix="/cook-statistics", tags=["cook-statistics"])

@router.get("/", response_model=list[CookStatisticsResponse])
def get_all_cook_statistics(
    skip: int = 0,
    limit: int = 100,
    service: CookStatisticsService = Depends(get_cook_statistics_service)
):
    return service.get_all_statistics(skip, limit)

@router.get("/{stat_id}", response_model=CookStatisticsResponse)
def get_cook_statistic(
    stat_id: int,
    service: CookStatisticsService = Depends(get_cook_statistics_service)
):
    stat = service.get_statistic_by_id(stat_id)
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook statistics not found"
        )
    return stat

@router.get("/cook/{cook_id}", response_model=CookStatisticsResponse)
def get_statistic_by_cook(
    cook_id: int,
    service: CookStatisticsService = Depends(get_cook_statistics_service)
):
    stat = service.get_statistic_by_cook(cook_id)
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Statistics for this cook not found"
        )
    return stat

@router.post("/", response_model=CookStatisticsResponse, status_code=status.HTTP_201_CREATED)
def create_cook_statistic(
    stat_data: CookStatisticsCreate,
    service: CookStatisticsService = Depends(get_cook_statistics_service)
):
    existing = service.get_statistic_by_cook(stat_data.cook_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statistics for cook {stat_data.cook_id} already exists"
        )
    return service.create_statistic(stat_data)

@router.put("/{stat_id}", response_model=CookStatisticsResponse)
def update_cook_statistic(
    stat_id: int,
    stat_data: CookStatisticsUpdate,
    service: CookStatisticsService = Depends(get_cook_statistics_service)
):
    stat = service.update_statistic(stat_id, stat_data)
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook statistics not found"
        )
    return stat

@router.patch("/cook/{cook_id}/update-orders", response_model=CookStatisticsResponse)
def update_cook_active_orders(
    cook_id: int,
    change: int = 1,
    service: CookStatisticsService = Depends(get_cook_statistics_service)
):
    stat = service.update_cook_active_orders(cook_id, change)
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook statistics not found"
        )
    return stat

@router.delete("/{stat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cook_statistic(
    stat_id: int,
    service: CookStatisticsService = Depends(get_cook_statistics_service)
):
    if not service.delete_statistic(stat_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook statistics not found"
        )