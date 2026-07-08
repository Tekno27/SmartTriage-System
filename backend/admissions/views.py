from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsNurseOrDoctor, IsStaff
from hospital.models import Bed

from .models import Admission, Surgery
from .serializers import AdmissionSerializer, SurgerySerializer

User = get_user_model()


class AdmissionListCreateView(generics.ListCreateAPIView):
    serializer_class = AdmissionSerializer
    permission_classes = [IsNurseOrDoctor]

    def get_queryset(self):
        qs = Admission.objects.select_related("patient", "ward", "bed", "admitted_by")
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def perform_create(self, serializer):
        bed = Bed.objects.get(pk=serializer.validated_data.pop("bed_id"))
        ward_id = serializer.validated_data.pop("ward_id")
        patient = User.objects.get(pk=serializer.validated_data.pop("patient_id"))
        bed.status = Bed.Status.OCCUPIED
        bed.save()
        serializer.save(patient=patient, ward_id=ward_id, bed=bed, admitted_by=self.request.user)


class AdmissionDischargeView(APIView):
    permission_classes = [IsNurseOrDoctor]

    def post(self, request, pk):
        try:
            admission = Admission.objects.select_related("bed").get(pk=pk)
        except Admission.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        admission.status = Admission.Status.DISCHARGED
        admission.discharged_at = timezone.now()
        admission.discharge_summary = request.data.get("discharge_summary", "")
        admission.bed.status = Bed.Status.AVAILABLE
        admission.bed.save()
        admission.save()
        return Response(AdmissionSerializer(admission).data)


class SurgeryListCreateView(generics.ListCreateAPIView):
    queryset = Surgery.objects.select_related("patient", "surgeon", "theatre")
    serializer_class = SurgerySerializer
    permission_classes = [IsStaff]

    def perform_create(self, serializer):
        patient = User.objects.get(pk=serializer.validated_data.pop("patient_id"))
        surgeon_id = serializer.validated_data.pop("surgeon_id", None)
        surgeon = User.objects.get(pk=surgeon_id) if surgeon_id else self.request.user
        serializer.save(patient=patient, surgeon=surgeon)
