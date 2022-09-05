import graphene
import graphene_django.filter as django_filter

import karrio.server.graph.utils as utils
import karrio.server.graph.extension.audit.types as types
import karrio.server.audit.models as models


class Query:
    auditlog = graphene.Field(
        types.AuditLogEntryType, id=graphene.String(required=True)
    )
    auditlogs = django_filter.DjangoFilterConnectionField(
        types.AuditLogEntryType,
        required=True,
        filterset_class=types.AuditLogEntryFilter,
        default_value=[],
    )

    @utils.authentication_required
    @utils.authorization_required(["AUDIT_LOGGING"])
    def resolve_auditlog(self, info, **kwargs):
        return models.AuditLogEntry.access_by(info.context).filter(**kwargs).first()

    @utils.authentication_required
    @utils.authorization_required(["AUDIT_LOGGING"])
    def resolve_auditlogs(self, info, **kwargs):
        return models.AuditLogEntry.access_by(info.context)
