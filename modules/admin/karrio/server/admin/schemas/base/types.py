import typing
import datetime
import strawberry
from constance import config
from django.conf import settings
from strawberry.types import Info

import karrio.server.graph.schemas.base as base
import karrio.server.graph.utils as utils
import karrio.server.admin.utils as admin


@strawberry.type
class _InstanceConfigType:
    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info) -> "InstanceConfigType":
        return InstanceConfigType(  # type: ignore
            **{k: getattr(config, k) for k in settings.CONSTANCE_CONFIG.keys()}
        )


InstanceConfigType = strawberry.type(
    type(
        "InstanceConfigType",
        (_InstanceConfigType,),
        {
            **{k: strawberry.UNSET for k, _ in settings.CONSTANCE_CONFIG.items()},
            "__annotations__": {
                k: typing.Optional[_def[2]]
                for k, _def in settings.CONSTANCE_CONFIG.items()
            },
        },
    )
)
