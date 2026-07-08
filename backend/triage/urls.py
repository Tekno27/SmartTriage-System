from django.urls import path

from .views import TriageAssessmentCreateView, TriageAssessmentDetailView

urlpatterns = [
    path("", TriageAssessmentCreateView.as_view(), name="triage-create"),
    path("<int:pk>/", TriageAssessmentDetailView.as_view(), name="triage-detail"),
]
