import { useState } from "react";

import {
  generatePredictions,
} from "../services/api";

import MetricCard from "../components/MetricCard";
import LoadingSpinner from "../components/LoadingSpinner";

function PredictionPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    try {
      setLoading(true);

      const res = await generatePredictions();

      setResult(res.data.data);
    } catch (error) {
      console.error(error);
      alert("Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>🔮 Prediction Dashboard</h1>

      <p>Generate predictions for your dataset and analyze uplift values.</p>

      <button onClick={handlePredict} disabled={loading}>
        {loading ? '⏳ Generating...' : '✨ Generate Predictions'}
      </button>

      {loading && <LoadingSpinner />}

      {result && (
        <>
          <div className="metrics-grid">
            <MetricCard
              title="Predictions Count"
              value={result.predictions_count}
              icon="📊"
            />

            <MetricCard
              title="Mean Uplift"
              value={result.uplift_mean?.toFixed(4)}
              icon="📈"
            />

            <MetricCard
              title="Std Uplift"
              value={result.uplift_std?.toFixed(4)}
              icon="📉"
            />

            <MetricCard
              title="Min Uplift"
              value={result.uplift_min?.toFixed(4)}
              icon="🔽"
            />

            <MetricCard
              title="Max Uplift"
              value={result.uplift_max?.toFixed(4)}
              icon="🔼"
            />
          </div>

          <div className="prediction-result">
            <h2>📋 Prediction Summary</h2>

            <pre style={{ 
              background: '#f7fafc', 
              padding: '16px', 
              borderRadius: '8px', 
              overflow: 'auto',
              maxHeight: '500px'
            }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        </>
      )}
    </div>
  );
}

export default PredictionPage;