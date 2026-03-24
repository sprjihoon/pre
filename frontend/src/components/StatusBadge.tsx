const STATUS_COLORS: Record<string, { bg: string; text: string }> = {
  active: { bg: "#e6f4ea", text: "#1e8e3e" },
  pending: { bg: "#fef7e0", text: "#e37400" },
  approved: { bg: "#e8f0fe", text: "#1a73e8" },
  rejected: { bg: "#fce8e6", text: "#d93025" },
  executed: { bg: "#e6f4ea", text: "#1e8e3e" },
  completed: { bg: "#e6f4ea", text: "#1e8e3e" },
  trained: { bg: "#e8f0fe", text: "#1a73e8" },
  llm_reviewed: { bg: "#f3e8fd", text: "#8430ce" },
  low: { bg: "#e6f4ea", text: "#1e8e3e" },
  medium: { bg: "#fef7e0", text: "#e37400" },
  high: { bg: "#fce8e6", text: "#d93025" },
};

interface Props {
  status: string;
}

export default function StatusBadge({ status }: Props) {
  const colors = STATUS_COLORS[status] || { bg: "#f1f3f4", text: "#666" };
  return (
    <span
      style={{
        display: "inline-block",
        padding: "3px 10px",
        borderRadius: 12,
        fontSize: 12,
        fontWeight: 500,
        background: colors.bg,
        color: colors.text,
      }}
    >
      {status}
    </span>
  );
}
