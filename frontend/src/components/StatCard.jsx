import AppIcon from "./AppIcon";

export default function StatCard({ label, value, icon, accent }) {
  return (
    <div className={`stat-card ${accent || ""}`}>
      <span className="stat-icon">{icon && <AppIcon name={icon} size={22} />}</span>
      <div>
        <span className="stat-value">{value}</span>
        <span className="stat-label">{label}</span>
      </div>
    </div>
  );
}
