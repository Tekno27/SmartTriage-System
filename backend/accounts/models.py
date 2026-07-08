import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student / Patient"
        NURSE = "nurse", "Nurse"
        DOCTOR = "doctor", "Doctor"
        ADMIN = "admin", "Administrator"
        RECEPTIONIST = "receptionist", "Receptionist"
        PHARMACIST = "pharmacist", "Pharmacist"
        LAB_TECH = "lab_technician", "Lab Technician"
        RADIOLOGIST = "radiologist", "Radiologist"
        ACCOUNTANT = "accountant", "Accountant"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    student_id = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    employee_id = models.CharField(max_length=30, blank=True)
    department = models.ForeignKey(
        "hospital.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff",
    )
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        ordering = ["last_name", "first_name"]

    @property
    def full_name(self):
        return self.get_full_name() or self.username

    def __str__(self):
        return f"{self.full_name} ({self.role})"
