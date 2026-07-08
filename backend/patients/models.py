from django.conf import settings
from django.db import models


class PatientProfile(models.Model):
    class NHISStatus(models.TextChoices):
        UNKNOWN = "unknown", "Unknown"
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        PENDING = "pending", "Pending Renewal"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )
    date_of_birth = models.DateField(null=True, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=120, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    ghana_card_number = models.CharField(max_length=30, blank=True)
    nhis_number = models.CharField(max_length=30, blank=True)
    nhis_status = models.CharField(
        max_length=20,
        choices=NHISStatus.choices,
        default=NHISStatus.UNKNOWN,
    )
    nhis_expiry_date = models.DateField(null=True, blank=True)
    nhis_verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__last_name", "user__first_name"]

    def __str__(self):
        return f"Profile for {self.user.full_name}"
