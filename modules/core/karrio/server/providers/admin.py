"""
Django Admin for Carrier Connection Models.

Provides admin interfaces for:
- SystemConnection: Admin-managed platform-wide connections
- Carrier: User/org-owned connections (registered via proxy models)
- LabelTemplate: Hidden from admin module navigation
"""
import functools
from django import forms
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model

import karrio.lib as lib
import karrio.references as ref
import karrio.server.core.utils as utils
import karrio.server.serializers as serializers
import karrio.server.core.dataunits as dataunits
import karrio.server.providers.models as providers

User = get_user_model()


def system_connection_admin(ext: str, connection_proxy):
    """Create admin class for a specific carrier's SystemConnection."""
    references = dataunits.contextual_reference(reduced=False)
    class_name = connection_proxy.__name__
    connection_fields = references["connection_fields"].get(ext) or {}
    connection_configs = references["connection_configs"].get(ext) or {}
    carrier_services = (references["services"].get(ext) or {}).keys()
    carrier_options = (references["options"].get(ext) or {}).keys()

    class _Form(forms.ModelForm):
        """Dynamic form for carrier-specific connection fields."""

        # Generate form fields for carrier-specific credentials
        for key, field in connection_fields.items():
            if field["type"] == "boolean":
                locals()[key] = forms.NullBooleanField(
                    required=field.get("required", False),
                    initial=None,
                )
            elif field["type"] == "integer":
                locals()[key] = forms.IntegerField(
                    required=field.get("required", False),
                )
            elif field["type"] == "float":
                locals()[key] = forms.FloatField(
                    required=field.get("required", False),
                )
            elif field["type"] == "string" and any(field.get("enum", [])):
                locals()[key] = forms.ChoiceField(
                    choices=[(None, ""), *[(_, _) for _ in field.get("enum", [])]],
                    widget=forms.Select(attrs={"class": "vTextField"}),
                    required=field.get("required", False),
                    initial=field.get("default"),
                )
            elif field["type"] == "string":
                locals()[key] = forms.CharField(
                    required=field.get("required", False),
                )

        # Generate form fields for carrier-specific config options
        for key, field in connection_configs.items():
            if key == "shipping_services":
                shipping_services = forms.MultipleChoiceField(
                    choices=[(_, _) for _ in carrier_services],
                    widget=forms.SelectMultiple(attrs={"class": "vTextField"}),
                    required=False,
                    initial=None,
                )
                continue

            if key == "shipping_options":
                shipping_options = forms.MultipleChoiceField(
                    choices=[(_, _) for _ in carrier_options],
                    widget=forms.SelectMultiple(attrs={"class": "vTextField"}),
                    required=False,
                    initial=None,
                )
                continue

            if field["type"] == "boolean":
                locals()[key] = forms.NullBooleanField(
                    required=False,
                    initial=None,
                )
            elif field["type"] == "integer":
                locals()[key] = forms.IntegerField(required=False)
            elif field["type"] == "float":
                locals()[key] = forms.FloatField(required=False)
            elif field["type"] == "string" and any(field.get("enum", [])):
                locals()[key] = forms.ChoiceField(
                    choices=[(None, ""), *[(_, _) for _ in field.get("enum", [])]],
                    widget=forms.Select(attrs={"class": "vTextField"}),
                    required=field.get("required", False),
                    initial=field.get("default"),
                )
            elif field["type"] == "string":
                locals()[key] = forms.CharField(required=False)

        class Meta:
            model = connection_proxy
            fields = "__all__"

        def __init__(self, *args, instance: providers.SystemConnection = None, **kwargs):
            if instance is not None:
                kwargs.update({"instance": instance})
                credentials = instance.credentials or {}
                config = instance.config or {}

                # Populate credential fields
                for key in [
                    k for k in self.base_fields.keys() if k in connection_fields.keys()
                ]:
                    self.base_fields[key].initial = credentials.get(key)

                # Populate config fields
                for key in [
                    k for k in self.base_fields.keys() if k in connection_configs.keys()
                ]:
                    self.base_fields[key].initial = config.get(key)

            super(_Form, self).__init__(*args, **kwargs)

        def save(self, commit: bool = True):
            config_data = lib.to_dict(
                {key: self.cleaned_data.get(key) for key in connection_configs.keys()}
            )
            credentials_data = lib.to_dict(
                {key: self.cleaned_data.get(key) for key in connection_fields.keys()}
            )

            # Remove processed fields from cleaned_data
            for key in connection_fields.keys():
                if key in self.cleaned_data:
                    self.cleaned_data.pop(key)

            for key in connection_configs.keys():
                if key in self.cleaned_data:
                    self.cleaned_data.pop(key)

            connection = super(_Form, self).save(commit)

            # Save credentials
            if any(connection_fields.keys()) and (commit or connection.pk is not None):
                connection.credentials = serializers.process_dictionaries_mutations(
                    ["credentials"], credentials_data, connection
                )
                connection.save()

            # Save config
            if any(connection_configs.keys()) and (commit or connection.pk is not None):
                connection.config = serializers.process_dictionaries_mutations(
                    ["config"], config_data, connection
                )
                connection.save()

            return connection

    _form: forms.ModelForm = type(f"{class_name}AdminForm", (_Form,), {})
    _fields = _form.base_fields.keys()

    class _Admin(admin.ModelAdmin):
        form = _form
        list_display = ("__str__", "carrier_id", "test_mode", "active")
        list_filter = ("active", "test_mode")
        search_fields = ("carrier_id",)

        fieldsets = [
            (
                None,
                {
                    "fields": [
                        f
                        for f in _fields
                        if f
                        not in [
                            *connection_fields.keys(),
                            *connection_configs.keys(),
                            "carrier_code",
                            "credentials",
                            "config",
                            "rate_sheet",
                            "metadata",
                            "metafields",  # M2M with through model - managed via API
                        ]
                    ],
                },
            ),
        ]

        if any(connection_fields.keys()):
            fieldsets += [
                (
                    "Credentials",
                    {
                        "fields": [k for k in connection_fields.keys() if k in _fields],
                    },
                ),
            ]

        if any(connection_configs.keys()):
            fieldsets += [
                (
                    "Configuration",
                    {
                        "fields": [k for k in connection_configs.keys() if k in _fields],
                    },
                ),
            ]

        formfield_overrides = {
            models.CharField: {
                "widget": forms.TextInput(
                    attrs={
                        "type": "text",
                        "readonly": "true",
                        "class": "vTextField",
                        "data-lpignore": "true",
                        "autocomplete": "keep-off",
                        "onfocus": "this.removeAttribute('readonly');",
                    }
                )
            },
        }

        def get_form(self, request, *args, **kwargs):
            form = super(_Admin, self).get_form(request, *args, **kwargs)
            form.request = request

            # Customize capabilities options specific to a carrier
            raw_capabilities = ref.get_carrier_capabilities(ext)
            form.base_fields["capabilities"].choices = [(c, c) for c in raw_capabilities]
            form.base_fields["capabilities"].initial = raw_capabilities

            return form

        def save_model(self, request, obj, form, change):
            obj.carrier_code = ext
            if obj.created_by is None:
                obj.created_by = request.user
            return super().save_model(request, obj, form, change)

    return type(f"{class_name}Admin", (_Admin,), {})


def create_system_connection_proxy(carrier_name: str, display_name: str):
    """Create a proxy model for a specific carrier's SystemConnection."""

    class _Manager(providers.SystemConnection.objects.__class__):
        def get_queryset(self):
            return super().get_queryset().filter(carrier_code=carrier_name)

    return type(
        f"{carrier_name}SystemConnection",
        (providers.SystemConnection,),
        {
            "Meta": type(
                "Meta",
                (),
                {
                    "proxy": True,
                    "__module__": __name__,
                    "verbose_name": f"{display_name} System Connection",
                    "verbose_name_plural": f"{display_name} System Connections",
                },
            ),
            "__module__": __name__,
            "objects": _Manager(),
        },
    )


@admin.register(providers.LabelTemplate)
class LabelTemplateAdmin(admin.ModelAdmin):
    """Hidden admin for LabelTemplate."""

    def has_module_permission(self, request):
        return False


@admin.register(providers.BrokeredConnection)
class BrokeredConnectionAdmin(admin.ModelAdmin):
    """Admin for viewing brokered connections (user-enabled system connections)."""

    list_display = (
        "__str__",
        "system_connection",
        "is_enabled",
        "created_by",
        "created_at",
    )
    list_filter = ("is_enabled", "system_connection__carrier_code")
    search_fields = ("carrier_id", "system_connection__carrier_id")
    readonly_fields = ("system_connection", "created_by", "created_at", "updated_at")
    exclude = ("metafields",)  # M2M with through model - managed via API

    def has_add_permission(self, request):
        # Brokered connections are created via API, not admin
        return False


@utils.skip_on_commands(["loaddata", "migrate", "makemigrations", "shell"])
def register_system_connection_admins():
    """Register admin for each carrier's SystemConnection proxy."""
    for carrier_name, display_name in ref.REFERENCES["carriers"].items():
        proxy = create_system_connection_proxy(carrier_name, display_name)
        admin.site.register(proxy, system_connection_admin(carrier_name, proxy))


register_system_connection_admins()
