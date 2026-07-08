import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "/api";

const client = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  login: (username, password) =>
    client.post("/auth/login/", { username, password }),
  me: () => client.get("/auth/me/"),
};

export const visitsApi = {
  checkIn: (data) => client.post("/visits/check-in/", data),
  queue: (status) => client.get("/visits/queue/", { params: status ? { status } : {} }),
  detail: (id) => client.get(`/visits/${id}/`),
  start: (id) => client.post(`/visits/${id}/start/`),
  complete: (id, data) => client.post(`/visits/${id}/complete/`, data),
  markTriaged: (id) => client.post(`/visits/${id}/triaged/`),
};

export const triageApi = {
  create: (data) => client.post("/triage/", data),
};

export const patientsApi = {
  profile: () => client.get("/patients/profile/"),
  qrUrl: () => `${API_BASE}/patients/qr/`,
};

export const pharmacyApi = {
  medications: () => client.get("/pharmacy/medications/"),
  prescriptions: (visitId) =>
    client.get("/pharmacy/prescriptions/", { params: visitId ? { visit: visitId } : {} }),
  createPrescription: (data) => client.post("/pharmacy/prescriptions/create/", data),
  dispense: (id) => client.post(`/pharmacy/prescriptions/${id}/dispense/`),
};

export const billingApi = {
  claims: () => client.get("/billing/claims/"),
  createClaim: (data) => client.post("/billing/claims/create/", data),
  submitClaim: (id) => client.post(`/billing/claims/${id}/submit/`),
};

export default client;
