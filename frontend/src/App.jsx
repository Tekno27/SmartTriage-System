import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Login from "./pages/Login";
import StudentCheckIn from "./pages/StudentCheckIn";
import NurseDashboard from "./pages/NurseDashboard";
import DoctorConsole from "./pages/DoctorConsole";

function ProtectedRoute({ children, role }) {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loading-screen">Loading…</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (role && user.role !== role) {
    const routes = { student: "/student", nurse: "/nurse", doctor: "/doctor" };
    return <Navigate to={routes[user.role] || "/login"} replace />;
  }

  return children;
}

function HomeRedirect() {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading-screen">Loading…</div>;
  if (!user) return <Navigate to="/login" replace />;
  const routes = { student: "/student", nurse: "/nurse", doctor: "/doctor" };
  return <Navigate to={routes[user.role] || "/login"} replace />;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/student"
            element={
              <ProtectedRoute role="student">
                <StudentCheckIn />
              </ProtectedRoute>
            }
          />
          <Route
            path="/nurse"
            element={
              <ProtectedRoute role="nurse">
                <NurseDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/doctor"
            element={
              <ProtectedRoute role="doctor">
                <DoctorConsole />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<HomeRedirect />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
