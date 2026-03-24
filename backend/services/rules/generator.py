"""규칙기반 엔진 - AI 없이도 항상 동작하는 기본 추천값 생성"""

from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.analysis import SkuAnalysis, CombinationAnalysis
from models.profile import SupplierProfile
from models.recommendation import Recommendation
from services.rules.calculator import (
    calculate_rule_qty, assess_risk,
    DEFAULT_MIN_QTY, DEFAULT_RECENT_WEIGHT, DEFAULT_WEEKDAY_WEIGHT,
)


async def _get_profile(db: AsyncSession, supplier_code: str) -> SupplierProfile | None:
    result = await db.execute(
        select(SupplierProfile).where(SupplierProfile.supplier_code == supplier_code)
    )
    return result.scalars().first()


async def generate_rule_based_recommendations(
    db: AsyncSession,
    target_date: date,
    supplier_code: str | None = None,
) -> list[Recommendation]:
    sku_q = select(SkuAnalysis)
    if supplier_code:
        sku_q = sku_q.where(SkuAnalysis.supplier_code == supplier_code)
    sku_q = sku_q.order_by(SkuAnalysis.analysis_date.desc())
    sku_result = await db.execute(sku_q)
    sku_analyses = sku_result.scalars().all()

    seen_keys: set[tuple[str, str]] = set()
    latest_skus: list[SkuAnalysis] = []
    for sa in sku_analyses:
        key = (sa.sku_code, sa.supplier_code)
        if key not in seen_keys:
            seen_keys.add(key)
            latest_skus.append(sa)

    combo_q = select(CombinationAnalysis)
    if supplier_code:
        combo_q = combo_q.where(CombinationAnalysis.supplier_code == supplier_code)
    combo_q = combo_q.order_by(CombinationAnalysis.analysis_date.desc())
    combo_result = await db.execute(combo_q)
    combo_analyses = combo_result.scalars().all()

    seen_combos: set[tuple[str, str]] = set()
    latest_combos: list[CombinationAnalysis] = []
    for ca in combo_analyses:
        key = (ca.combination_key, ca.supplier_code)
        if key not in seen_combos:
            seen_combos.add(key)
            latest_combos.append(ca)

    recommendations: list[Recommendation] = []
    profiles_cache: dict[str, SupplierProfile | None] = {}

    for sa in latest_skus:
        if sa.supplier_code not in profiles_cache:
            profiles_cache[sa.supplier_code] = await _get_profile(db, sa.supplier_code)
        profile = profiles_cache[sa.supplier_code]

        min_qty = profile.min_prepack_qty if profile else DEFAULT_MIN_QTY
        recent_w = profile.recent_weight if profile else DEFAULT_RECENT_WEIGHT
        weekday_w = profile.weekday_weight if profile else DEFAULT_WEEKDAY_WEIGHT
        conservative = profile.conservative_mode if profile else False

        qty = calculate_rule_qty(
            sa.avg_7d, sa.avg_30d, sa.avg_same_weekday,
            sa.repetition_rate, recent_w, weekday_w, min_qty, conservative,
        )
        if qty <= 0:
            continue

        risk = assess_risk(sa.repetition_rate, sa.volatility)

        rec = Recommendation(
            target_date=target_date,
            supplier_code=sa.supplier_code,
            target_type="sku",
            target_key=sa.sku_code,
            rule_based_qty=qty,
            final_recommended_qty=qty,
            risk_level=risk,
            status="pending",
        )
        db.add(rec)
        recommendations.append(rec)

    for ca in latest_combos:
        if ca.supplier_code not in profiles_cache:
            profiles_cache[ca.supplier_code] = await _get_profile(db, ca.supplier_code)
        profile = profiles_cache[ca.supplier_code]

        min_qty = profile.min_prepack_qty if profile else DEFAULT_MIN_QTY
        conservative = profile.conservative_mode if profile else False

        qty = round(ca.avg_quantity * ca.repetition_rate)
        if conservative:
            qty = round(qty * 0.85)
        if 0 < qty < min_qty:
            qty = min_qty
        if qty <= 0:
            continue

        risk = "low" if ca.repetition_rate >= 0.7 else ("medium" if ca.repetition_rate >= 0.4 else "high")

        rec = Recommendation(
            target_date=target_date,
            supplier_code=ca.supplier_code,
            target_type="combination",
            target_key=ca.combination_key,
            rule_based_qty=qty,
            final_recommended_qty=qty,
            risk_level=risk,
            status="pending",
        )
        db.add(rec)
        recommendations.append(rec)

    await db.commit()
    return recommendations
