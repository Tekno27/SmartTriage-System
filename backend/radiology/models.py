from django.conf import settings
from django.db import models


class ImagingType(models.Model):
    class Modality(models.TextChoices):
        XRAY = "xray", "X-Ray"
        ULTRASOUND = "ultrasound", "Ultrasound"
        CT = "ct", "CT Scan"
        MRI = "mri", "MRI"
        MAMMOGRAPHY = "mammography", "Mammography"

    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    modality = models.CharField(max_length=20, choices=Modality.choices)
    body_part = models.CharField(max_length=80, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["modality", "name"]

    def __str__(self):
        return self.name


class ImagingOrder(models.Model):
    class Status(models.TextChoices):
        ORDERED = "ordered", "Ordered"
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="imaging_orders")
    visit = models.ForeignKey("visits.Visit", on_delete=models.CASCADE, related_name="imaging_orders")
    imaging_type = models.ForeignKey(ImagingType, on_delete=models.PROTECT)
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="imaging_orders_placed",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ORDERED)
    clinical_indication = models.TextField()
    findings = models.TextField(blank=True)
    impression = models.TextField(blank=True)
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="imaging_reports",
    )
    ordered_at = models.DateTimeField(auto_now_add=True)
    reported_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-ordered_at"]

    def __str__(self):
        return f"{self.imaging_type.name} — {self.patient.full_name}"
