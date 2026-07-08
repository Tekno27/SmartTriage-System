import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import PatientCard from "../components/PatientCard";
import StatCard from "../components/StatCard";
import AIRecommendationPanel from "../components/AIRecommendationPanel";
import PainGauge from "../components/PainGauge";
import SymptomPicker from "../components/SymptomPicker";
import AppIcon from "../components/AppIcon";
import { patientsApi, triageApi, visitsApi } from "../api/client";

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
  const [stats, setStats] = useState({});
  const [selected, setSelected] = useState(null);
  const [triage, setTriage] = useState(emptyTriage);
  const [symptomOptions, setSymptomOptions] = useState([]);
  const [aiData, setAiData] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [message, setMessage] = useState("");

  const loadQueue = async () => {
    const [queueRes, statsRes] = await Promise.all([visitsApi.queue(), visitsApi.stats()]);
    setQueue(queueRes.data);
    setStats(statsRes.data);
  };

  useEffect(() => {
    loadQueue();
    patientsApi.symptoms().then((res) => setSymptomOptions(res.data));
    const interval = setInterval(loadQueue, 10000);
    return () => clearInterval(interval);
  }, []);

  const selectPatient = async (visit) => {
    setSelected(visit);
    setTriage({
      ...emptyTriage,
      pain_level: visit.pain_level || 0,
      symptoms: visit.symptoms || [],
    });
    setAiLoading(true);
    try {
      const res = await visitsApi.aiRecommendations({
        visit_id: visit.id,
        mode: "triage",
      });
      setAiData(res.data);
    } catch {
      setAiData(null);
    } finally {
      setAiLoading(false);
    }
  };

  const refreshAi = async () => {
    if (!selected) return;
    setAiLoading(true);
    const res = await visitsApi.aiRecommendations({
      visit_id: selected.id,
      mode: "triage",
      vitals: {
        temperature: triage.temperature,
        heart_rate: triage.heart_rate,
        systolic_bp: triage.systolic_bp,
      },
    });
    setAiData(res.data);
    setAiLoading(false);
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
      setMessage(`Triage complete for ${selected.patient.full_name}. Sent to doctor queue.`);
      setSelected(null);
      setTriage(emptyTriage);
      setAiData(null);
      loadQueue();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Failed to save triage.");
    }
  };

  return (
    <AppShell title="Nurse Dashboard" subtitle="Live triage queue">
      <div className="stats-row">
        <StatCard label="Waiting" value={stats.waiting || 0} icon="clock" />
        <StatCard label="Triaged" value={stats.triaged || 0} icon="stethoscope" />
        <StatCard label="In Consultation" value={stats.in_consultation || 0} icon="doctor" />
        <StatCard label="Critical" value={stats.critical || 0} icon="alert" accent="critical" />
      </div>

      <div className="dashboard-grid">
        <section className="panel">
          <div className="panel-header">
            <h2>Live Queue</h2>
            <span className="badge">{queue.length} patients</span>
          </div>
          <div className="queue-list">
            {queue.length === 0 && (
              <div className="empty-state small">
                <AppIcon name="circleCheck" size={24} />
                <p>Queue is clear</p>
              </div>
            )}
            {queue.map((visit) => (
              <PatientCard
                key={visit.id}
                visit={visit}
                onAction={selectPatient}
                actionLabel="Triage"
                active={selected?.id === visit.id}
              />
            ))}
          </div>
        </section>

        <section className="panel triage-panel">
          {selected ? (
            <>
              <div className="panel-header">
                <h2>Triage: {selected.patient.full_name}</h2>
                <span className="queue-num">{selected.queue_number}</span>
              </div>

              <div className="patient-intake-summary">
                <h4>Student reported</h4>
                <div className="intake-chips">
                  {(selected.symptoms || []).map((s) => (
                    <span key={s} className="chip active">{s.replace(/_/g, " ")}</span>
                  ))}
                </div>
                <p>Pain: <strong>{selected.pain_level}/10</strong> · NHIS: {selected.nhis_verified ? "Verified" : "Unverified"}</p>
              </div>

              <AIRecommendationPanel data={aiData} loading={aiLoading} />

              <form onSubmit={submitTriage} className="stack-form">
                <h3>Vital Signs</h3>
                <div className="grid-2">
                  <label>Temp (°C)<input type="number" step="0.1" value={triage.temperature} onChange={(e) => setTriage({ ...triage, temperature: e.target.value })} onBlur={refreshAi} /></label>
                  <label>Heart rate<input type="number" value={triage.heart_rate} onChange={(e) => setTriage({ ...triage, heart_rate: e.target.value })} onBlur={refreshAi} /></label>
                  <label>Systolic BP<input type="number" value={triage.systolic_bp} onChange={(e) => setTriage({ ...triage, systolic_bp: e.target.value })} onBlur={refreshAi} /></label>
                  <label>Diastolic BP<input type="number" value={triage.diastolic_bp} onChange={(e) => setTriage({ ...triage, diastolic_bp: e.target.value })} /></label>
                </div>

                <SymptomPicker
                  symptoms={symptomOptions}
                  selected={triage.symptoms}
                  onChange={(s) => setTriage({ ...triage, symptoms: s })}
                  label="Confirm / add symptoms"
                />

                <PainGauge
                  value={triage.pain_level}
                  onChange={(v) => setTriage({ ...triage, pain_level: v })}
                  label="Pain level (nurse assessment)"
                />

                <button className="btn btn-primary" type="submit">
                  Complete triage & send to doctor
                </button>
              </form>
            </>
          ) : (
            <div className="empty-state">
              <span className="empty-icon"><AppIcon name="stethoscope" size={40} /></span>
              <h3>Select a patient</h3>
              <p className="muted">Tap a patient from the queue to begin triage with AI assistance.</p>
            </div>
          )}
          {message && <p className="success">{message}</p>}
        </section>
      </div>
    </AppShell>
  );
}
