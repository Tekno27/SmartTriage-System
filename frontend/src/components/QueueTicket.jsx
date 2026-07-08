import { UrgencyBadge } from "./UrgencyRail";

export default function QueueTicket({ visit }) {
  if (!visit) return null;

  return (
    <div className="queue-ticket">
      <div className="ticket-header">
        <span className="ticket-label">Your Queue Number</span>
        <UrgencyBadge urgency={visit.urgency} />
      </div>
      <div className="ticket-number">{visit.queue_number || "—"}</div>
      <p className="ticket-message">
        Please wait in the waiting area. A nurse will call you for triage shortly.
      </p>
      <div className="ticket-details">
        <div><span>Pain level</span><strong>{visit.pain_level}/10</strong></div>
        <div><span>Priority</span><strong>{visit.urgency}</strong></div>
        <div><span>NHIS</span><strong>{visit.nhis_verified ? "Verified" : "Unverified"}</strong></div>
      </div>
    </div>
  );
}
