from datetime import date
from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from services.print import generate_print_html

router = APIRouter(prefix="/api/print", tags=["출력"])


@router.get("/work-order", response_class=HTMLResponse)
async def print_work_order(
    target_date: date = Query(...),
    supplier_code: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    html = await generate_print_html(db, target_date, supplier_code)
    return HTMLResponse(content=html)
