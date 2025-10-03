from django.db import models
from django.contrib import admin
import auditlog.admin as auditlog

import karrio.server.audit.models as audit


class LogEntryAdmin(auditlog.LogEntryAdmin):
    list_display = [*auditlog.LogEntryAdmin.list_display, "org_name"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.filter(
            models.Q(org__users__id=request.user.id)
            | models.Q(actor_id=request.user.id)
            | models.Q(object_pk=request.user.id)
            | models.Q(actor__isnull=True)
        )
        # return queryset

    def org_name(self, obj):
        return getattr(getattr(obj, "link", None), "org", "system")


admin.site.unregister(auditlog.LogEntry)
admin.site.register(audit.AuditLogEntry, LogEntryAdmin)
