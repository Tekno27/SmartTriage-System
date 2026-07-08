from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/triage/", include("triage.urls")),
    path("api/visits/", include("visits.urls")),
    path("api/pharmacy/", include("pharmacy.urls")),
    path("api/billing/", include("billing.urls")),
]
