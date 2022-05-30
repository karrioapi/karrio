from karrio.server.settings.base import *


INSTALLED_APPS += [
    "strawberry.django",
]

# GRAPHENE = {"SCHEMA": "karrio.server.graph.schema.schema", "MIDDLEWARE": []}
