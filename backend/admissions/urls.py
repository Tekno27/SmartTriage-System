from django.urls import path

from .views import AdmissionDischargeView, AdmissionListCreateView, SurgeryListCreateView

urlpatterns = [
    path("", AdmissionListCreateView.as_view(), name="admissions"),
    path("<int:pk>/discharge/", AdmissionDischargeView.as_view(), name="admission-discharge"),
    path("surgeries/", SurgeryListCreateView.as_view(), name="surgeries"),
]
