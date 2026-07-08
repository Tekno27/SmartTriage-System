import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import AppIcon from "../components/AppIcon";
import QueueTicket from "../components/QueueTicket";
import { visitsApi } from "../api/client";

export default function StudentStatus() {
  const [visit, setVisit] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = () => visitsApi.myVisit().then((res) => setVisit(res.data.visit)).finally(() => setLoading(false));
    load();
    const interval = setInterval(load, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <AppShell title="My Queue Status" subtitle="Track your visit">
      {loading ? (
        <p className="muted">Loading…</p>
      ) : visit ? (
        <QueueTicket visit={visit} />
      ) : (
        <div className="empty-state">
          <span className="empty-icon"><AppIcon name="ticket" size={40} /></span>
          <h2>No active visit</h2>
          <p className="muted">You haven't checked in yet. Head to Check In to get started.</p>
        </div>
      )}
    </AppShell>
  );
}
