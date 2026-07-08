from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Invoice, InvoiceLineItem, NHISClaim, Payment


class NHISClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = NHISClaim
        fields = [
            "id", "visit", "patient_nhis_number", "claim_number",
            "consultation_fee", "medication_cost", "lab_cost",
            "total_amount", "nhis_coverage", "patient_copay",
            "status", "diagnosis_code", "notes", "submitted_by",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "claim_number", "total_amount", "nhis_coverage",
            "patient_copay", "submitted_by", "created_at", "updated_at",
        ]


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = ["id", "description", "quantity", "unit_price", "total"]
        read_only_fields = ["id", "total"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "invoice", "amount", "method", "reference", "received_by", "paid_at"]
        read_only_fields = ["id", "received_by", "paid_at"]


class InvoiceSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    line_items = InvoiceLineItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id", "invoice_number", "patient", "visit", "admission",
            "subtotal", "tax", "total", "amount_paid", "balance",
            "status", "due_date", "notes", "line_items", "payments",
            "created_by", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "invoice_number", "patient", "balance",
            "created_by", "created_at", "updated_at",
        ]
