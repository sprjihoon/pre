from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.recommendation import RecommendationOut
from services.rules_engine import generate_rule_based_recommendations

router = APIRouter(prefix="/api/rules", tags=["규칙기반 엔진"])


@router.post("/generate", response_model=list[RecommendationOut])
async def generate_recommendations(
    target_date: date = Query(default=None),
    supplier_code: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    target = target_date or date.today()
    return await generate_rule_based_recommendations(db, target, supplier_code)
