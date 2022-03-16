from karrio.server.settings.base import *


INSTALLED_APPS += [
    "graphene_django",
]

GRAPHENE = {"SCHEMA": "karrio.server.graph.schema.schema", "MIDDLEWARE": []}
