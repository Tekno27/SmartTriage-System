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
            "queue_number",
            "patient",
            "chief_complaint",
            "symptoms",
            "symptoms_description",
            "pain_level",
            "nhis_verified",
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
            "queue_number",
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
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    student_id = serializers.CharField(write_only=True, required=False)
    ghana_card_number = serializers.CharField(write_only=True, required=False)
    nhis_number = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Visit
        fields = [
            "symptoms",
            "pain_level",
            "symptoms_description",
            "first_name",
            "last_name",
            "student_id",
            "ghana_card_number",
            "nhis_number",
        ]


class VisitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ["status", "consultation_notes", "diagnosis"]
