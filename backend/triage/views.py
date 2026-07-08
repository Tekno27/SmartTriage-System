from rest_framework import generics

from accounts.permissions import IsNurseOrDoctor

from .models import TriageAssessment
from .serializers import TriageAssessmentSerializer


class TriageAssessmentCreateView(generics.CreateAPIView):
    queryset = TriageAssessment.objects.all()
    serializer_class = TriageAssessmentSerializer
    permission_classes = [IsNurseOrDoctor]

    def perform_create(self, serializer):
        serializer.save(assessed_by=self.request.user)


class TriageAssessmentDetailView(generics.RetrieveAPIView):
    queryset = TriageAssessment.objects.select_related("visit", "assessed_by")
    serializer_class = TriageAssessmentSerializer
    permission_classes = [IsNurseOrDoctor]
