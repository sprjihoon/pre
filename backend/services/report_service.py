from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from services.validation_service import get_validation_results, get_report_summary
from schemas.validation import ReportSummary


async def generate_report(
    db: AsyncSession,
    period_start: date,
    period_end: date,
    supplier_code: str | None = None,
) -> dict:
    summary = await get_report_summary(db, period_start, period_end, supplier_code)
    details = await get_validation_results(db, supplier_code=supplier_code)

    filtered = [
        d for d in details
        if period_start <= d.target_date <= period_end
    ]

    return {
        "summary": summary,
        "details": filtered,
    }
