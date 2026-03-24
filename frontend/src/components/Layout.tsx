import { NavLink, Outlet } from "react-router-dom";

const NAV_ITEMS = [
  { to: "/", label: "대시보드", icon: "📊" },
  { to: "/upload", label: "업로드", icon: "📁" },
  { to: "/analysis", label: "분석", icon: "🔍" },
  { to: "/recommendation", label: "추천/승인", icon: "✅" },
  { to: "/location", label: "로케이션", icon: "📍" },
  { to: "/print", label: "지시서", icon: "🖨️" },
  { to: "/report", label: "리포트", icon: "📈" },
  { to: "/backtest", label: "백테스트", icon: "🧪" },
  { to: "/profile", label: "프로파일", icon: "⚙️" },
];

export default function Layout() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside style={sidebarStyle}>
        <div style={logoStyle}>
          <span style={{ fontSize: 20 }}>📦</span>
          <span style={{ fontWeight: 700, fontSize: 16 }}>프리패킹</span>
        </div>
        <nav style={{ display: "flex", flexDirection: "column", gap: 2 }}>
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              style={({ isActive }) => ({
                ...navLinkStyle,
                background: isActive ? "#e8f0fe" : "transparent",
                color: isActive ? "#1a73e8" : "#444",
                fontWeight: isActive ? 600 : 400,
              })}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>
      <main style={mainStyle}>
        <Outlet />
      </main>
    </div>
  );
}

const sidebarStyle: React.CSSProperties = {
  width: 220,
  background: "#fafbfc",
  borderRight: "1px solid #e0e0e0",
  padding: "16px 8px",
  display: "flex",
  flexDirection: "column",
  gap: 8,
  flexShrink: 0,
};

const logoStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: 8,
  padding: "8px 12px",
  marginBottom: 16,
};

const navLinkStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: 10,
  padding: "10px 14px",
  borderRadius: 8,
  textDecoration: "none",
  fontSize: 14,
  transition: "background 0.15s",
};

const mainStyle: React.CSSProperties = {
  flex: 1,
  padding: "24px 32px",
  background: "#fff",
  overflowY: "auto",
};
