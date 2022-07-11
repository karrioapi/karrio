from auditlog.models import LogEntry
from django.utils.translation import gettext_lazy as _

import karrio.server.core.models as core


class AuditLogEntry(LogEntry, core.ControlledAccessModel):
    class Meta:
        proxy = True
        verbose_name = _("log entry")
        verbose_name_plural = _("log entries")

    @property
    def object_type(self):
        return "auditlog"
