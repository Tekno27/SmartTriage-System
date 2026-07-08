from django.urls import path

from .views import NHISClaimCreateView, NHISClaimDetailView, NHISClaimListView, NHISClaimSubmitView

urlpatterns = [
    path("claims/", NHISClaimListView.as_view(), name="claim-list"),
    path("claims/create/", NHISClaimCreateView.as_view(), name="claim-create"),
    path("claims/<int:pk>/", NHISClaimDetailView.as_view(), name="claim-detail"),
    path("claims/<int:pk>/submit/", NHISClaimSubmitView.as_view(), name="claim-submit"),
]
