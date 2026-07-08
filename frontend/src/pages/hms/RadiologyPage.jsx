import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import DataTable from "../../components/DataTable";
import StatCard from "../../components/StatCard";
import { radiologyApi } from "../../api/client";

export default function RadiologyPage() {
  const [orders, setOrders] = useState([]);
  const [types, setTypes] = useState([]);

  useEffect(() => {
    radiologyApi.orders().then((r) => setOrders(r.data));
    radiologyApi.types().then((r) => setTypes(r.data));
  }, []);

  const pending = orders.filter((o) => o.status !== "completed").length;

  const columns = [
    { key: "id", label: "Order #" },
    { key: "patient", label: "Patient", render: (r) => r.patient?.full_name },
    { key: "imaging_type", label: "Study", render: (r) => r.imaging_type?.name },
    { key: "status", label: "Status", render: (r) => <span className={`status-pill ${r.status}`}>{r.status}</span> },
    { key: "ordered_at", label: "Ordered", render: (r) => new Date(r.ordered_at).toLocaleString() },
  ];

  return (
    <AppShell title="Radiology" subtitle="Medical imaging">
      <div className="stats-row compact">
        <StatCard label="Pending Studies" value={pending} icon="clock" />
        <StatCard label="Imaging Types" value={types.length} icon="radiology" />
      </div>
      <section className="panel">
        <h2>Imaging Orders</h2>
        <DataTable columns={columns} rows={orders} emptyMessage="No imaging orders." />
      </section>
      <section className="panel">
        <h2>Available Studies</h2>
        <div className="test-grid">
          {types.map((t) => (
            <div key={t.id} className="test-card">
              <strong>{t.code}</strong>
              <span>{t.name}</span>
              <span className="muted small">{t.modality} · GHS {t.price}</span>
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
