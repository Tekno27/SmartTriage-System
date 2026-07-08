from django.db import models, transaction
from django.utils import timezone


class Medication(models.Model):
    name = models.CharField(max_length=120)
    generic_name = models.CharField(max_length=120, blank=True)
    unit = models.CharField(max_length=30, default="tablet")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MedicationBatch(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name="batches")
    batch_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    quantity_on_hand = models.PositiveIntegerField(default=0)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["expiry_date", "received_at"]
        unique_together = [("medication", "batch_number")]

    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    def __str__(self):
        return f"{self.medication.name} — batch {self.batch_number}"


class Prescription(models.Model):
    visit = models.ForeignKey("visits.Visit", on_delete=models.CASCADE, related_name="prescriptions")
    medication = models.ForeignKey(Medication, on_delete=models.PROTECT)
    quantity_prescribed = models.PositiveIntegerField()
    dosage_instructions = models.TextField()
    prescribed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="prescriptions",
    )
    is_dispensed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.medication.name} for visit #{self.visit_id}"


class DispenseRecord(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="dispenses")
    batch = models.ForeignKey(MedicationBatch, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    dispensed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="dispenses",
    )
    dispensed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-dispensed_at"]


class FEFODispenser:
    """First-Expired-First-Out medication dispensing."""

    @staticmethod
    @transaction.atomic
    def dispense(prescription, dispensed_by, quantity=None):
        qty_needed = quantity or prescription.quantity_prescribed
        batches = (
            MedicationBatch.objects.select_for_update()
            .filter(
                medication=prescription.medication,
                quantity_on_hand__gt=0,
                expiry_date__gte=timezone.now().date(),
            )
            .order_by("expiry_date", "received_at")
        )

        records = []
        remaining = qty_needed

        for batch in batches:
            if remaining <= 0:
                break
            take = min(batch.quantity_on_hand, remaining)
            batch.quantity_on_hand -= take
            batch.save(update_fields=["quantity_on_hand"])
            records.append(
                DispenseRecord.objects.create(
                    prescription=prescription,
                    batch=batch,
                    quantity=take,
                    dispensed_by=dispensed_by,
                )
            )
            remaining -= take

        if remaining > 0:
            raise ValueError(
                f"Insufficient stock for {prescription.medication.name}. "
                f"Short by {remaining} {prescription.medication.unit}(s)."
            )

        prescription.is_dispensed = True
        prescription.save(update_fields=["is_dispensed"])
        return records
