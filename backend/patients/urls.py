from django.urls import path

from .views import (
    CommonSymptomsView,
    NHISVerifyPreviewView,
    NHISVerifyView,
    PatientProfileView,
    QRCheckInView,
    QRLookupView,
)

urlpatterns = [
    path("profile/", PatientProfileView.as_view(), name="patient-profile"),
    path("symptoms/", CommonSymptomsView.as_view(), name="common-symptoms"),
    path("nhis/verify/", NHISVerifyView.as_view(), name="nhis-verify"),
    path("nhis/check/", NHISVerifyPreviewView.as_view(), name="nhis-check"),
    path("qr/", QRCheckInView.as_view(), name="patient-qr"),
    path("qr/<uuid:token>/", QRLookupView.as_view(), name="patient-qr-lookup"),
]
