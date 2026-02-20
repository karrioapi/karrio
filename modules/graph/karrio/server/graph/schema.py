import pkgutil
import strawberry
import strawberry.schema.config as config
from strawberry.types import Info

from karrio.server.core.logging import logger
import karrio.server.graph.schemas as schemas

QUERIES: list = []
MUTATIONS: list = []
EXTRA_TYPES: list = []

# Register karrio graphql schemas
for _, name, _ in pkgutil.iter_modules(schemas.__path__):  # type: ignore
    try:
        schema = __import__(f"{schemas.__name__}.{name}", fromlist=[name])
        if hasattr(schema, "Query"):
            QUERIES.append(schema.Query)
        if hasattr(schema, "Mutation"):
            MUTATIONS.append(schema.Mutation)
        if hasattr(schema, "extra_types"):
            EXTRA_TYPES += schema.extra_types
    except Exception as e:
        logger.warning("Failed to register GraphQL schema", schema_name=name, error=str(e))
        logger.exception("GraphQL schema registration error", schema_name=name)


# Fallback placeholder to prevent empty schema errors when no modules are installed
if not QUERIES:

    @strawberry.type
    class _FallbackQuery:
        @strawberry.field
        def _placeholder(self, info: Info) -> str:
            return "No GraphQL schemas registered"

    QUERIES.append(_FallbackQuery)

if not MUTATIONS:

    @strawberry.type
    class _FallbackMutation:
        @strawberry.mutation
        def _placeholder(self, info: Info) -> str:
            return "No GraphQL schemas registered"

    MUTATIONS.append(_FallbackMutation)


@strawberry.type
class Query(*QUERIES):  # type: ignore
    pass


@strawberry.type
class Mutation(*MUTATIONS):  # type: ignore
    pass


schema = strawberry.Schema(  # type: ignore
    query=Query,
    mutation=Mutation,
    types=[*EXTRA_TYPES],
    config=config.StrawberryConfig(auto_camel_case=False),
    extensions=[],
)
