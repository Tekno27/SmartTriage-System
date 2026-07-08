import io

import qrcode
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsStudent

from .models import PatientProfile
from .serializers import PatientProfileSerializer

User = get_user_model()


class PatientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile


class QRCheckInView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(str(request.user.qr_token))
        qr.make(fit=True)
        image = qr.make_image(fill_color="#0d4f4f", back_color="#f5f0e8")
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return HttpResponse(buffer.getvalue(), content_type="image/png")


class QRLookupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, token):
        try:
            user = User.objects.get(qr_token=token, role=User.Role.STUDENT)
        except User.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        profile, _ = PatientProfile.objects.get_or_create(user=user)
        return Response(PatientProfileSerializer(profile).data)
