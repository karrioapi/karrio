import typing
import datetime
import strawberry
from strawberry.types import Info

import karrio.server.graph.schemas.base as base
import karrio.server.graph.utils as utils
import karrio.server.admin.utils as admin


@strawberry.type
class InstanceType:
    id: str

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info) -> typing.Optional["InstanceType"]:
        pass
