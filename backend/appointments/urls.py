from django.urls import path

from .views import AppointmentConfirmView, AppointmentDetailView, AppointmentListCreateView

urlpatterns = [
    path("", AppointmentListCreateView.as_view(), name="appointments"),
    path("<int:pk>/", AppointmentDetailView.as_view(), name="appointment-detail"),
    path("<int:pk>/confirm/", AppointmentConfirmView.as_view(), name="appointment-confirm"),
]
