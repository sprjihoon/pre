from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.location import (
    LocationMasterCreate, LocationMasterOut,
    LocationHistoryOut, LocationAssignRequest,
)
from services.location_service import (
    get_locations, create_location, assign_location,
    clear_location, get_location_history,
)

router = APIRouter(prefix="/api/location", tags=["로케이션"])


@router.get("", response_model=list[LocationMasterOut])
async def list_locations(zone: str = Query(default=None), db: AsyncSession = Depends(get_db)):
    return await get_locations(db, zone)


@router.post("", response_model=LocationMasterOut)
async def add_location(body: LocationMasterCreate, db: AsyncSession = Depends(get_db)):
    return await create_location(db, body.location_code, body.zone, body.description)


@router.post("/{location_id}/assign", response_model=LocationHistoryOut)
async def assign(location_id: int, body: LocationAssignRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await assign_location(db, location_id, body.target_key, body.target_type, body.quantity, body.memo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{location_id}/clear", response_model=LocationHistoryOut)
async def clear(location_id: int, memo: str = Query(default=None), db: AsyncSession = Depends(get_db)):
    try:
        return await clear_location(db, location_id, memo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{location_id}/history", response_model=list[LocationHistoryOut])
async def history(location_id: int, db: AsyncSession = Depends(get_db)):
    return await get_location_history(db, location_id)
