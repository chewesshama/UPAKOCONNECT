from django.contrib import admin
from .models import FellowshipMember

@admin.register(FellowshipMember)
class FellowshipMemberAdmin(admin.ModelAdmin):
    list_display = ("nationality", "phone_number", "original_location", "current_location_region")
    search_fields = ("phone_number", "passport_number")
