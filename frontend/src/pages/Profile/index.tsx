import { useEffect, useState } from "react";
import PageHeader from "../../components/PageHeader";
import Button from "../../components/Button";
import Card from "../../components/Card";
import Table, { type Column } from "../../components/Table";
import { profileApi } from "../../api";
import type { SupplierProfile } from "../../types";

export default function ProfilePage() {
  const [profiles, setProfiles] = useState<SupplierProfile[]>([]);
  const [editing, setEditing] = useState<SupplierProfile | null>(null);

  const load = () => profileApi.list().then((r) => setProfiles(r.data));
  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    const code = prompt("업체코드:");
    const name = prompt("업체명:");
    if (!code || !name) return;
    await profileApi.create({ supplier_code: code, supplier_name: name });
    load();
  };

  const handleDelete = async (code: string) => {
    if (!confirm(`${code} 프로파일을 삭제하시겠습니까?`)) return;
    await profileApi.delete(code);
    load();
  };

  const handleSave = async () => {
    if (!editing) return;
    await profileApi.update(editing.supplier_code, editing);
    setEditing(null);
    load();
  };

  const cols: Column<SupplierProfile>[] = [
    { key: "supplier_code", header: "업체코드", width: 80 },
    { key: "supplier_name", header: "업체명" },
    { key: "min_prepack_qty", header: "최소수량", width: 70, align: "right" },
    { key: "recent_weight", header: "최근가중치", width: 80, align: "right" },
    { key: "weekday_weight", header: "요일가중치", width: 80, align: "right" },
    { key: "conservative_mode", header: "보수적", width: 60, align: "center", render: (r) => r.conservative_mode ? "✓" : "" },
    { key: "llm_review_level", header: "LLM수준", width: 70 },
    {
      key: "actions",
      header: "작업",
      width: 120,
      render: (r) => (
        <div style={{ display: "flex", gap: 4 }}>
          <Button size="sm" variant="secondary" onClick={() => setEditing({ ...r })}>수정</Button>
          <Button size="sm" variant="danger" onClick={() => handleDelete(r.supplier_code)}>삭제</Button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="업체별 프로파일"
        description="업체(공급처)별 프리패킹 설정을 관리합니다."
        actions={<Button onClick={handleCreate}>프로파일 추가</Button>}
      />

      <Card title="프로파일 목록">
        <Table columns={cols} data={profiles} />
      </Card>

      {editing && (
        <Card title={`프로파일 수정 - ${editing.supplier_code}`} style={{ marginTop: 16 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
            {([
              ["supplier_name", "업체명", "text"],
              ["min_prepack_qty", "최소수량", "number"],
              ["recent_weight", "최근가중치", "number"],
              ["weekday_weight", "요일가중치", "number"],
              ["new_sku_exclude_days", "신규SKU 제외일", "number"],
              ["overpredict_penalty", "과대예측 패널티", "number"],
              ["llm_review_level", "LLM 수준", "text"],
            ] as const).map(([key, label, type]) => (
              <label key={key} style={{ fontSize: 13 }}>
                {label}
                <input
                  type={type}
                  value={String(editing[key as keyof SupplierProfile] ?? "")}
                  onChange={(e) =>
                    setEditing({
                      ...editing,
                      [key]: type === "number" ? parseFloat(e.target.value) || 0 : e.target.value,
                    })
                  }
                  style={{ ...inputStyle, display: "block", width: "100%", marginTop: 4 }}
                />
              </label>
            ))}
            <label style={{ fontSize: 13, display: "flex", alignItems: "center", gap: 6 }}>
              <input
                type="checkbox"
                checked={editing.conservative_mode}
                onChange={(e) => setEditing({ ...editing, conservative_mode: e.target.checked })}
              />
              보수적 모드
            </label>
            <label style={{ fontSize: 13, display: "flex", alignItems: "center", gap: 6 }}>
              <input
                type="checkbox"
                checked={editing.combination_priority}
                onChange={(e) => setEditing({ ...editing, combination_priority: e.target.checked })}
              />
              조합 우선
            </label>
          </div>
          <div style={{ marginTop: 16, display: "flex", gap: 8 }}>
            <Button onClick={handleSave}>저장</Button>
            <Button variant="secondary" onClick={() => setEditing(null)}>취소</Button>
          </div>
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
