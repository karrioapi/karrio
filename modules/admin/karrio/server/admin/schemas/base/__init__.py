import typing
import strawberry
from strawberry.types import Info
import strawberry.schema.config as config

import karrio.server.graph.schemas.base as base
import karrio.server.admin.schemas.base.mutations as mutations
import karrio.server.admin.schemas.base.inputs as inputs
import karrio.server.admin.schemas.base.types as types
import karrio.server.admin.utils as utils

extra_types: list = []


def get_admin(root) -> str:
    return "admin"


@strawberry.type
class Query:
    configs: types.InstanceConfigType = strawberry.field(
        resolver=types.InstanceConfigType.resolve
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_configs(
        self, info: Info, input: inputs.InstanceConfigMutationInput
    ) -> mutations.InstanceConfigMutation:
        return mutations.InstanceConfigMutation.mutate(info, **input.to_dict())
