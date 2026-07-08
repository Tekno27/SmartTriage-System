import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "/api";

const client = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const authApi = {
  login: (username, password) => client.post("/auth/login/", { username, password }),
  me: () => client.get("/auth/me/"),
};

export const hospitalApi = {
  overview: () => client.get("/hospital/overview/"),
  departments: () => client.get("/hospital/departments/"),
  wards: () => client.get("/hospital/wards/"),
  beds: (params) => client.get("/hospital/beds/", { params }),
  theatres: () => client.get("/hospital/theatres/"),
};

export const appointmentsApi = {
  list: (params) => client.get("/appointments/", { params }),
  create: (data) => client.post("/appointments/", data),
  confirm: (id) => client.post(`/appointments/${id}/confirm/`),
};

export const admissionsApi = {
  list: (params) => client.get("/admissions/", { params }),
  create: (data) => client.post("/admissions/", data),
  discharge: (id, data) => client.post(`/admissions/${id}/discharge/`, data),
  surgeries: () => client.get("/admissions/surgeries/"),
};

export const laboratoryApi = {
  tests: () => client.get("/laboratory/tests/"),
  orders: (params) => client.get("/laboratory/orders/", { params }),
  createOrder: (data) => client.post("/laboratory/orders/", data),
  submitResult: (id, data) => client.post(`/laboratory/results/${id}/`, data),
};

export const radiologyApi = {
  types: () => client.get("/radiology/types/"),
  orders: (params) => client.get("/radiology/orders/", { params }),
  createOrder: (data) => client.post("/radiology/orders/", data),
  submitReport: (id, data) => client.post(`/radiology/orders/${id}/report/`, data),
};

export const inventoryApi = {
  items: () => client.get("/inventory/items/"),
  movements: () => client.get("/inventory/movements/"),
};

export const recordsApi = {
  list: (params) => client.get("/records/", { params }),
  create: (data) => client.post("/records/", data),
};

export const notificationsApi = {
  list: () => client.get("/notifications/"),
  markRead: (id) => client.post(`/notifications/${id}/read/`),
  markAllRead: () => client.post("/notifications/read-all/"),
};

export const visitsApi = {
  checkIn: (data) => client.post("/visits/check-in/", data),
  myVisit: () => client.get("/visits/my-visit/"),
  queue: (status) => client.get("/visits/queue/", { params: status ? { status } : {} }),
  stats: () => client.get("/visits/stats/"),
  detail: (id) => client.get(`/visits/${id}/`),
  start: (id) => client.post(`/visits/${id}/start/`),
  complete: (id, data) => client.post(`/visits/${id}/complete/`, data),
  markTriaged: (id) => client.post(`/visits/${id}/triaged/`),
  aiRecommendations: (data) => client.post("/visits/ai/recommendations/", data),
};

export const triageApi = {
  create: (data) => client.post("/triage/", data),
};

export const patientsApi = {
  profile: () => client.get("/patients/profile/"),
  updateProfile: (data) => client.patch("/patients/profile/", data),
  symptoms: () => client.get("/patients/symptoms/"),
  verifyNhis: (nhis_number) => client.post("/patients/nhis/verify/", { nhis_number }),
  checkNhis: (nhis_number) => client.post("/patients/nhis/check/", { nhis_number }),
};

export const pharmacyApi = {
  medications: () => client.get("/pharmacy/medications/"),
  batches: () => client.get("/pharmacy/batches/"),
  prescriptions: (visitId) =>
    client.get("/pharmacy/prescriptions/", { params: visitId ? { visit: visitId } : {} }),
  createPrescription: (data) => client.post("/pharmacy/prescriptions/create/", data),
  dispense: (id) => client.post(`/pharmacy/prescriptions/${id}/dispense/`),
};

export const billingApi = {
  claims: () => client.get("/billing/claims/"),
  createClaim: (data) => client.post("/billing/claims/create/", data),
  submitClaim: (id) => client.post(`/billing/claims/${id}/submit/`),
  invoices: () => client.get("/billing/invoices/"),
  createInvoice: (data) => client.post("/billing/invoices/", data),
  createPayment: (data) => client.post("/billing/payments/", data),
};

export default client;
