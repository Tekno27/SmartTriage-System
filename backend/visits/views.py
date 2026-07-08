from django.db.models import Count
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsDoctor, IsNurse, IsNurseOrDoctor, IsStudent
from patients.models import PatientProfile
from patients.nhis import apply_nhis_verification
from triage.ai_engine import get_diagnosis_recommendations, get_triage_recommendations

from .models import Visit
from .serializers import VisitCreateSerializer, VisitSerializer, VisitUpdateSerializer


class VisitCheckInView(generics.CreateAPIView):
    serializer_class = VisitCreateSerializer
    permission_classes = [IsStudent]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        data = serializer.validated_data

        if data.get("first_name"):
            user.first_name = data["first_name"]
        if data.get("last_name"):
            user.last_name = data["last_name"]
        if data.get("student_id"):
            user.student_id = data["student_id"]
        user.save()

        profile, _ = PatientProfile.objects.get_or_create(user=user)
        if data.get("ghana_card_number"):
            profile.ghana_card_number = data["ghana_card_number"]

        nhis_result = {"valid": False, "status": "unknown"}
        if data.get("nhis_number"):
            nhis_result = apply_nhis_verification(profile, data["nhis_number"])

        active_visit = Visit.objects.filter(
            patient=user,
            status__in=[
                Visit.Status.CHECKED_IN,
                Visit.Status.TRIAGED,
                Visit.Status.WAITING,
                Visit.Status.IN_CONSULTATION,
            ],
        ).first()
        if active_visit:
            return Response(
                {"detail": "You already have an active visit.", "visit": VisitSerializer(active_visit).data},
                status=status.HTTP_400_BAD_REQUEST,
            )

        visit = Visit(
            patient=user,
            symptoms=data.get("symptoms", []),
            pain_level=data.get("pain_level", 0),
            symptoms_description=data.get("symptoms_description", ""),
            nhis_verified=nhis_result.get("valid", False),
            status=Visit.Status.CHECKED_IN,
        )
        visit.apply_initial_triage()
        visit.save()

        ai = get_triage_recommendations(
            symptoms=visit.symptoms,
            pain_level=visit.pain_level,
            chief_complaint=visit.chief_complaint,
        )

        return Response(
            {
                "visit": VisitSerializer(visit).data,
                "nhis": nhis_result,
                "ai_preview": ai,
            },
            status=status.HTTP_201_CREATED,
        )


class MyVisitView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        visit = (
            Visit.objects.filter(
                patient=request.user,
                status__in=[
                    Visit.Status.CHECKED_IN,
                    Visit.Status.TRIAGED,
                    Visit.Status.WAITING,
                    Visit.Status.IN_CONSULTATION,
                ],
            )
            .select_related("patient")
            .first()
        )
        if not visit:
            return Response({"visit": None})
        return Response({"visit": VisitSerializer(visit).data})


class VisitQueueView(generics.ListAPIView):
    serializer_class = VisitSerializer
    permission_classes = [IsNurseOrDoctor]

    def get_queryset(self):
        statuses = self.request.query_params.get("status")
        queryset = Visit.objects.select_related("patient", "assigned_doctor")
        if statuses:
            queryset = queryset.filter(status__in=statuses.split(","))
        else:
            queryset = queryset.exclude(status__in=[Visit.Status.COMPLETED, Visit.Status.CANCELLED])
        return queryset


class DashboardStatsView(APIView):
    permission_classes = [IsNurseOrDoctor]

    def get(self, request):
        today = timezone.now().date()
        active = Visit.objects.exclude(
            status__in=[Visit.Status.COMPLETED, Visit.Status.CANCELLED]
        )
        return Response(
            {
                "waiting": active.filter(status=Visit.Status.CHECKED_IN).count(),
                "triaged": active.filter(status__in=[Visit.Status.TRIAGED, Visit.Status.WAITING]).count(),
                "in_consultation": active.filter(status=Visit.Status.IN_CONSULTATION).count(),
                "critical": active.filter(urgency=Visit.Urgency.CRITICAL).count(),
                "completed_today": Visit.objects.filter(completed_at__date=today).count(),
                "total_active": active.count(),
            }
        )


class VisitDetailView(generics.RetrieveUpdateAPIView):
    queryset = Visit.objects.select_related("patient", "assigned_doctor")
    permission_classes = [IsNurseOrDoctor]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return VisitUpdateSerializer
        return VisitSerializer


class VisitStartConsultationView(APIView):
    permission_classes = [IsDoctor]

    def post(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            return Response({"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND)

        visit.status = Visit.Status.IN_CONSULTATION
        visit.assigned_doctor = request.user
        visit.consultation_started_at = timezone.now()
        visit.save()
        return Response(VisitSerializer(visit).data)


class VisitCompleteView(APIView):
    permission_classes = [IsDoctor]

    def post(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk, assigned_doctor=request.user)
        except Visit.DoesNotExist:
            return Response({"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND)

        visit.status = Visit.Status.COMPLETED
        visit.completed_at = timezone.now()
        visit.diagnosis = request.data.get("diagnosis", visit.diagnosis)
        visit.consultation_notes = request.data.get("consultation_notes", visit.consultation_notes)
        visit.save()
        return Response(VisitSerializer(visit).data)


class NurseMarkTriagedView(APIView):
    permission_classes = [IsNurse]

    def post(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            return Response({"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND)

        visit.status = Visit.Status.WAITING
        visit.triaged_at = timezone.now()
        visit.save()
        return Response(VisitSerializer(visit).data)


class AIRecommendationsView(APIView):
    permission_classes = [IsNurseOrDoctor]

    def post(self, request):
        visit_id = request.data.get("visit_id")
        mode = request.data.get("mode", "triage")

        visit = None
        if visit_id:
            try:
                visit = Visit.objects.select_related("patient").get(pk=visit_id)
            except Visit.DoesNotExist:
                return Response({"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND)

        symptoms = request.data.get("symptoms") or (visit.symptoms if visit else [])
        pain_level = request.data.get("pain_level", visit.pain_level if visit else 0)
        chief_complaint = request.data.get("chief_complaint", visit.chief_complaint if visit else "")
        vitals = request.data.get("vitals", {})

        if mode == "diagnosis":
            result = get_diagnosis_recommendations(
                symptoms=symptoms,
                pain_level=pain_level,
                chief_complaint=chief_complaint,
                triage_score=visit.triage_score if visit else 0,
                urgency=visit.urgency if visit else "routine",
            )
        else:
            result = get_triage_recommendations(
                symptoms=symptoms,
                pain_level=pain_level,
                chief_complaint=chief_complaint,
                vitals=vitals,
            )

        return Response(result)
