import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout({ children, title }) {
  const { user, logout } = useAuth();

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">
          <Link to="/">SmartTriage</Link>
          <span className="brand-sub">UCC Health Clinic</span>
        </div>
        {user && (
          <div className="header-actions">
            <span className="user-pill">
              {user.full_name} · {user.role}
            </span>
            <button className="btn btn-ghost" onClick={logout}>
              Sign out
            </button>
          </div>
        )}
      </header>
      <main className="app-main">
        {title && <h1 className="page-title">{title}</h1>}
        {children}
      </main>
    </div>
  );
}
