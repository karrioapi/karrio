import typing
import logging
import strawberry
from constance import config
from strawberry.types import Info

import karrio.server.conf as conf
import karrio.server.core.utils as core
import karrio.server.graph.utils as utils
import karrio.server.admin.utils as admin
import karrio.server.admin.schemas.base.types as types
import karrio.server.admin.schemas.base.inputs as inputs


@strawberry.type
class InstanceConfigMutation(utils.BaseMutation):
    configs: typing.Optional[types.InstanceConfigType] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def mutate(
        info: Info,
        **input: inputs.InstanceConfigMutationInput,
    ) -> "InstanceConfigMutation":
        for k, v in input.items():
            setattr(config, k, v)
        return InstanceConfigMutation(config=types.InstanceConfigType.resolve(info))
