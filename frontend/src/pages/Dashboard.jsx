function Dashboard() {
  return (
    <div>
      <h1>📊 Uplift Modeling Dashboard</h1>

      <p>
        ✨ Advanced FastAPI + React dashboard for uplift modeling with real-time analytics
      </p>

      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Quick Start</h3>
          <p style={{ color: '#667eea', fontSize: '16px', marginTop: '8px' }}>
            → Upload data<br/>
            → Train model<br/>
            → Make predictions
          </p>
        </div>
        <div className="metric-card">
          <h3>Features</h3>
          <p style={{ color: '#667eea', fontSize: '16px', marginTop: '8px' }}>
            ✓ Data management<br/>
            ✓ Model training<br/>
            ✓ Performance evaluation
          </p>
        </div>
        <div className="metric-card">
          <h3>Status</h3>
          <p style={{ color: '#667eea', fontSize: '16px', marginTop: '8px' }}>
            🟢 System Online<br/>
            📡 Ready for input<br/>
            ⚡ High performance
          </p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;