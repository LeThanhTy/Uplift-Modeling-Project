import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <div>
        <h2>🚀 Uplift Modeling</h2>
      </div>

      <div className="nav-links">
        <Link to="/">📊 Dashboard</Link>
        <Link to="/data">📁 Data</Link>
        <Link to="/training">🎓 Training</Link>
        <Link to="/prediction">🔮 Prediction</Link>
        <Link to="/evaluation">📈 Evaluation</Link>
      </div>
    </nav>
  );
}

export default Navbar;