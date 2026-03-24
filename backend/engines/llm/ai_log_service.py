from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.llm import LLMReview


async def get_llm_reviews(
    db: AsyncSession,
    recommendation_id: int | None = None,
    review_type: str | None = None,
) -> list[LLMReview]:
    q = select(LLMReview).order_by(LLMReview.reviewed_at.desc())
    if recommendation_id:
        q = q.where(LLMReview.recommendation_id == recommendation_id)
    if review_type:
        q = q.where(LLMReview.review_type == review_type)
    result = await db.execute(q)
    return list(result.scalars().all())
