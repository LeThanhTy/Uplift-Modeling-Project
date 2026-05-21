import Plot from "react-plotly.js";

function DecileChart({ data }) {
  const plotLayout = {
    title: {
      text: "📊 Decile Analysis",
      font: { size: 18, color: '#1a202c', family: 'Segoe UI' }
    },
    xaxis: {
      title: "Decile",
      gridcolor: '#e2e8f0',
    },
    yaxis: {
      title: "Uplift Values",
      gridcolor: '#e2e8f0',
    },
    width: 800,
    height: 400,
    plot_bgcolor: '#f7fafc',
    paper_bgcolor: 'white',
    margin: { l: 60, r: 40, t: 60, b: 60 }
  };

  return (
    <Plot
      data={[
        {
          x: data.deciles,
          y: data.uplift_values,
          type: "bar",
          marker: {
            color: '#764ba2',
            line: {
              color: '#667eea',
              width: 2
            }
          },
          name: 'Uplift'
        },
      ]}
      layout={plotLayout}
      config={{ responsive: true, displayModeBar: true }}
    />
  );
}

export default DecileChart;