import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import DataTable from "../../components/DataTable";
import StatCard from "../../components/StatCard";
import { appointmentsApi, hospitalApi } from "../../api/client";

export default function ReceptionDashboard() {
  const [appointments, setAppointments] = useState([]);
  const [stats, setStats] = useState({});

  useEffect(() => {
    appointmentsApi.list().then((r) => setAppointments(r.data.slice(0, 10)));
    hospitalApi.overview().then((r) => setStats(r.data));
  }, []);

  const columns = [
    { key: "patient", label: "Patient", render: (r) => r.patient?.full_name },
    { key: "doctor", label: "Doctor", render: (r) => r.doctor?.full_name },
    { key: "scheduled_at", label: "Time", render: (r) => new Date(r.scheduled_at).toLocaleString() },
    { key: "status", label: "Status", render: (r) => <span className={`status-pill ${r.status}`}>{r.status}</span> },
  ];

  return (
    <AppShell title="Reception" subtitle="Front desk operations">
      <div className="stats-row compact">
        <StatCard label="Today's Appointments" value={stats.today_appointments || 0} icon="calendar" />
        <StatCard label="Active Visits" value={stats.active_visits || 0} icon="hospital" />
        <StatCard label="Available Beds" value={stats.available_beds || 0} icon="bed" />
        <StatCard label="Admissions" value={stats.active_admissions || 0} icon="wards" />
      </div>
      <section className="panel">
        <h2>Upcoming Appointments</h2>
        <DataTable columns={columns} rows={appointments} emptyMessage="No appointments scheduled." />
      </section>
    </AppShell>
  );
}
