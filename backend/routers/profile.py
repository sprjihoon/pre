from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.profile import (
    SupplierProfileCreate, SupplierProfileUpdate, SupplierProfileOut,
    ExclusionRuleCreate, ExclusionRuleOut,
)
from services.profile_service import (
    get_profiles, get_profile, create_profile, update_profile, delete_profile,
    get_exclusion_rules, create_exclusion_rule, deactivate_exclusion_rule,
)

router = APIRouter(prefix="/api/profile", tags=["업체 프로파일"])


@router.get("", response_model=list[SupplierProfileOut])
async def list_profiles(db: AsyncSession = Depends(get_db)):
    return await get_profiles(db)


@router.get("/{supplier_code}", response_model=SupplierProfileOut)
async def get_one(supplier_code: str, db: AsyncSession = Depends(get_db)):
    result = await get_profile(db, supplier_code)
    if not result:
        raise HTTPException(status_code=404, detail="프로파일을 찾을 수 없습니다.")
    return result


@router.post("", response_model=SupplierProfileOut)
async def create(body: SupplierProfileCreate, db: AsyncSession = Depends(get_db)):
    return await create_profile(db, body)


@router.patch("/{supplier_code}", response_model=SupplierProfileOut)
async def update(supplier_code: str, body: SupplierProfileUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await update_profile(db, supplier_code, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{supplier_code}")
async def delete(supplier_code: str, db: AsyncSession = Depends(get_db)):
    result = await delete_profile(db, supplier_code)
    if not result:
        raise HTTPException(status_code=404, detail="프로파일을 찾을 수 없습니다.")
    return {"ok": True}


@router.get("/exclusions/list", response_model=list[ExclusionRuleOut])
async def list_exclusions(supplier_code: str = None, db: AsyncSession = Depends(get_db)):
    return await get_exclusion_rules(db, supplier_code)


@router.post("/exclusions", response_model=ExclusionRuleOut)
async def add_exclusion(body: ExclusionRuleCreate, db: AsyncSession = Depends(get_db)):
    return await create_exclusion_rule(db, body)


@router.delete("/exclusions/{rule_id}")
async def remove_exclusion(rule_id: int, db: AsyncSession = Depends(get_db)):
    result = await deactivate_exclusion_rule(db, rule_id)
    if not result:
        raise HTTPException(status_code=404, detail="규칙을 찾을 수 없습니다.")
    return {"ok": True}
