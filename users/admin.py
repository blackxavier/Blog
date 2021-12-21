from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    search_fields = (
        "email",
        "username",
        "first_name",
    )
    list_filter = ("email", "username", "first_name", "is_active", "is_staff")
    ordering = ("-date_created",)
    list_display = ("email", "username", "first_name", "is_active", "is_staff")
    fieldsets = (
        (
            "User Information",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Personal", {"fields": ("about_user",)}),
    )
    add_fieldsets = (
        (
            "Create new user",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


admin.site.register(User, UserAdminConfig)