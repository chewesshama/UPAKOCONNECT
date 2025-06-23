from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "gender",
                "marital_status",
                "phone_number",
                "nationality",
                "role",
                "department",
                "region",
                "district",
                "ward",
                "profile_picture",
            )
        }),
    )
    list_display = ("username", "role", "department", "phone_number", "nationality")
