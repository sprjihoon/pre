interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  size?: "sm" | "md";
}

const VARIANTS: Record<string, React.CSSProperties> = {
  primary: { background: "#1a73e8", color: "#fff", border: "none" },
  secondary: { background: "#f1f3f4", color: "#333", border: "1px solid #dadce0" },
  danger: { background: "#d93025", color: "#fff", border: "none" },
  ghost: { background: "transparent", color: "#1a73e8", border: "none" },
};

export default function Button({ variant = "primary", size = "md", style, ...props }: Props) {
  const v = VARIANTS[variant];
  return (
    <button
      style={{
        ...v,
        padding: size === "sm" ? "6px 12px" : "8px 18px",
        borderRadius: 8,
        fontSize: size === "sm" ? 12 : 14,
        fontWeight: 500,
        cursor: props.disabled ? "not-allowed" : "pointer",
        opacity: props.disabled ? 0.5 : 1,
        transition: "opacity 0.15s",
        fontFamily: "inherit",
        ...style,
      }}
      {...props}
    />
  );
}
