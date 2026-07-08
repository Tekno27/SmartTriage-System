from rest_framework import serializers

from .models import NHISClaim


class NHISClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = NHISClaim
        fields = [
            "id",
            "visit",
            "patient_nhis_number",
            "claim_number",
            "consultation_fee",
            "medication_cost",
            "lab_cost",
            "total_amount",
            "nhis_coverage",
            "patient_copay",
            "status",
            "diagnosis_code",
            "notes",
            "submitted_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "claim_number",
            "total_amount",
            "nhis_coverage",
            "patient_copay",
            "submitted_by",
            "created_at",
            "updated_at",
        ]
