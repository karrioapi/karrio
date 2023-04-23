import functools
from django import forms
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

import karrio.lib as lib
import karrio.references as ref
import karrio.server.serializers as serializers
import karrio.server.providers.models as carriers

User = get_user_model()
SUPPORTED_CONNECTION_CONFIGS = [
    "cost_center",
    "enforce_zpl",
    "default_currency",
    "language_code",
    "label_type",
    "shipping_options",
    "shipping_services",
]


def model_admin(ext: str, carrier):
    import karrio.server.core.datatypes as datatypes
    import karrio.server.core.dataunits as dataunits
    import karrio.server.graph.serializers as graph_serializers

    class_name = carrier.__name__
    references = dataunits.contextual_reference(reduced=False)
    connection_configs = [
        _
        for _ in (references["connection_configs"].get(ext) or {}).keys()
        if _ in SUPPORTED_CONNECTION_CONFIGS
    ]
    carrier_services = (references["services"].get(ext) or {}).keys()
    carrier_options = (references["options"].get(ext) or {}).keys()

    class _Form(forms.ModelForm):
        for key in connection_configs:
            if key == "cost_center":
                cost_center = forms.CharField(
                    required=False,
                )
            if key == "language_code":
                language_code = forms.ChoiceField(
                    choices=[("en", "EN"), ("fr", "FR")],
                    widget=forms.Select(attrs={"class": "vTextField"}),
                    required=False,
                )
            if key == "default_currency":
                default_currency = forms.ChoiceField(
                    choices=datatypes.CURRENCIES,
                    widget=forms.Select(attrs={"class": "vTextField"}),
                    required=False,
                )
            if key == "label_type":
                label_type = forms.ChoiceField(
                    choices=[(None, ""), *datatypes.LABEL_TYPES],
                    widget=forms.Select(attrs={"class": "vTextField"}),
                    required=False,
                    initial=None,
                )
            if key == "enforce_zpl":
                enforce_zpl = forms.NullBooleanField(
                    required=False,
                    initial=None,
                )
            if key == "shipping_services":
                shipping_services = forms.MultipleChoiceField(
                    choices=[(_, _) for _ in carrier_services],
                    widget=forms.SelectMultiple(attrs={"class": "vTextField"}),
                    required=False,
                    initial=None,
                )
            if key == "shipping_options":
                shipping_options = forms.MultipleChoiceField(
                    choices=[(_, _) for _ in carrier_options],
                    widget=forms.SelectMultiple(attrs={"class": "vTextField"}),
                    required=False,
                    initial=None,
                )

        class Meta:
            model = carrier
            fields = "__all__"

        def __init__(self, *args, instance: carriers.Carrier = None, **kwargs):
            if instance is not None:
                kwargs.update({"instance": instance})
                config = carriers.Carrier.resolve_config(
                    instance, is_system_config=True
                )

                for key in connection_configs:
                    self.base_fields[key].initial = (
                        None if config is None else config.config.get(key)
                    )

            super(_Form, self).__init__(*args, **kwargs)

        def save(self, commit: bool = True):
            config_data = lib.to_dict(
                {key: self.cleaned_data.get(key) for key in connection_configs}
            )
            carrier = super(_Form, self).save(commit)

            if any(connection_configs) and (commit or carrier.pk is not None):
                config = carriers.Carrier.resolve_config(carrier, is_system_config=True)
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
                (
                    carriers.CarrierConfig.objects.create(
                        created_by=created_by,
                        carrier=carrier,
                        config=config_value,
                    )
                    if config is None
                    else carriers.CarrierConfig.objects.filter(carrier=carrier).update(
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
        exclude = (
            ["active_users", "services"]
            if hasattr(carrier, "services")
            else ["active_users"]
        )
        fieldsets = [
            (
                None,
                {
                    "fields": [
                        _
                        for _ in _fields
                        if _
                        not in [
                            *connection_configs,
                            "active_users",
                            "services",
                            "is_system",
                        ]
                    ],
                },
            ),
        ]

        if any(connection_configs):
            fieldsets += [
                (  # type: ignore
                    "Connection Config",
                    {
                        "fields": [_ for _ in connection_configs if _ in _fields],
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

        if hasattr(carrier, "services"):

            class _ServiceInline(admin.TabularInline):
                model = carrier.services.through
                extra = 0

                def get_formset(self, request, obj, **kwargs):
                    formset = super().get_formset(request, obj, **kwargs)
                    _filter = (
                        models.Q()
                        if obj is None
                        else models.Q(
                            **{f"{class_name.lower()}__id": getattr(obj, "id", None)}
                        )
                    )
                    _filter = _filter | models.Q(
                        **{
                            f"{field.name}__isnull": True
                            for field in carriers.ServiceLevel._meta.get_fields()
                            if "settings" in field.name
                        }
                    )
                    formset.form.base_fields[
                        "servicelevel"
                    ].queryset = carriers.ServiceLevel.objects.filter(
                        _filter
                    ).distinct()
                    return formset

            inlines += [_ServiceInline]

        if settings.MULTI_ORGANIZATIONS:

            class ActiveOrgInline(admin.TabularInline):
                model = carrier.active_orgs.through
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
                model = carrier.active_users.through
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
            carrier_name = next(
                (k for k, v in carriers.MODELS.items() if v == carrier), None
            )
            raw_capabilities = ref.get_carrier_capabilities(carrier_name)
            form.base_fields["capabilities"].choices = [
                (c, c) for c in raw_capabilities
            ]
            form.base_fields["capabilities"].initial = raw_capabilities

            return form

        def save_model(self, request, obj, form, change):
            obj.is_system = True
            return super().save_model(request, obj, form, change)

    return type(f"{class_name}Admin", (_Admin,), {})


@admin.register(carriers.ServiceLevel)
class ServiceLevelAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

    def has_module_permission(self, request):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["currency"].required = True
        form.base_fields["currency"].initial = "USD"

        form.base_fields["created_by"].initial = request.user
        field = form.base_fields["created_by"]
        field.widget = field.hidden_widget()
        return form


@admin.register(carriers.LabelTemplate)
class LabelTemplateAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


for name, model in carriers.MODELS.items():
    admin.site.register(model, model_admin(name, model))
