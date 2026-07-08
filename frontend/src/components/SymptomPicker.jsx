import { SymptomIcon } from "./AppIcon";

export default function SymptomPicker({ symptoms, selected, onChange, label }) {
  const toggle = (id) => {
    if (selected.includes(id)) {
      onChange(selected.filter((s) => s !== id));
    } else {
      onChange([...selected, id]);
    }
  };

  return (
    <div className="symptom-picker">
      {label && <p className="symptom-picker-label">{label}</p>}
      <p className="muted small">Tap all that apply — no typing needed</p>
      <div className="symptom-grid">
        {symptoms.map((symptom) => (
          <button
            key={symptom.id}
            type="button"
            className={`symptom-tile ${selected.includes(symptom.id) ? "selected" : ""}`}
            onClick={() => toggle(symptom.id)}
          >
            <span className="symptom-icon"><SymptomIcon symptomId={symptom.id} size={22} /></span>
            <span className="symptom-name">{symptom.label}</span>
          </button>
        ))}
      </div>
      {selected.length > 0 && (
        <p className="symptom-count">{selected.length} symptom{selected.length !== 1 ? "s" : ""} selected</p>
      )}
    </div>
  );
}
