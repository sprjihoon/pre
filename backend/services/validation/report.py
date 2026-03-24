from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.validation import ValidationResult
from schemas.validation import ReportSummary


async def get_report_summary(
    db: AsyncSession,
    period_start: date,
    period_end: date,
    supplier_code: str | None = None,
) -> ReportSummary:
    q = select(ValidationResult).where(
        ValidationResult.target_date >= period_start,
        ValidationResult.target_date <= period_end,
    )
    if supplier_code:
        q = q.where(ValidationResult.supplier_code == supplier_code)

    result = await db.execute(q)
    results = result.scalars().all()

    if not results:
        return ReportSummary(
            period_start=period_start,
            period_end=period_end,
            supplier_code=supplier_code,
            total_predictions=0,
            avg_accuracy=0.0,
            avg_usage_rate=0.0,
            avg_unwrap_rate=0.0,
            overpredict_count=0,
            underpredict_count=0,
        )

    return ReportSummary(
        period_start=period_start,
        period_end=period_end,
        supplier_code=supplier_code,
        total_predictions=len(results),
        avg_accuracy=round(sum(r.accuracy for r in results) / len(results), 4),
        avg_usage_rate=round(sum(r.usage_rate for r in results) / len(results), 4),
        avg_unwrap_rate=round(sum(r.unwrap_rate for r in results) / len(results), 4),
        overpredict_count=sum(1 for r in results if r.is_overpredict),
        underpredict_count=sum(1 for r in results if r.is_underpredict),
    )
