import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import StatCard from "../../components/StatCard";
import { hospitalApi } from "../../api/client";

export default function WardsPage() {
  const [wards, setWards] = useState([]);
  const [overview, setOverview] = useState({});

  useEffect(() => {
    hospitalApi.wards().then((r) => setWards(r.data));
    hospitalApi.overview().then((r) => setOverview(r.data));
  }, []);

  return (
    <AppShell title="Wards & Beds" subtitle="Bed occupancy management">
      <div className="stats-row compact">
        <StatCard label="Wards" value={overview.wards || 0} icon="wards" />
        <StatCard label="Total Beds" value={overview.total_beds || 0} icon="bed" />
        <StatCard label="Available" value={overview.available_beds || 0} icon="circleCheck" />
        <StatCard label="Occupied" value={overview.occupied_beds || 0} icon="alert" />
      </div>
      <div className="wards-grid">
        {wards.map((ward) => (
          <div key={ward.id} className="panel ward-card">
            <div className="ward-card-header">
              <h3>{ward.name}</h3>
              <span className="badge">{ward.ward_type}</span>
            </div>
            <p className="muted small">{ward.department_name} · Floor {ward.floor || "—"}</p>
            <div className="bed-bar">
              <div className="bed-bar-fill" style={{ width: `${ward.total_beds ? ((ward.total_beds - ward.available_beds) / ward.total_beds) * 100 : 0}%` }} />
            </div>
            <p className="bed-stats">{ward.available_beds} available / {ward.total_beds} total</p>
            <div className="bed-grid">
              {ward.beds?.map((bed) => (
                <span key={bed.id} className={`bed-chip ${bed.status}`}>{bed.bed_number}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </AppShell>
  );
}
