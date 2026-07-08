import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        NURSE = "nurse", "Nurse"
        DOCTOR = "doctor", "Doctor"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    student_id = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        ordering = ["last_name", "first_name"]

    @property
    def full_name(self):
        return self.get_full_name() or self.username

    def __str__(self):
        return f"{self.full_name} ({self.role})"
