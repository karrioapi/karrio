from django.conf import settings

from purplship.references import collect_providers_data, collect_references
from purpleserver.core.serializers import CustomsContentType, Incoterm


APP_NAME = getattr(settings, 'APP_NAME', 'Purplship')
APP_VERSION = getattr(settings, 'VERSION')
PACKAGE_MAPPERS = collect_providers_data()

REFERENCE_MODELS = {
    **collect_references(),
    "customs_content_type": {c.name: c.value for c in list(CustomsContentType)},
    "incoterms": {c.name: c.value for c in list(Incoterm)},

    "APP_NAME": APP_NAME,
    "APP_VERSION": APP_VERSION,
}
