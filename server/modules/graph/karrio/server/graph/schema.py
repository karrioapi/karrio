import pkgutil
import logging
import strawberry
import strawberry.schema.config as config

import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas as schemas

logger = logging.getLogger(__name__)

QUERIES: list = []
MUTATIONS: list = []

# Register karrio graphql schemas
for _, name, _ in pkgutil.iter_modules(schemas.__path__): # type: ignore
    try:
        schema = __import__(f"{schemas.__name__}.{name}", fromlist=[name])
        if hasattr(schema, "Query"):
            QUERIES.append(schema.Query)
        if hasattr(schema, "Mutation"):
            MUTATIONS.append(schema.Mutation)
    except Exception as e:
        logger.warning(f'Failed to register "{name}" schema')
        logger.exception(e)


@strawberry.type
class Query(*QUERIES): # type: ignore
    pass


@strawberry.type
class Mutation(*MUTATIONS): # type: ignore
    pass


schema = strawberry.Schema( # type: ignore
    query=Query,
    mutation=Mutation,
    types=[*base.extra_types],
    config=config.StrawberryConfig(auto_camel_case=False),
)
