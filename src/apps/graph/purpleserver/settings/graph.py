from purpleserver.settings.base import INSTALLED_APPS


INSTALLED_APPS = [
    *INSTALLED_APPS,

    'graphene_django',
]

GRAPHENE = {
    "SCHEMA": "purpleserver.graph.schema.schema"
}
