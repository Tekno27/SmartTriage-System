import UrgencyRail, { UrgencyBadge } from "./UrgencyRail";

export default function PatientCard({ visit, onAction, actionLabel }) {
  const patient = visit.patient;

  return (
    <article className="patient-card">
      <UrgencyRail urgency={visit.urgency} />
      <div className="patient-card-body">
        <header className="patient-card-header">
          <div>
            <h3>{patient.full_name}</h3>
            <p className="muted">{patient.student_id || patient.username}</p>
          </div>
          <UrgencyBadge urgency={visit.urgency} />
        </header>
        <p className="complaint">{visit.chief_complaint}</p>
        <div className="patient-meta">
          <span>Score: {visit.triage_score}</span>
          <span>Status: {visit.status.replace(/_/g, " ")}</span>
        </div>
        {onAction && (
          <button className="btn btn-primary" onClick={() => onAction(visit)}>
            {actionLabel}
          </button>
        )}
      </div>
    </article>
  );
}
