import django.forms as forms
from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse

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
    list_display = ("slug", "name", "related_object", "active", "created_at", "preview_link")
    search_fields = ("name", "description", "slug", "related_object")
    list_filter = ("slug", "active")
    readonly_fields = ("created_by", "full_preview_url")

    def preview_link(self, obj):
        """Return a clickable preview link that opens in a new tab"""
        url = obj.preview_url()
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer">Preview</a>',
            url
        )

    preview_link.short_description = "Preview"

    def full_preview_url(self, obj):
        """Return the full absolute URL for the preview"""
        if obj.pk:
            request = self.request if hasattr(self, 'request') else None
            if request:
                relative_url = obj.preview_url()
                absolute_url = request.build_absolute_uri(relative_url)
                return format_html(
                    '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>',
                    absolute_url, absolute_url
                )
            else:
                # Fallback if request is not available
                relative_url = obj.preview_url()
                return f"(Relative URL: {relative_url})"
        return "Save the template first to generate preview URL"

    full_preview_url.short_description = "Full Preview URL"

    def get_queryset(self, request):
        if settings.MULTI_ORGANIZATIONS:
            return models.DocumentTemplate.objects.all().filter(
                link__org__users__id=request.user.id
            )

        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        # Store request for use in full_preview_url method
        self.request = request
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

        if settings.MULTI_ORGANIZATIONS:
            import karrio.server.serializers as serializers

            serializers.link_org(obj, request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Store request for use in full_preview_url method
        self.request = request
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        # Store request for use in full_preview_url method
        self.request = request
        return super().add_view(request, form_url, extra_context)


# Register your models here.
admin.site.register(models.DocumentTemplate, DocumentTemplateAdmin)
