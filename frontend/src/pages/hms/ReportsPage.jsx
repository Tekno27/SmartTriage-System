import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import StatCard from "../../components/StatCard";
import { hospitalApi } from "../../api/client";

export default function ReportsPage() {
  const [stats, setStats] = useState({});

  useEffect(() => {
    hospitalApi.overview().then((r) => setStats(r.data));
  }, []);

  const occupancy = stats.total_beds
    ? Math.round(((stats.occupied_beds || 0) / stats.total_beds) * 100)
    : 0;

  return (
    <AppShell title="Reports & Analytics" subtitle="Hospital performance metrics">
      <div className="stats-row">
        <StatCard label="Bed Occupancy" value={`${occupancy}%`} icon="wards" />
        <StatCard label="Departments" value={stats.departments || 0} icon="hospital" />
        <StatCard label="Active Visits" value={stats.active_visits || 0} icon="stethoscope" />
        <StatCard label="Completed Today" value={stats.completed_today || 0} icon="circleCheck" />
      </div>
      <div className="reports-grid">
        <section className="panel">
          <h3>Clinical Activity</h3>
          <ul className="report-list">
            <li><span>Active OPD Visits</span><strong>{stats.active_visits || 0}</strong></li>
            <li><span>Inpatient Admissions</span><strong>{stats.active_admissions || 0}</strong></li>
            <li><span>Scheduled Surgeries</span><strong>{stats.scheduled_surgeries || 0}</strong></li>
            <li><span>Today's Appointments</span><strong>{stats.today_appointments || 0}</strong></li>
          </ul>
        </section>
        <section className="panel">
          <h3>Diagnostics</h3>
          <ul className="report-list">
            <li><span>Pending Lab Orders</span><strong>{stats.pending_lab_orders || 0}</strong></li>
            <li><span>Pending Imaging</span><strong>{stats.pending_imaging || 0}</strong></li>
          </ul>
        </section>
        <section className="panel">
          <h3>Finance</h3>
          <ul className="report-list">
            <li><span>Pending Invoices</span><strong>{stats.pending_invoices || 0}</strong></li>
            <li><span>NHIS Claims Pending</span><strong>{stats.nhis_claims_pending || 0}</strong></li>
          </ul>
        </section>
        <section className="panel">
          <h3>Capacity</h3>
          <ul className="report-list">
            <li><span>Total Beds</span><strong>{stats.total_beds || 0}</strong></li>
            <li><span>Available Beds</span><strong>{stats.available_beds || 0}</strong></li>
            <li><span>Occupied Beds</span><strong>{stats.occupied_beds || 0}</strong></li>
            <li><span>Wards</span><strong>{stats.wards || 0}</strong></li>
          </ul>
        </section>
      </div>
    </AppShell>
  );
}
