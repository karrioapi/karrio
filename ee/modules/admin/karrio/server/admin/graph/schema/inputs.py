import typing
import strawberry

import karrio.server.graph.utils as utils


@strawberry.input
class InstanceConfigMutationInput(utils.BaseInput):
    ALLOW_ADMIN_APPROVED_SIGNUP: typing.Optional[bool] = strawberry.UNSET
