from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsDoctor, IsNurse, IsNurseOrDoctor, IsStudent
from patients.models import PatientProfile

from .models import Visit
from .serializers import VisitCreateSerializer, VisitSerializer, VisitUpdateSerializer


class VisitCheckInView(generics.CreateAPIView):
    serializer_class = VisitCreateSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        PatientProfile.objects.get_or_create(user=self.request.user)
        serializer.save(patient=self.request.user, status=Visit.Status.CHECKED_IN)


class VisitQueueView(generics.ListAPIView):
    serializer_class = VisitSerializer
    permission_classes = [IsNurseOrDoctor]

    def get_queryset(self):
        statuses = self.request.query_params.get("status")
        queryset = Visit.objects.select_related("patient", "assigned_doctor")
        if statuses:
            queryset = queryset.filter(status__in=statuses.split(","))
        else:
            queryset = queryset.exclude(status__in=[Visit.Status.COMPLETED, Visit.Status.CANCELLED])
        return queryset


class VisitDetailView(generics.RetrieveUpdateAPIView):
    queryset = Visit.objects.select_related("patient", "assigned_doctor")
    permission_classes = [IsNurseOrDoctor]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return VisitUpdateSerializer
        return VisitSerializer


class VisitStartConsultationView(APIView):
    permission_classes = [IsDoctor]

    def post(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            return Response({"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND)

        visit.status = Visit.Status.IN_CONSULTATION
        visit.assigned_doctor = request.user
        visit.consultation_started_at = timezone.now()
        visit.save()
        return Response(VisitSerializer(visit).data)


class VisitCompleteView(APIView):
    permission_classes = [IsDoctor]

    def post(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk, assigned_doctor=request.user)
        except Visit.DoesNotExist:
            return Response({"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND)

        visit.status = Visit.Status.COMPLETED
        visit.completed_at = timezone.now()
        visit.diagnosis = request.data.get("diagnosis", visit.diagnosis)
        visit.consultation_notes = request.data.get("consultation_notes", visit.consultation_notes)
        visit.save()
        return Response(VisitSerializer(visit).data)


class NurseMarkTriagedView(APIView):
    permission_classes = [IsNurse]

    def post(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            return Response({"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND)

        visit.status = Visit.Status.WAITING
        visit.triaged_at = timezone.now()
        visit.save()
        return Response(VisitSerializer(visit).data)
