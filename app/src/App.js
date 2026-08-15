import { Navigate, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import StartupSetup from "./pages/StartupSetup";
import StartupOverview from "./pages/StartupOverview";
import MarketingPlan from "./pages/MarketingPlan";
import MarketResearch from "./pages/MarketResearch";
import SWOTAnalysis from "./pages/SWOTAnalysis";
import "./App.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/startups/new" element={<StartupSetup />} />
      <Route path="/startups/:startupId" element={<StartupOverview />} />
      <Route path="/startups/:startupId/marketing-plan" element={<MarketingPlan />} />
      <Route path="/startups/:startupId/market-research" element={<MarketResearch />} />
      <Route path="/startups/:startupId/swot-analysis" element={<SWOTAnalysis />} />
      <Route path="/marketing-plan" element={<MarketingPlan />} />
      <Route path="/market-research" element={<MarketResearch />} />
      <Route path="/swot-analysis" element={<SWOTAnalysis />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
