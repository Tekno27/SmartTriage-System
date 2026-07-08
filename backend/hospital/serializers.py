from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Bed, Department, Theatre, Ward


class DepartmentSerializer(serializers.ModelSerializer):
    staff_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id", "name", "code", "description", "head", "is_active", "staff_count"]

    def get_staff_count(self, obj):
        return obj.staff.count()


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ["id", "ward", "bed_number", "status", "notes"]


class WardSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    total_beds = serializers.IntegerField(read_only=True)
    available_beds = serializers.IntegerField(read_only=True)
    beds = BedSerializer(many=True, read_only=True)

    class Meta:
        model = Ward
        fields = [
            "id", "name", "department", "department_name", "ward_type",
            "floor", "is_active", "total_beds", "available_beds", "beds",
        ]


class TheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields = ["id", "name", "department", "is_available"]
