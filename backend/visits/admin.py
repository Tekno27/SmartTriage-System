from django.contrib import admin

from .models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "status", "urgency", "triage_score", "checked_in_at")
    list_filter = ("status", "urgency")
    search_fields = ("patient__username", "patient__student_id", "chief_complaint")
