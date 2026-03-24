import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import DashboardPage from "./pages/Dashboard";
import UploadPage from "./pages/Upload";
import AnalysisPage from "./pages/Analysis";
import RecommendationPage from "./pages/Recommendation";
import LocationPage from "./pages/Location";
import PrintPage from "./pages/Print";
import ReportPage from "./pages/Report";
import BacktestPage from "./pages/Backtest";
import ProfilePage from "./pages/Profile";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/recommendation" element={<RecommendationPage />} />
          <Route path="/location" element={<LocationPage />} />
          <Route path="/print" element={<PrintPage />} />
          <Route path="/report" element={<ReportPage />} />
          <Route path="/backtest" element={<BacktestPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
