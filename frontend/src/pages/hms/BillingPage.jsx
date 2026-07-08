import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import DataTable from "../../components/DataTable";
import StatCard from "../../components/StatCard";
import { billingApi } from "../../api/client";

export default function BillingPage() {
  const [claims, setClaims] = useState([]);
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    billingApi.claims().then((r) => setClaims(r.data));
    billingApi.invoices().then((r) => setInvoices(r.data));
  }, []);

  const pendingClaims = claims.filter((c) => ["draft", "submitted"].includes(c.status)).length;
  const unpaid = invoices.filter((i) => !["paid", "cancelled"].includes(i.status)).length;

  return (
    <AppShell title="Billing & Finance" subtitle="Invoices, payments & NHIS claims">
      <div className="stats-row compact">
        <StatCard label="NHIS Claims" value={claims.length} icon="landmark" />
        <StatCard label="Pending Claims" value={pendingClaims} icon="clock" />
        <StatCard label="Invoices" value={invoices.length} icon="receipt" />
        <StatCard label="Unpaid" value={unpaid} icon="billing" />
      </div>
      <section className="panel">
        <h2>NHIS Claims</h2>
        <DataTable
          columns={[
            { key: "claim_number", label: "Claim #" },
            { key: "patient", label: "NHIS No.", render: (r) => r.patient_nhis_number },
            { key: "total", label: "Total", render: (r) => `GHS ${r.total_amount}` },
            { key: "coverage", label: "NHIS", render: (r) => `GHS ${r.nhis_coverage}` },
            { key: "copay", label: "Co-pay", render: (r) => `GHS ${r.patient_copay}` },
            { key: "status", label: "Status", render: (r) => <span className={`status-pill ${r.status}`}>{r.status}</span> },
          ]}
          rows={claims}
          emptyMessage="No NHIS claims."
        />
      </section>
      <section className="panel">
        <h2>Invoices</h2>
        <DataTable
          columns={[
            { key: "invoice_number", label: "Invoice #" },
            { key: "patient", label: "Patient", render: (r) => r.patient?.full_name },
            { key: "total", label: "Total", render: (r) => `GHS ${r.total}` },
            { key: "paid", label: "Paid", render: (r) => `GHS ${r.amount_paid}` },
            { key: "balance", label: "Balance", render: (r) => `GHS ${r.balance}` },
            { key: "status", label: "Status", render: (r) => <span className={`status-pill ${r.status}`}>{r.status}</span> },
          ]}
          rows={invoices}
          emptyMessage="No invoices."
        />
      </section>
    </AppShell>
  );
}
