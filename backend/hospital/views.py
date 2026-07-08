from django.db.models import Count, Q
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsStaff
from admissions.models import Admission, Surgery
from appointments.models import Appointment
from billing.models import Invoice, NHISClaim, Payment
from inventory.models import SupplyItem
from laboratory.models import LabOrder
from radiology.models import ImagingOrder
from visits.models import Visit

from .models import Bed, Department, Theatre, Ward
from .serializers import BedSerializer, DepartmentSerializer, TheatreSerializer, WardSerializer


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer
    permission_classes = [IsStaff]


class WardListView(generics.ListAPIView):
    queryset = Ward.objects.filter(is_active=True).select_related("department").prefetch_related("beds")
    serializer_class = WardSerializer
    permission_classes = [IsStaff]


class BedListView(generics.ListAPIView):
    serializer_class = BedSerializer
    permission_classes = [IsStaff]

    def get_queryset(self):
        qs = Bed.objects.select_related("ward")
        ward = self.request.query_params.get("ward")
        status = self.request.query_params.get("status")
        if ward:
            qs = qs.filter(ward_id=ward)
        if status:
            qs = qs.filter(status=status)
        return qs


class TheatreListView(generics.ListAPIView):
    queryset = Theatre.objects.select_related("department")
    serializer_class = TheatreSerializer
    permission_classes = [IsStaff]


class HospitalOverviewView(APIView):
    permission_classes = [IsStaff]

    def get(self, request):
        today_visits = Visit.objects.exclude(status__in=["completed", "cancelled"]).count()
        return Response({
            "departments": Department.objects.filter(is_active=True).count(),
            "wards": Ward.objects.filter(is_active=True).count(),
            "total_beds": Bed.objects.count(),
            "available_beds": Bed.objects.filter(status=Bed.Status.AVAILABLE).count(),
            "occupied_beds": Bed.objects.filter(status=Bed.Status.OCCUPIED).count(),
            "active_admissions": Admission.objects.filter(status=Admission.Status.ADMITTED).count(),
            "today_appointments": Appointment.objects.filter(status__in=["scheduled", "confirmed"]).count(),
            "pending_lab_orders": LabOrder.objects.exclude(status__in=["completed", "cancelled"]).count(),
            "pending_imaging": ImagingOrder.objects.exclude(status__in=["completed", "cancelled"]).count(),
            "active_visits": today_visits,
            "pending_invoices": Invoice.objects.filter(status__in=["draft", "sent", "partial", "overdue"]).count(),
            "low_stock_items": SupplyItem.objects.filter(is_active=True).annotate(
                stock=Count("batches")
            ).count(),  # simplified
            "scheduled_surgeries": Surgery.objects.filter(status=Surgery.Status.SCHEDULED).count(),
            "nhis_claims_pending": NHISClaim.objects.filter(status__in=["draft", "submitted"]).count(),
        })
