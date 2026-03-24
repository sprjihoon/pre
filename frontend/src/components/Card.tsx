interface Props {
  title?: string;
  children: React.ReactNode;
  style?: React.CSSProperties;
}

export default function Card({ title, children, style }: Props) {
  return (
    <div
      style={{
        border: "1px solid #e0e0e0",
        borderRadius: 12,
        padding: 20,
        background: "#fff",
        ...style,
      }}
    >
      {title && (
        <h3 style={{ fontSize: 15, fontWeight: 600, margin: "0 0 14px", color: "#333" }}>
          {title}
        </h3>
      )}
      {children}
    </div>
  );
}
