from django.contrib import admin
from .models import Patient, Baby, VisitRecord

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone_number',
        'nationality',
        'expected_delivery_date',
        'is_active_pregnancy',
    )

@admin.register(Baby)
class BabyAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'gender',
        'dob',
        'twins_status',
        'health_status',
    )

@admin.register(VisitRecord)
class VisitRecordAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'visit_date',
        'seen_by',
    )
