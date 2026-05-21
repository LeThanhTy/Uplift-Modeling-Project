import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import DataPage from "./pages/DataPage";
import TrainingPage from "./pages/TrainingPage";
import PredictionPage from "./pages/PredictionPage";
import EvaluationPage from "./pages/EvaluationPage";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <div className="container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/data" element={<DataPage />} />
          <Route path="/training" element={<TrainingPage />} />
          <Route path="/prediction" element={<PredictionPage />} />
          <Route path="/evaluation" element={<EvaluationPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;