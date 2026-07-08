from rest_framework import serializers

from .models import DispenseRecord, Medication, MedicationBatch, Prescription


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["id", "name", "generic_name", "unit", "description", "is_active"]


class MedicationBatchSerializer(serializers.ModelSerializer):
    medication = MedicationSerializer(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = MedicationBatch
        fields = [
            "id",
            "medication",
            "batch_number",
            "expiry_date",
            "quantity_on_hand",
            "is_expired",
            "received_at",
        ]


class PrescriptionSerializer(serializers.ModelSerializer):
    medication = MedicationSerializer(read_only=True)
    medication_id = serializers.PrimaryKeyRelatedField(
        queryset=Medication.objects.all(),
        source="medication",
        write_only=True,
    )

    class Meta:
        model = Prescription
        fields = [
            "id",
            "visit",
            "medication",
            "medication_id",
            "quantity_prescribed",
            "dosage_instructions",
            "prescribed_by",
            "is_dispensed",
            "created_at",
        ]
        read_only_fields = ["id", "medication", "prescribed_by", "is_dispensed", "created_at"]
