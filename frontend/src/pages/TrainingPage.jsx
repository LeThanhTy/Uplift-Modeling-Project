import { useState } from "react";
import { trainModel } from "../services/api";
import LoadingSpinner from "../components/LoadingSpinner";

function TrainingPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleTrain = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await trainModel("t_learner");
      setResult(res.data.data);
    } catch (error) {
      setError("Model training failed. Please check your data and try again.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const renderResultTable = (data) => {
    if (!data || typeof data !== 'object') {
      return <p style={{ color: '#666' }}>No data to display</p>;
    }

    const isArray = Array.isArray(data);
    const items = isArray ? data : Object.entries(data);

    if (isArray && data.length > 0 && typeof data[0] === 'object') {
      const columns = Object.keys(data[0]);
      return (
        <table className="data-table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx}>
                {columns.map((col) => (
                  <td key={`${idx}-${col}`}>
                    {typeof row[col] === 'object' 
                      ? JSON.stringify(row[col]) 
                      : String(row[col])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      );
    }

    return (
      <table className="data-table">
        <thead>
          <tr>
            <th>Property</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {items.map(([key, value], idx) => (
            <tr key={idx}>
              <td>{key}</td>
              <td>
                {typeof value === 'object' 
                  ? JSON.stringify(value) 
                  : String(value)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div className="training-page-container">
      <div className="training-content">
        <div className="training-header">
          <h1 style={{ color: '#000', marginBottom: '8px' }}>🎓 Model Training</h1>
          <p style={{ color: '#666666', margin: 0 }}>Train T-Learner uplift model with your data</p>
        </div>

        <div className="training-card">
          <div className="training-info">
            <h3 style={{ color: '#000', marginTop: 0 }}>T-Learner Model</h3>
            <p style={{ color: '#666666', fontSize: '14px', marginBottom: '20px' }}>
              T-Learner (Two-Learner) trains separate models for treated and control groups, 
              enabling precise uplift estimation through targeted treatment effect analysis.
            </p>
          </div>

          <button 
            onClick={handleTrain} 
            disabled={loading}
            className="train-button"
            style={{
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? '⏳ Training in progress...' : '🚀 Start Training'}
          </button>
        </div>

        {loading && (
          <div className="loading-section">
            <LoadingSpinner />
            <p style={{ color: '#666666', textAlign: 'center', marginTop: '16px' }}>
              Training model... This may take a few moments
            </p>
          </div>
        )}

        {error && (
          <div className="alert-error" style={{ marginTop: '24px' }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && !loading && (
          <div className="result-section">
            <h2 style={{ color: '#000', marginBottom: '24px' }}>✅ Training Results</h2>
            <div className="result-card">
              {renderResultTable(result)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default TrainingPage;