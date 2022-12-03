from django.db import models
from django.contrib import admin
from django import forms

import karrio.server.providers.models as carriers


def model_admin(carrier):
    class_name = carrier.__name__

    class _Admin(admin.ModelAdmin):
        list_display = ("__str__", "test_mode", "active")
        exclude = (
            ["active_users", "services"]
            if hasattr(carrier, "services")
            else ["active_users"]
        )
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
            }
        }

        if hasattr(carrier, "services"):
            class _ServiceInline(admin.TabularInline):
                model = carrier.services.through
                extra = 0

                def get_formset(self, request, obj, **kwargs):
                    formset = super().get_formset(request, obj, **kwargs)
                    _filter = models.Q() if obj is None else models.Q(**{
                        f"{class_name.lower()}__id": getattr(obj, "id", None)
                    })
                    _filter = _filter | models.Q(**{
                        f"{field.name}__isnull": True
                        for field in carriers.ServiceLevel._meta.get_fields()
                        if 'settings' in field.name
                    })
                    formset.form.base_fields["servicelevel"].queryset = carriers.ServiceLevel.objects.filter(_filter).distinct()
                    return formset

            inlines = [_ServiceInline]

        def get_queryset(self, request):
            query = super().get_queryset(request)
            return query.filter(created_by=None)

    return type(f"{class_name}Admin", (_Admin,), {})


@admin.register(carriers.ServiceLevel)
class ServiceLevelAdmin(admin.ModelAdmin):
    # form = ServiceLevelForm
    list_display = ("__str__",)
    def has_module_permission(self, request):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['cost'].required = True
        form.base_fields['cost'].initial = 10
        form.base_fields['currency'].required = True
        form.base_fields['currency'].initial = "USD"

        form.base_fields['created_by'].initial = request.user
        field = form.base_fields['created_by']
        field.widget = field.hidden_widget()
        return form


@admin.register(carriers.LabelTemplate)
class LabelTemplateAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


for name, model in carriers.MODELS.items():
    admin.site.register(model, model_admin(model))
