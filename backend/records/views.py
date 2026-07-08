from rest_framework import generics

from accounts.permissions import IsStaff, IsStudent

from .models import MedicalRecord
from .serializers import MedicalRecordSerializer


class MedicalRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsStaff]

    def get_queryset(self):
        qs = MedicalRecord.objects.select_related("patient", "created_by")
        patient = self.request.query_params.get("patient")
        if patient:
            qs = qs.filter(patient_id=patient)
        if self.request.user.role == "student":
            qs = qs.filter(patient=self.request.user)
        return qs

    def get_permissions(self):
        if self.request.method == "GET" and self.request.user.role == "student":
            return [IsStudent()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
