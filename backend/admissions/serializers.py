from rest_framework import serializers

from accounts.serializers import UserSerializer
from hospital.serializers import BedSerializer, WardSerializer

from .models import Admission, Surgery


class AdmissionSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    ward = WardSerializer(read_only=True)
    bed = BedSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    ward_id = serializers.IntegerField(write_only=True)
    bed_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Admission
        fields = [
            "id", "patient", "patient_id", "visit", "ward", "ward_id", "bed", "bed_id",
            "admitted_by", "attending_doctor", "diagnosis_on_admission", "admission_notes",
            "status", "admitted_at", "discharged_at", "discharge_summary",
        ]
        read_only_fields = ["id", "patient", "ward", "bed", "admitted_by", "admitted_at", "discharged_at"]


class SurgerySerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    surgeon_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Surgery
        fields = [
            "id", "patient", "patient_id", "visit", "admission", "surgeon", "surgeon_id",
            "theatre", "procedure_name", "scheduled_at", "duration_minutes", "status",
            "pre_op_notes", "post_op_notes", "created_at",
        ]
        read_only_fields = ["id", "patient", "surgeon", "created_at"]
