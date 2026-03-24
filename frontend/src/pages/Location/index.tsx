import { useEffect, useState } from "react";
import PageHeader from "../../components/PageHeader";
import Button from "../../components/Button";
import Card from "../../components/Card";
import Table, { type Column } from "../../components/Table";
import { locationApi, stockApi } from "../../api";
import type { LocationMaster, PrepackStock } from "../../types";

export default function LocationPage() {
  const [locations, setLocations] = useState<LocationMaster[]>([]);
  const [stocks, setStocks] = useState<PrepackStock[]>([]);
  const [tab, setTab] = useState<"loc" | "stock">("loc");

  const loadLocations = () => locationApi.list().then((r) => setLocations(r.data));
  const loadStocks = () => stockApi.list().then((r) => setStocks(r.data));

  useEffect(() => {
    loadLocations();
    loadStocks();
  }, []);

  const addLocation = async () => {
    const code = prompt("로케이션 코드:");
    if (!code) return;
    const zone = prompt("존(zone):") || undefined;
    const desc = prompt("설명:") || undefined;
    await locationApi.create({ location_code: code, zone, description: desc });
    loadLocations();
  };

  const handleAssign = async (locId: number) => {
    const key = prompt("대상 (SKU코드 또는 조합키):");
    if (!key) return;
    const type = prompt("구분 (sku / combination):", "sku") || "sku";
    const qty = prompt("수량:", "0");
    await locationApi.assign(locId, { target_key: key, target_type: type, quantity: parseInt(qty || "0") });
    loadLocations();
  };

  const handleClear = async (locId: number) => {
    await locationApi.clear(locId);
    loadLocations();
  };

  const handleUnwrap = async (stockId: number) => {
    const qty = prompt("해체 수량:");
    if (!qty) return;
    const reason = prompt("사유:") || undefined;
    try {
      await stockApi.unwrap({ stock_id: stockId, unwrap_qty: parseInt(qty), reason });
      loadStocks();
    } catch (e: unknown) {
      alert((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "해체 실패");
    }
  };

  const locCols: Column<LocationMaster>[] = [
    { key: "location_code", header: "코드", width: 100 },
    { key: "zone", header: "존", width: 60 },
    { key: "description", header: "설명" },
    { key: "current_sku", header: "현재 SKU" },
    { key: "current_combination", header: "현재 조합" },
    {
      key: "actions",
      header: "작업",
      width: 160,
      render: (r) => (
        <div style={{ display: "flex", gap: 4 }}>
          <Button size="sm" onClick={() => handleAssign(r.id)}>배정</Button>
          <Button size="sm" variant="secondary" onClick={() => handleClear(r.id)}>비우기</Button>
        </div>
      ),
    },
  ];

  const stockCols: Column<PrepackStock>[] = [
    { key: "id", header: "ID", width: 50 },
    { key: "target_type", header: "구분", width: 60 },
    { key: "target_key", header: "대상" },
    { key: "supplier_code", header: "업체", width: 80 },
    { key: "current_qty", header: "현재수량", width: 80, align: "right" },
    { key: "location_code", header: "로케이션", width: 80 },
    { key: "status", header: "상태", width: 80 },
    {
      key: "actions",
      header: "작업",
      width: 100,
      render: (r) => (
        <div style={{ display: "flex", gap: 4 }}>
          <Button size="sm" variant="danger" onClick={() => handleUnwrap(r.id)}>해체</Button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="로케이션 / 재고 / 해체"
        description="로케이션 관리, 선포장 재고 현황 및 해체 처리"
        actions={<Button onClick={addLocation}>로케이션 추가</Button>}
      />

      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <Button variant={tab === "loc" ? "primary" : "secondary"} size="sm" onClick={() => setTab("loc")}>로케이션</Button>
        <Button variant={tab === "stock" ? "primary" : "secondary"} size="sm" onClick={() => setTab("stock")}>재고</Button>
      </div>

      {tab === "loc" ? (
        <Card title="로케이션 목록">
          <Table columns={locCols} data={locations} />
        </Card>
      ) : (
        <Card title="선포장 재고">
          <Table columns={stockCols} data={stocks} />
        </Card>
      )}
    </div>
  );
}
