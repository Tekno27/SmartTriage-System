# SmartTriage-System

A role-based patient triage and clinic management system built for the University of Cape Coast (UCC) health clinic, developed as an HCI course project.

## Overview

SmartTriage streamlines the patient intake and treatment workflow across three roles — **students**, **nurses**, and **doctors** — with a focus on reducing wait times, prioritizing urgent cases, and digitizing pharmacy and billing operations.

## Features

### Student Flow
- QR code-based check-in
- Simple, guided intake form

### Nurse Dashboard
- Live queue view with semantic urgency indicators (color-coded spine rails)
- Triage scoring at point of intake

### Doctor Console
- Prioritized patient queue based on triage score
- Full patient history and consultation view

### Backend Systems
- **Triage scoring** — automated urgency calculation from intake data
- **Pharmacy (FEFO dispensing)** — First-Expired-First-Out medication dispensing logic
- **NHIS billing** — National Health Insurance Scheme claims and billing support
- **Role-based authentication** — separate access levels for students, nurses, and doctors

## Design System

- **Color palette:** deep teal and warm paper tones
- **Typography:** Source Serif Pro (headings/body) + IBM Plex Sans (UI elements)
- **Urgency signaling:** color-coded spine rails on patient records for at-a-glance triage status

## Tech Stack

**Frontend**
- React

**Backend**
- Django REST Framework
- Six modular apps covering: triage scoring, pharmacy/dispensing, billing (NHIS), and role-based auth

## Project Background

Built as an HCI (Human-Computer Interaction) coursework project for UCC's health clinic. The project included a full research and documentation phase alongside implementation:

- User research and questionnaires
- Hierarchical Task Analysis (HTA)
- Simulated research data for evaluation
- Full HCI report documenting the design process

## Getting Started

```bash
# Clone the repository
git clone <your-repo-url>
cd smarttriage

# Backend setup
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend setup
cd frontend
npm install
npm start
```

## Roles & Access

| Role    | Access                                      |
|---------|----------------------------------------------|
| Student | QR check-in, intake form                     |
| Nurse   | Queue dashboard, triage scoring               |
| Doctor  | Prioritized queue, patient history, consult   |

## License

Add your license here.

## Author

Nii Teiko Aryee
