from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.validation import ValidationResultOut, ReportSummary
from services.validation_service import run_validation, get_validation_results, get_report_summary

router = APIRouter(prefix="/api/validation", tags=["검증"])


@router.post("/run", response_model=list[ValidationResultOut])
async def validate(
    target_date: date = Query(...),
    supplier_code: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    return await run_validation(db, target_date, supplier_code)


@router.get("", response_model=list[ValidationResultOut])
async def list_validations(
    target_date: date = Query(default=None),
    supplier_code: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    return await get_validation_results(db, target_date, supplier_code)
