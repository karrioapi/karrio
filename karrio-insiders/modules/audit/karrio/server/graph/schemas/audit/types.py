import typing
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.audit.inputs as inputs
import karrio.server.audit.filters as filters
import karrio.server.audit.models as models


@strawberry.type
class AuditLogEntryType:
    object_type: str
    id: str
    object_pk: str
    object_id: int
    object_str: str
    action: inputs.LogEntryAction

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["AUDIT_LOGGING"])
    def resolve(info, id: str) -> typing.Optional["AuditLogEntryType"]:
        return models.AuditLogEntry.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["AUDIT_LOGGING"])
    def resolve_list(
        info,
        filter: typing.Optional[inputs.AuditLogEntryFilter] = strawberry.UNSET,
    ) -> utils.Connection["AuditLogEntryType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.AuditLogEntryFilter()
        queryset = filters.AuditLogEntryFilter(
            _filter.to_dict(), models.AuditLogEntry.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())

