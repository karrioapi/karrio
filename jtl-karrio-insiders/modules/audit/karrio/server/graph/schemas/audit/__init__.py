import strawberry

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.audit.types as types


@strawberry.type
class Query:
    auditlog: types.AuditLogEntryType = strawberry.field(resolver=types.AuditLogEntryType.resolve)
    auditlogs: utils.Connection[types.AuditLogEntryType] = strawberry.field(
        resolver=types.AuditLogEntryType.resolve_list
    )
