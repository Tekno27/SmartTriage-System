from django.urls import path

from .views import BedListView, DepartmentListView, HospitalOverviewView, TheatreListView, WardListView

urlpatterns = [
    path("overview/", HospitalOverviewView.as_view(), name="hospital-overview"),
    path("departments/", DepartmentListView.as_view(), name="departments"),
    path("wards/", WardListView.as_view(), name="wards"),
    path("beds/", BedListView.as_view(), name="beds"),
    path("theatres/", TheatreListView.as_view(), name="theatres"),
]
