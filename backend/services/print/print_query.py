"""작업 지시서 데이터 조회 및 HTML 조립"""

from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.recommendation import Recommendation
from models.approval import Approval
from services.print.print_template import html_header, html_supplier_section, html_footer


async def generate_print_html(
    db: AsyncSession,
    target_date: date,
    supplier_code: str | None = None,
) -> str:
    q = (
        select(Recommendation, Approval)
        .join(Approval, Recommendation.id == Approval.recommendation_id)
        .where(
            Recommendation.target_date == target_date,
            Approval.action.in_(["approved", "modified"]),
        )
    )
    if supplier_code:
        q = q.where(Recommendation.supplier_code == supplier_code)
    q = q.order_by(Recommendation.supplier_code, Recommendation.target_type, Recommendation.target_key)

    result = await db.execute(q)
    rows = result.all()

    grouped: dict[str, list] = {}
    for rec, apv in rows:
        if rec.supplier_code not in grouped:
            grouped[rec.supplier_code] = []
        grouped[rec.supplier_code].append({
            "target_type": "SKU" if rec.target_type == "sku" else "조합",
            "target_key": rec.target_key,
            "qty": apv.approved_qty or rec.final_recommended_qty,
            "risk": rec.risk_level or "-",
            "memo": apv.memo or "",
        })

    html_parts = [html_header(target_date)]
    for sup_code, items in grouped.items():
        html_parts.append(html_supplier_section(sup_code, items))
    html_parts.append(html_footer())

    return "\n".join(html_parts)
