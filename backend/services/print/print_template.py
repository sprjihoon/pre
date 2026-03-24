"""작업 지시서 HTML 템플릿"""

from datetime import date


def html_header(target_date: date) -> str:
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


def html_supplier_section(supplier_code: str, items: list[dict]) -> str:
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


def html_footer() -> str:
    return """
<div class="footer">
  본 지시서는 프리패킹 예측 시스템에서 자동 생성되었습니다.
</div>
</body>
</html>"""
