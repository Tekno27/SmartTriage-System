import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import DataTable from "../../components/DataTable";
import StatCard from "../../components/StatCard";
import { pharmacyApi } from "../../api/client";

export default function PharmacyPage() {
  const [medications, setMedications] = useState([]);
  const [prescriptions, setPrescriptions] = useState([]);
  const [batches, setBatches] = useState([]);

  useEffect(() => {
    pharmacyApi.medications().then((r) => setMedications(r.data));
    pharmacyApi.prescriptions().then((r) => setPrescriptions(r.data));
    pharmacyApi.batches().then((r) => setBatches(r.data));
  }, []);

  const pending = prescriptions.filter((p) => !p.is_dispensed).length;

  const columns = [
    { key: "medication", label: "Medication", render: (r) => r.medication?.name },
    { key: "quantity", label: "Qty", render: (r) => r.quantity_prescribed },
    { key: "status", label: "Status", render: (r) => r.is_dispensed ? "Dispensed" : "Pending" },
    { key: "date", label: "Date", render: (r) => new Date(r.created_at).toLocaleDateString() },
  ];

  return (
    <AppShell title="Pharmacy" subtitle="FEFO medication dispensing">
      <div className="stats-row compact">
        <StatCard label="Pending Rx" value={pending} icon="pharmacy" />
        <StatCard label="Medications" value={medications.length} icon="clipboard" />
        <StatCard label="Batches" value={batches.length} icon="inventory" />
      </div>
      <section className="panel">
        <h2>Prescriptions</h2>
        <DataTable columns={columns} rows={prescriptions} emptyMessage="No prescriptions." />
      </section>
      <section className="panel">
        <h2>Inventory (FEFO)</h2>
        <DataTable
          columns={[
            { key: "med", label: "Medication", render: (r) => r.medication?.name },
            { key: "batch", label: "Batch", render: (r) => r.batch_number },
            { key: "qty", label: "Qty", render: (r) => r.quantity_on_hand },
            { key: "exp", label: "Expiry", render: (r) => r.expiry_date },
          ]}
          rows={batches}
          emptyMessage="No stock."
        />
      </section>
    </AppShell>
  );
}
