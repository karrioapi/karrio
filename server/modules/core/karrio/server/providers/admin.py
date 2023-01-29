import functools
from django import forms
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model

import karrio.references as ref
import karrio.server.providers.models as carriers

User = get_user_model()


def model_admin(carrier):
    class_name = carrier.__name__

    class _Admin(admin.ModelAdmin):
        list_display = ("__str__", "test_mode", "active")
        exclude = (
            ["active_users", "services"]
            if hasattr(carrier, "services")
            else ["active_users"]
        )
        inlines = []
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
            return query.filter(created_by=None)

        def get_form(self, *args, **kwargs):
            form = super().get_form(*args, **kwargs)

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

    return type(f"{class_name}Admin", (_Admin,), {})


@admin.register(carriers.ServiceLevel)
class ServiceLevelAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

    def has_module_permission(self, request):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["cost"].required = True
        form.base_fields["cost"].initial = 10
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
    admin.site.register(model, model_admin(model))
