import { useState } from "react";
import PageHeader from "../../components/PageHeader";
import Button from "../../components/Button";
import Card from "../../components/Card";
import { printApi } from "../../api";

export default function PrintPage() {
  const [date, setDate] = useState("");
  const [supplier, setSupplier] = useState("");

  const handlePrint = () => {
    if (!date) {
      alert("대상 날짜를 선택하세요.");
      return;
    }
    const url = printApi.workOrderUrl(date, supplier || undefined);
    window.open(url, "_blank");
  };

  return (
    <div>
      <PageHeader title="작업 지시서 출력" description="승인된 프리패킹 작업 지시서를 인쇄합니다." />

      <Card title="출력 설정">
        <div style={{ display: "flex", gap: 16, alignItems: "center", flexWrap: "wrap" }}>
          <label style={{ fontSize: 13 }}>
            작업일:
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              style={inputStyle}
            />
          </label>
          <label style={{ fontSize: 13 }}>
            업체코드:
            <input
              value={supplier}
              onChange={(e) => setSupplier(e.target.value)}
              placeholder="전체"
              style={inputStyle}
            />
          </label>
          <Button onClick={handlePrint}>인쇄 미리보기</Button>
        </div>
        <p style={{ fontSize: 12, color: "#888", marginTop: 12 }}>
          * 새 탭에서 지시서가 열리면 브라우저의 인쇄(Ctrl+P) 기능으로 출력하세요.
        </p>
      </Card>

      <Card title="지시서 안내" style={{ marginTop: 16 }}>
        <div style={{ fontSize: 13, lineHeight: 1.8, color: "#555" }}>
          <div>지시서에는 다음 항목이 포함됩니다:</div>
          <ul style={{ paddingLeft: 20 }}>
            <li>작업일자, 업체명</li>
            <li>대상 구분(SKU/조합), 대상명</li>
            <li>최종 승인 수량</li>
            <li>위험도, 메모</li>
            <li>체크칸 (작업자 확인용)</li>
            <li>작업자 메모란</li>
          </ul>
          <div>업체별로 그룹핑되어 A4 용지에 최적화됩니다.</div>
        </div>
      </Card>
    </div>
  );
}

const inputStyle: React.CSSProperties = {
  padding: "6px 10px",
  border: "1px solid #dadce0",
  borderRadius: 6,
  fontSize: 13,
  fontFamily: "inherit",
  marginLeft: 6,
};
