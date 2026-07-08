import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import client, { visitsApi } from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function StudentCheckIn() {
  const { user } = useAuth();
  const [complaint, setComplaint] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [qrSrc, setQrSrc] = useState("");

  useEffect(() => {
    let objectUrl = "";
    client
      .get("/patients/qr/", { responseType: "blob" })
      .then((res) => {
        objectUrl = URL.createObjectURL(res.data);
        setQrSrc(objectUrl);
      })
      .catch(() => setQrSrc(""));
    return () => {
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, []);

  const handleCheckIn = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      await visitsApi.checkIn({
        chief_complaint: complaint,
        symptoms_description: symptoms,
      });
      setMessage("Check-in successful! Please wait to be called for triage.");
      setComplaint("");
      setSymptoms("");
    } catch (err) {
      setMessage(err.response?.data?.detail || "Check-in failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout title="Student Check-In">
      <div className="two-column">
        <section className="panel">
          <h2>Your QR Code</h2>
          <p className="muted">Show this at the clinic reception for quick identification.</p>
          <div className="qr-frame">
            {qrSrc ? (
              <img src={qrSrc} alt="Student QR code" className="qr-image" />
            ) : (
              <p className="muted">Loading QR code…</p>
            )}
          </div>
          <p className="muted small">Student: {user?.full_name} ({user?.student_id})</p>
        </section>

        <section className="panel">
          <h2>Intake Form</h2>
          <form onSubmit={handleCheckIn} className="stack-form">
            <label>
              Chief complaint
              <textarea
                value={complaint}
                onChange={(e) => setComplaint(e.target.value)}
                placeholder="Describe your main concern…"
                required
                rows={3}
              />
            </label>
            <label>
              Additional symptoms
              <textarea
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                placeholder="Fever, headache, nausea…"
                rows={3}
              />
            </label>
            <button className="btn btn-primary" type="submit" disabled={loading}>
              {loading ? "Submitting…" : "Check in"}
            </button>
          </form>
          {message && <p className="success">{message}</p>}
        </section>
      </div>
    </Layout>
  );
}
