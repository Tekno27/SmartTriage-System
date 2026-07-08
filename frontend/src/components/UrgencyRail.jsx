const URGENCY_COLORS = {
  routine: "#6b8f8f",
  low: "#4a9b6f",
  moderate: "#c9a227",
  high: "#d4742a",
  critical: "#c0392b",
};

export default function UrgencyRail({ urgency = "routine" }) {
  return (
    <div
      className="urgency-rail"
      style={{ backgroundColor: URGENCY_COLORS[urgency] || URGENCY_COLORS.routine }}
      title={urgency}
    />
  );
}

export function UrgencyBadge({ urgency }) {
  return (
    <span className={`urgency-badge urgency-${urgency}`}>{urgency}</span>
  );
}
