from django.urls import path

from .views import PatientProfileView, QRCheckInView, QRLookupView

urlpatterns = [
    path("profile/", PatientProfileView.as_view(), name="patient-profile"),
    path("qr/", QRCheckInView.as_view(), name="patient-qr"),
    path("qr/<uuid:token>/", QRLookupView.as_view(), name="patient-qr-lookup"),
]
