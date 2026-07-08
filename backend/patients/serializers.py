from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import PatientProfile


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            "id",
            "user",
            "date_of_birth",
            "blood_type",
            "allergies",
            "chronic_conditions",
            "emergency_contact",
            "emergency_phone",
            "nhis_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
