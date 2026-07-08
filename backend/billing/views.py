import uuid

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsNurseOrDoctor

from .models import NHISClaim
from .serializers import NHISClaimSerializer


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
    permission_classes = [IsNurseOrDoctor]


class NHISClaimDetailView(generics.RetrieveUpdateAPIView):
    queryset = NHISClaim.objects.select_related("visit", "submitted_by")
    serializer_class = NHISClaimSerializer
    permission_classes = [IsNurseOrDoctor]


class NHISClaimSubmitView(APIView):
    permission_classes = [IsNurseOrDoctor]

    def post(self, request, pk):
        try:
            claim = NHISClaim.objects.get(pk=pk)
        except NHISClaim.DoesNotExist:
            return Response({"detail": "Claim not found."}, status=status.HTTP_404_NOT_FOUND)

        claim.status = NHISClaim.Status.SUBMITTED
        claim.save()
        return Response(NHISClaimSerializer(claim).data)
