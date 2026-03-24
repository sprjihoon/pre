import { useState } from "react";
import PageHeader from "../../components/PageHeader";
import Button from "../../components/Button";
import Card from "../../components/Card";
import StatCard from "../../components/StatCard";
import Table, { type Column } from "../../components/Table";
import { validationApi, reportApi } from "../../api";
import type { ValidationResult, ReportSummary } from "../../types";

export default function ReportPage() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [supplier, setSupplier] = useState("");
  const [summary, setSummary] = useState<ReportSummary | null>(null);
  const [details, setDetails] = useState<ValidationResult[]>([]);
  const [targetDate, setTargetDate] = useState("");

  const loadReport = async () => {
    if (!startDate || !endDate) { alert("기간을 선택하세요."); return; }
    const s = await reportApi.summary(startDate, endDate, supplier || undefined);
    setSummary(s.data);
    const d = await validationApi.list(undefined, supplier || undefined);
    setDetails(d.data.filter((v) => v.target_date >= startDate && v.target_date <= endDate));
  };

  const runValidation = async () => {
    if (!targetDate) { alert("검증일을 선택하세요."); return; }
    await validationApi.run(targetDate, supplier || undefined);
    alert("검증 완료");
  };

  const detailCols: Column<ValidationResult>[] = [
    { key: "target_date", header: "날짜", width: 100 },
    { key: "supplier_code", header: "업체", width: 80 },
    { key: "target_key", header: "대상" },
    { key: "predicted_qty", header: "예측", width: 60, align: "right" },
    { key: "actual_qty", header: "실제", width: 60, align: "right" },
    { key: "accuracy", header: "정확도", width: 70, align: "right", render: (r) => `${(r.accuracy * 100).toFixed(1)}%` },
    { key: "usage_rate", header: "사용률", width: 70, align: "right", render: (r) => `${(r.usage_rate * 100).toFixed(1)}%` },
    { key: "unwrap_rate", header: "해체율", width: 70, align: "right", render: (r) => `${(r.unwrap_rate * 100).toFixed(1)}%` },
    {
      key: "is_overpredict",
      header: "과대",
      width: 50,
      align: "center",
      render: (r) => r.is_overpredict ? "⬆️" : "",
    },
    {
      key: "is_underpredict",
      header: "과소",
      width: 50,
      align: "center",
      render: (r) => r.is_underpredict ? "⬇️" : "",
    },
  ];

  return (
    <div>
      <PageHeader title="검증 / 리포트" description="예측 vs 실제 비교 분석 및 정확도 리포트" />

      <Card>
        <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap", marginBottom: 12 }}>
          <label style={{ fontSize: 13 }}>
            검증일: <input type="date" value={targetDate} onChange={(e) => setTargetDate(e.target.value)} style={inputStyle} />
          </label>
          <label style={{ fontSize: 13 }}>
            업체: <input value={supplier} onChange={(e) => setSupplier(e.target.value)} placeholder="전체" style={inputStyle} />
          </label>
          <Button onClick={runValidation}>검증 실행</Button>
        </div>
        <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
          <label style={{ fontSize: 13 }}>
            시작: <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} style={inputStyle} />
          </label>
          <label style={{ fontSize: 13 }}>
            종료: <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} style={inputStyle} />
          </label>
          <Button variant="secondary" onClick={loadReport}>리포트 조회</Button>
        </div>
      </Card>

      {summary && (
        <div style={{ display: "flex", gap: 16, margin: "16px 0", flexWrap: "wrap" }}>
          <StatCard label="총 예측 건수" value={summary.total_predictions} />
          <StatCard label="평균 정확도" value={`${(summary.avg_accuracy * 100).toFixed(1)}%`} color="#1e8e3e" />
          <StatCard label="평균 사용률" value={`${(summary.avg_usage_rate * 100).toFixed(1)}%`} color="#1a73e8" />
          <StatCard label="평균 해체율" value={`${(summary.avg_unwrap_rate * 100).toFixed(1)}%`} color="#d93025" />
          <StatCard label="과대예측" value={summary.overpredict_count} color="#e37400" />
          <StatCard label="과소예측" value={summary.underpredict_count} color="#8430ce" />
        </div>
      )}

      <Card title="검증 상세" style={{ marginTop: 16 }}>
        <Table columns={detailCols} data={details} />
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
};
