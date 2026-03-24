from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.llm import LLMReviewOut, LLMReviewRequest
from engines.llm.ai_validator_service import review_recommendations
from engines.llm.ai_log_service import get_llm_reviews

router = APIRouter(prefix="/api/llm", tags=["LLM 검증"])


@router.post("/review", response_model=list[LLMReviewOut])
async def review(body: LLMReviewRequest, db: AsyncSession = Depends(get_db)):
    return await review_recommendations(db, body.recommendation_ids, body.review_level)


@router.get("/reviews", response_model=list[LLMReviewOut])
async def list_reviews(
    recommendation_id: int = Query(default=None),
    review_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    return await get_llm_reviews(db, recommendation_id, review_type)
