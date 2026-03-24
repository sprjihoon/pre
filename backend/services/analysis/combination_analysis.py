from datetime import date
from collections import defaultdict

import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.analysis import CombinationAnalysis
from services.analysis.common import get_active_records


async def run_combination_analysis(
    db: AsyncSession,
    analysis_date: date,
    supplier_code: str | None = None,
) -> list[CombinationAnalysis]:
    records = await get_active_records(db, supplier_code)
    if not records:
        return []

    combo_data: dict[tuple[str, str], list[tuple[date, int]]] = defaultdict(list)
    for r in records:
        if r.combination_key:
            combo_data[(r.combination_key, r.supplier_code)].append((r.order_date, r.quantity))

    total_dates = set()
    for r in records:
        total_dates.add(r.order_date)
    total_date_count = len(total_dates)

    results = []
    for (combo_key, sup_code), entries in combo_data.items():
        entries.sort(key=lambda x: x[0])
        combo_dates = set(d for d, q in entries)
        all_qtys = [q for d, q in entries]

        occurrence_rate = len(combo_dates) / total_date_count if total_date_count > 0 else 0.0
        avg_quantity = float(np.mean(all_qtys)) if all_qtys else 0.0

        if combo_dates:
            date_range = (max(combo_dates) - min(combo_dates)).days + 1
            repetition_rate = len(combo_dates) / date_range if date_range > 0 else 0.0
        else:
            repetition_rate = 0.0

        analysis = CombinationAnalysis(
            combination_key=combo_key,
            supplier_code=sup_code,
            analysis_date=analysis_date,
            occurrence_rate=round(occurrence_rate, 4),
            avg_quantity=round(avg_quantity, 2),
            repetition_rate=round(repetition_rate, 4),
            total_occurrences=len(entries),
        )
        db.add(analysis)
        results.append(analysis)

    await db.commit()
    return results


async def get_combination_analyses(
    db: AsyncSession,
    supplier_code: str | None = None,
    analysis_date: date | None = None,
) -> list[CombinationAnalysis]:
    q = select(CombinationAnalysis)
    if supplier_code:
        q = q.where(CombinationAnalysis.supplier_code == supplier_code)
    if analysis_date:
        q = q.where(CombinationAnalysis.analysis_date == analysis_date)
    q = q.order_by(CombinationAnalysis.repetition_rate.desc())
    result = await db.execute(q)
    return list(result.scalars().all())
