from datetime import date, timedelta
import numpy as np
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models.upload import UploadRecord, UploadFile
from models.analysis import SkuAnalysis, CombinationAnalysis


async def _get_active_records(db: AsyncSession, supplier_code: str | None = None):
    q = (
        select(UploadRecord)
        .join(UploadFile)
        .where(UploadFile.is_active == True)
    )
    if supplier_code:
        q = q.where(UploadRecord.supplier_code == supplier_code)
    result = await db.execute(q)
    return result.scalars().all()


async def run_sku_analysis(
    db: AsyncSession,
    analysis_date: date,
    supplier_code: str | None = None,
) -> list[SkuAnalysis]:
    records = await _get_active_records(db, supplier_code)
    if not records:
        return []

    from collections import defaultdict
    sku_data: dict[tuple[str, str], list[tuple[date, int]]] = defaultdict(list)
    for r in records:
        sku_data[(r.sku_code, r.supplier_code)].append((r.order_date, r.quantity))

    results = []
    for (sku_code, sup_code), entries in sku_data.items():
        entries.sort(key=lambda x: x[0])
        all_dates = [e[0] for e in entries]
        all_qtys = [e[1] for e in entries]

        d7 = analysis_date - timedelta(days=7)
        d30 = analysis_date - timedelta(days=30)

        qty_7d = [q for d, q in entries if d7 <= d < analysis_date]
        qty_30d = [q for d, q in entries if d30 <= d < analysis_date]

        weekday = analysis_date.weekday()
        qty_weekday = [q for d, q in entries if d.weekday() == weekday and d < analysis_date]

        avg_7d = float(np.mean(qty_7d)) if qty_7d else 0.0
        avg_30d = float(np.mean(qty_30d)) if qty_30d else 0.0
        avg_same_weekday = float(np.mean(qty_weekday)) if qty_weekday else 0.0

        unique_dates = set(all_dates)
        if all_dates:
            date_range = (max(all_dates) - min(all_dates)).days + 1
            repetition_rate = len(unique_dates) / date_range if date_range > 0 else 0.0
        else:
            repetition_rate = 0.0

        volatility = float(np.std(all_qtys)) / float(np.mean(all_qtys)) if all_qtys and np.mean(all_qtys) > 0 else 0.0

        sorted_dates = sorted(unique_dates, reverse=True)
        consecutive = 0
        for i, d in enumerate(sorted_dates):
            if i == 0:
                consecutive = 1
            elif (sorted_dates[i - 1] - d).days == 1:
                consecutive += 1
            else:
                break

        analysis = SkuAnalysis(
            sku_code=sku_code,
            supplier_code=sup_code,
            analysis_date=analysis_date,
            avg_7d=round(avg_7d, 2),
            avg_30d=round(avg_30d, 2),
            avg_same_weekday=round(avg_same_weekday, 2),
            repetition_rate=round(repetition_rate, 4),
            volatility=round(volatility, 4),
            total_days_appeared=len(unique_dates),
            consecutive_days=consecutive,
        )
        db.add(analysis)
        results.append(analysis)

    await db.commit()
    return results


async def run_combination_analysis(
    db: AsyncSession,
    analysis_date: date,
    supplier_code: str | None = None,
) -> list[CombinationAnalysis]:
    records = await _get_active_records(db, supplier_code)
    if not records:
        return []

    from collections import defaultdict
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


async def get_sku_analyses(
    db: AsyncSession,
    supplier_code: str | None = None,
    analysis_date: date | None = None,
) -> list[SkuAnalysis]:
    q = select(SkuAnalysis)
    if supplier_code:
        q = q.where(SkuAnalysis.supplier_code == supplier_code)
    if analysis_date:
        q = q.where(SkuAnalysis.analysis_date == analysis_date)
    q = q.order_by(SkuAnalysis.repetition_rate.desc())
    result = await db.execute(q)
    return list(result.scalars().all())


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
