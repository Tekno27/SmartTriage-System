from django.conf import settings
from django.db import models


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        INFO = "info", "Info"
        ALERT = "alert", "Alert"
        LAB = "lab", "Lab Result"
        APPOINTMENT = "appointment", "Appointment"
        BILLING = "billing", "Billing"
        INVENTORY = "inventory", "Low Stock"
        ADMISSION = "admission", "Admission"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices, default=NotificationType.INFO)
    link = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} → {self.recipient.username}"
