from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from karrio.server.user.models import Token

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    add_form_template = None
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("full_name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "email",
        "full_name",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
        "last_login",
        "date_joined",
    )
    search_fields = ("email", "full_name")
    ordering = ("email",)


class TokenAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "user",
        *(["organization"] if settings.MULTI_ORGANIZATIONS else []),
        "created",
    )
    fields = ("user",)
    ordering = ("-created",)

    def has_add_permission(self, request, obj=None):
        return not settings.MULTI_ORGANIZATIONS

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.filter(user=request.user)


admin.site.register(Token, TokenAdmin)
admin.site.register(User, UserAdmin)
