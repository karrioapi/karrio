from purpleserver.settings.base import INSTALLED_APPS


INSTALLED_APPS = [
    *INSTALLED_APPS,

    'graphene_django',
    'django_filters',
]

GRAPHENE = {
    "SCHEMA": "purpleserver.graph.schema.schema",
    "MIDDLEWARE": []
}
