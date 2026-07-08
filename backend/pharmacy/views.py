from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsClinicalOrPharmacist, IsDoctor

from .models import FEFODispenser, Medication, MedicationBatch, Prescription
from .serializers import (
    MedicationBatchSerializer,
    MedicationSerializer,
    PrescriptionSerializer,
)


class MedicationListView(generics.ListAPIView):
    queryset = Medication.objects.filter(is_active=True)
    serializer_class = MedicationSerializer
    permission_classes = [IsClinicalOrPharmacist]


class MedicationBatchListView(generics.ListAPIView):
    queryset = MedicationBatch.objects.select_related("medication")
    serializer_class = MedicationBatchSerializer
    permission_classes = [IsClinicalOrPharmacist]


class PrescriptionCreateView(generics.CreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsDoctor]

    def perform_create(self, serializer):
        serializer.save(prescribed_by=self.request.user)


class PrescriptionListView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsClinicalOrPharmacist]

    def get_queryset(self):
        queryset = Prescription.objects.select_related("medication", "visit", "prescribed_by")
        visit_id = self.request.query_params.get("visit")
        if visit_id:
            queryset = queryset.filter(visit_id=visit_id)
        return queryset


class DispensePrescriptionView(APIView):
    permission_classes = [IsClinicalOrPharmacist]

    def post(self, request, pk):
        try:
            prescription = Prescription.objects.select_related("medication").get(pk=pk)
        except Prescription.DoesNotExist:
            return Response({"detail": "Prescription not found."}, status=status.HTTP_404_NOT_FOUND)

        if prescription.is_dispensed:
            return Response({"detail": "Already dispensed."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            records = FEFODispenser.dispense(prescription, request.user)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "prescription": PrescriptionSerializer(prescription).data,
                "dispensed_batches": [
                    {"batch": r.batch.batch_number, "quantity": r.quantity, "expiry": r.batch.expiry_date}
                    for r in records
                ],
            }
        )
