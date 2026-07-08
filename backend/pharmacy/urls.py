from django.urls import path

from .views import (
    DispensePrescriptionView,
    MedicationBatchListView,
    MedicationListView,
    PrescriptionCreateView,
    PrescriptionListView,
)

urlpatterns = [
    path("medications/", MedicationListView.as_view(), name="medication-list"),
    path("batches/", MedicationBatchListView.as_view(), name="batch-list"),
    path("prescriptions/", PrescriptionListView.as_view(), name="prescription-list"),
    path("prescriptions/create/", PrescriptionCreateView.as_view(), name="prescription-create"),
    path("prescriptions/<int:pk>/dispense/", DispensePrescriptionView.as_view(), name="prescription-dispense"),
]
