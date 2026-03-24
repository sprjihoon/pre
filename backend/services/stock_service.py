from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.stock import PrepackStock


async def get_stocks(
    db: AsyncSession,
    supplier_code: str | None = None,
    status: str | None = None,
) -> list[PrepackStock]:
    q = select(PrepackStock)
    if supplier_code:
        q = q.where(PrepackStock.supplier_code == supplier_code)
    if status:
        q = q.where(PrepackStock.status == status)
    result = await db.execute(q)
    return list(result.scalars().all())


async def create_or_update_stock(
    db: AsyncSession,
    target_type: str,
    target_key: str,
    supplier_code: str,
    qty: int,
    location_code: str | None = None,
) -> PrepackStock:
    result = await db.execute(
        select(PrepackStock).where(
            PrepackStock.target_key == target_key,
            PrepackStock.supplier_code == supplier_code,
            PrepackStock.status == "active",
        )
    )
    stock = result.scalars().first()

    if stock:
        stock.current_qty += qty
        stock.last_updated = datetime.now()
        if location_code:
            stock.location_code = location_code
    else:
        stock = PrepackStock(
            target_type=target_type,
            target_key=target_key,
            supplier_code=supplier_code,
            current_qty=qty,
            location_code=location_code,
            status="active",
            last_updated=datetime.now(),
        )
        db.add(stock)

    await db.commit()
    await db.refresh(stock)
    return stock


async def deduct_stock(db: AsyncSession, stock_id: int, qty: int) -> PrepackStock:
    result = await db.execute(
        select(PrepackStock).where(PrepackStock.id == stock_id)
    )
    stock = result.scalars().first()
    if not stock:
        raise ValueError("재고를 찾을 수 없습니다.")
    if stock.current_qty < qty:
        raise ValueError("차감 수량이 현재 재고보다 많습니다.")

    stock.current_qty -= qty
    stock.last_updated = datetime.now()
    if stock.current_qty == 0:
        stock.status = "depleted"

    await db.commit()
    await db.refresh(stock)
    return stock
