from django.conf import settings
from django.db import models
from django.utils import timezone

from triage.scoring import calculate_triage_score


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
    queue_number = models.CharField(max_length=10, blank=True)
    chief_complaint = models.TextField(blank=True)
    symptoms = models.JSONField(default=list, blank=True)
    symptoms_description = models.TextField(blank=True)
    pain_level = models.PositiveSmallIntegerField(default=0)
    nhis_verified = models.BooleanField(default=False)
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

    @staticmethod
    def generate_queue_number(urgency: str) -> str:
        prefix_map = {
            "critical": "C",
            "high": "H",
            "moderate": "M",
            "low": "L",
            "routine": "R",
        }
        prefix = prefix_map.get(urgency, "R")
        today = timezone.now().date()
        count = (
            Visit.objects.filter(checked_in_at__date=today, queue_number__startswith=prefix).count()
            + 1
        )
        return f"{prefix}{count:03d}"

    def apply_initial_triage(self):
        score, urgency = calculate_triage_score(
            temperature=None,
            heart_rate=None,
            systolic_bp=None,
            pain_level=self.pain_level,
            symptoms=self.symptoms,
        )
        self.triage_score = score
        self.urgency = urgency
        if not self.queue_number:
            self.queue_number = self.generate_queue_number(urgency)

    def save(self, *args, **kwargs):
        if not self.chief_complaint and self.symptoms:
            labels = [s.replace("_", " ").title() for s in self.symptoms[:3]]
            self.chief_complaint = ", ".join(labels)
        super().save(*args, **kwargs)
