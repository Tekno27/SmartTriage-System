from django.contrib import admin

from .models import NHISClaim


@admin.register(NHISClaim)
class NHISClaimAdmin(admin.ModelAdmin):
    list_display = ("claim_number", "visit", "status", "total_amount", "nhis_coverage", "created_at")
    list_filter = ("status",)
