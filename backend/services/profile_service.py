from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.profile import SupplierProfile, ExclusionRule
from schemas.profile import SupplierProfileCreate, SupplierProfileUpdate, ExclusionRuleCreate


async def get_profiles(db: AsyncSession) -> list[SupplierProfile]:
    result = await db.execute(select(SupplierProfile).order_by(SupplierProfile.supplier_code))
    return list(result.scalars().all())


async def get_profile(db: AsyncSession, supplier_code: str) -> SupplierProfile | None:
    result = await db.execute(
        select(SupplierProfile).where(SupplierProfile.supplier_code == supplier_code)
    )
    return result.scalars().first()


async def create_profile(db: AsyncSession, data: SupplierProfileCreate) -> SupplierProfile:
    profile = SupplierProfile(**data.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def update_profile(
    db: AsyncSession, supplier_code: str, data: SupplierProfileUpdate
) -> SupplierProfile:
    profile = await get_profile(db, supplier_code)
    if not profile:
        raise ValueError("프로파일을 찾을 수 없습니다.")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_profile(db: AsyncSession, supplier_code: str) -> bool:
    profile = await get_profile(db, supplier_code)
    if not profile:
        return False
    await db.delete(profile)
    await db.commit()
    return True


async def get_exclusion_rules(
    db: AsyncSession, supplier_code: str | None = None
) -> list[ExclusionRule]:
    q = select(ExclusionRule).where(ExclusionRule.is_active == True)
    if supplier_code:
        q = q.where(ExclusionRule.supplier_code == supplier_code)
    result = await db.execute(q)
    return list(result.scalars().all())


async def create_exclusion_rule(db: AsyncSession, data: ExclusionRuleCreate) -> ExclusionRule:
    rule = ExclusionRule(**data.model_dump())
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


async def deactivate_exclusion_rule(db: AsyncSession, rule_id: int) -> bool:
    result = await db.execute(
        select(ExclusionRule).where(ExclusionRule.id == rule_id)
    )
    rule = result.scalars().first()
    if not rule:
        return False
    rule.is_active = False
    await db.commit()
    return True
