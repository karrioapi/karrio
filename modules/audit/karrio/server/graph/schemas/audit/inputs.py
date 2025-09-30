import typing
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.audit.serializers as serializers


LogEntryAction: typing.Any = strawberry.enum(serializers.LogEntryAction)


@strawberry.input
class AuditLogEntryFilter(utils.Paginated):
    object_pk: typing.Optional[str] = strawberry.UNSET
    action: typing.List[str] = strawberry.UNSET
