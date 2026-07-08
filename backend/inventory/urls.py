from django.urls import path

from .views import StockMovementListCreateView, SupplyItemListView

urlpatterns = [
    path("items/", SupplyItemListView.as_view(), name="supply-items"),
    path("movements/", StockMovementListCreateView.as_view(), name="stock-movements"),
]
