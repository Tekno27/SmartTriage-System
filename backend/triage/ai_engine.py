"""Rule-based AI recommendations for triage and diagnosis assistance."""

COMMON_SYMPTOMS = [
    {"id": "fever", "label": "Fever"},
    {"id": "headache", "label": "Headache"},
    {"id": "stomach_pain", "label": "Stomach Pain"},
    {"id": "nausea_vomiting", "label": "Nausea / Vomiting"},
    {"id": "cough", "label": "Cough"},
    {"id": "sore_throat", "label": "Sore Throat"},
    {"id": "chest_pain", "label": "Chest Pain"},
    {"id": "difficulty_breathing", "label": "Difficulty Breathing"},
    {"id": "dizziness", "label": "Dizziness"},
    {"id": "body_aches", "label": "Body Aches"},
    {"id": "runny_nose", "label": "Runny Nose"},
    {"id": "rash", "label": "Rash"},
    {"id": "diarrhoea", "label": "Diarrhoea"},
    {"id": "ear_pain", "label": "Ear Pain"},
    {"id": "eye_irritation", "label": "Eye Irritation"},
    {"id": "fatigue", "label": "Fatigue / Weakness"},
    {"id": "back_pain", "label": "Back Pain"},
    {"id": "injury_trauma", "label": "Injury / Trauma"},
    {"id": "allergic_reaction", "label": "Allergic Reaction"},
    {"id": "chills", "label": "Chills"},
]

SYMPTOM_KNOWLEDGE = {
    "fever": {
        "conditions": ["Malaria", "Typhoid fever", "Upper respiratory infection", "UTI"],
        "actions": ["Check temperature", "Malaria RDT if endemic", "Hydration status"],
        "urgency": "moderate",
    },
    "headache": {
        "conditions": ["Tension headache", "Migraine", "Malaria", "Hypertension"],
        "actions": ["Check BP", "Assess for neck stiffness", "Pain score"],
        "urgency": "low",
    },
    "stomach_pain": {
        "conditions": ["Gastritis", "Appendicitis", "Food poisoning", "Peptic ulcer"],
        "actions": ["Palpate abdomen", "Nausea/vomiting history", "Bowel sounds"],
        "urgency": "moderate",
    },
    "nausea_vomiting": {
        "conditions": ["Gastroenteritis", "Food poisoning", "Pregnancy", "Migraine"],
        "actions": ["Hydration check", "Recent food intake", "Electrolytes if severe"],
        "urgency": "moderate",
    },
    "cough": {
        "conditions": ["Common cold", "Bronchitis", "Pneumonia", "TB (if chronic)"],
        "actions": ["Auscultate chest", "Duration of cough", "Sputum colour"],
        "urgency": "low",
    },
    "sore_throat": {
        "conditions": ["Pharyngitis", "Strep throat", "Viral URI"],
        "actions": ["Examine throat", "Check for tonsillar exudate", "Fever check"],
        "urgency": "low",
    },
    "chest_pain": {
        "conditions": ["Angina", "Musculoskeletal pain", "Anxiety", "GERD"],
        "actions": ["ECG if available", "Vitals immediately", "Pain character assessment"],
        "urgency": "high",
    },
    "difficulty_breathing": {
        "conditions": ["Asthma exacerbation", "Pneumonia", "Anaphylaxis", "Heart failure"],
        "actions": ["SpO2 reading", "Peak flow if asthmatic", "Urgent vitals"],
        "urgency": "critical",
    },
    "dizziness": {
        "conditions": ["Dehydration", "Anaemia", "Vertigo", "Hypotension"],
        "actions": ["BP sitting/standing", "Blood glucose if available", "Hydration"],
        "urgency": "moderate",
    },
    "body_aches": {
        "conditions": ["Malaria", "Flu", "Dengue", "Overexertion"],
        "actions": ["Temperature check", "Malaria RDT", "Joint examination"],
        "urgency": "low",
    },
    "runny_nose": {
        "conditions": ["Common cold", "Allergic rhinitis", "Sinusitis"],
        "actions": ["Nasal examination", "Allergy history"],
        "urgency": "routine",
    },
    "rash": {
        "conditions": ["Allergic reaction", "Measles", "Dermatitis", "Drug eruption"],
        "actions": ["Distribution pattern", "Recent medications", "Itch assessment"],
        "urgency": "moderate",
    },
    "diarrhoea": {
        "conditions": ["Gastroenteritis", "Cholera (if outbreak)", "Food poisoning"],
        "actions": ["Hydration status", "Stool frequency", "Blood in stool?"],
        "urgency": "moderate",
    },
    "ear_pain": {
        "conditions": ["Otitis media", "Ear wax impaction", "Swimmer's ear"],
        "actions": ["Otoscopic exam", "Fever check"],
        "urgency": "low",
    },
    "eye_irritation": {
        "conditions": ["Conjunctivitis", "Foreign body", "Allergic conjunctivitis"],
        "actions": ["Eye examination", "Discharge type", "Vision check"],
        "urgency": "low",
    },
    "fatigue": {
        "conditions": ["Anaemia", "Malaria", "Depression", "Chronic illness"],
        "actions": ["Hb if available", "Sleep pattern", "Malaria RDT"],
        "urgency": "low",
    },
    "back_pain": {
        "conditions": ["Muscle strain", "UTI", "Kidney stones", "Disc problem"],
        "actions": ["Urinary symptoms?", "Neurological exam", "Pain radiation"],
        "urgency": "low",
    },
    "injury_trauma": {
        "conditions": ["Sprain", "Fracture", "Laceration", "Contusion"],
        "actions": ["Wound assessment", "Neurovascular check", "X-ray if indicated"],
        "urgency": "moderate",
    },
    "allergic_reaction": {
        "conditions": ["Urticaria", "Anaphylaxis", "Drug allergy", "Food allergy"],
        "actions": ["Airway assessment", "Antihistamine ready", "Epi if anaphylaxis"],
        "urgency": "high",
    },
    "chills": {
        "conditions": ["Malaria", "Sepsis", "Flu", "UTI"],
        "actions": ["Temperature", "Malaria RDT", "Blood culture if febrile"],
        "urgency": "moderate",
    },
}

URGENCY_RANK = {"routine": 0, "low": 1, "moderate": 2, "high": 3, "critical": 4}

MEDICATION_SUGGESTIONS = {
    "Malaria": [
        {"name": "Artemether-Lumefantrine", "dosage": "4 tablets twice daily for 3 days"},
        {"name": "Paracetamol", "dosage": "1g every 6 hours as needed for fever"},
    ],
    "Upper respiratory infection": [
        {"name": "Paracetamol", "dosage": "1g every 6 hours for fever/pain"},
        {"name": "Amoxicillin", "dosage": "500mg three times daily for 5 days if bacterial"},
    ],
    "Gastroenteritis": [
        {"name": "Oral Rehydration Salts", "dosage": "As directed until hydrated"},
        {"name": "Paracetamol", "dosage": "1g every 6 hours if fever present"},
    ],
    "Tension headache": [
        {"name": "Paracetamol", "dosage": "1g every 6 hours as needed"},
        {"name": "Ibuprofen", "dosage": "400mg every 8 hours with food"},
    ],
    "Pharyngitis": [
        {"name": "Paracetamol", "dosage": "1g every 6 hours"},
        {"name": "Amoxicillin", "dosage": "500mg three times daily for 7 days if bacterial"},
    ],
    "Common cold": [
        {"name": "Paracetamol", "dosage": "1g every 6 hours for symptoms"},
    ],
    "Musculoskeletal pain": [
        {"name": "Ibuprofen", "dosage": "400mg every 8 hours with food"},
        {"name": "Paracetamol", "dosage": "1g every 6 hours"},
    ],
    "Allergic reaction": [
        {"name": "Chlorpheniramine", "dosage": "4mg every 6 hours"},
        {"name": "Hydrocortisone cream", "dosage": "Apply to affected area twice daily"},
    ],
}


def _merge_conditions(symptoms):
    conditions = []
    actions = []
    max_urgency = "routine"
    for symptom in symptoms or []:
        knowledge = SYMPTOM_KNOWLEDGE.get(symptom, {})
        for cond in knowledge.get("conditions", []):
            if cond not in conditions:
                conditions.append(cond)
        for action in knowledge.get("actions", []):
            if action not in actions:
                actions.append(action)
        hint = knowledge.get("urgency", "routine")
        if URGENCY_RANK.get(hint, 0) > URGENCY_RANK.get(max_urgency, 0):
            max_urgency = hint
    return conditions[:5], actions[:6], max_urgency


def get_triage_recommendations(*, symptoms, pain_level=0, chief_complaint="", vitals=None):
    conditions, actions, urgency_hint = _merge_conditions(symptoms)
    vitals = vitals or {}

    if pain_level >= 8:
        urgency_hint = "high" if urgency_hint != "critical" else urgency_hint
    if pain_level >= 9:
        urgency_hint = "critical"

    confidence = min(95, 55 + len(symptoms) * 8 + (10 if pain_level >= 5 else 0))

    summary_parts = []
    if symptoms:
        summary_parts.append(f"Patient reports {len(symptoms)} symptom(s)")
    if pain_level:
        summary_parts.append(f"pain level {pain_level}/10")
    if chief_complaint:
        summary_parts.append(f"chief concern: {chief_complaint}")

    return {
        "type": "triage",
        "summary": "AI analysis: " + (". ".join(summary_parts) + "." if summary_parts else "Limited data available."),
        "possible_conditions": conditions or ["Further assessment needed"],
        "recommended_actions": actions or ["Complete vital signs", "Full patient history"],
        "suggested_urgency": urgency_hint,
        "confidence": confidence,
        "disclaimer": "AI-assisted suggestion only. Clinical judgment required.",
    }


def get_diagnosis_recommendations(*, symptoms, pain_level=0, chief_complaint="", triage_score=0, urgency="routine"):
    conditions, actions, _ = _merge_conditions(symptoms)

    differential = []
    for i, cond in enumerate(conditions[:4]):
        likelihood = "high" if i == 0 else "moderate" if i < 3 else "low"
        differential.append({"condition": cond, "likelihood": likelihood})

    medications = []
    seen = set()
    for cond in conditions[:3]:
        for med in MEDICATION_SUGGESTIONS.get(cond, []):
            key = med["name"]
            if key not in seen:
                seen.add(key)
                medications.append({**med, "for_condition": cond})

    suggested_tests = []
    symptom_set = set(symptoms or [])
    if "fever" in symptom_set or "chills" in symptom_set or "body_aches" in symptom_set:
        suggested_tests.append("Malaria Rapid Diagnostic Test")
    if "chest_pain" in symptom_set or "difficulty_breathing" in symptom_set:
        suggested_tests.append("ECG / Chest X-ray if available")
    if "difficulty_breathing" in symptom_set:
        suggested_tests.append("Pulse oximetry (SpO2)")
    if not suggested_tests:
        suggested_tests.append("Basic vital signs review")

    return {
        "type": "diagnosis",
        "summary": f"Based on {len(symptoms)} reported symptoms, triage score {triage_score}, urgency {urgency}.",
        "differential_diagnosis": differential or [{"condition": "Clinical assessment required", "likelihood": "moderate"}],
        "suggested_tests": suggested_tests,
        "recommended_medications": medications[:5],
        "clinical_notes": actions[:4],
        "confidence": min(92, 50 + len(symptoms) * 7 + triage_score * 2),
        "disclaimer": "AI-assisted suggestion only. Final diagnosis by attending physician.",
    }
