from django.urls import path

from .views import ImagingOrderListCreateView, ImagingReportView, ImagingTypeListView

urlpatterns = [
    path("types/", ImagingTypeListView.as_view(), name="imaging-types"),
    path("orders/", ImagingOrderListCreateView.as_view(), name="imaging-orders"),
    path("orders/<int:pk>/report/", ImagingReportView.as_view(), name="imaging-report"),
]
