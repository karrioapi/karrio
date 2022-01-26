from django.conf import settings
from django.urls import reverse
from django.forms import model_to_dict
from rest_framework.request import Request

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


def contextual_reference(request: Request):
    import purplship.server.core.validators as validators
    import purplship.server.core.gateway as gateway

    is_authenticated = request.auth is not None
    host = request.build_absolute_uri(
        reverse("purplship.server.core:metadata", kwargs={})
    )
    references = {
        **METADATA,
        "ADMIN": f"{host}admin/",
        "OPENAPI": f"{host}openapi",
        "GRAPHQL": f"{host}graphql",
        "ADDRESS_AUTO_COMPLETE": validators.Address.get_info(is_authenticated),
        **REFERENCE_MODELS,
    }

    if is_authenticated:
        custom_carriers = [
            c.settings
            for c in gateway.Carriers.list(context=request, carrier_name="generic")
        ]
        extra_carriers = {
            c.custom_carrier_name: c.verbose_name for c in custom_carriers
        }
        extra_services = {
            c.custom_carrier_name: {
                s.service_code: s.service_code for s in c.services.all()
            }
            for c in custom_carriers
        }
        extra_service_names = {
            name: {key: key.upper().replace("_", " ") for key, _ in value.items()}
            for name, value in extra_services.items()
        }

        references.update(
            dict(
                carriers={**references["carriers"], **extra_carriers},
                services={**references["services"], **extra_services},
                service_names={**references["service_names"], **extra_service_names},
            )
        )

    return references
