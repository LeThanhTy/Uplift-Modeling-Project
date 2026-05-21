import Plot from "react-plotly.js";

function StrategyChart({ data }) {
  const plotLayout = {
    title: {
      text: "🎯 Strategy Comparison",
      font: { size: 18, color: '#1a202c', family: 'Segoe UI' }
    },
    xaxis: {
      title: "Strategy",
      gridcolor: '#e2e8f0',
    },
    yaxis: {
      title: "Gains",
      gridcolor: '#e2e8f0',
    },
    width: 800,
    height: 400,
    plot_bgcolor: '#f7fafc',
    paper_bgcolor: 'white',
    margin: { l: 60, r: 40, t: 60, b: 60 },
    padding: 20
  };

  return (
    <Plot
      data={[
        {
          x: data.strategies,
          y: data.gains,
          type: "bar",
          marker: {
            color: '#667eea',
            line: {
              color: '#764ba2',
              width: 2
            }
          },
          name: 'Gains'
        },
      ]}
      layout={plotLayout}
      config={{ responsive: true, displayModeBar: true }}
    />
  );
}

export default StrategyChart;