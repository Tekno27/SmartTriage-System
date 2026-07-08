from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_departments",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ward(models.Model):
    class WardType(models.TextChoices):
        GENERAL = "general", "General"
        ICU = "icu", "ICU"
        MATERNITY = "maternity", "Maternity"
        PEDIATRIC = "pediatric", "Pediatric"
        EMERGENCY = "emergency", "Emergency"
        SURGICAL = "surgical", "Surgical"
        ISOLATION = "isolation", "Isolation"

    name = models.CharField(max_length=120)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="wards")
    ward_type = models.CharField(max_length=20, choices=WardType.choices, default=WardType.GENERAL)
    floor = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.department.code})"

    @property
    def total_beds(self):
        return self.beds.count()

    @property
    def available_beds(self):
        return self.beds.filter(status=Bed.Status.AVAILABLE).count()


class Bed(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        OCCUPIED = "occupied", "Occupied"
        MAINTENANCE = "maintenance", "Maintenance"
        RESERVED = "reserved", "Reserved"

    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="beds")
    bed_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["ward", "bed_number"]
        unique_together = [("ward", "bed_number")]

    def __str__(self):
        return f"{self.ward.name} — Bed {self.bed_number}"


class Theatre(models.Model):
    name = models.CharField(max_length=80)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="theatres")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
