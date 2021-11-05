from purplship.server.settings.base import *


INSTALLED_APPS += [
    'graphene_django',
]

GRAPHENE = {
    "SCHEMA": "purplship.server.graph.schema.schema",
    "MIDDLEWARE": []
}
