from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.base_user import BaseUserManager

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "first_name", "last_name", "age", "education", "show_bio", "image", "date_joined")
    list_filter = ("email", "is_staff", "is_active", "date_joined")
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name", "age", "education", "bio", "image")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email","education")
    ordering = ("email", "date_joined")

    object = BaseUserManager()



