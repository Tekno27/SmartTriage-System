from django.conf import settings
from django.db import models


class SupplyCategory(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SupplyItem(models.Model):
    name = models.CharField(max_length=120)
    sku = models.CharField(max_length=40, unique=True)
    category = models.ForeignKey(SupplyCategory, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.CharField(max_length=30, default="unit")
    reorder_level = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        return sum(b.quantity_on_hand for b in self.batches.all())


class SupplyBatch(models.Model):
    item = models.ForeignKey(SupplyItem, on_delete=models.CASCADE, related_name="batches")
    batch_number = models.CharField(max_length=50)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["expiry_date"]
        unique_together = [("item", "batch_number")]


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = "in", "Stock In"
        OUT = "out", "Stock Out"
        ADJUSTMENT = "adjustment", "Adjustment"

    item = models.ForeignKey(SupplyItem, on_delete=models.CASCADE, related_name="movements")
    batch = models.ForeignKey(SupplyBatch, on_delete=models.SET_NULL, null=True, blank=True)
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
