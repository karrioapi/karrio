# type: ignore
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

import strawberry
from strawberry.schema.config import StrawberryConfig
from karrio.server.graph.schemas.base import Query, Mutation, extra_types


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=False),
    types=[*extra_types],
)
