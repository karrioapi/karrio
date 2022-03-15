import pkgutil
import logging
import typing
import graphene
from graphene_django.debug import DjangoDebug

import karrio.server.graph.extension as extensions

logger = logging.getLogger(__name__)

QUERIES: typing.List[graphene.ObjectType] = []
MUTATIONS: typing.List[graphene.ObjectType] = []

# Register karrio graphql schemas
for _, name, _ in pkgutil.iter_modules(extensions.__path__):
    try:
        schema = __import__(f"{extensions.__name__}.{name}", fromlist=[name])
        hasattr(schema, "Query") and QUERIES.append(schema.Query)
        hasattr(schema, "Mutation") and MUTATIONS.append(schema.Mutation)
    except Exception as e:
        logger.warning(f'Failed to register "{name}" schema')
        logger.exception(e)


class Query(*QUERIES, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(*MUTATIONS, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)
