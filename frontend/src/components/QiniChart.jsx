import Plot from "react-plotly.js";

function QiniChart({ data }) {
  const plotLayout = {
    title: {
      text: "Qini Curve - Model Performance",
      font: { size: 18, color: '#1a202c', family: 'Segoe UI' }
    },
    xaxis: {
      title: "Customer Percentile",
      gridcolor: '#e2e8f0',
      showgrid: true,
      zeroline: false
    },
    yaxis: {
      title: "Cumulative Uplift",
      gridcolor: '#e2e8f0',
      showgrid: true,
      zeroline: false
    },
    width: 900,
    height: 500,
    plot_bgcolor: '#f7fafc',
    paper_bgcolor: 'white',
    hovermode: 'x unified',
    margin: { l: 60, r: 40, t: 60, b: 60 }
  };

  return (
    <Plot
      data={[
        {
          x: data.customers,
          y: data.uplift,
          type: "scatter",
          mode: "lines",
          name: "🎯 Uplift Model",
          line: {
            color: '#667eea',
            width: 3
          }
        },
        {
          x: data.customers,
          y: data.random,
          type: "scatter",
          mode: "lines",
          name: "📊 Random Baseline",
          line: {
            color: '#cbd5e0',
            width: 2,
            dash: 'dash'
          }
        },
      ]}
      layout={plotLayout}
      config={{ responsive: true, displayModeBar: true }}
    />
  );
}

export default QiniChart;