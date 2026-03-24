import { useState } from "react";
import PageHeader from "../../components/PageHeader";
import Button from "../../components/Button";
import Card from "../../components/Card";
import Table, { type Column } from "../../components/Table";
import StatusBadge from "../../components/StatusBadge";
import { rulesApi, recommendationApi, llmApi } from "../../api";
import type { Recommendation } from "../../types";

export default function RecommendationPage() {
  const [date, setDate] = useState("");
  const [supplier, setSupplier] = useState("");
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState<Set<number>>(new Set());

  const generate = async () => {
    setLoading(true);
    try {
      const r = await rulesApi.generate(date || undefined, supplier || undefined);
      setRecs(r.data);
    } catch {
      alert("추천 생성 실패");
    } finally {
      setLoading(false);
    }
  };

  const load = async () => {
    const r = await recommendationApi.list({
      target_date: date || undefined,
      supplier_code: supplier || undefined,
    });
    setRecs(r.data);
  };

  const handleApprove = async (id: number, action: string) => {
    const qty = action === "modified" ? prompt("수정 수량을 입력하세요:") : null;
    const memo = prompt("메모 (선택):") || undefined;
    try {
      await recommendationApi.approve(id, {
        action,
        approved_qty: qty ? parseInt(qty) : undefined,
        memo,
      });
      load();
    } catch (e: unknown) {
      alert((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "처리 실패");
    }
  };

  const handleExecute = async (id: number) => {
    const qty = prompt("실제 포장 수량을 입력하세요:");
    if (!qty) return;
    try {
      await recommendationApi.execute(id, parseInt(qty));
      load();
    } catch (e: unknown) {
      alert((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "실행 실패");
    }
  };

  const handleLLMReview = async () => {
    const ids = Array.from(selected);
    if (ids.length === 0) { alert("추천을 선택하세요."); return; }
    try {
      await llmApi.review(ids, "light");
      alert("LLM 검증 완료");
      load();
    } catch {
      alert("LLM 검증 실패");
    }
  };

  const toggleSelect = (id: number) => {
    setSelected((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const cols: Column<Recommendation>[] = [
    {
      key: "select",
      header: "",
      width: 30,
      render: (r) => (
        <input type="checkbox" checked={selected.has(r.id)} onChange={() => toggleSelect(r.id)} />
      ),
    },
    { key: "id", header: "ID", width: 50 },
    { key: "target_date", header: "대상일", width: 100 },
    { key: "supplier_code", header: "업체", width: 70 },
    { key: "target_type", header: "구분", width: 60 },
    { key: "target_key", header: "대상" },
    { key: "rule_based_qty", header: "규칙기반", width: 70, align: "right" },
    { key: "dl_predicted_qty", header: "DL예측", width: 60, align: "right", render: (r) => r.dl_predicted_qty ?? "-" },
    { key: "final_recommended_qty", header: "최종추천", width: 70, align: "right" },
    { key: "risk_level", header: "위험도", width: 60, render: (r) => r.risk_level ? <StatusBadge status={r.risk_level} /> : "-" },
    { key: "status", header: "상태", width: 80, render: (r) => <StatusBadge status={r.status} /> },
    { key: "llm_review_result", header: "LLM", width: 70, render: (r) => r.llm_review_result || "-" },
    {
      key: "actions",
      header: "작업",
      width: 200,
      render: (r) => (
        <div style={{ display: "flex", gap: 4 }}>
          {r.status === "pending" || r.status === "llm_reviewed" ? (
            <>
              <Button size="sm" onClick={() => handleApprove(r.id, "approved")}>승인</Button>
              <Button size="sm" variant="secondary" onClick={() => handleApprove(r.id, "modified")}>수정</Button>
              <Button size="sm" variant="danger" onClick={() => handleApprove(r.id, "rejected")}>거절</Button>
            </>
          ) : r.status === "approved" ? (
            <Button size="sm" onClick={() => handleExecute(r.id)}>실행</Button>
          ) : null}
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader title="추천 / 승인 / 실행" description="추천 목록을 확인하고 승인/수정/거절 후 실행합니다." />

      <Card>
        <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
          <label style={{ fontSize: 13 }}>
            대상일: <input type="date" value={date} onChange={(e) => setDate(e.target.value)} style={inputStyle} />
          </label>
          <label style={{ fontSize: 13 }}>
            업체: <input value={supplier} onChange={(e) => setSupplier(e.target.value)} placeholder="전체" style={inputStyle} />
          </label>
          <Button onClick={generate} disabled={loading}>{loading ? "생성 중..." : "추천 생성"}</Button>
          <Button variant="secondary" onClick={load}>조회</Button>
          <Button variant="ghost" onClick={handleLLMReview}>LLM 검증</Button>
        </div>
      </Card>

      <Card style={{ marginTop: 16 }} title={`추천 목록 (${recs.length}건)`}>
        <Table columns={cols} data={recs} />
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
