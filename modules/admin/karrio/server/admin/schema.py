import pkgutil
import strawberry
import strawberry.schema.config as config
from strawberry.types import Info

import karrio.server.admin.schemas as schemas
from karrio.server.core.logging import logger

QUERIES: list = []
MUTATIONS: list = []
EXTRA_TYPES: list = []

# Register karrio admin graphql schemas
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
        logger.warning("Failed to register schema", schema_name=name, error=str(e), exc_info=True)


# Fallback placeholder to prevent empty schema errors when no modules are installed
if not QUERIES:

    @strawberry.type
    class _FallbackQuery:
        @strawberry.field
        def _placeholder(self, info: Info) -> str:
            return "No admin GraphQL schemas registered"

    QUERIES.append(_FallbackQuery)


@strawberry.type
class Query(*QUERIES):  # type: ignore
    pass


schema_kwargs = dict(
    query=Query,
    types=[*EXTRA_TYPES],
    config=config.StrawberryConfig(auto_camel_case=False),
    extensions=[],
)

if MUTATIONS:

    @strawberry.type
    class Mutation(*MUTATIONS):  # type: ignore
        pass

    schema_kwargs["mutation"] = Mutation

schema = strawberry.federation.Schema(**schema_kwargs)  # type: ignore
