from django.urls import path

from .views import (
    InvoiceDetailView,
    InvoiceListCreateView,
    NHISClaimCreateView,
    NHISClaimDetailView,
    NHISClaimListView,
    NHISClaimSubmitView,
    PaymentCreateView,
)

urlpatterns = [
    path("claims/", NHISClaimListView.as_view(), name="claim-list"),
    path("claims/create/", NHISClaimCreateView.as_view(), name="claim-create"),
    path("claims/<int:pk>/", NHISClaimDetailView.as_view(), name="claim-detail"),
    path("claims/<int:pk>/submit/", NHISClaimSubmitView.as_view(), name="claim-submit"),
    path("invoices/", InvoiceListCreateView.as_view(), name="invoice-list"),
    path("invoices/<int:pk>/", InvoiceDetailView.as_view(), name="invoice-detail"),
    path("payments/", PaymentCreateView.as_view(), name="payment-create"),
]
