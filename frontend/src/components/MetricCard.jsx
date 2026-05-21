function MetricCard({ title, value, icon = "📊" }) {
  return (
    <div className="metric-card">
      <div style={{ fontSize: '28px', marginBottom: '8px' }}>{icon}</div>
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}

export default MetricCard;