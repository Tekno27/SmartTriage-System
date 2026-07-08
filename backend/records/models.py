from django.conf import settings
from django.db import models


class MedicalRecord(models.Model):
    class RecordType(models.TextChoices):
        CONSULTATION = "consultation", "Consultation"
        LAB = "lab", "Laboratory"
        IMAGING = "imaging", "Imaging"
        ADMISSION = "admission", "Admission"
        DISCHARGE = "discharge", "Discharge Summary"
        SURGERY = "surgery", "Surgery"
        PRESCRIPTION = "prescription", "Prescription"
        NURSING = "nursing", "Nursing Note"
        GENERAL = "general", "General"

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="medical_records")
    visit = models.ForeignKey("visits.Visit", on_delete=models.SET_NULL, null=True, blank=True)
    record_type = models.CharField(max_length=20, choices=RecordType.choices, default=RecordType.GENERAL)
    title = models.CharField(max_length=200)
    summary = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="records_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.patient.full_name}"
