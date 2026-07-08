import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import PatientCard from "../components/PatientCard";
import { triageApi, visitsApi } from "../api/client";

const SYMPTOM_OPTIONS = [
  "chest_pain",
  "difficulty_breathing",
  "severe_bleeding",
  "fever",
  "headache",
  "nausea",
];

const emptyTriage = {
  temperature: "",
  heart_rate: "",
  systolic_bp: "",
  diastolic_bp: "",
  pain_level: 0,
  symptoms: [],
  notes: "",
};

export default function NurseDashboard() {
  const [queue, setQueue] = useState([]);
  const [selected, setSelected] = useState(null);
  const [triage, setTriage] = useState(emptyTriage);
  const [message, setMessage] = useState("");

  const loadQueue = async () => {
    const res = await visitsApi.queue();
    setQueue(res.data);
  };

  useEffect(() => {
    loadQueue();
    const interval = setInterval(loadQueue, 10000);
    return () => clearInterval(interval);
  }, []);

  const toggleSymptom = (symptom) => {
    setTriage((prev) => ({
      ...prev,
      symptoms: prev.symptoms.includes(symptom)
        ? prev.symptoms.filter((s) => s !== symptom)
        : [...prev.symptoms, symptom],
    }));
  };

  const submitTriage = async (e) => {
    e.preventDefault();
    if (!selected) return;
    try {
      await triageApi.create({
        visit: selected.id,
        temperature: triage.temperature || null,
        heart_rate: triage.heart_rate || null,
        systolic_bp: triage.systolic_bp || null,
        diastolic_bp: triage.diastolic_bp || null,
        pain_level: Number(triage.pain_level),
        symptoms: triage.symptoms,
        notes: triage.notes,
      });
      await visitsApi.markTriaged(selected.id);
      setMessage(`Triage saved for ${selected.patient.full_name}.`);
      setSelected(null);
      setTriage(emptyTriage);
      loadQueue();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Failed to save triage.");
    }
  };

  return (
    <Layout title="Nurse Dashboard">
      <div className="two-column wide-right">
        <section>
          <h2>Live Queue</h2>
          <div className="queue-list">
            {queue.length === 0 && <p className="muted">No patients in queue.</p>}
            {queue.map((visit) => (
              <PatientCard
                key={visit.id}
                visit={visit}
                onAction={setSelected}
                actionLabel="Triage"
              />
            ))}
          </div>
        </section>

        <section className="panel">
          <h2>Triage Assessment</h2>
          {selected ? (
            <form onSubmit={submitTriage} className="stack-form">
              <p>
                Patient: <strong>{selected.patient.full_name}</strong>
              </p>
              <div className="grid-2">
                <label>
                  Temp (°C)
                  <input
                    type="number"
                    step="0.1"
                    value={triage.temperature}
                    onChange={(e) => setTriage({ ...triage, temperature: e.target.value })}
                  />
                </label>
                <label>
                  Heart rate
                  <input
                    type="number"
                    value={triage.heart_rate}
                    onChange={(e) => setTriage({ ...triage, heart_rate: e.target.value })}
                  />
                </label>
                <label>
                  Systolic BP
                  <input
                    type="number"
                    value={triage.systolic_bp}
                    onChange={(e) => setTriage({ ...triage, systolic_bp: e.target.value })}
                  />
                </label>
                <label>
                  Diastolic BP
                  <input
                    type="number"
                    value={triage.diastolic_bp}
                    onChange={(e) => setTriage({ ...triage, diastolic_bp: e.target.value })}
                  />
                </label>
              </div>
              <label>
                Pain level (0–10)
                <input
                  type="range"
                  min="0"
                  max="10"
                  value={triage.pain_level}
                  onChange={(e) => setTriage({ ...triage, pain_level: e.target.value })}
                />
                <span>{triage.pain_level}</span>
              </label>
              <fieldset>
                <legend>Symptoms</legend>
                <div className="chip-group">
                  {SYMPTOM_OPTIONS.map((symptom) => (
                    <button
                      key={symptom}
                      type="button"
                      className={`chip ${triage.symptoms.includes(symptom) ? "active" : ""}`}
                      onClick={() => toggleSymptom(symptom)}
                    >
                      {symptom.replace(/_/g, " ")}
                    </button>
                  ))}
                </div>
              </fieldset>
              <label>
                Notes
                <textarea
                  value={triage.notes}
                  onChange={(e) => setTriage({ ...triage, notes: e.target.value })}
                  rows={3}
                />
              </label>
              <button className="btn btn-primary" type="submit">
                Save triage & send to doctor
              </button>
            </form>
          ) : (
            <p className="muted">Select a patient from the queue to begin triage.</p>
          )}
          {message && <p className="success">{message}</p>}
        </section>
      </div>
    </Layout>
  );
}
