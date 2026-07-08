from django.conf import settings
from django.db import models

from .scoring import calculate_triage_score


class TriageAssessment(models.Model):
    class Urgency(models.TextChoices):
        ROUTINE = "routine", "Routine"
        LOW = "low", "Low"
        MODERATE = "moderate", "Moderate"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    visit = models.OneToOneField(
        "visits.Visit",
        on_delete=models.CASCADE,
        related_name="triage_assessment",
    )
    assessed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="triage_assessments",
    )
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    heart_rate = models.PositiveSmallIntegerField(null=True, blank=True)
    systolic_bp = models.PositiveSmallIntegerField(null=True, blank=True)
    diastolic_bp = models.PositiveSmallIntegerField(null=True, blank=True)
    respiratory_rate = models.PositiveSmallIntegerField(null=True, blank=True)
    oxygen_saturation = models.PositiveSmallIntegerField(null=True, blank=True)
    pain_level = models.PositiveSmallIntegerField(default=0)
    symptoms = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    urgency = models.CharField(max_length=20, choices=Urgency.choices, default=Urgency.ROUTINE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def compute_score(self):
        self.score, self.urgency = calculate_triage_score(
            temperature=float(self.temperature) if self.temperature is not None else None,
            heart_rate=self.heart_rate,
            systolic_bp=self.systolic_bp,
            pain_level=self.pain_level,
            symptoms=self.symptoms,
        )

    def save(self, *args, **kwargs):
        self.compute_score()
        super().save(*args, **kwargs)
        self.visit.triage_score = self.score
        self.visit.urgency = self.urgency
        self.visit.save(update_fields=["triage_score", "urgency", "updated_at"])

    def __str__(self):
        return f"Triage for visit #{self.visit_id} — {self.urgency} ({self.score})"
