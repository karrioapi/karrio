import typing
import strawberry
from django.conf import settings

import karrio.server.graph.utils as utils


InstanceConfigMutationInput = strawberry.input(
    type(
        "InstanceConfigMutationInput",
        (utils.BaseInput,),
        {
            **{k: strawberry.UNSET for k, _ in settings.CONSTANCE_CONFIG.items()},
            "__annotations__": {
                k: typing.Optional[_def[2]]
                for k, _def in settings.CONSTANCE_CONFIG.items()
            },
        },
    )
)
