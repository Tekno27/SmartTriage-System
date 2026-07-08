import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import PatientCard from "../components/PatientCard";
import { UrgencyBadge } from "../components/UrgencyRail";
import { billingApi, pharmacyApi, visitsApi } from "../api/client";

export default function DoctorConsole() {
  const [queue, setQueue] = useState([]);
  const [activeVisit, setActiveVisit] = useState(null);
  const [medications, setMedications] = useState([]);
  const [prescriptions, setPrescriptions] = useState([]);
  const [notes, setNotes] = useState("");
  const [diagnosis, setDiagnosis] = useState("");
  const [rxForm, setRxForm] = useState({ medication_id: "", quantity_prescribed: 1, dosage_instructions: "" });
  const [message, setMessage] = useState("");

  const loadQueue = async () => {
    const res = await visitsApi.queue("waiting,in_consultation,triaged");
    setQueue(res.data);
  };

  useEffect(() => {
    loadQueue();
    pharmacyApi.medications().then((res) => setMedications(res.data));
  }, []);

  const startConsultation = async (visit) => {
    const res = await visitsApi.start(visit.id);
    setActiveVisit(res.data);
    setNotes(res.data.consultation_notes || "");
    setDiagnosis(res.data.diagnosis || "");
    loadPrescriptions(res.data.id);
    loadQueue();
  };

  const loadPrescriptions = async (visitId) => {
    const res = await pharmacyApi.prescriptions(visitId);
    setPrescriptions(res.data);
  };

  const completeConsultation = async () => {
    if (!activeVisit) return;
    await visitsApi.complete(activeVisit.id, {
      consultation_notes: notes,
      diagnosis,
    });
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
    <Layout title="Doctor Console">
      <div className="two-column wide-right">
        <section>
          <h2>Prioritized Queue</h2>
          <div className="queue-list">
            {queue.map((visit) => (
              <PatientCard
                key={visit.id}
                visit={visit}
                onAction={startConsultation}
                actionLabel={visit.status === "in_consultation" ? "Resume" : "Consult"}
              />
            ))}
          </div>
        </section>

        <section className="panel">
          <h2>Consultation</h2>
          {activeVisit ? (
            <div className="stack-form">
              <div className="consult-header">
                <h3>{activeVisit.patient.full_name}</h3>
                <UrgencyBadge urgency={activeVisit.urgency} />
              </div>
              <p className="complaint">{activeVisit.chief_complaint}</p>
              <label>
                Diagnosis
                <textarea value={diagnosis} onChange={(e) => setDiagnosis(e.target.value)} rows={2} />
              </label>
              <label>
                Consultation notes
                <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={4} />
              </label>

              <h3>Prescribe medication</h3>
              <form onSubmit={prescribe} className="grid-2">
                <label>
                  Medication
                  <select
                    value={rxForm.medication_id}
                    onChange={(e) => setRxForm({ ...rxForm, medication_id: e.target.value })}
                    required
                  >
                    <option value="">Select…</option>
                    {medications.map((med) => (
                      <option key={med.id} value={med.id}>
                        {med.name}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  Quantity
                  <input
                    type="number"
                    min="1"
                    value={rxForm.quantity_prescribed}
                    onChange={(e) =>
                      setRxForm({ ...rxForm, quantity_prescribed: e.target.value })
                    }
                  />
                </label>
                <label className="span-2">
                  Dosage instructions
                  <input
                    value={rxForm.dosage_instructions}
                    onChange={(e) =>
                      setRxForm({ ...rxForm, dosage_instructions: e.target.value })
                    }
                    placeholder="1 tablet twice daily after meals"
                    required
                  />
                </label>
                <button className="btn btn-secondary" type="submit">
                  Add prescription
                </button>
              </form>

              {prescriptions.length > 0 && (
                <ul className="rx-list">
                  {prescriptions.map((rx) => (
                    <li key={rx.id}>
                      {rx.medication.name} × {rx.quantity_prescribed}
                      {rx.is_dispensed ? " (dispensed)" : ""}
                    </li>
                  ))}
                </ul>
              )}

              <button className="btn btn-primary" onClick={completeConsultation}>
                Complete consultation & create NHIS claim
              </button>
            </div>
          ) : (
            <p className="muted">Select a patient to begin consultation.</p>
          )}
          {message && <p className="success">{message}</p>}
        </section>
      </div>
    </Layout>
  );
}
