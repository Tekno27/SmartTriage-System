from decimal import Decimal

from django.conf import settings
from django.db import models


class NHISClaim(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        PAID = "paid", "Paid"

    visit = models.OneToOneField("visits.Visit", on_delete=models.CASCADE, related_name="nhis_claim")
    patient_nhis_number = models.CharField(max_length=30)
    claim_number = models.CharField(max_length=40, unique=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("25.00"))
    medication_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    lab_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    nhis_coverage = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    patient_copay = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    diagnosis_code = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="submitted_claims",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def calculate_totals(self):
        self.total_amount = self.consultation_fee + self.medication_cost + self.lab_cost
        self.nhis_coverage = (self.total_amount * Decimal("0.70")).quantize(Decimal("0.01"))
        self.patient_copay = self.total_amount - self.nhis_coverage

    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Claim {self.claim_number} — {self.status}"
