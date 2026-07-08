import uuid
from decimal import Decimal

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAccountant, IsNurseOrDoctor

from .models import Invoice, NHISClaim, Payment
from .serializers import InvoiceSerializer, NHISClaimSerializer, PaymentSerializer


class NHISClaimCreateView(generics.CreateAPIView):
    queryset = NHISClaim.objects.all()
    serializer_class = NHISClaimSerializer
    permission_classes = [IsNurseOrDoctor]

    def perform_create(self, serializer):
        claim_number = f"NHIS-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        serializer.save(submitted_by=self.request.user, claim_number=claim_number)


class NHISClaimListView(generics.ListAPIView):
    queryset = NHISClaim.objects.select_related("visit", "submitted_by")
    serializer_class = NHISClaimSerializer
    permission_classes = [IsAccountant]


class NHISClaimDetailView(generics.RetrieveUpdateAPIView):
    queryset = NHISClaim.objects.select_related("visit", "submitted_by")
    serializer_class = NHISClaimSerializer
    permission_classes = [IsAccountant]


class NHISClaimSubmitView(APIView):
    permission_classes = [IsAccountant]

    def post(self, request, pk):
        try:
            claim = NHISClaim.objects.get(pk=pk)
        except NHISClaim.DoesNotExist:
            return Response({"detail": "Claim not found."}, status=status.HTTP_404_NOT_FOUND)
        claim.status = NHISClaim.Status.SUBMITTED
        claim.save()
        return Response(NHISClaimSerializer(claim).data)


class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAccountant]

    def get_queryset(self):
        return Invoice.objects.select_related("patient", "created_by").prefetch_related("line_items", "payments")

    def perform_create(self, serializer):
        inv_num = f"INV-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:5].upper()}"
        serializer.save(created_by=self.request.user, invoice_number=inv_num)


class InvoiceDetailView(generics.RetrieveAPIView):
    queryset = Invoice.objects.select_related("patient").prefetch_related("line_items", "payments")
    serializer_class = InvoiceSerializer
    permission_classes = [IsAccountant]


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAccountant]

    def perform_create(self, serializer):
        payment = serializer.save(received_by=self.request.user)
        invoice = payment.invoice
        invoice.amount_paid += payment.amount
        if invoice.amount_paid >= invoice.total:
            invoice.status = Invoice.Status.PAID
        elif invoice.amount_paid > 0:
            invoice.status = Invoice.Status.PARTIAL
        invoice.save()
