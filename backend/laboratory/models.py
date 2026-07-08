from django.conf import settings
from django.db import models


class LabTest(models.Model):
    class Category(models.TextChoices):
        HEMATOLOGY = "hematology", "Hematology"
        BIOCHEMISTRY = "biochemistry", "Biochemistry"
        MICROBIOLOGY = "microbiology", "Microbiology"
        SEROLOGY = "serology", "Serology"
        URINALYSIS = "urinalysis", "Urinalysis"
        PARASITOLOGY = "parasitology", "Parasitology"

    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    unit = models.CharField(max_length=30, blank=True)
    normal_range = models.CharField(max_length=80, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    turnaround_hours = models.PositiveSmallIntegerField(default=24)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.code} — {self.name}"


class LabOrder(models.Model):
    class Status(models.TextChoices):
        ORDERED = "ordered", "Ordered"
        COLLECTED = "collected", "Sample Collected"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class Priority(models.TextChoices):
        ROUTINE = "routine", "Routine"
        URGENT = "urgent", "Urgent"
        STAT = "stat", "STAT"

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lab_orders")
    visit = models.ForeignKey("visits.Visit", on_delete=models.CASCADE, related_name="lab_orders")
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="lab_orders_placed",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ORDERED)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.ROUTINE)
    clinical_notes = models.TextField(blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-ordered_at"]

    def __str__(self):
        return f"Lab Order #{self.pk} — {self.patient.full_name}"


class LabOrderItem(models.Model):
    order = models.ForeignKey(LabOrder, on_delete=models.CASCADE, related_name="items")
    test = models.ForeignKey(LabTest, on_delete=models.PROTECT)
    result_value = models.CharField(max_length=100, blank=True)
    is_abnormal = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    resulted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lab_results_entered",
    )
    resulted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("order", "test")]

    def __str__(self):
        return f"{self.test.name} for order #{self.order_id}"
