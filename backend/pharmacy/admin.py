from django.contrib import admin

from .models import DispenseRecord, Medication, MedicationBatch, Prescription


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ("name", "generic_name", "unit", "is_active")
    search_fields = ("name", "generic_name")


@admin.register(MedicationBatch)
class MedicationBatchAdmin(admin.ModelAdmin):
    list_display = ("medication", "batch_number", "expiry_date", "quantity_on_hand")
    list_filter = ("expiry_date",)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("medication", "visit", "quantity_prescribed", "is_dispensed", "created_at")


@admin.register(DispenseRecord)
class DispenseRecordAdmin(admin.ModelAdmin):
    list_display = ("prescription", "batch", "quantity", "dispensed_at")
