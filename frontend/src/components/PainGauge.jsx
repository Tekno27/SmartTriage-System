import AppIcon from "./AppIcon";

const PAIN_LEVELS = [
  { max: 0, label: "No pain", color: "#6b8f8f", icon: "smile" },
  { max: 2, label: "Mild", color: "#4a9b6f", icon: "smile" },
  { max: 4, label: "Moderate", color: "#c9a227", icon: "meh" },
  { max: 6, label: "Uncomfortable", color: "#d4742a", icon: "meh" },
  { max: 8, label: "Severe", color: "#c0392b", icon: "frown" },
  { max: 10, label: "Worst pain", color: "#8b0000", icon: "frown" },
];

function getPainInfo(level) {
  return PAIN_LEVELS.find((p) => level <= p.max) || PAIN_LEVELS[PAIN_LEVELS.length - 1];
}

export default function PainGauge({ value, onChange, label = "How much pain are you in?" }) {
  const info = getPainInfo(Number(value));

  return (
    <div className="pain-gauge">
      <div className="pain-gauge-header">
        <span className="pain-label">{label}</span>
        <span className="pain-emoji" style={{ color: info.color }}>
          <AppIcon name={info.icon} size={24} />
        </span>
      </div>
      <div className="pain-scale">
        {Array.from({ length: 11 }, (_, i) => (
          <button
            key={i}
            type="button"
            className={`pain-dot ${Number(value) === i ? "active" : ""} ${i <= Number(value) ? "filled" : ""}`}
            style={{ "--dot-color": i <= Number(value) ? info.color : undefined }}
            onClick={() => onChange(i)}
            aria-label={`Pain level ${i}`}
          >
            {i}
          </button>
        ))}
      </div>
      <div className="pain-readout" style={{ color: info.color }}>
        <strong>{value}/10</strong> — {info.label}
      </div>
      <input
        type="range"
        min="0"
        max="10"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="pain-slider"
      />
    </div>
  );
}
