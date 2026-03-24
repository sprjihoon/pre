from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.recommendation import Recommendation


async def get_recommendations(
    db: AsyncSession,
    target_date: date | None = None,
    supplier_code: str | None = None,
    status: str | None = None,
) -> list[Recommendation]:
    q = select(Recommendation).order_by(Recommendation.created_at.desc())
    if target_date:
        q = q.where(Recommendation.target_date == target_date)
    if supplier_code:
        q = q.where(Recommendation.supplier_code == supplier_code)
    if status:
        q = q.where(Recommendation.status == status)
    result = await db.execute(q)
    return list(result.scalars().all())
