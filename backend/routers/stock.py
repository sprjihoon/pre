from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.location import StockOut, UnwrapRequest, UnwrapOut
from services.stock_service import get_stocks, deduct_stock
from services.unwrap_service import unwrap_stock, get_unwrap_records

router = APIRouter(prefix="/api/stock", tags=["재고"])


@router.get("", response_model=list[StockOut])
async def list_stocks(
    supplier_code: str = Query(default=None),
    status: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    return await get_stocks(db, supplier_code, status)


@router.post("/{stock_id}/deduct", response_model=StockOut)
async def deduct(stock_id: int, qty: int = Query(...), db: AsyncSession = Depends(get_db)):
    try:
        return await deduct_stock(db, stock_id, qty)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/unwrap", response_model=UnwrapOut)
async def unwrap(body: UnwrapRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await unwrap_stock(
            db, body.stock_id, body.unwrap_qty,
            body.reason, body.is_returned, body.return_location,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/unwrap-records", response_model=list[UnwrapOut])
async def list_unwraps(stock_id: int = Query(default=None), db: AsyncSession = Depends(get_db)):
    return await get_unwrap_records(db, stock_id)
