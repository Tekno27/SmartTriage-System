from django.urls import path

from .views import MedicalRecordListCreateView

urlpatterns = [
    path("", MedicalRecordListCreateView.as_view(), name="medical-records"),
]
