function StatusCard({ title, status, icon = "📌" }) {
  return (
    <div className={`status-card ${status ? "completed" : "pending"}`}>
      <div style={{ fontSize: '24px', marginBottom: '8px' }}>{icon}</div>
      <h3>{title}</h3>

      <p style={{ color: status ? '#48bb78' : '#ed8936', fontWeight: '600' }}>
        {status ? "✅ Completed" : "⏳ Pending"}
      </p>
    </div>
  );
}

export default StatusCard;