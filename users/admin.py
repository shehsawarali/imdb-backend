from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin site settings for User model
    """

    fields = [
        "image",
        "email",
        "first_name",
        "last_name",
        "country",
        "age",
        ("is_superuser", "is_active"),
        ("date_joined", "last_login"),
        "timezone",
        ("login_alert_preference", "email_list_preference"),
    ]
    list_display = ("id", "email", "first_name", "last_name", "is_active")
    search_fields = ("id", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    def has_delete_permission(self, request, obj=None):
        return False
