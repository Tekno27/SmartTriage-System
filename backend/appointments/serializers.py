from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True, required=False)
    doctor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id", "patient", "doctor", "patient_id", "doctor_id", "department",
            "visit", "scheduled_at", "duration_minutes", "reason", "status",
            "notes", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "patient", "doctor", "visit", "created_at", "updated_at"]
