import { useState } from "react";
import {
  loadData,
  exploreData,
  preprocessData,
} from "../services/api";

function DataPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLoad = async () => {
    setLoading(true);
    try {
      const res = await loadData();
      setResult(res.data.data);
    } catch (error) {
      alert("Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  const handleExplore = async () => {
    setLoading(true);
    try {
      const res = await exploreData();
      setResult(res.data.data);
    } catch (error) {
      alert("Failed to explore data");
    } finally {
      setLoading(false);
    }
  };

  const handlePreprocess = async () => {
    setLoading(true);
    try {
      const res = await preprocessData();
      console.log(res.data.data);
      setResult(res.data.data);
    } catch (error) {
      alert("Failed to preprocess data");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>📁 Data Processing</h1>

      <p>Upload, explore, and preprocess your data for model training.</p>

      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '24px' }}>
        <button onClick={handleLoad} disabled={loading}>
          {loading ? '⏳ Processing...' : '📥 Load Data'}
        </button>

        <button onClick={handleExplore} disabled={loading}>
          {loading ? '⏳ Processing...' : '🔍 Explore Data'}
        </button>

        <button onClick={handlePreprocess} disabled={loading}>
          {loading ? '⏳ Processing...' : '⚙️ Preprocess'}
        </button>
      </div>

      {result && (
        <div className="chart-container">
          <h3>📊 Result</h3>
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
      )}

      {result && result['data'] != null && (
        <div className="chart-container">
          <h3>📊 Result 20 First Rows</h3>

          {/* TABLE */}
          <div
            style={{
              overflowX: "auto",
              border: "1px solid #e2e8f0",
              borderRadius: "12px",
              marginTop: "20px",
            }}
          >
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                minWidth: "1200px",
              }}
            >
              <thead
                style={{
                  background: "#0f172a",
                  color: "white",
                }}
              >
                <tr>
                  {Object.keys(result['data'][0]).map((key) => (
                    <th
                      key={key}
                      style={{
                        padding: "12px",
                        textAlign: "left",
                        borderBottom: "1px solid #334155",
                      }}
                    >
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {result['data'].map((row, rowIndex) => (
                  <tr
                    key={rowIndex}
                    style={{
                      background:
                        rowIndex % 2 === 0
                          ? "#ffffff"
                          : "#f8fafc",
                    }}
                  >
                    {Object.values(row).map((value, colIndex) => (
                      <td
                        key={colIndex}
                        style={{
                          padding: "10px 12px",
                          borderBottom: "1px solid #e2e8f0",
                          fontSize: "14px",
                        }}
                      >
                        {String(value)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default DataPage;