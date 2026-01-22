"""
Django admin configuration for Pricing module.
"""

import importlib

from django import forms
from django.contrib import admin
from karrio.server.pricing.models import Markup, Fee

if importlib.util.find_spec("karrio.server.orgs") is not None:
    import karrio.server.orgs.models as orgs


# ─────────────────────────────────────────────────────────────────────────────
# MARKUP ADMIN
# ─────────────────────────────────────────────────────────────────────────────


class MarkupAdmin(admin.ModelAdmin):
    """Admin interface for Markup model."""

    list_display = ("name", "amount", "markup_type", "active", "is_visible")
    list_filter = ("active", "is_visible", "markup_type")
    search_fields = ("name", "carrier_codes", "service_codes")
    readonly_fields = ("id",)

    fieldsets = (
        (None, {
            "fields": (
                "id",
                ("name", "active"),
                ("amount", "markup_type"),
                "is_visible",
            )
        }),
        ("Filters", {
            "classes": ("collapse",),
            "description": "Leave empty to apply to all carriers/services/connections",
            "fields": (
                "carrier_codes",
                "service_codes",
                "connection_ids",
            ),
        }),
        ("Metadata", {
            "classes": ("collapse",),
            "fields": ("metadata",),
        }),
    )

    if importlib.util.find_spec("karrio.server.orgs") is not None:

        class MarkupForm(forms.ModelForm):
            class Meta:
                model = Markup
                fields = "__all__"

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                if kwargs.get("instance") is not None:
                    self.fields["organizations"].initial = kwargs["instance"].org.all()

            organizations = forms.ModelMultipleChoiceField(
                queryset=orgs.Organization.objects.all(),
                required=False,
                help_text="Organizations this markup applies to. Leave empty for global.",
            )

            def save(self, commit=True):
                instance = super().save(commit=commit)
                instance.save()
                organizations = self.cleaned_data.get("organizations", [])
                instance.org.set(organizations)
                return instance

        form = MarkupForm
        fieldsets += ((None, {"fields": ("organizations",)}),)


admin.site.register(Markup, MarkupAdmin)


# ─────────────────────────────────────────────────────────────────────────────
# FEE ADMIN (Read-only)
# ─────────────────────────────────────────────────────────────────────────────


class FeeAdmin(admin.ModelAdmin):
    """Admin interface for Fee model (read-only)."""

    list_display = ("name", "amount", "currency", "carrier_code", "service_code", "created_at")
    list_filter = ("markup_type", "carrier_code", "currency")
    search_fields = ("name", "shipment__id", "markup__id")
    readonly_fields = (
        "id", "shipment", "markup", "name", "amount", "currency",
        "markup_type", "markup_percentage", "carrier_code", "service_code",
        "connection_id", "created_at",
    )
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {
            "fields": ("id", "shipment", "markup")
        }),
        ("Fee Details", {
            "fields": (
                "name",
                ("amount", "currency"),
                ("markup_type", "markup_percentage"),
            )
        }),
        ("Context", {
            "fields": (
                "carrier_code",
                "service_code",
                "connection_id",
            )
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )

    def has_add_permission(self, request):
        """Fees are created automatically, not manually."""
        return False

    def has_change_permission(self, request, obj=None):
        """Fees should not be edited."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Allow deletion for cleanup purposes."""
        return True


admin.site.register(Fee, FeeAdmin)


# ─────────────────────────────────────────────────────────────────────────────
# LEGACY ALIAS
# ─────────────────────────────────────────────────────────────────────────────

# For backward compatibility
SurchargeAdmin = MarkupAdmin
