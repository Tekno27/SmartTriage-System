from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsReceptionist, IsStaff, IsStudent

from .models import Appointment
from .serializers import AppointmentSerializer

User = get_user_model()


class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsStaff]

    def get_queryset(self):
        qs = Appointment.objects.select_related("patient", "doctor", "department")
        patient = self.request.query_params.get("patient")
        doctor = self.request.query_params.get("doctor")
        status_filter = self.request.query_params.get("status")
        if patient:
            qs = qs.filter(patient_id=patient)
        if doctor:
            qs = qs.filter(doctor_id=doctor)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if self.request.user.role == "student":
            qs = qs.filter(patient=self.request.user)
        return qs

    def get_permissions(self):
        if self.request.user.role == "student":
            return [permissions.IsAuthenticated()]
        return [IsStaff()]

    def perform_create(self, serializer):
        patient_id = serializer.validated_data.pop("patient_id", None)
        doctor_id = serializer.validated_data.pop("doctor_id")
        patient = User.objects.get(pk=patient_id) if patient_id else self.request.user
        doctor = User.objects.get(pk=doctor_id)
        serializer.save(patient=patient, doctor=doctor, created_by=self.request.user)


class AppointmentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.select_related("patient", "doctor")
    serializer_class = AppointmentSerializer
    permission_classes = [IsStaff]


class AppointmentConfirmView(APIView):
    permission_classes = [IsReceptionist]

    def post(self, request, pk):
        try:
            appt = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        appt.status = Appointment.Status.CONFIRMED
        appt.save()
        return Response(AppointmentSerializer(appt).data)
