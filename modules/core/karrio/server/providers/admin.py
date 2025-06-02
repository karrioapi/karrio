import functools
from django import forms
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

import karrio.lib as lib
import karrio.references as ref
import karrio.server.core.utils as utils
import karrio.server.serializers as serializers
import karrio.server.core.dataunits as dataunits
import karrio.server.providers.models as providers

User = get_user_model()


def model_admin(ext: str, carrierProxy):
    references = dataunits.contextual_reference(reduced=False)
    class_name = carrierProxy.__name__
    connection_fields = references["connection_fields"].get(ext) or {}
    connection_configs = references["connection_configs"].get(ext) or {}
    carrier_services = (references["services"].get(ext) or {}).keys()
    carrier_options = (references["options"].get(ext) or {}).keys()

    class _Form(forms.ModelForm):

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

            else:
                pass

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
                locals()[key] = forms.IntegerField(
                    required=False,
                )

            elif field["type"] == "float":
                locals()[key] = forms.FloatField(
                    required=False,
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
                    required=False,
                )

            else:
                pass

        class Meta:
            model = carrierProxy
            fields = "__all__"

        def __init__(self, *args, instance: providers.Carrier = None, **kwargs):
            if instance is not None:
                kwargs.update({"instance": instance})
                credentials = instance.credentials
                config = providers.Carrier.resolve_config(
                    instance, is_system_config=True
                )

                for key in [
                    _ for _ in self.base_fields.keys() if _ in connection_fields.keys()
                ]:
                    self.base_fields[key].initial = (
                        None if credentials is None else credentials.get(key)
                    )

                for key in [
                    _ for _ in self.base_fields.keys() if _ in connection_configs.keys()
                ]:
                    self.base_fields[key].initial = (
                        None if config is None else config.config.get(key)
                    )

            super(_Form, self).__init__(*args, **kwargs)

        def save(self, commit: bool = True):
            config_data = lib.to_dict(
                {key: self.cleaned_data.get(key) for key in connection_configs.keys()}
            )
            credentials_data = lib.to_dict(
                {key: self.cleaned_data.get(key) for key in connection_fields.keys()}
            )

            for key in connection_fields.keys():
                if key in self.cleaned_data:
                    self.cleaned_data.pop(key)

            for key in connection_configs.keys():
                if key in self.cleaned_data:
                    self.cleaned_data.pop(key)

            carrier = super(_Form, self).save(commit)

            if any(connection_fields.keys()) and (commit or carrier.pk is not None):
                carrier.credentials = serializers.process_dictionaries_mutations(
                    ["credentials"], credentials_data, carrier
                )
                carrier.save()

            if any(connection_configs.keys()) and (commit or carrier.pk is not None):
                config = providers.Carrier.resolve_config(
                    carrier, is_system_config=True
                )
                created_by = getattr(config, "created_by", self.request.user)
                config_value = lib.to_dict(
                    serializers.process_dictionaries_mutations(
                        ["config"], config_data, config
                    )
                )

                if config is None and len(config_value.keys()) == 0:
                    # Skip configuration persistence...
                    return carrier

                # Save or update the carrier config...
                lib.identity(
                    providers.CarrierConfig.objects.create(
                        created_by=created_by,
                        carrier=carrier,
                        config=config_value,
                    )
                    if config is None
                    else providers.CarrierConfig.objects.filter(carrier=carrier).update(
                        config=config_value
                    )
                )

            return carrier

    _form: forms.ModelForm = type(f"{class_name}AdminForm", (_Form,), {})
    _fields = _form.base_fields.keys()

    class _Admin(admin.ModelAdmin):
        form = _form
        inlines = []
        list_display = ("__str__", "test_mode", "active")
        exclude = ["active_users"]
        fieldsets = [
            (
                None,
                {
                    "fields": [
                        _
                        for _ in _fields
                        if _
                        not in [
                            *connection_fields.keys(),
                            *connection_configs.keys(),
                            "carrier_code",
                            "credentials",
                            "active_users",
                            "is_system",
                            "rate_sheet",
                            "metadata",
                        ]
                    ],
                },
            ),
        ]

        if any(connection_fields.keys()):
            fieldsets += [
                (  # type: ignore
                    "Connection Fields",
                    {
                        "fields": [_ for _ in connection_fields.keys() if _ in _fields],
                    },
                ),
            ]

        if any(connection_configs.keys()):
            fieldsets += [
                (  # type: ignore
                    "Connection Config",
                    {
                        "fields": [
                            _ for _ in connection_configs.keys() if _ in _fields
                        ],
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
                        "data - lpignore": "true",
                        "autocomplete": "keep-off",
                        "onfocus": "this.removeAttribute('readonly');",
                    }
                )
            },
        }

        if settings.MULTI_ORGANIZATIONS:

            class ActiveOrgInline(admin.TabularInline):
                model = carrierProxy.active_orgs.through
                verbose_name = "Activated for organization"
                extra = 0

                def get_formset(self, request, obj, **kwargs):
                    from karrio.server.orgs.models import Organization

                    initial = []
                    orgs = Organization.objects.filter(
                        users__id=request.user.id
                    ).distinct()
                    self.max_num = orgs.count()

                    if obj is None and request.method == "GET":
                        self.extra = orgs.count()
                        initial += [{"organization": o.id} for o in orgs]

                    formset = super().get_formset(request, obj, **kwargs)
                    formset.__init__ = functools.partialmethod(
                        formset.__init__, initial=initial
                    )
                    organization_field = formset.form.base_fields["organization"]
                    organization_field.queryset = orgs
                    organization_field.widget.can_add_related = False
                    organization_field.widget.can_change_related = False

                    return formset

            inlines += [ActiveOrgInline]

        else:

            class ActiveUserInline(admin.TabularInline):
                model = carrierProxy.active_users.through
                exta = 0
                verbose_name = "Activated for user"

                def get_formset(self, request, obj, **kwargs):
                    initial = []
                    users = User.objects.all()
                    self.max_num = users.count()

                    if obj is None and request.method == "GET":
                        self.extra = users.count()
                        initial += [{"user": o.id} for o in users]

                    formset = super().get_formset(request, obj, **kwargs)
                    formset.__init__ = functools.partialmethod(
                        formset.__init__, initial=initial
                    )
                    user_field = formset.form.base_fields["user"]
                    user_field.queryset = users
                    user_field.widget.can_add_related = False
                    user_field.widget.can_change_related = False

                    return formset

            inlines += [ActiveUserInline]

        def get_queryset(self, request):
            query = super().get_queryset(request)
            return query.filter(models.Q(is_system=True) | models.Q(created_by=None))

        def get_form(self, request, *args, **kwargs):
            form = super(_Admin, self).get_form(request, *args, **kwargs)
            form.request = request

            # Customize capabilities options specific to a carrier.
            raw_capabilities = ref.get_carrier_capabilities(ext)
            form.base_fields["capabilities"].choices = [
                (c, c) for c in raw_capabilities
            ]
            form.base_fields["capabilities"].initial = raw_capabilities

            return form

        def save_model(self, request, obj, form, change):
            obj.is_system = True
            obj.carrier_code = ext
            return super().save_model(request, obj, form, change)

    return type(f"{class_name}Admin", (_Admin,), {})


@admin.register(providers.LabelTemplate)
class LabelTemplateAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@utils.skip_on_commands()
def register_carrier_admins():
    for carrier_name, display_name in ref.REFERENCES["carriers"].items():
        proxy = providers.create_carrier_proxy(carrier_name, display_name)
        admin.site.register(proxy, model_admin(carrier_name, proxy))


register_carrier_admins()
