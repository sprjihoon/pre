import { useEffect, useState, useRef } from "react";
import PageHeader from "../../components/PageHeader";
import Button from "../../components/Button";
import Table, { type Column } from "../../components/Table";
import StatusBadge from "../../components/StatusBadge";
import Card from "../../components/Card";
import { uploadApi } from "../../api";
import type { UploadFile, UploadRecord } from "../../types";

export default function UploadPage() {
  const [files, setFiles] = useState<UploadFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<UploadFile | null>(null);
  const [records, setRecords] = useState<UploadRecord[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const loadFiles = () => {
    uploadApi.list(false).then((r) => setFiles(r.data));
  };

  useEffect(() => { loadFiles(); }, []);

  const handleUpload = async () => {
    const f = fileRef.current?.files?.[0];
    if (!f) return;
    setUploading(true);
    try {
      await uploadApi.upload(f);
      loadFiles();
      if (fileRef.current) fileRef.current.value = "";
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "업로드 실패";
      alert(msg);
    } finally {
      setUploading(false);
    }
  };

  const handleSelect = async (row: UploadFile) => {
    setSelectedFile(row);
    const r = await uploadApi.records(row.id);
    setRecords(r.data);
  };

  const fileCols: Column<UploadFile>[] = [
    { key: "id", header: "ID", width: 50, align: "center" },
    { key: "original_filename", header: "파일명" },
    { key: "file_type", header: "형식", width: 60, align: "center" },
    { key: "record_count", header: "레코드 수", width: 80, align: "right" },
    { key: "version", header: "버전", width: 50, align: "center" },
    {
      key: "date_range_start",
      header: "기간",
      render: (r) => `${r.date_range_start || ""} ~ ${r.date_range_end || ""}`,
    },
    {
      key: "status",
      header: "상태",
      width: 80,
      align: "center",
      render: (r) => <StatusBadge status={r.status} />,
    },
    {
      key: "uploaded_at",
      header: "업로드 일시",
      render: (r) => new Date(r.uploaded_at).toLocaleString("ko-KR"),
    },
  ];

  const recCols: Column<UploadRecord>[] = [
    { key: "order_date", header: "주문일", width: 100 },
    { key: "supplier_code", header: "업체코드", width: 80 },
    { key: "supplier_name", header: "업체명" },
    { key: "sku_code", header: "SKU코드", width: 100 },
    { key: "sku_name", header: "SKU명" },
    { key: "option_name", header: "옵션" },
    { key: "quantity", header: "수량", width: 60, align: "right" },
    { key: "combination_key", header: "조합키" },
  ];

  return (
    <div>
      <PageHeader
        title="업로드 관리"
        description="배송통계 파일을 업로드하고 파싱된 데이터를 확인합니다."
        actions={
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <input ref={fileRef} type="file" accept=".xlsx,.xls,.csv" style={{ fontSize: 13 }} />
            <Button onClick={handleUpload} disabled={uploading}>
              {uploading ? "업로드 중..." : "업로드"}
            </Button>
          </div>
        }
      />

      <Card title="업로드 이력">
        <Table columns={fileCols} data={files} onRowClick={handleSelect} />
      </Card>

      {selectedFile && (
        <Card title={`레코드 상세 - ${selectedFile.original_filename} (v${selectedFile.version})`} style={{ marginTop: 16 }}>
          <Table columns={recCols} data={records} />
        </Card>
      )}
    </div>
  );
}
