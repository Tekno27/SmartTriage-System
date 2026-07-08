from django.contrib import admin

from .models import TriageAssessment


@admin.register(TriageAssessment)
class TriageAssessmentAdmin(admin.ModelAdmin):
    list_display = ("visit", "urgency", "score", "assessed_by", "created_at")
    list_filter = ("urgency",)
