from django.urls import path

from .views import LabOrderListCreateView, LabResultEntryView, LabTestListView

urlpatterns = [
    path("tests/", LabTestListView.as_view(), name="lab-tests"),
    path("orders/", LabOrderListCreateView.as_view(), name="lab-orders"),
    path("results/<int:pk>/", LabResultEntryView.as_view(), name="lab-result"),
]
