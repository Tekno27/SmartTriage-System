import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import StatCard from "../../components/StatCard";
import { hospitalApi, admissionsApi } from "../../api/client";

export default function TheatrePage() {
  const [theatres, setTheatres] = useState([]);
  const [surgeries, setSurgeries] = useState([]);

  useEffect(() => {
    hospitalApi.theatres().then((r) => setTheatres(r.data));
    admissionsApi.surgeries().then((r) => setSurgeries(r.data));
  }, []);

  const scheduled = surgeries.filter((s) => s.status === "scheduled").length;

  return (
    <AppShell title="Operating Theatre" subtitle="Surgery scheduling">
      <div className="stats-row compact">
        <StatCard label="Theatres" value={theatres.length} icon="theatre" />
        <StatCard label="Scheduled" value={scheduled} icon="calendar" />
        <StatCard label="Total Surgeries" value={surgeries.length} icon="clipboard" />
      </div>
      <div className="two-column">
        <section className="panel">
          <h2>Theatres</h2>
          {theatres.map((t) => (
            <div key={t.id} className="theatre-row">
              <strong>{t.name}</strong>
              <span className={t.is_available ? "verified" : "error-text"}>{t.is_available ? "Available" : "In Use"}</span>
            </div>
          ))}
        </section>
        <section className="panel">
          <h2>Scheduled Surgeries</h2>
          {surgeries.length === 0 && <p className="muted">No surgeries scheduled.</p>}
          {surgeries.map((s) => (
            <div key={s.id} className="surgery-card">
              <strong>{s.procedure_name}</strong>
              <p className="muted small">{s.patient?.full_name} · {new Date(s.scheduled_at).toLocaleString()}</p>
              <span className={`status-pill ${s.status}`}>{s.status}</span>
            </div>
          ))}
        </section>
      </div>
    </AppShell>
  );
}
