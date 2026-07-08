import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { NAV_SECTIONS } from "../config/navigation";
import AppIcon from "./AppIcon";

export default function AppShell({ children, title, subtitle }) {
  const { user, logout } = useAuth();
  const location = useLocation();
  const sections = user ? NAV_SECTIONS[user.role] || [] : [];

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="topbar-left">
          <Link to={user ? `/${user.role === "admin" ? "admin" : user.role}` : "/"} className="brand-link">
            <span className="brand-logo"><AppIcon name="hospital" size={20} /></span>
            <div>
              <strong>SmartTriage HMS</strong>
              <span className="brand-sub">UCC Health Clinic</span>
            </div>
          </Link>
        </div>
        <div className="topbar-center">
          {title && <h1 className="topbar-title">{title}</h1>}
          {subtitle && <span className="topbar-subtitle">{subtitle}</span>}
        </div>
        <div className="topbar-right">
          {user && (
            <>
              <div className="user-chip">
                <span className="user-avatar">{user.first_name?.[0] || "?"}</span>
                <div>
                  <strong>{user.full_name}</strong>
                  <span className="role-tag">{user.role?.replace(/_/g, " ")}</span>
                </div>
              </div>
              <button className="btn btn-ghost-sm" onClick={logout}>Sign out</button>
            </>
          )}
        </div>
      </header>

      <div className="app-body">
        {user && (
          <aside className="sidebar">
            <nav className="sidebar-nav">
              {sections.map((section) => (
                <div key={section.section} className="nav-section">
                  <span className="nav-section-label">{section.section}</span>
                  {section.links.map((link) => (
                    <Link
                      key={link.to}
                      to={link.to}
                      className={`sidebar-link ${location.pathname === link.to ? "active" : ""}`}
                    >
                      <span className="sidebar-icon"><AppIcon name={link.icon} size={18} /></span>
                      {link.label}
                    </Link>
                  ))}
                </div>
              ))}
            </nav>
            <div className="sidebar-footer">
              <div className="ai-badge">
                <AppIcon name="sparkles" size={14} /> AI-assisted HMS
              </div>
            </div>
          </aside>
        )}
        <main className="main-content">{children}</main>
      </div>

      <footer className="bottombar">
        <span>SmartTriage HMS · University of Cape Coast</span>
        <span className="muted">Full Hospital Management System</span>
      </footer>
    </div>
  );
}
