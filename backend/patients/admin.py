from django.contrib import admin

from .models import PatientProfile


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "nhis_number", "blood_type", "updated_at")
    search_fields = ("user__username", "user__student_id", "nhis_number")
