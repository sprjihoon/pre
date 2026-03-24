import { useEffect, useState } from "react";
import PageHeader from "../../components/PageHeader";
import Button from "../../components/Button";
import Card from "../../components/Card";
import Table, { type Column } from "../../components/Table";
import StatusBadge from "../../components/StatusBadge";
import { dlApi } from "../../api";
import type { DLModel, BacktestResult } from "../../types";

export default function BacktestPage() {
  const [models, setModels] = useState<DLModel[]>([]);
  const [backtests, setBacktests] = useState<BacktestResult[]>([]);
  const [selectedModel, setSelectedModel] = useState<DLModel | null>(null);
  const [training, setTraining] = useState(false);

  useEffect(() => {
    dlApi.models().then((r) => setModels(r.data));
  }, []);

  const handleTrain = async () => {
    const type = prompt("모델 타입 (lstm / transformer):", "lstm") || "lstm";
    setTraining(true);
    try {
      const r = await dlApi.train({ model_type: type, epochs: 50 });
      setModels((prev) => [r.data, ...prev]);
      alert("학습 완료");
    } catch (e: unknown) {
      alert((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "학습 실패");
    } finally {
      setTraining(false);
    }
  };

  const handleBacktest = async (modelId: number) => {
    const start = prompt("테스트 시작일 (YYYY-MM-DD):");
    const end = prompt("테스트 종료일 (YYYY-MM-DD):");
    if (!start || !end) return;
    try {
      await dlApi.backtest({ model_id: modelId, test_start: start, test_end: end });
      alert("백테스트 완료");
      loadBacktests(modelId);
    } catch (e: unknown) {
      alert((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "백테스트 실패");
    }
  };

  const handleActivate = async (modelId: number) => {
    try {
      await dlApi.activate(modelId);
      alert("모델 활성화 완료");
      dlApi.models().then((r) => setModels(r.data));
    } catch (e: unknown) {
      alert((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "활성화 실패");
    }
  };

  const loadBacktests = async (modelId: number) => {
    const r = await dlApi.backtests(modelId);
    setBacktests(r.data);
  };

  const modelCols: Column<DLModel>[] = [
    { key: "id", header: "ID", width: 50 },
    { key: "model_name", header: "모델명" },
    { key: "model_type", header: "타입", width: 80 },
    { key: "train_accuracy", header: "학습정확도", width: 90, align: "right", render: (r) => r.train_accuracy ? `${(r.train_accuracy * 100).toFixed(1)}%` : "-" },
    { key: "status", header: "상태", width: 80, render: (r) => <StatusBadge status={r.status} /> },
    { key: "trained_at", header: "학습일시", render: (r) => r.trained_at ? new Date(r.trained_at).toLocaleString("ko-KR") : "-" },
    {
      key: "actions",
      header: "작업",
      width: 200,
      render: (r) => (
        <div style={{ display: "flex", gap: 4 }}>
          <Button size="sm" variant="secondary" onClick={() => { setSelectedModel(r); loadBacktests(r.id); }}>백테스트 보기</Button>
          <Button size="sm" onClick={() => handleBacktest(r.id)}>백테스트</Button>
          {r.status !== "active" && <Button size="sm" variant="ghost" onClick={() => handleActivate(r.id)}>활성화</Button>}
        </div>
      ),
    },
  ];

  const btCols: Column<BacktestResult>[] = [
    { key: "id", header: "ID", width: 50 },
    { key: "test_start", header: "시작일", width: 100 },
    { key: "test_end", header: "종료일", width: 100 },
    { key: "sku_accuracy", header: "SKU정확도", width: 90, align: "right", render: (r) => `${(r.sku_accuracy * 100).toFixed(1)}%` },
    { key: "usage_rate", header: "사용률", width: 70, align: "right", render: (r) => `${(r.usage_rate * 100).toFixed(1)}%` },
    { key: "overpredict_rate", header: "과대예측", width: 70, align: "right", render: (r) => `${(r.overpredict_rate * 100).toFixed(1)}%` },
    { key: "underpredict_rate", header: "과소예측", width: 70, align: "right", render: (r) => `${(r.underpredict_rate * 100).toFixed(1)}%` },
  ];

  return (
    <div>
      <PageHeader
        title="딥러닝 / 백테스트"
        description="모델 학습, 백테스트 실행, 모델 활성화 관리"
        actions={<Button onClick={handleTrain} disabled={training}>{training ? "학습 중..." : "모델 학습"}</Button>}
      />

      <Card title="모델 목록">
        <Table columns={modelCols} data={models} />
      </Card>

      {selectedModel && (
        <Card title={`백테스트 결과 - ${selectedModel.model_name}`} style={{ marginTop: 16 }}>
          <Table columns={btCols} data={backtests} />
        </Card>
      )}
    </div>
  );
}
