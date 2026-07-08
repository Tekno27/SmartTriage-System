from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import MedicalRecord


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = MedicalRecord
        fields = [
            "id", "patient", "visit", "record_type", "title", "summary",
            "created_by", "created_by_name", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "patient", "created_by", "created_by_name", "created_at", "updated_at"]
