from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.recommendation import Recommendation
from models.approval import Approval
from models.execution import Execution


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
