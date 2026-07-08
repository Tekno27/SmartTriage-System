import AppIcon from "./AppIcon";

const STEPS = ["scan", "details", "insurance", "symptoms", "confirm"];

export default function StepWizard({ currentStep, steps }) {
  const currentIndex = typeof currentStep === "number" ? currentStep : 0;

  return (
    <div className="step-wizard">
      {steps.map((label, i) => (
        <div key={label} className={`step-item ${i <= currentIndex ? "done" : ""} ${i === currentIndex ? "active" : ""}`}>
          <div className="step-circle">
            {i < currentIndex ? <AppIcon name="check" size={14} /> : i + 1}
          </div>
          <span className="step-name">{label}</span>
          {i < steps.length - 1 && <div className="step-line" />}
        </div>
      ))}
    </div>
  );
}
