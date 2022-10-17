from django.urls import reverse
from rest_framework.request import Request

from karrio.server.conf import settings
import karrio.references as references
import karrio.core.units as units
import karrio.server.providers.models as providers


PACKAGE_MAPPERS = references.collect_providers_data()

REFERENCE_MODELS = {
    **references.collect_references(),
    "customs_content_type": {c.name: c.value for c in list(units.CustomsContentType)},
    "incoterms": {c.name: c.value for c in list(units.Incoterm)},
}
REFERENCE_EXCLUSIONS = [
    "currencies",
    "incoterms",
    "weight_units",
    "dimension_units",
    "payment_types",
    "option_names",
    "customs_content_type",
    "options",
]
CARRIER_NAMES = list(sorted(providers.MODELS.keys()))
CARRIER_HUBS = list(sorted(REFERENCE_MODELS["carrier_hubs"].keys()))
NON_HUBS_CARRIERS = [
    carrier_name for carrier_name in CARRIER_NAMES if carrier_name not in CARRIER_HUBS
]


def contextual_metadata(request: Request):
    host = (
        request.build_absolute_uri(reverse("karrio.server.core:metadata", kwargs={}))
        if hasattr(request, "build_absolute_uri")
        else ""
    )
    return {
        "VERSION": settings.VERSION,
        "APP_NAME": settings.APP_NAME,
        **({"APP_WEBSITE": settings.APP_WEBSITE} if settings.APP_WEBSITE else {}),
        "ADMIN": f"{host}admin/",
        "OPENAPI": f"{host}openapi",
        "GRAPHQL": f"{host}graphql",
        **{
            flag: getattr(settings, flag, None)
            for flag, _ in settings.FEATURE_FLAGS
        },
    }


def contextual_reference(request: Request = None, reduced: bool = True):
    import karrio.server.core.validators as validators
    import karrio.server.core.gateway as gateway
    import karrio.server.core.middleware as middleware

    request = request or middleware.SessionContext.get_current_request()
    is_authenticated = (
        request.user.is_authenticated if hasattr(request, "user") else False
    )
    references = {
        **contextual_metadata(request),
        "ADDRESS_AUTO_COMPLETE": validators.Address.get_info(is_authenticated),
        **{
            k: v
            for k, v in REFERENCE_MODELS.items()
            if k not in (REFERENCE_EXCLUSIONS if reduced else [])
        },
    }

    if is_authenticated and "generic" in providers.MODELS:
        custom_carriers = [
            c.settings
            for c in gateway.Carriers.list(context=request, carrier_name="generic")
        ]
        extra_carriers = {
            c.custom_carrier_name: c.display_name for c in custom_carriers
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
                custom_carriers=extra_carriers,
                services={**references["services"], **extra_services},
                service_names={**references["service_names"], **extra_service_names},
            )
        )

    return references
