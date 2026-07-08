from rest_framework import generics

from accounts.permissions import IsPharmacist, IsStaff

from .models import StockMovement, SupplyItem
from .serializers import StockMovementSerializer, SupplyItemSerializer


class SupplyItemListView(generics.ListAPIView):
    queryset = SupplyItem.objects.filter(is_active=True).select_related("category")
    serializer_class = SupplyItemSerializer
    permission_classes = [IsStaff]


class StockMovementListCreateView(generics.ListCreateAPIView):
    serializer_class = StockMovementSerializer
    permission_classes = [IsPharmacist]

    def get_queryset(self):
        return StockMovement.objects.select_related("item", "performed_by").order_by("-created_at")[:50]

    def perform_create(self, serializer):
        movement = serializer.save(performed_by=self.request.user)
        item = movement.item
        if movement.batch:
            batch = movement.batch
            if movement.movement_type == "in":
                batch.quantity_on_hand += movement.quantity
            elif movement.movement_type == "out":
                batch.quantity_on_hand = max(0, batch.quantity_on_hand - movement.quantity)
            batch.save()
