from django.conf import settings
from django.db import models


class Visit(models.Model):
    class Status(models.TextChoices):
        CHECKED_IN = "checked_in", "Checked In"
        TRIAGED = "triaged", "Triaged"
        WAITING = "waiting", "Waiting for Doctor"
        IN_CONSULTATION = "in_consultation", "In Consultation"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class Urgency(models.TextChoices):
        ROUTINE = "routine", "Routine"
        LOW = "low", "Low"
        MODERATE = "moderate", "Moderate"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="visits",
    )
    chief_complaint = models.TextField()
    symptoms_description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CHECKED_IN)
    triage_score = models.PositiveSmallIntegerField(default=0)
    urgency = models.CharField(max_length=20, choices=Urgency.choices, default=Urgency.ROUTINE)
    assigned_doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_visits",
    )
    consultation_notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    checked_in_at = models.DateTimeField(auto_now_add=True)
    triaged_at = models.DateTimeField(null=True, blank=True)
    consultation_started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-triage_score", "checked_in_at"]

    def __str__(self):
        return f"Visit #{self.pk} — {self.patient.full_name} ({self.status})"
