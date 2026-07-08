import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import PatientCard from "../components/PatientCard";
import StatCard from "../components/StatCard";
import AIRecommendationPanel from "../components/AIRecommendationPanel";
import AppIcon from "../components/AppIcon";
import { UrgencyBadge } from "../components/UrgencyRail";
import { billingApi, pharmacyApi, visitsApi } from "../api/client";

export default function DoctorConsole() {
  const [queue, setQueue] = useState([]);
  const [stats, setStats] = useState({});
  const [activeVisit, setActiveVisit] = useState(null);
  const [medications, setMedications] = useState([]);
  const [prescriptions, setPrescriptions] = useState([]);
  const [aiData, setAiData] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [notes, setNotes] = useState("");
  const [diagnosis, setDiagnosis] = useState("");
  const [rxForm, setRxForm] = useState({ medication_id: "", quantity_prescribed: 1, dosage_instructions: "" });
  const [message, setMessage] = useState("");

  const loadQueue = async () => {
    const [queueRes, statsRes] = await Promise.all([
      visitsApi.queue("waiting,in_consultation,triaged"),
      visitsApi.stats(),
    ]);
    setQueue(queueRes.data);
    setStats(statsRes.data);
  };

  useEffect(() => {
    loadQueue();
    pharmacyApi.medications().then((res) => setMedications(res.data));
  }, []);

  const loadAi = async (visit) => {
    setAiLoading(true);
    try {
      const res = await visitsApi.aiRecommendations({ visit_id: visit.id, mode: "diagnosis" });
      setAiData(res.data);
    } catch {
      setAiData(null);
    } finally {
      setAiLoading(false);
    }
  };

  const startConsultation = async (visit) => {
    const res = await visitsApi.start(visit.id);
    setActiveVisit(res.data);
    setNotes(res.data.consultation_notes || "");
    setDiagnosis(res.data.diagnosis || "");
    loadPrescriptions(res.data.id);
    loadAi(res.data);
    loadQueue();
  };

  const loadPrescriptions = async (visitId) => {
    const res = await pharmacyApi.prescriptions(visitId);
    setPrescriptions(res.data);
  };

  const applyMedicationSuggestion = (med) => {
    const match = medications.find(
      (m) => m.name.toLowerCase().includes(med.name.split(" ")[0].toLowerCase())
    );
    setRxForm({
      medication_id: match?.id || "",
      quantity_prescribed: 1,
      dosage_instructions: med.dosage,
    });
  };

  const completeConsultation = async () => {
    if (!activeVisit) return;
    await visitsApi.complete(activeVisit.id, { consultation_notes: notes, diagnosis });
    await billingApi.createClaim({
      visit: activeVisit.id,
      patient_nhis_number: activeVisit.patient.student_id
        ? `NHIS-${activeVisit.patient.student_id}`
        : "NHIS-UNKNOWN",
      consultation_fee: "25.00",
      medication_cost: "10.00",
      diagnosis_code: "Z00.0",
    });
    setMessage(`Consultation completed for ${activeVisit.patient.full_name}.`);
    setActiveVisit(null);
    setAiData(null);
    setPrescriptions([]);
    loadQueue();
  };

  const prescribe = async (e) => {
    e.preventDefault();
    if (!activeVisit) return;
    await pharmacyApi.createPrescription({
      visit: activeVisit.id,
      ...rxForm,
      quantity_prescribed: Number(rxForm.quantity_prescribed),
    });
    setRxForm({ medication_id: "", quantity_prescribed: 1, dosage_instructions: "" });
    loadPrescriptions(activeVisit.id);
  };

  return (
    <AppShell title="Doctor Console" subtitle="AI-assisted consultations">
      <div className="stats-row">
        <StatCard label="Waiting" value={stats.triaged || 0} icon="clock" />
        <StatCard label="In Consultation" value={stats.in_consultation || 0} icon="doctor" />
        <StatCard label="Completed Today" value={stats.completed_today || 0} icon="circleCheck" />
        <StatCard label="Critical" value={stats.critical || 0} icon="alert" accent="critical" />
      </div>

      <div className="dashboard-grid">
        <section className="panel">
          <div className="panel-header">
            <h2>Priority Queue</h2>
            <span className="badge">{queue.length} patients</span>
          </div>
          <div className="queue-list">
            {queue.map((visit) => (
              <PatientCard
                key={visit.id}
                visit={visit}
                onAction={startConsultation}
                actionLabel={visit.status === "in_consultation" ? "Resume" : "Consult"}
                active={activeVisit?.id === visit.id}
              />
            ))}
          </div>
        </section>

        <section className="panel consult-panel">
          {activeVisit ? (
            <>
              <div className="consult-header">
                <div>
                  <h2>{activeVisit.patient.full_name}</h2>
                  <span className="muted">{activeVisit.queue_number} · Index {activeVisit.patient.student_id}</span>
                </div>
                <UrgencyBadge urgency={activeVisit.urgency} />
              </div>

              <div className="patient-intake-summary">
                <div className="intake-chips">
                  {(activeVisit.symptoms || []).map((s) => (
                    <span key={s} className="chip active">{s.replace(/_/g, " ")}</span>
                  ))}
                </div>
                <p>Pain: {activeVisit.pain_level}/10 · Score: {activeVisit.triage_score}</p>
              </div>

              <AIRecommendationPanel data={aiData} loading={aiLoading} />

              {aiData?.recommended_medications?.length > 0 && (
                <div className="ai-quick-rx">
                  <h4>Quick prescribe from AI</h4>
                  <div className="chip-group">
                    {aiData.recommended_medications.map((med, i) => (
                      <button key={i} type="button" className="chip" onClick={() => applyMedicationSuggestion(med)}>
                        + {med.name}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <div className="stack-form">
                <label>
                  Diagnosis
                  <textarea value={diagnosis} onChange={(e) => setDiagnosis(e.target.value)} rows={2} placeholder="Enter or use AI suggestion above" />
                </label>
                <label>
                  Consultation notes
                  <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={3} />
                </label>

                <h3>Prescription</h3>
                <form onSubmit={prescribe} className="grid-2">
                  <label>
                    Medication
                    <select value={rxForm.medication_id} onChange={(e) => setRxForm({ ...rxForm, medication_id: e.target.value })} required>
                      <option value="">Select…</option>
                      {medications.map((med) => (
                        <option key={med.id} value={med.id}>{med.name}</option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Quantity
                    <input type="number" min="1" value={rxForm.quantity_prescribed} onChange={(e) => setRxForm({ ...rxForm, quantity_prescribed: e.target.value })} />
                  </label>
                  <label className="span-2">
                    Dosage
                    <input value={rxForm.dosage_instructions} onChange={(e) => setRxForm({ ...rxForm, dosage_instructions: e.target.value })} required />
                  </label>
                  <button className="btn btn-secondary" type="submit">Add prescription</button>
                </form>

                {prescriptions.length > 0 && (
                  <ul className="rx-list">
                    {prescriptions.map((rx) => (
                      <li key={rx.id}>{rx.medication.name} × {rx.quantity_prescribed}{rx.is_dispensed ? " (dispensed)" : ""}</li>
                    ))}
                  </ul>
                )}

                <button className="btn btn-primary" onClick={completeConsultation}>
                  Complete & create NHIS claim
                </button>
              </div>
            </>
          ) : (
            <div className="empty-state">
              <span className="empty-icon"><AppIcon name="doctor" size={40} /></span>
              <h3>Select a patient</h3>
              <p className="muted">Choose from the priority queue to start an AI-assisted consultation.</p>
            </div>
          )}
          {message && <p className="success">{message}</p>}
        </section>
      </div>
    </AppShell>
  );
}
