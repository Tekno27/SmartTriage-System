import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import DataTable from "../../components/DataTable";
import { appointmentsApi } from "../../api/client";

export default function AppointmentsPage() {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    appointmentsApi.list().then((r) => setAppointments(r.data));
  }, []);

  const columns = [
    { key: "id", label: "#" },
    { key: "patient", label: "Patient", render: (r) => r.patient?.full_name },
    { key: "doctor", label: "Doctor", render: (r) => `Dr. ${r.doctor?.last_name}` },
    { key: "scheduled_at", label: "Date & Time", render: (r) => new Date(r.scheduled_at).toLocaleString() },
    { key: "reason", label: "Reason" },
    { key: "status", label: "Status", render: (r) => <span className={`status-pill ${r.status}`}>{r.status}</span> },
  ];

  return (
    <AppShell title="Appointments" subtitle="Schedule & manage appointments">
      <section className="panel">
        <DataTable columns={columns} rows={appointments} emptyMessage="No appointments found." />
      </section>
    </AppShell>
  );
}
