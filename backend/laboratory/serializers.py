from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import LabOrder, LabOrderItem, LabTest


class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ["id", "name", "code", "category", "unit", "normal_range", "price", "turnaround_hours", "is_active"]


class LabOrderItemSerializer(serializers.ModelSerializer):
    test = LabTestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(queryset=LabTest.objects.all(), source="test", write_only=True)

    class Meta:
        model = LabOrderItem
        fields = ["id", "test", "test_id", "result_value", "is_abnormal", "notes", "resulted_by", "resulted_at"]
        read_only_fields = ["id", "test", "resulted_by", "resulted_at"]


class LabOrderSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    items = LabOrderItemSerializer(many=True, read_only=True)
    test_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = LabOrder
        fields = [
            "id", "patient", "visit", "ordered_by", "status", "priority",
            "clinical_notes", "items", "test_ids", "ordered_at", "completed_at",
        ]
        read_only_fields = ["id", "patient", "ordered_by", "items", "ordered_at", "completed_at"]
