import UrgencyRail, { UrgencyBadge } from "./UrgencyRail";

export default function PatientCard({ visit, onAction, actionLabel, active }) {
  const patient = visit.patient;

  return (
    <article className={`patient-card ${active ? "active" : ""}`}>
      <UrgencyRail urgency={visit.urgency} />
      <div className="patient-card-body">
        <header className="patient-card-header">
          <div>
            <div className="card-title-row">
              {visit.queue_number && <span className="queue-badge">{visit.queue_number}</span>}
              <h3>{patient.full_name}</h3>
            </div>
            <p className="muted">{patient.student_id || patient.username}</p>
          </div>
          <UrgencyBadge urgency={visit.urgency} />
        </header>
        {visit.chief_complaint && <p className="complaint">{visit.chief_complaint}</p>}
        <div className="patient-meta">
          <span>Score: {visit.triage_score}</span>
          <span>Pain: {visit.pain_level}/10</span>
          <span>{visit.status.replace(/_/g, " ")}</span>
        </div>
        {onAction && (
          <button className="btn btn-primary btn-sm" onClick={() => onAction(visit)}>
            {actionLabel}
          </button>
        )}
      </div>
    </article>
  );
}
