from rest_framework import serializers

from .models import StockMovement, SupplyBatch, SupplyCategory, SupplyItem


class SupplyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyCategory
        fields = ["id", "name", "description"]


class SupplyBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyBatch
        fields = ["id", "item", "batch_number", "quantity_on_hand", "expiry_date", "received_at"]


class SupplyItemSerializer(serializers.ModelSerializer):
    total_stock = serializers.IntegerField(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = SupplyItem
        fields = [
            "id", "name", "sku", "category", "category_name", "unit",
            "reorder_level", "total_stock", "is_low_stock", "is_active",
        ]

    def get_is_low_stock(self, obj):
        return obj.total_stock <= obj.reorder_level


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ["id", "item", "batch", "movement_type", "quantity", "reason", "performed_by", "created_at"]
        read_only_fields = ["id", "performed_by", "created_at"]
