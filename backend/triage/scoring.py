"""Automated triage scoring from intake vitals and symptoms."""

URGENCY_LEVELS = [
    (0, "routine", "Routine"),
    (1, "low", "Low"),
    (2, "moderate", "Moderate"),
    (3, "high", "High"),
    (4, "critical", "Critical"),
]


def calculate_triage_score(
    *,
    temperature,
    heart_rate,
    systolic_bp,
    pain_level,
    symptoms,
):
    score = 0

    if temperature is not None:
        if temperature >= 39.0:
            score += 3
        elif temperature >= 38.0:
            score += 2
        elif temperature >= 37.5:
            score += 1

    if heart_rate is not None:
        if heart_rate >= 120 or heart_rate <= 50:
            score += 3
        elif heart_rate >= 100 or heart_rate <= 55:
            score += 2
        elif heart_rate >= 90:
            score += 1

    if systolic_bp is not None:
        if systolic_bp >= 180 or systolic_bp <= 90:
            score += 3
        elif systolic_bp >= 160 or systolic_bp <= 100:
            score += 2

    if pain_level is not None:
        if pain_level >= 8:
            score += 3
        elif pain_level >= 5:
            score += 2
        elif pain_level >= 3:
            score += 1

    urgent_symptoms = {
        "chest_pain",
        "difficulty_breathing",
        "severe_bleeding",
        "loss_of_consciousness",
        "seizure",
        "allergic_reaction",
        "injury_trauma",
    }
    moderate_symptoms = {
        "fever", "chills", "stomach_pain", "nausea_vomiting", "diarrhoea", "rash",
    }
    symptom_set = set(symptoms or [])
    score += min(len(symptom_set & urgent_symptoms) * 2, 6)
    score += min(len(symptom_set & moderate_symptoms), 3)

    score = min(score, 10)

    if score >= 8:
        urgency = "critical"
    elif score >= 6:
        urgency = "high"
    elif score >= 4:
        urgency = "moderate"
    elif score >= 2:
        urgency = "low"
    else:
        urgency = "routine"

    return score, urgency
