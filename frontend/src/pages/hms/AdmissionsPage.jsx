import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import DataTable from "../../components/DataTable";
import StatCard from "../../components/StatCard";
import { admissionsApi } from "../../api/client";

export default function AdmissionsPage() {
  const [admissions, setAdmissions] = useState([]);

  useEffect(() => {
    admissionsApi.list().then((r) => setAdmissions(r.data));
  }, []);

  const active = admissions.filter((a) => a.status === "admitted").length;

  const columns = [
    { key: "patient", label: "Patient", render: (r) => r.patient?.full_name },
    { key: "ward", label: "Ward", render: (r) => r.ward?.name },
    { key: "bed", label: "Bed", render: (r) => r.bed?.bed_number },
    { key: "diagnosis", label: "Diagnosis", render: (r) => r.diagnosis_on_admission?.slice(0, 40) },
    { key: "admitted_at", label: "Admitted", render: (r) => new Date(r.admitted_at).toLocaleDateString() },
    { key: "status", label: "Status", render: (r) => <span className={`status-pill ${r.status}`}>{r.status}</span> },
  ];

  return (
    <AppShell title="Admissions" subtitle="Inpatient management">
      <div className="stats-row compact">
        <StatCard label="Currently Admitted" value={active} icon="bed" />
        <StatCard label="Total Records" value={admissions.length} icon="clipboard" />
      </div>
      <section className="panel">
        <DataTable columns={columns} rows={admissions} emptyMessage="No admissions recorded." />
      </section>
    </AppShell>
  );
}
