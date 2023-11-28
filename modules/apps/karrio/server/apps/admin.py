from django.contrib import admin
from karrio.server.apps import models


class AppAdmin(admin.ModelAdmin):
    list_display = ("id", "is_public", "is_published", "launch_url", "created_at")

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.filter(id__in=models.App.access_by(request.user))


class AppInstallationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    readonly_fields = [
        f.name
        for f in models.AppInstallation._meta.get_fields()
        if f.name not in ["org", "link"]
    ]

    def has_add_permission(self, request) -> bool:
        return False

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.filter(id__in=models.AppInstallation.access_by(request.user))


admin.site.register(models.App, AppAdmin)
admin.site.register(models.AppInstallation, AppInstallationAdmin)
