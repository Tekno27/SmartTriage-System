from django.urls import path

from .views import (
    AIRecommendationsView,
    DashboardStatsView,
    MyVisitView,
    NurseMarkTriagedView,
    VisitCheckInView,
    VisitCompleteView,
    VisitDetailView,
    VisitQueueView,
    VisitStartConsultationView,
)

urlpatterns = [
    path("check-in/", VisitCheckInView.as_view(), name="visit-check-in"),
    path("my-visit/", MyVisitView.as_view(), name="my-visit"),
    path("queue/", VisitQueueView.as_view(), name="visit-queue"),
    path("stats/", DashboardStatsView.as_view(), name="visit-stats"),
    path("ai/recommendations/", AIRecommendationsView.as_view(), name="ai-recommendations"),
    path("<int:pk>/", VisitDetailView.as_view(), name="visit-detail"),
    path("<int:pk>/start/", VisitStartConsultationView.as_view(), name="visit-start"),
    path("<int:pk>/complete/", VisitCompleteView.as_view(), name="visit-complete"),
    path("<int:pk>/triaged/", NurseMarkTriagedView.as_view(), name="visit-triaged"),
]
