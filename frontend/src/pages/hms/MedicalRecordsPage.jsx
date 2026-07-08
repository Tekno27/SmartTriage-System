import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import DataTable from "../../components/DataTable";
import { recordsApi } from "../../api/client";

export default function MedicalRecordsPage() {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    recordsApi.list().then((r) => setRecords(r.data));
  }, []);

  const columns = [
    { key: "title", label: "Title" },
    { key: "type", label: "Type", render: (r) => <span className="badge">{r.record_type}</span> },
    { key: "patient", label: "Patient", render: (r) => r.patient?.full_name },
    { key: "author", label: "Created By", render: (r) => r.created_by_name },
    { key: "date", label: "Date", render: (r) => new Date(r.created_at).toLocaleDateString() },
  ];

  return (
    <AppShell title="Medical Records" subtitle="Patient health records (EMR)">
      <section className="panel">
        <DataTable columns={columns} rows={records} emptyMessage="No records found." />
      </section>
      {records.map((r) => (
        <div key={r.id} className="panel record-detail">
          <h3>{r.title}</h3>
          <p className="muted small">{r.record_type} · {r.created_by_name} · {new Date(r.created_at).toLocaleString()}</p>
          <p>{r.summary}</p>
        </div>
      ))}
    </AppShell>
  );
}
