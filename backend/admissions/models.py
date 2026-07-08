from django.conf import settings
from django.db import models
from django.utils import timezone


class Admission(models.Model):
    class Status(models.TextChoices):
        ADMITTED = "admitted", "Admitted"
        DISCHARGED = "discharged", "Discharged"
        TRANSFERRED = "transferred", "Transferred"

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="admissions")
    visit = models.ForeignKey("visits.Visit", on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey("hospital.Ward", on_delete=models.PROTECT, related_name="admissions")
    bed = models.ForeignKey("hospital.Bed", on_delete=models.PROTECT, related_name="admissions")
    admitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="admissions_made",
    )
    attending_doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attending_admissions",
    )
    diagnosis_on_admission = models.TextField()
    admission_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ADMITTED)
    admitted_at = models.DateTimeField(default=timezone.now)
    discharged_at = models.DateTimeField(null=True, blank=True)
    discharge_summary = models.TextField(blank=True)

    class Meta:
        ordering = ["-admitted_at"]

    def __str__(self):
        return f"Admission #{self.pk} — {self.patient.full_name}"


class Surgery(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="surgeries")
    visit = models.ForeignKey("visits.Visit", on_delete=models.SET_NULL, null=True, blank=True)
    admission = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True)
    surgeon = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="surgeries_performed",
    )
    theatre = models.ForeignKey("hospital.Theatre", on_delete=models.SET_NULL, null=True, blank=True)
    procedure_name = models.CharField(max_length=200)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    pre_op_notes = models.TextField(blank=True)
    post_op_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_at"]
        verbose_name_plural = "surgeries"

    def __str__(self):
        return f"{self.procedure_name} — {self.patient.full_name}"
