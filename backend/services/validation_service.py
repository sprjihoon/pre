from datetime import date
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models.validation import ValidationResult
from models.recommendation import Recommendation
from models.execution import Execution
from models.approval import Approval
from schemas.validation import ReportSummary


async def run_validation(
    db: AsyncSession,
    target_date: date,
    supplier_code: str | None = None,
) -> list[ValidationResult]:
    q = (
        select(Recommendation, Execution)
        .join(Approval, Recommendation.id == Approval.recommendation_id)
        .join(Execution, Approval.id == Execution.approval_id)
        .where(Recommendation.target_date == target_date)
    )
    if supplier_code:
        q = q.where(Recommendation.supplier_code == supplier_code)

    result = await db.execute(q)
    rows = result.all()

    validations = []
    for rec, exe in rows:
        predicted = rec.final_recommended_qty
        actual = exe.used_qty

        if predicted > 0:
            accuracy = min(actual / predicted, 1.0) if actual <= predicted else predicted / actual
            usage_rate = actual / predicted
            unwrap_rate = exe.remaining_qty / predicted if exe.remaining_qty > 0 else 0.0
        else:
            accuracy = 0.0
            usage_rate = 0.0
            unwrap_rate = 0.0

        vr = ValidationResult(
            target_date=target_date,
            supplier_code=rec.supplier_code,
            target_key=rec.target_key,
            predicted_qty=predicted,
            actual_qty=actual,
            accuracy=round(accuracy, 4),
            usage_rate=round(usage_rate, 4),
            unwrap_rate=round(unwrap_rate, 4),
            is_overpredict=predicted > actual,
            is_underpredict=predicted < actual,
        )
        db.add(vr)
        validations.append(vr)

    await db.commit()
    return validations


async def get_validation_results(
    db: AsyncSession,
    target_date: date | None = None,
    supplier_code: str | None = None,
) -> list[ValidationResult]:
    q = select(ValidationResult)
    if target_date:
        q = q.where(ValidationResult.target_date == target_date)
    if supplier_code:
        q = q.where(ValidationResult.supplier_code == supplier_code)
    result = await db.execute(q)
    return list(result.scalars().all())


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
