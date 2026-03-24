import { useEffect, useState } from "react";
import PageHeader from "../../components/PageHeader";
import StatCard from "../../components/StatCard";
import Card from "../../components/Card";
import { dashboardApi } from "../../api";
import type { DashboardSummary } from "../../types";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    dashboardApi.summary().then((r) => setSummary(r.data)).catch(() => {});
  }, []);

  return (
    <div>
      <PageHeader title="대시보드" description="프리패킹 시스템 전체 현황" />

      <div style={{ display: "flex", gap: 16, marginBottom: 24, flexWrap: "wrap" }}>
        <StatCard label="활성 업로드 파일" value={summary?.active_uploads ?? "-"} />
        <StatCard label="전체 추천 건수" value={summary?.total_recommendations ?? "-"} color="#5f6368" />
        <StatCard label="승인 대기" value={summary?.pending_recommendations ?? "-"} color="#e37400" />
        <StatCard label="활성 재고" value={summary?.active_stocks ?? "-"} color="#1e8e3e" />
        <StatCard
          label="평균 정확도"
          value={summary ? `${(summary.avg_accuracy * 100).toFixed(1)}%` : "-"}
          color="#8430ce"
        />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <Card title="운영 흐름">
          <div style={{ fontSize: 13, lineHeight: 2, color: "#555" }}>
            <div>1. 배송통계 파일 업로드</div>
            <div>2. 데이터 파싱 및 누적 저장</div>
            <div>3. 반복 SKU/조합 분석 실행</div>
            <div>4. 규칙기반 추천값 생성</div>
            <div>5. (선택) 딥러닝 예측 + LLM 검증</div>
            <div>6. 추천 목록 → 승인 → 실행</div>
            <div>7. 작업 지시서 출력</div>
            <div>8. 로케이션 배정 / 재고 관리</div>
            <div>9. 검증 리포트 생성</div>
          </div>
        </Card>
        <Card title="시스템 정보">
          <div style={{ fontSize: 13, lineHeight: 2, color: "#555" }}>
            <div>백엔드: FastAPI + SQLAlchemy + PostgreSQL</div>
            <div>프론트엔드: React + TypeScript + Vite</div>
            <div>예측 엔진: 규칙기반 + PyTorch (LSTM/Transformer)</div>
            <div>검증 엔진: OpenAI GPT</div>
            <div>상태 관리: Zustand</div>
          </div>
        </Card>
      </div>
    </div>
  );
}
