from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsClinicalOrRadiologist, IsRadiologist

from .models import ImagingOrder, ImagingType
from .serializers import ImagingOrderSerializer, ImagingTypeSerializer


class ImagingTypeListView(generics.ListAPIView):
    queryset = ImagingType.objects.filter(is_active=True)
    serializer_class = ImagingTypeSerializer
    permission_classes = [IsClinicalOrRadiologist]


class ImagingOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = ImagingOrderSerializer
    permission_classes = [IsClinicalOrRadiologist]

    def get_queryset(self):
        qs = ImagingOrder.objects.select_related("patient", "imaging_type", "ordered_by")
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def perform_create(self, serializer):
        serializer.save(ordered_by=self.request.user)


class ImagingReportView(APIView):
    permission_classes = [IsRadiologist]

    def post(self, request, pk):
        try:
            order = ImagingOrder.objects.get(pk=pk)
        except ImagingOrder.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        order.findings = request.data.get("findings", "")
        order.impression = request.data.get("impression", "")
        order.status = ImagingOrder.Status.COMPLETED
        order.reported_by = request.user
        order.reported_at = timezone.now()
        order.save()
        return Response(ImagingOrderSerializer(order).data)
