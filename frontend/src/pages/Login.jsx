import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import { useAuth } from "../context/AuthContext";

const ROLE_ROUTES = {
  student: "/student",
  nurse: "/nurse",
  doctor: "/doctor",
};

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
      navigate(ROLE_ROUTES[user.role] || "/");
    } catch {
      setError("Invalid credentials. Try student1 / nurse1 / doctor1 with password demo1234.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <section className="login-card">
        <h1>Welcome to SmartTriage</h1>
        <p className="muted">Sign in to access your clinic dashboard.</p>
        <form onSubmit={handleSubmit} className="stack-form">
          <label>
            Username
            <input value={username} onChange={(e) => setUsername(e.target.value)} required />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          {error && <p className="error">{error}</p>}
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>
        <div className="demo-hint">
          <p>Demo accounts:</p>
          <ul>
            <li><strong>student1</strong> — QR check-in & intake</li>
            <li><strong>nurse1</strong> — triage queue</li>
            <li><strong>doctor1</strong> — consultation console</li>
          </ul>
        </div>
      </section>
    </Layout>
  );
}
