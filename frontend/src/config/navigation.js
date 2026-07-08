/** Role-based hospital navigation — icon values map to AppIcon names */

export const ROLE_HOME = {
  admin: "/admin",
  student: "/student",
  nurse: "/nurse",
  doctor: "/doctor",
  receptionist: "/reception",
  pharmacist: "/pharmacy",
  lab_technician: "/laboratory",
  radiologist: "/radiology",
  accountant: "/billing",
};

export const NAV_SECTIONS = {
  admin: [
    { section: "Overview", links: [{ to: "/admin", label: "Dashboard", icon: "hospital" }] },
    { section: "Clinical", links: [
      { to: "/nurse", label: "Triage Queue", icon: "stethoscope" },
      { to: "/doctor", label: "Consultations", icon: "doctor" },
      { to: "/records", label: "Medical Records", icon: "records" },
    ]},
    { section: "Operations", links: [
      { to: "/reception", label: "Reception", icon: "reception" },
      { to: "/appointments", label: "Appointments", icon: "calendar" },
      { to: "/admissions", label: "Admissions", icon: "bed" },
      { to: "/wards", label: "Wards & Beds", icon: "wards" },
      { to: "/theatre", label: "Theatre", icon: "theatre" },
    ]},
    { section: "Diagnostics", links: [
      { to: "/laboratory", label: "Laboratory", icon: "laboratory" },
      { to: "/radiology", label: "Radiology", icon: "radiology" },
    ]},
    { section: "Support", links: [
      { to: "/pharmacy", label: "Pharmacy", icon: "pharmacy" },
      { to: "/inventory", label: "Inventory", icon: "inventory" },
      { to: "/billing", label: "Billing & NHIS", icon: "billing" },
      { to: "/reports", label: "Reports", icon: "reports" },
    ]},
  ],
  student: [
    { section: "Patient", links: [
      { to: "/student", label: "Check In", icon: "clipboard" },
      { to: "/student/status", label: "My Queue", icon: "ticket" },
      { to: "/appointments", label: "Appointments", icon: "calendar" },
      { to: "/records", label: "My Records", icon: "records" },
    ]},
  ],
  nurse: [
    { section: "Clinical", links: [
      { to: "/nurse", label: "Triage Queue", icon: "stethoscope" },
      { to: "/admissions", label: "Admissions", icon: "bed" },
      { to: "/wards", label: "Wards", icon: "wards" },
      { to: "/records", label: "Records", icon: "records" },
    ]},
  ],
  doctor: [
    { section: "Clinical", links: [
      { to: "/doctor", label: "Consultations", icon: "doctor" },
      { to: "/laboratory", label: "Lab Orders", icon: "laboratory" },
      { to: "/radiology", label: "Imaging Orders", icon: "radiology" },
      { to: "/admissions", label: "Admissions", icon: "bed" },
      { to: "/theatre", label: "Surgery", icon: "theatre" },
      { to: "/records", label: "Records", icon: "records" },
    ]},
  ],
  receptionist: [
    { section: "Front Desk", links: [
      { to: "/reception", label: "Dashboard", icon: "reception" },
      { to: "/appointments", label: "Appointments", icon: "calendar" },
      { to: "/admissions", label: "Admissions", icon: "bed" },
      { to: "/wards", label: "Bed Status", icon: "wards" },
    ]},
  ],
  pharmacist: [
    { section: "Pharmacy", links: [
      { to: "/pharmacy", label: "Dispensing", icon: "pharmacy" },
      { to: "/inventory", label: "Inventory", icon: "inventory" },
    ]},
  ],
  lab_technician: [
    { section: "Laboratory", links: [
      { to: "/laboratory", label: "Lab Dashboard", icon: "laboratory" },
    ]},
  ],
  radiologist: [
    { section: "Radiology", links: [
      { to: "/radiology", label: "Imaging Dashboard", icon: "radiology" },
    ]},
  ],
  accountant: [
    { section: "Finance", links: [
      { to: "/billing", label: "Billing & NHIS", icon: "billing" },
      { to: "/reports", label: "Reports", icon: "reports" },
    ]},
  ],
};
