from django_filters import rest_framework as filters

import karrio.server.audit.models as models


class AuditLogEntryFilter(filters.FilterSet):
    object_pk = filters.CharFilter(field_name="object_pk", lookup_expr="icontains")
    action = filters.CharFilter(
        field_name="action",
        lookup_expr="icontains",
        help_text="audit log action",
    )

    class Meta:
        model = models.AuditLogEntry
        fields: list = []
