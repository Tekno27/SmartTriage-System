import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import StepWizard from "../components/StepWizard";
import SymptomPicker from "../components/SymptomPicker";
import PainGauge from "../components/PainGauge";
import QueueTicket from "../components/QueueTicket";
import client, { patientsApi, visitsApi } from "../api/client";
import { useAuth } from "../context/AuthContext";

const STEP_IDS = ["scan", "details", "insurance", "symptoms", "confirm"];
const STEP_LABELS = ["QR Scan", "Your Info", "NHIS", "Symptoms", "Confirm"];

export default function StudentCheckIn() {
  const { user } = useAuth();
  const [step, setStep] = useState(0);
  const [qrSrc, setQrSrc] = useState("");
  const [symptomOptions, setSymptomOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    student_id: "",
    ghana_card_number: "",
    nhis_number: "",
  });
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [painLevel, setPainLevel] = useState(0);
  const [nhisResult, setNhisResult] = useState(null);
  const [completedVisit, setCompletedVisit] = useState(null);

  useEffect(() => {
    patientsApi.profile().then((res) => {
      const p = res.data;
      setForm({
        first_name: p.first_name || user?.first_name || "",
        last_name: p.last_name || user?.last_name || "",
        student_id: p.student_id || user?.student_id || "",
        ghana_card_number: p.ghana_card_number || "",
        nhis_number: p.nhis_number || `NHIS-${p.student_id || user?.student_id || "STU001"}`,
      });
    });
    patientsApi.symptoms().then((res) => setSymptomOptions(res.data));
    visitsApi.myVisit().then((res) => {
      if (res.data.visit) setCompletedVisit(res.data.visit);
    });

    let objectUrl = "";
    client.get("/patients/qr/", { responseType: "blob" }).then((res) => {
      objectUrl = URL.createObjectURL(res.data);
      setQrSrc(objectUrl);
    });
    return () => { if (objectUrl) URL.revokeObjectURL(objectUrl); };
  }, [user]);

  const verifyNhis = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await patientsApi.checkNhis(form.nhis_number);
      setNhisResult(res.data);
    } catch {
      setError("Could not verify NHIS. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const submitCheckIn = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await visitsApi.checkIn({
        ...form,
        symptoms: selectedSymptoms,
        pain_level: painLevel,
      });
      setCompletedVisit(res.data.visit);
      setStep(STEP_IDS.length);
    } catch (err) {
      if (err.response?.data?.visit) {
        setCompletedVisit(err.response.data.visit);
        setStep(STEP_IDS.length);
      } else {
        setError(err.response?.data?.detail || "Check-in failed.");
      }
    } finally {
      setLoading(false);
    }
  };

  const next = () => {
    if (step === 2 && !nhisResult) {
      verifyNhis().then(() => setStep((s) => s + 1));
      return;
    }
    setStep((s) => s + 1);
  };

  const currentStepId = STEP_IDS[step];

  if (completedVisit) {
    return (
      <AppShell title="You're checked in!" subtitle="Please wait in the waiting area">
        <div className="checkin-done">
          <QueueTicket visit={completedVisit} />
          <p className="success center">A nurse will call your queue number shortly.</p>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell title="Patient Check-In" subtitle="Quick & easy — just a few taps">
      <StepWizard
        currentStep={step}
        steps={STEP_LABELS}
      />

      <div className="intake-panel">
        {currentStepId === "scan" && (
          <div className="intake-step">
            <h2>Welcome! Scan or show your QR code</h2>
            <p className="muted">Show this code at reception, or tap continue if you've already scanned.</p>
            <div className="qr-frame large">
              {qrSrc ? <img src={qrSrc} alt="Your QR code" className="qr-image" /> : <p>Loading…</p>}
            </div>
            <p className="center muted">Hello, <strong>{user?.full_name}</strong></p>
          </div>
        )}

        {currentStepId === "details" && (
          <div className="intake-step">
            <h2>Confirm your details</h2>
            <p className="muted">We've pre-filled what we know. Tap to edit if needed.</p>
            <div className="grid-2">
              <label>First name<input value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} /></label>
              <label>Last name<input value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} /></label>
              <label>Index / Student ID<input value={form.student_id} onChange={(e) => setForm({ ...form, student_id: e.target.value })} /></label>
              <label>Ghana Card Number<input value={form.ghana_card_number} onChange={(e) => setForm({ ...form, ghana_card_number: e.target.value })} placeholder="GHA-XXXXXXXXX-X" /></label>
            </div>
          </div>
        )}

        {currentStepId === "insurance" && (
          <div className="intake-step">
            <h2>NHIS Insurance Check</h2>
            <p className="muted">We'll verify your National Health Insurance is active and renewed.</p>
            <label>
              NHIS Card Number
              <input value={form.nhis_number} onChange={(e) => { setForm({ ...form, nhis_number: e.target.value }); setNhisResult(null); }} />
            </label>
            <button className="btn btn-secondary" onClick={verifyNhis} disabled={loading}>
              {loading ? "Checking…" : "Verify NHIS"}
            </button>
            {nhisResult && (
              <div className={`nhis-result ${nhisResult.valid ? "success-box" : "error-box"}`}>
                <strong>{nhisResult.valid ? "Insurance Active" : "Insurance Issue"}</strong>
                <p>{nhisResult.message}</p>
                {nhisResult.expiry_date && <p className="small">Expires: {nhisResult.expiry_date}</p>}
              </div>
            )}
          </div>
        )}

        {currentStepId === "symptoms" && (
          <div className="intake-step">
            <h2>How are you feeling?</h2>
            <p className="muted">Tap your symptoms — no need to type anything.</p>
            <SymptomPicker
              symptoms={symptomOptions}
              selected={selectedSymptoms}
              onChange={setSelectedSymptoms}
            />
            <PainGauge value={painLevel} onChange={setPainLevel} />
          </div>
        )}

        {currentStepId === "confirm" && (
          <div className="intake-step">
            <h2>Review & confirm</h2>
            <div className="confirm-card">
              <div className="confirm-row"><span>Name</span><strong>{form.first_name} {form.last_name}</strong></div>
              <div className="confirm-row"><span>Index</span><strong>{form.student_id}</strong></div>
              <div className="confirm-row"><span>NHIS</span><strong>{nhisResult?.valid ? "Active" : form.nhis_number}</strong></div>
              <div className="confirm-row"><span>Symptoms</span><strong>{selectedSymptoms.length} selected</strong></div>
              <div className="confirm-row"><span>Pain</span><strong>{painLevel}/10</strong></div>
            </div>
            <p className="muted small">AI will assign your queue priority based on your symptoms and pain level.</p>
          </div>
        )}

        {error && <p className="error">{error}</p>}

        <div className="intake-nav">
          {step > 0 && (
            <button className="btn btn-secondary" onClick={() => setStep((s) => s - 1)}>Back</button>
          )}
          {currentStepId !== "confirm" ? (
            <button className="btn btn-primary" onClick={next} disabled={currentStepId === "symptoms" && selectedSymptoms.length === 0}>
              Continue
            </button>
          ) : (
            <button className="btn btn-primary" onClick={submitCheckIn} disabled={loading}>
              {loading ? "Submitting…" : "Get my queue number"}
            </button>
          )}
        </div>
      </div>
    </AppShell>
  );
}
