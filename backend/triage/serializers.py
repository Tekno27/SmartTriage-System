from rest_framework import serializers

from .models import TriageAssessment


class TriageAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriageAssessment
        fields = [
            "id",
            "visit",
            "assessed_by",
            "temperature",
            "heart_rate",
            "systolic_bp",
            "diastolic_bp",
            "respiratory_rate",
            "oxygen_saturation",
            "pain_level",
            "symptoms",
            "notes",
            "score",
            "urgency",
            "created_at",
        ]
        read_only_fields = ["id", "assessed_by", "score", "urgency", "created_at"]
