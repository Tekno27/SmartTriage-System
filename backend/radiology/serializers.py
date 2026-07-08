from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import ImagingOrder, ImagingType


class ImagingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagingType
        fields = ["id", "name", "code", "modality", "body_part", "price", "is_active"]


class ImagingOrderSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    imaging_type = ImagingTypeSerializer(read_only=True)
    imaging_type_id = serializers.PrimaryKeyRelatedField(queryset=ImagingType.objects.all(), source="imaging_type", write_only=True)

    class Meta:
        model = ImagingOrder
        fields = [
            "id", "patient", "visit", "imaging_type", "imaging_type_id", "ordered_by",
            "status", "clinical_indication", "findings", "impression", "reported_by",
            "ordered_at", "reported_at",
        ]
        read_only_fields = ["id", "patient", "imaging_type", "ordered_by", "reported_by", "ordered_at", "reported_at"]
