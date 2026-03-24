from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.location import LocationMaster, LocationHistory


async def get_locations(db: AsyncSession, zone: str | None = None) -> list[LocationMaster]:
    q = select(LocationMaster).where(LocationMaster.is_active == True)
    if zone:
        q = q.where(LocationMaster.zone == zone)
    q = q.order_by(LocationMaster.location_code)
    result = await db.execute(q)
    return list(result.scalars().all())


async def create_location(
    db: AsyncSession, location_code: str, zone: str | None = None, description: str | None = None
) -> LocationMaster:
    loc = LocationMaster(
        location_code=location_code,
        zone=zone,
        description=description,
    )
    db.add(loc)
    await db.commit()
    await db.refresh(loc)
    return loc


async def assign_location(
    db: AsyncSession,
    location_id: int,
    target_key: str,
    target_type: str,
    quantity: int,
    memo: str | None = None,
) -> LocationHistory:
    result = await db.execute(
        select(LocationMaster).where(LocationMaster.id == location_id)
    )
    loc = result.scalars().first()
    if not loc:
        raise ValueError("로케이션을 찾을 수 없습니다.")

    if target_type == "sku":
        loc.current_sku = target_key
    else:
        loc.current_combination = target_key

    history = LocationHistory(
        location_id=location_id,
        action="assign",
        target_key=target_key,
        quantity=quantity,
        action_at=datetime.now(),
        memo=memo,
    )
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


async def clear_location(db: AsyncSession, location_id: int, memo: str | None = None) -> LocationHistory:
    result = await db.execute(
        select(LocationMaster).where(LocationMaster.id == location_id)
    )
    loc = result.scalars().first()
    if not loc:
        raise ValueError("로케이션을 찾을 수 없습니다.")

    prev_key = loc.current_sku or loc.current_combination
    loc.current_sku = None
    loc.current_combination = None

    history = LocationHistory(
        location_id=location_id,
        action="clear",
        target_key=prev_key,
        quantity=0,
        action_at=datetime.now(),
        memo=memo,
    )
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


async def get_location_history(db: AsyncSession, location_id: int) -> list[LocationHistory]:
    result = await db.execute(
        select(LocationHistory)
        .where(LocationHistory.location_id == location_id)
        .order_by(LocationHistory.action_at.desc())
    )
    return list(result.scalars().all())
