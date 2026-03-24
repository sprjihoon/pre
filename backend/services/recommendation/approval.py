from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.recommendation import Recommendation
from models.approval import Approval


async def approve_recommendation(
    db: AsyncSession,
    recommendation_id: int,
    action: str,
    approved_qty: int | None = None,
    memo: str | None = None,
) -> Approval:
    result = await db.execute(
        select(Recommendation).where(Recommendation.id == recommendation_id)
    )
    rec = result.scalars().first()
    if not rec:
        raise ValueError("추천을 찾을 수 없습니다.")
    if rec.status not in ("pending", "llm_reviewed"):
        raise ValueError(f"현재 상태({rec.status})에서는 승인할 수 없습니다.")

    existing = await db.execute(
        select(Approval).where(Approval.recommendation_id == recommendation_id)
    )
    if existing.scalars().first():
        raise ValueError("이미 승인/거절 처리된 추천입니다.")

    if action == "modified" and approved_qty is not None:
        rec.final_recommended_qty = approved_qty

    rec.status = "approved" if action in ("approved", "modified") else "rejected"

    approval = Approval(
        recommendation_id=recommendation_id,
        action=action,
        approved_qty=approved_qty if action == "modified" else rec.final_recommended_qty,
        memo=memo,
        approved_at=datetime.now(),
    )
    db.add(approval)
    await db.commit()
    await db.refresh(approval)
    return approval
