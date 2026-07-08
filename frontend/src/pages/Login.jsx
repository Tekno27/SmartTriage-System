import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { ROLE_HOME } from "../config/navigation";
import AppIcon from "../components/AppIcon";

const DEMO_ACCOUNTS = [
  { label: "Student", username: "student1", icon: "student" },
  { label: "Nurse", username: "nurse1", icon: "stethoscope" },
  { label: "Doctor", username: "doctor1", icon: "doctor" },
  { label: "Admin", username: "admin1", icon: "hospital" },
  { label: "Reception", username: "reception1", icon: "reception" },
  { label: "Pharmacist", username: "pharmacist1", icon: "pharmacy" },
  { label: "Lab Tech", username: "labtech1", icon: "laboratory" },
  { label: "Radiologist", username: "radiologist1", icon: "radiology" },
  { label: "Accountant", username: "accountant1", icon: "billing" },
];

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("student1");
  const [password, setPassword] = useState("demo1234");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const user = await login(username, password);
      navigate(ROLE_HOME[user.role] || "/");
    } catch {
      setError("Invalid credentials. Try student1 / nurse1 / doctor1 — password demo1234.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-left">
        <Link to="/" className="brand-link">
          <span className="brand-logo"><AppIcon name="hospital" size={20} /></span>
          <div><strong>SmartTriage</strong><span className="brand-sub">UCC Health Clinic</span></div>
        </Link>
        <h1>Sign in to continue</h1>
        <p className="muted">Access your role-based dashboard with AI-assisted triage tools.</p>
      </div>
      <section className="login-card">
        <form onSubmit={handleSubmit} className="stack-form">
          <label>Username<input value={username} onChange={(e) => setUsername(e.target.value)} required /></label>
          <label>Password<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required /></label>
          {error && <p className="error">{error}</p>}
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>
        <div className="demo-hint">
          <p><strong>Demo accounts</strong> (password: demo1234)</p>
          <div className="demo-accounts">
            {DEMO_ACCOUNTS.map((a) => (
              <button key={a.username} type="button" className="demo-btn" onClick={() => { setUsername(a.username); setPassword("demo1234"); }}>
                <AppIcon name={a.icon} size={14} /> {a.label}
              </button>
            ))}
          </div>
        </div>
        <Link to="/" className="back-link">← Back to home</Link>
      </section>
    </div>
  );
}
