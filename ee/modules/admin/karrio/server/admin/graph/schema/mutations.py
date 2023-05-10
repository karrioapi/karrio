import typing
import strawberry
from strawberry.types import Info
from rest_framework import exceptions

import karrio.server.conf as conf
import karrio.server.core.utils as core
import karrio.server.graph.utils as utils
import karrio.server.admin.graph.schema.types as types
import karrio.server.admin.graph.schema.inputs as inputs
import karrio.server.admin.utils as admin


@strawberry.type
class InstanceConfigMutation(utils.BaseMutation):
    tenant: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def mutate(
        info: Info,
        **input: inputs.InstanceConfigMutationInput,
    ) -> "InstanceConfigMutation":
        pass
