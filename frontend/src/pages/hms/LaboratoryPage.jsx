import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import DataTable from "../../components/DataTable";
import StatCard from "../../components/StatCard";
import { laboratoryApi } from "../../api/client";

export default function LaboratoryPage() {
  const [orders, setOrders] = useState([]);
  const [tests, setTests] = useState([]);

  useEffect(() => {
    laboratoryApi.orders().then((r) => setOrders(r.data));
    laboratoryApi.tests().then((r) => setTests(r.data));
  }, []);

  const pending = orders.filter((o) => !["completed", "cancelled"].includes(o.status)).length;

  const columns = [
    { key: "id", label: "Order #" },
    { key: "patient", label: "Patient", render: (r) => r.patient?.full_name },
    { key: "priority", label: "Priority", render: (r) => <span className={`status-pill ${r.priority}`}>{r.priority}</span> },
    { key: "status", label: "Status", render: (r) => <span className={`status-pill ${r.status}`}>{r.status}</span> },
    { key: "items", label: "Tests", render: (r) => r.items?.map((i) => i.test?.code).join(", ") },
    { key: "ordered_at", label: "Ordered", render: (r) => new Date(r.ordered_at).toLocaleString() },
  ];

  return (
    <AppShell title="Laboratory" subtitle="Lab orders & results">
      <div className="stats-row compact">
        <StatCard label="Pending Orders" value={pending} icon="clock" />
        <StatCard label="Test Catalog" value={tests.length} icon="laboratory" />
        <StatCard label="Total Orders" value={orders.length} icon="clipboard" />
      </div>
      <section className="panel">
        <h2>Lab Orders</h2>
        <DataTable columns={columns} rows={orders} emptyMessage="No lab orders." />
      </section>
      <section className="panel">
        <h2>Available Tests</h2>
        <div className="test-grid">
          {tests.map((t) => (
            <div key={t.id} className="test-card">
              <strong>{t.code}</strong>
              <span>{t.name}</span>
              <span className="muted small">{t.category} · GHS {t.price}</span>
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
