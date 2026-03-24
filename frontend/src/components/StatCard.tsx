interface Props {
  label: string;
  value: string | number;
  sub?: string;
  color?: string;
}

export default function StatCard({ label, value, sub, color = "#1a73e8" }: Props) {
  return (
    <div
      style={{
        border: "1px solid #e0e0e0",
        borderRadius: 12,
        padding: "18px 22px",
        minWidth: 160,
        flex: 1,
      }}
    >
      <div style={{ fontSize: 12, color: "#888", marginBottom: 6 }}>{label}</div>
      <div style={{ fontSize: 26, fontWeight: 700, color }}>{value}</div>
      {sub && <div style={{ fontSize: 12, color: "#999", marginTop: 4 }}>{sub}</div>}
    </div>
  );
}
