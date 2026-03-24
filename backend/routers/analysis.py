from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.analysis import SkuAnalysisOut, CombinationAnalysisOut
from services.analysis import (
    run_sku_analysis, run_combination_analysis,
    get_sku_analyses, get_combination_analyses,
)

router = APIRouter(prefix="/api/analysis", tags=["분석"])


@router.post("/sku", response_model=list[SkuAnalysisOut])
async def analyze_sku(
    analysis_date: date = Query(default=None),
    supplier_code: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    target = analysis_date or date.today()
    results = await run_sku_analysis(db, target, supplier_code)
    return results


@router.post("/combination", response_model=list[CombinationAnalysisOut])
async def analyze_combination(
    analysis_date: date = Query(default=None),
    supplier_code: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    target = analysis_date or date.today()
    results = await run_combination_analysis(db, target, supplier_code)
    return results


@router.get("/sku", response_model=list[SkuAnalysisOut])
async def list_sku_analyses(
    supplier_code: str = Query(default=None),
    analysis_date: date = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    return await get_sku_analyses(db, supplier_code, analysis_date)


@router.get("/combination", response_model=list[CombinationAnalysisOut])
async def list_combination_analyses(
    supplier_code: str = Query(default=None),
    analysis_date: date = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    return await get_combination_analyses(db, supplier_code, analysis_date)
