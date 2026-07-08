import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { ROLE_HOME } from "./config/navigation";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import StudentCheckIn from "./pages/StudentCheckIn";
import StudentStatus from "./pages/StudentStatus";
import NurseDashboard from "./pages/NurseDashboard";
import DoctorConsole from "./pages/DoctorConsole";
import AdminDashboard from "./pages/hms/AdminDashboard";
import ReceptionDashboard from "./pages/hms/ReceptionDashboard";
import AppointmentsPage from "./pages/hms/AppointmentsPage";
import AdmissionsPage from "./pages/hms/AdmissionsPage";
import WardsPage from "./pages/hms/WardsPage";
import LaboratoryPage from "./pages/hms/LaboratoryPage";
import RadiologyPage from "./pages/hms/RadiologyPage";
import PharmacyPage from "./pages/hms/PharmacyPage";
import BillingPage from "./pages/hms/BillingPage";
import InventoryPage from "./pages/hms/InventoryPage";
import MedicalRecordsPage from "./pages/hms/MedicalRecordsPage";
import TheatrePage from "./pages/hms/TheatrePage";
import ReportsPage from "./pages/hms/ReportsPage";

function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading-screen">Loading…</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) {
    return <Navigate to={ROLE_HOME[user.role] || "/login"} replace />;
  }
  return children;
}

function HomeRedirect() {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading-screen">Loading…</div>;
  if (!user) return <Landing />;
  return <Navigate to={ROLE_HOME[user.role] || "/login"} replace />;
}

const ALL_STAFF = ["admin", "nurse", "doctor", "receptionist", "pharmacist", "lab_technician", "radiologist", "accountant"];
const CLINICAL = ["admin", "nurse", "doctor"];

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomeRedirect />} />
          <Route path="/login" element={<Login />} />

          {/* Clinical */}
          <Route path="/student" element={<ProtectedRoute roles={["student"]}><StudentCheckIn /></ProtectedRoute>} />
          <Route path="/student/status" element={<ProtectedRoute roles={["student"]}><StudentStatus /></ProtectedRoute>} />
          <Route path="/nurse" element={<ProtectedRoute roles={["nurse", "admin"]}><NurseDashboard /></ProtectedRoute>} />
          <Route path="/doctor" element={<ProtectedRoute roles={["doctor", "admin"]}><DoctorConsole /></ProtectedRoute>} />

          {/* HMS Modules */}
          <Route path="/admin" element={<ProtectedRoute roles={["admin"]}><AdminDashboard /></ProtectedRoute>} />
          <Route path="/reception" element={<ProtectedRoute roles={["receptionist", "admin"]}><ReceptionDashboard /></ProtectedRoute>} />
          <Route path="/appointments" element={<ProtectedRoute roles={[...ALL_STAFF, "student"]}><AppointmentsPage /></ProtectedRoute>} />
          <Route path="/admissions" element={<ProtectedRoute roles={["admin", "nurse", "doctor", "receptionist"]}><AdmissionsPage /></ProtectedRoute>} />
          <Route path="/wards" element={<ProtectedRoute roles={["admin", "nurse", "receptionist"]}><WardsPage /></ProtectedRoute>} />
          <Route path="/laboratory" element={<ProtectedRoute roles={["admin", "doctor", "nurse", "lab_technician"]}><LaboratoryPage /></ProtectedRoute>} />
          <Route path="/radiology" element={<ProtectedRoute roles={["admin", "doctor", "nurse", "radiologist"]}><RadiologyPage /></ProtectedRoute>} />
          <Route path="/pharmacy" element={<ProtectedRoute roles={["admin", "pharmacist", "doctor"]}><PharmacyPage /></ProtectedRoute>} />
          <Route path="/billing" element={<ProtectedRoute roles={["admin", "accountant", "doctor"]}><BillingPage /></ProtectedRoute>} />
          <Route path="/inventory" element={<ProtectedRoute roles={["admin", "pharmacist"]}><InventoryPage /></ProtectedRoute>} />
          <Route path="/records" element={<ProtectedRoute roles={[...ALL_STAFF, "student"]}><MedicalRecordsPage /></ProtectedRoute>} />
          <Route path="/theatre" element={<ProtectedRoute roles={["admin", "doctor", "nurse"]}><TheatrePage /></ProtectedRoute>} />
          <Route path="/reports" element={<ProtectedRoute roles={["admin", "accountant"]}><ReportsPage /></ProtectedRoute>} />

          {/* Legacy redirects */}
          <Route path="/nurse/triage" element={<Navigate to="/nurse" replace />} />
          <Route path="/doctor/consult" element={<Navigate to="/doctor" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
