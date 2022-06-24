from auditlog.models import LogEntry

import karrio.server.core.models as core


class AuditLogEntry(LogEntry, core.ControlledAccessModel):
    class Meta:
        proxy = True

    @property
    def object_type(self):
        return "auditlog"
