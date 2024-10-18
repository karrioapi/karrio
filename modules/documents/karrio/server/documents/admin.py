import django.forms as forms
from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework_tracking.admin import APIRequestLog

import karrio.server.documents.models as models
import karrio.server.documents.serializers.base as serializers


class DocumentTemplateAdminForm(forms.ModelForm):
    class Meta:
        model = models.DocumentTemplate
        fields = "__all__"
        widgets = {
            "template": forms.Textarea(attrs={"rows": 30, "cols": 100}),
            "related_object": forms.Select(
                choices=[
                    (c.name, c.name) for c in list(serializers.TemplateRelatedObject)
                ]
            ),
        }


class DocumentTemplateAdmin(admin.ModelAdmin):
    form = DocumentTemplateAdminForm
    list_display = ("slug", "name", "related_object", "active", "created_at")
    search_fields = ("name", "description", "slug", "related_object")
    list_filter = ("slug", "active")
    readonly_fields = ("created_by",)

    def get_queryset(self, request):
        if settings.MULTI_ORGANIZATIONS:
            return models.DocumentTemplate.objects.all().filter(
                link__org__users__id=request.user.id
            )

        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

        if settings.MULTI_ORGANIZATIONS:
            import karrio.server.serializers as serializers

            serializers.link_org(obj, request)


# Register your models here.
admin.site.register(models.DocumentTemplate, DocumentTemplateAdmin)
