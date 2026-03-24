"""작업 지시서 HTML 생성 서비스"""

from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.recommendation import Recommendation
from models.approval import Approval


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

    html_parts = [_html_header(target_date)]
    for sup_code, items in grouped.items():
        html_parts.append(_html_supplier_section(sup_code, items))
    html_parts.append(_html_footer())

    return "\n".join(html_parts)


def _html_header(target_date: date) -> str:
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>프리패킹 작업 지시서 - {target_date}</title>
<style>
  @media print {{
    @page {{ size: A4; margin: 15mm; }}
    .page-break {{ page-break-before: always; }}
    body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Malgun Gothic', sans-serif; font-size: 12px; color: #333; }}
  .header {{ text-align: center; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 10px; }}
  .header h1 {{ font-size: 20px; }}
  .header .date {{ font-size: 14px; color: #666; margin-top: 4px; }}
  .supplier-section {{ margin-bottom: 30px; }}
  .supplier-name {{ font-size: 16px; font-weight: bold; background: #f0f0f0; padding: 8px 12px; margin-bottom: 10px; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 15px; }}
  th, td {{ border: 1px solid #999; padding: 6px 10px; text-align: left; }}
  th {{ background: #e8e8e8; font-weight: bold; }}
  .check-col {{ width: 40px; text-align: center; }}
  .memo-row td {{ border-top: none; }}
  .footer {{ margin-top: 30px; font-size: 11px; color: #666; text-align: center; }}
  .notes {{ margin-top: 20px; padding: 10px; border: 1px dashed #999; min-height: 60px; }}
  .notes-title {{ font-weight: bold; margin-bottom: 5px; }}
</style>
</head>
<body>
<div class="header">
  <h1>프리패킹 작업 지시서</h1>
  <div class="date">작업일: {target_date.strftime('%Y년 %m월 %d일')}</div>
</div>"""


def _html_supplier_section(supplier_code: str, items: list[dict]) -> str:
    rows = ""
    for i, item in enumerate(items, 1):
        rows += f"""
    <tr>
      <td>{i}</td>
      <td>{item['target_type']}</td>
      <td>{item['target_key']}</td>
      <td style="text-align:right; font-weight:bold;">{item['qty']}</td>
      <td>{item['risk']}</td>
      <td>{item['memo']}</td>
      <td class="check-col">☐</td>
    </tr>"""

    return f"""
<div class="supplier-section">
  <div class="supplier-name">업체: {supplier_code}</div>
  <table>
    <thead>
      <tr>
        <th style="width:40px;">No</th>
        <th style="width:60px;">구분</th>
        <th>대상</th>
        <th style="width:70px;">수량</th>
        <th style="width:60px;">위험도</th>
        <th>메모</th>
        <th class="check-col">확인</th>
      </tr>
    </thead>
    <tbody>{rows}
    </tbody>
  </table>
  <div class="notes">
    <div class="notes-title">작업자 메모:</div>
  </div>
</div>"""


def _html_footer() -> str:
    return """
<div class="footer">
  본 지시서는 프리패킹 예측 시스템에서 자동 생성되었습니다.
</div>
</body>
</html>"""
