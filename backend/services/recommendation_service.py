from datetime import date, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.recommendation import Recommendation
from models.approval import Approval
from models.execution import Execution


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


async def create_execution(
    db: AsyncSession,
    approval_id: int,
    actual_packed_qty: int,
) -> Execution:
    result = await db.execute(
        select(Approval).where(Approval.id == approval_id)
    )
    approval = result.scalars().first()
    if not approval:
        raise ValueError("승인 정보를 찾을 수 없습니다.")

    existing = await db.execute(
        select(Execution).where(Execution.approval_id == approval_id)
    )
    if existing.scalars().first():
        raise ValueError("이미 실행 기록이 있습니다.")

    execution = Execution(
        approval_id=approval_id,
        actual_packed_qty=actual_packed_qty,
        remaining_qty=actual_packed_qty,
        status="executed",
        executed_at=datetime.now(),
    )
    db.add(execution)

    rec_result = await db.execute(
        select(Recommendation).where(Recommendation.id == approval.recommendation_id)
    )
    rec = rec_result.scalars().first()
    if rec:
        rec.status = "executed"

    await db.commit()
    await db.refresh(execution)
    return execution


async def update_execution(
    db: AsyncSession,
    execution_id: int,
    used_qty: int | None = None,
    remaining_qty: int | None = None,
    status: str | None = None,
) -> Execution:
    result = await db.execute(
        select(Execution).where(Execution.id == execution_id)
    )
    execution = result.scalars().first()
    if not execution:
        raise ValueError("실행 기록을 찾을 수 없습니다.")

    if used_qty is not None:
        execution.used_qty = used_qty
        execution.remaining_qty = execution.actual_packed_qty - used_qty
    if remaining_qty is not None:
        execution.remaining_qty = remaining_qty
    if status:
        execution.status = status
        if status == "completed":
            execution.completed_at = datetime.now()

    await db.commit()
    await db.refresh(execution)
    return execution
