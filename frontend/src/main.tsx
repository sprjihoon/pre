import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

const globalStyles = document.createElement("style");
globalStyles.textContent = `
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #f8f9fa;
    color: #1a1a1a;
    -webkit-font-smoothing: antialiased;
  }
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: #c1c1c1; border-radius: 3px; }
  input, select, textarea { font-family: inherit; }
`;
document.head.appendChild(globalStyles);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
