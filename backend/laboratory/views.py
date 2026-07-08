from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsClinicalOrLab, IsLabTech

from .models import LabOrder, LabOrderItem, LabTest
from .serializers import LabOrderSerializer, LabTestSerializer


class LabTestListView(generics.ListAPIView):
    queryset = LabTest.objects.filter(is_active=True)
    serializer_class = LabTestSerializer
    permission_classes = [IsClinicalOrLab]


class LabOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = LabOrderSerializer
    permission_classes = [IsClinicalOrLab]

    def get_queryset(self):
        qs = LabOrder.objects.select_related("patient", "ordered_by").prefetch_related("items__test")
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def perform_create(self, serializer):
        test_ids = serializer.validated_data.pop("test_ids", [])
        order = serializer.save(ordered_by=self.request.user)
        for tid in test_ids:
            LabOrderItem.objects.create(order=order, test_id=tid)


class LabResultEntryView(APIView):
    permission_classes = [IsLabTech]

    def post(self, request, pk):
        try:
            item = LabOrderItem.objects.select_related("order").get(pk=pk)
        except LabOrderItem.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        item.result_value = request.data.get("result_value", "")
        item.is_abnormal = request.data.get("is_abnormal", False)
        item.notes = request.data.get("notes", "")
        item.resulted_by = request.user
        item.resulted_at = timezone.now()
        item.save()
        order = item.order
        if not order.items.filter(result_value="").exists():
            order.status = LabOrder.Status.COMPLETED
            order.completed_at = timezone.now()
            order.save()
        return Response({"detail": "Result saved."})
