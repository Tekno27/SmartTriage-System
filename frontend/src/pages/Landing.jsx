import { Link } from "react-router-dom";
import AppIcon from "../components/AppIcon";

export default function Landing() {
  return (
    <div className="landing">
      <header className="landing-header">
        <div className="brand-link">
          <span className="brand-logo"><AppIcon name="hospital" size={20} /></span>
          <div>
            <strong>SmartTriage</strong>
            <span className="brand-sub">UCC Health Clinic</span>
          </div>
        </div>
        <Link to="/login" className="btn btn-primary">Staff Sign In</Link>
      </header>

      <section className="landing-hero">
        <div className="hero-content">
          <span className="hero-badge"><AppIcon name="sparkles" size={14} /> AI-Powered Triage</span>
          <h1>Faster care, smarter hospitals</h1>
          <p>
            SmartTriage is a full Hospital Management System for the University of Cape Coast health clinic —
            from AI-powered triage and OPD to admissions, laboratory, radiology, pharmacy, billing, and more.
          </p>
          <div className="hero-actions">
            <Link to="/login" className="btn btn-primary btn-lg">Get Started</Link>
            <a href="#how-it-works" className="btn btn-secondary btn-lg">How it works</a>
          </div>
        </div>
        <div className="hero-visual">
          <div className="hero-card">
            <div className="hero-card-row"><span>Queue</span><strong className="queue-preview">H004</strong></div>
            <div className="hero-card-row"><span>Priority</span><span className="urgency-badge urgency-moderate">moderate</span></div>
            <div className="hero-card-row"><span>NHIS</span><span className="verified"><AppIcon name="circleCheck" size={14} /> Active</span></div>
            <div className="hero-ai-hint"><AppIcon name="sparkles" size={14} /> AI assessed in seconds</div>
          </div>
        </div>
      </section>

      <section id="how-it-works" className="landing-steps">
        <h2>How it works</h2>
        <div className="steps-grid">
          <div className="step-card">
            <span className="step-num">1</span>
            <h3>Scan QR Code</h3>
            <p>Arrive at the clinic and scan your student QR code for instant identification.</p>
          </div>
          <div className="step-card">
            <span className="step-num">2</span>
            <h3>Confirm Details</h3>
            <p>Verify your name, index number, and NHIS card. We check your insurance is active.</p>
          </div>
          <div className="step-card">
            <span className="step-num">3</span>
            <h3>Tap Your Symptoms</h3>
            <p>No typing — just tap common symptoms and set your pain level on a simple gauge.</p>
          </div>
          <div className="step-card">
            <span className="step-num">4</span>
            <h3>Get Your Number</h3>
            <p>AI prioritises your case. Receive a queue number based on how urgent your situation is.</p>
          </div>
        </div>
      </section>

      <section className="landing-roles">
        <h2>Built for every role</h2>
        <div className="roles-grid">
          <div className="role-card">
            <span className="role-icon"><AppIcon name="student" size={32} /></span>
            <h3>Students</h3>
            <p>Quick check-in with QR code and symptom taps. Get your queue number and wait comfortably.</p>
          </div>
          <div className="role-card">
            <span className="role-icon"><AppIcon name="stethoscope" size={32} /></span>
            <h3>Nurses</h3>
            <p>Live priority queue with AI triage suggestions. Vitals entry and instant urgency scoring.</p>
          </div>
          <div className="role-card">
            <span className="role-icon"><AppIcon name="doctor" size={32} /></span>
            <h3>Doctors</h3>
            <p>AI-assisted differential diagnosis and medication suggestions. Full patient history at a glance.</p>
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <p>SmartTriage · University of Cape Coast · HCI Course Project</p>
        <p className="muted">Nii Teiko Aryee</p>
      </footer>
    </div>
  );
}
