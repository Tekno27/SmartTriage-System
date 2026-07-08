from django.urls import path

from .views import (
    NurseMarkTriagedView,
    VisitCheckInView,
    VisitCompleteView,
    VisitDetailView,
    VisitQueueView,
    VisitStartConsultationView,
)

urlpatterns = [
    path("check-in/", VisitCheckInView.as_view(), name="visit-check-in"),
    path("queue/", VisitQueueView.as_view(), name="visit-queue"),
    path("<int:pk>/", VisitDetailView.as_view(), name="visit-detail"),
    path("<int:pk>/start/", VisitStartConsultationView.as_view(), name="visit-start"),
    path("<int:pk>/complete/", VisitCompleteView.as_view(), name="visit-complete"),
    path("<int:pk>/triaged/", NurseMarkTriagedView.as_view(), name="visit-triaged"),
]
