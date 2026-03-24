import { useState } from "react";
import PageHeader from "../../components/PageHeader";
import Button from "../../components/Button";
import Card from "../../components/Card";
import Table, { type Column } from "../../components/Table";
import { analysisApi } from "../../api";
import type { SkuAnalysis, CombinationAnalysis } from "../../types";

export default function AnalysisPage() {
  const [date, setDate] = useState("");
  const [supplier, setSupplier] = useState("");
  const [skuData, setSkuData] = useState<SkuAnalysis[]>([]);
  const [comboData, setComboData] = useState<CombinationAnalysis[]>([]);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState<"sku" | "combo">("sku");

  const runAnalysis = async () => {
    setLoading(true);
    try {
      const [s, c] = await Promise.all([
        analysisApi.runSku(date || undefined, supplier || undefined),
        analysisApi.runCombination(date || undefined, supplier || undefined),
      ]);
      setSkuData(s.data);
      setComboData(c.data);
    } catch {
      alert("분석 실행 실패");
    } finally {
      setLoading(false);
    }
  };

  const loadData = async () => {
    const [s, c] = await Promise.all([
      analysisApi.listSku(supplier || undefined, date || undefined),
      analysisApi.listCombination(supplier || undefined, date || undefined),
    ]);
    setSkuData(s.data);
    setComboData(c.data);
  };

  const skuCols: Column<SkuAnalysis>[] = [
    { key: "sku_code", header: "SKU코드" },
    { key: "supplier_code", header: "업체코드", width: 80 },
    { key: "avg_7d", header: "7일 평균", width: 80, align: "right" },
    { key: "avg_30d", header: "30일 평균", width: 80, align: "right" },
    { key: "avg_same_weekday", header: "요일 평균", width: 80, align: "right" },
    { key: "repetition_rate", header: "반복률", width: 70, align: "right", render: (r) => `${(r.repetition_rate * 100).toFixed(1)}%` },
    { key: "volatility", header: "변동성", width: 70, align: "right", render: (r) => r.volatility.toFixed(3) },
    { key: "total_days_appeared", header: "출현일수", width: 70, align: "right" },
    { key: "consecutive_days", header: "연속일", width: 60, align: "right" },
  ];

  const comboCols: Column<CombinationAnalysis>[] = [
    { key: "combination_key", header: "조합키" },
    { key: "supplier_code", header: "업체코드", width: 80 },
    { key: "occurrence_rate", header: "발생률", width: 70, align: "right", render: (r) => `${(r.occurrence_rate * 100).toFixed(1)}%` },
    { key: "avg_quantity", header: "평균수량", width: 80, align: "right" },
    { key: "repetition_rate", header: "반복률", width: 70, align: "right", render: (r) => `${(r.repetition_rate * 100).toFixed(1)}%` },
    { key: "total_occurrences", header: "총 발생", width: 70, align: "right" },
  ];

  return (
    <div>
      <PageHeader title="분석" description="반복 SKU 및 조합 분석을 실행하고 결과를 확인합니다." />

      <Card>
        <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
          <label style={{ fontSize: 13 }}>
            분석일: <input type="date" value={date} onChange={(e) => setDate(e.target.value)} style={inputStyle} />
          </label>
          <label style={{ fontSize: 13 }}>
            업체코드: <input value={supplier} onChange={(e) => setSupplier(e.target.value)} placeholder="전체" style={inputStyle} />
          </label>
          <Button onClick={runAnalysis} disabled={loading}>{loading ? "분석 중..." : "분석 실행"}</Button>
          <Button variant="secondary" onClick={loadData}>조회</Button>
        </div>
      </Card>

      <div style={{ display: "flex", gap: 8, margin: "16px 0" }}>
        <Button variant={tab === "sku" ? "primary" : "secondary"} size="sm" onClick={() => setTab("sku")}>
          SKU 분석 ({skuData.length})
        </Button>
        <Button variant={tab === "combo" ? "primary" : "secondary"} size="sm" onClick={() => setTab("combo")}>
          조합 분석 ({comboData.length})
        </Button>
      </div>

      {tab === "sku" ? (
        <Card title="SKU별 분석 결과">
          <Table columns={skuCols} data={skuData} />
        </Card>
      ) : (
        <Card title="조합별 분석 결과">
          <Table columns={comboCols} data={comboData} />
        </Card>
      )}
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
