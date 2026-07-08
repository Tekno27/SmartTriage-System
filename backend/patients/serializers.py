from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import PatientProfile


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    student_id = serializers.CharField(source="user.student_id", required=False)

    class Meta:
        model = PatientProfile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "student_id",
            "date_of_birth",
            "blood_type",
            "allergies",
            "chronic_conditions",
            "emergency_contact",
            "emergency_phone",
            "ghana_card_number",
            "nhis_number",
            "nhis_status",
            "nhis_expiry_date",
            "nhis_verified_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "nhis_status",
            "nhis_expiry_date",
            "nhis_verified_at",
            "created_at",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user
        if "first_name" in user_data:
            user.first_name = user_data["first_name"]
        if "last_name" in user_data:
            user.last_name = user_data["last_name"]
        if "student_id" in user_data:
            user.student_id = user_data["student_id"]
        user.save()
        return super().update(instance, validated_data)
