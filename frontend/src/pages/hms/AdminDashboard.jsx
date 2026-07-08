import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AppShell from "../../components/AppShell";
import StatCard from "../../components/StatCard";
import AppIcon from "../../components/AppIcon";
import client from "../../api/client";

const MODULES = [
  { to: "/nurse", icon: "stethoscope", label: "Triage", desc: "AI-assisted patient triage" },
  { to: "/doctor", icon: "doctor", label: "Consultations", desc: "Doctor console" },
  { to: "/reception", icon: "reception", label: "Reception", desc: "Front desk operations" },
  { to: "/appointments", icon: "calendar", label: "Appointments", desc: "Scheduling" },
  { to: "/admissions", icon: "bed", label: "Admissions", desc: "Inpatient management" },
  { to: "/wards", icon: "wards", label: "Wards & Beds", desc: "Bed occupancy" },
  { to: "/laboratory", icon: "laboratory", label: "Laboratory", desc: "Lab orders & results" },
  { to: "/radiology", icon: "radiology", label: "Radiology", desc: "Medical imaging" },
  { to: "/pharmacy", icon: "pharmacy", label: "Pharmacy", desc: "FEFO dispensing" },
  { to: "/inventory", icon: "inventory", label: "Inventory", desc: "Supplies & stock" },
  { to: "/billing", icon: "billing", label: "Billing", desc: "Invoices & NHIS" },
  { to: "/theatre", icon: "theatre", label: "Theatre", desc: "Surgery scheduling" },
  { to: "/records", icon: "records", label: "Records", desc: "Medical records" },
  { to: "/reports", icon: "reports", label: "Reports", desc: "Analytics" },
];

export default function AdminDashboard() {
  const [stats, setStats] = useState({});

  useEffect(() => {
    client.get("/hospital/overview/").then((r) => setStats(r.data));
  }, []);

  return (
    <AppShell title="Hospital Dashboard" subtitle="System-wide overview">
      <div className="stats-row">
        <StatCard label="Active Visits" value={stats.active_visits || 0} icon="hospital" />
        <StatCard label="Admissions" value={stats.active_admissions || 0} icon="bed" />
        <StatCard label="Available Beds" value={`${stats.available_beds || 0}/${stats.total_beds || 0}`} icon="wards" />
        <StatCard label="Pending Labs" value={stats.pending_lab_orders || 0} icon="laboratory" />
        <StatCard label="Pending Imaging" value={stats.pending_imaging || 0} icon="radiology" />
        <StatCard label="Appointments" value={stats.today_appointments || 0} icon="calendar" />
        <StatCard label="Surgeries" value={stats.scheduled_surgeries || 0} icon="theatre" />
        <StatCard label="NHIS Claims" value={stats.nhis_claims_pending || 0} icon="billing" />
      </div>

      <h2 className="section-heading">Hospital Modules</h2>
      <div className="module-grid">
        {MODULES.map((m) => (
          <Link key={m.to} to={m.to} className="module-card">
            <span className="module-icon"><AppIcon name={m.icon} size={28} /></span>
            <strong>{m.label}</strong>
            <span className="muted small">{m.desc}</span>
          </Link>
        ))}
      </div>
    </AppShell>
  );
}
