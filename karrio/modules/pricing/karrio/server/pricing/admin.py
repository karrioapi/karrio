import importlib

from django import forms
from django.contrib import admin
from karrio.server.pricing.models import Surcharge

if importlib.util.find_spec("karrio.server.orgs") is not None:
    import karrio.server.orgs.models as orgs


class SurchargeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (("name", "active"), ("amount", "surcharge_type"))}),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": (
                    "carriers",
                    "carrier_accounts",
                    "services",
                ),
            },
        ),
    )

    if importlib.util.find_spec("karrio.server.orgs") is not None:

        class SurchargeForm(forms.ModelForm):
            class Meta:
                model = Surcharge
                fields = "__all__"

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                if kwargs.get("instance") is not None:
                    self.fields["organizations"].initial = kwargs["instance"].org.all()

            organizations = forms.ModelMultipleChoiceField(
                queryset=orgs.Organization.objects.all(), required=False
            )

            def save(self, commit=True):
                instance = super().save(commit=commit)
                instance.save()
                organizations = self.cleaned_data.get("organizations", [])
                instance.org.set(organizations)
                return instance

        form = SurchargeForm
        fieldsets += ((None, {"fields": ("organizations",)}),)


admin.site.register(Surcharge, SurchargeAdmin)
