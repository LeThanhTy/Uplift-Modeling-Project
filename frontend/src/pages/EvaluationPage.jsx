import { useState } from "react";

import {
  getMetrics,
  getQini,
} from "../services/api";

import QiniChart from "../components/QiniChart";
import MetricCard from "../components/MetricCard";
import LoadingSpinner from "../components/LoadingSpinner";

function EvaluationPage() {
  const [metrics, setMetrics] = useState(null);
  const [qini, setQini] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLoadEvaluation = async () => {
    try {
      setLoading(true);
      const metricsRes = await getMetrics();
      const qiniRes = await getQini();

      setMetrics(metricsRes.data.data);
      setQini(qiniRes.data.data);
    } catch (error) {
      console.error(error);
      alert(
        "❌ Please generate predictions first."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>📈 Model Evaluation</h1>

      <p>Analyze model performance with detailed metrics and visualizations.</p>

      <button onClick={handleLoadEvaluation} disabled={loading}>
        {loading ? '⏳ Loading...' : '📊 Load Evaluation'}
      </button>

      {loading && <LoadingSpinner />}

      {metrics && (
        <div className="metrics-grid">
          <MetricCard
            title="Qini Coefficient"
            value={metrics.qini_coefficient?.toFixed(4)}
            icon="🎯"
          />

          <MetricCard
            title="Uplift @ 10%"
            value={metrics.uplift_at_10?.toFixed(4)}
            icon="🚀"
          />

          <MetricCard
            title="AUUC"
            value={metrics.auuc?.toFixed(4) || "N/A"}
            icon="📊"
          />
        </div>
      )}

      {qini && (
        <div className="chart-container">
          <h3>📉 Qini Curve Analysis</h3>
          <QiniChart data={qini} />
        </div>
      )}
    </div>
  );
}

export default EvaluationPage;