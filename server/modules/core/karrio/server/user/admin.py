from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import models as forms
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
        "test_mode",
        "created",
    )
    fields = ("user", "test_mode")
    ordering = ("-created",)

    if settings.MULTI_ORGANIZATIONS:
        from karrio.server.orgs.admin import TokenLinkInline

        inlines = [TokenLinkInline]

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.filter(user=request.user)

    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["user"].queryset = User.objects.filter(
            orgs_organization__users__id=request.user.id
        ).distinct()
        return form


admin.site.register(Token, TokenAdmin)
admin.site.register(User, UserAdmin)
