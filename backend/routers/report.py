from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.validation import ReportSummary
from services.validation import get_report_summary

router = APIRouter(prefix="/api/report", tags=["리포트"])


@router.get("/summary", response_model=ReportSummary)
async def report_summary(
    period_start: date = Query(...),
    period_end: date = Query(...),
    supplier_code: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    return await get_report_summary(db, period_start, period_end, supplier_code)
