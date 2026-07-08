from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Visit


class VisitSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    assigned_doctor = UserSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = [
            "id",
            "patient",
            "chief_complaint",
            "symptoms_description",
            "status",
            "triage_score",
            "urgency",
            "assigned_doctor",
            "consultation_notes",
            "diagnosis",
            "checked_in_at",
            "triaged_at",
            "consultation_started_at",
            "completed_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "patient",
            "triage_score",
            "urgency",
            "assigned_doctor",
            "checked_in_at",
            "triaged_at",
            "consultation_started_at",
            "completed_at",
            "updated_at",
        ]


class VisitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ["chief_complaint", "symptoms_description"]


class VisitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ["status", "consultation_notes", "diagnosis"]
