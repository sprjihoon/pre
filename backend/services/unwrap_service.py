from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.stock import PrepackStock
from models.unwrap import UnwrapRecord


async def unwrap_stock(
    db: AsyncSession,
    stock_id: int,
    unwrap_qty: int,
    reason: str | None = None,
    is_returned: bool = False,
    return_location: str | None = None,
) -> UnwrapRecord:
    result = await db.execute(
        select(PrepackStock).where(PrepackStock.id == stock_id)
    )
    stock = result.scalars().first()
    if not stock:
        raise ValueError("재고를 찾을 수 없습니다.")
    if stock.current_qty < unwrap_qty:
        raise ValueError(f"해체 수량({unwrap_qty})이 현재 재고({stock.current_qty})보다 많습니다.")

    stock.current_qty -= unwrap_qty
    stock.last_updated = datetime.now()
    if stock.current_qty == 0:
        stock.status = "unwrapped"

    record = UnwrapRecord(
        stock_id=stock_id,
        unwrap_qty=unwrap_qty,
        reason=reason,
        is_returned=is_returned,
        return_location=return_location,
        unwrapped_at=datetime.now(),
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_unwrap_records(db: AsyncSession, stock_id: int | None = None) -> list[UnwrapRecord]:
    q = select(UnwrapRecord).order_by(UnwrapRecord.unwrapped_at.desc())
    if stock_id:
        q = q.where(UnwrapRecord.stock_id == stock_id)
    result = await db.execute(q)
    return list(result.scalars().all())
