from django.conf import settings

from purplship.references import collect_providers_data, collect_references
from purplship.server.core.serializers import CustomsContentType, Incoterm


PACKAGE_MAPPERS = collect_providers_data()

METADATA = {
    "APP_NAME": getattr(settings, "APP_NAME", "purplship"),
    "APP_VERSION": getattr(settings, "VERSION"),
    "APP_WEBSITE": getattr(settings, "APP_WEBSITE", "https://purplship.com"),
    "MULTI_ORGANIZATIONS": getattr(settings, "MULTI_ORGANIZATIONS", False),
    "ORDERS_MANAGEMENT": getattr(settings, "ORDERS_MANAGEMENT", False),
}

REFERENCE_MODELS = {
    **collect_references(),
    "customs_content_type": {c.name: c.value for c in list(CustomsContentType)},
    "incoterms": {c.name: c.value for c in list(Incoterm)},
}
