import typing
import strawberry
from strawberry.types import Info
import strawberry.schema.config as config

import karrio.server.graph.schemas.base as base
import karrio.server.admin.graph.schema.mutations as mutations
import karrio.server.admin.graph.schema.inputs as inputs
import karrio.server.admin.graph.schema.types as types
import karrio.server.admin.utils as utils

extra_types: list = []


def get_admin(root) -> str:
    return "admin"


@strawberry.type
class Query:
    admin: typing.Optional[str] = strawberry.field(resolver=get_admin)


@strawberry.type
class Mutation:
    pass


schema = strawberry.federation.Schema(  # type: ignore
    query=Query,
    # mutation=Mutation,
    config=config.StrawberryConfig(auto_camel_case=False),
    enable_federation_2=True,
)
