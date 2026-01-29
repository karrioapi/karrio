from constance import config
from django.urls import reverse
from rest_framework.request import Request

import karrio.lib as lib
import karrio.references as ref
import karrio.core.units as units
import karrio.server.conf as conf
import karrio.server.core.utils as utils


PACKAGE_MAPPERS = ref.collect_providers_data()
REFERENCE_MODELS = {
    **ref.collect_references(),
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
CARRIER_NAMES = list(sorted(set([*REFERENCE_MODELS["carriers"].keys(), "generic"])))
CARRIER_HUBS = list(sorted(REFERENCE_MODELS["carrier_hubs"].keys()))
NON_HUBS_CARRIERS = [
    carrier_name for carrier_name in CARRIER_NAMES if carrier_name not in CARRIER_HUBS
]


def contextual_metadata(request: Request):
    # Detect HTTPS from headers (for proxied environments like Caddy/ALB)
    is_https = False
    if hasattr(request, 'META'):
        # Check X-Forwarded-Proto header (set by load balancers/proxies)
        forwarded_proto = request.META.get('HTTP_X_FORWARDED_PROTO', '').lower()
        # Check if request is secure (Django's built-in HTTPS detection)
        is_secure = getattr(request, 'is_secure', lambda: False)()
        is_https = forwarded_proto == 'https' or is_secure

    if hasattr(request, "build_absolute_uri"):
        _host: str = request.build_absolute_uri(
            reverse("karrio.server.core:metadata", kwargs={})
        )
        # Override protocol if we detected HTTPS but build_absolute_uri returned HTTP
        if is_https and _host.startswith('http://'):
            _host = _host.replace('http://', 'https://', 1)
    else:
        _host = "/"

    host = _host[:-1] if _host[-1] == "/" else _host
    name = lib.identity(
        getattr(conf.settings.tenant, "name", conf.settings.APP_NAME)
        if conf.settings.MULTI_TENANTS
        else getattr(config, "APP_NAME", None) or conf.settings.APP_NAME
    )
    website = lib.identity(
        getattr(conf.settings.tenant, "website", conf.settings.APP_WEBSITE)
        if conf.settings.MULTI_TENANTS
        else getattr(config, "APP_WEBSITE", None) or conf.settings.APP_WEBSITE
    )

    # Batch fetch all feature flags
    flag_names = [flag for flag, _ in conf.settings.FEATURE_FLAGS]

    if conf.settings.MULTI_TENANTS:
        # In multi-tenancy mode, feature flags come from tenant.feature_flags (JSON field)
        # No N+1 issue since it's a single field access on an already-loaded tenant object
        tenant = conf.settings.tenant
        tenant_flags = getattr(tenant, "feature_flags", {}) if tenant else {}
        feature_flags = {
            flag: tenant_flags.get(flag, getattr(conf.settings, flag, None))
            for flag in flag_names
        }
    else:
        # In single-tenant mode, batch fetch from Constance to avoid N+1 queries
        constance_values = utils.batch_get_constance_values(flag_names)
        feature_flags = {
            flag: (
                constance_values.get(flag)
                if flag in constance_values
                else getattr(conf.settings, flag, None)
            )
            for flag in flag_names
        }

    return {
        "VERSION": conf.settings.VERSION,
        "APP_NAME": name,
        "APP_WEBSITE": website,
        "HOST": f"{host}/",
        "ADMIN": f"{host}/admin",
        "GRAPHQL": f"{host}/graphql",
        "OPENAPI": f"{host}/openapi",
        **feature_flags,
    }


def _get_system_credentials_status() -> dict:
    """Compute which carriers have system credentials configured.

    Returns dict like:
    {
        "dhl_parcel_de": {"production": True, "sandbox": False},
        "teleship": {"production": True, "sandbox": True},
    }
    """
    result = {}

    for carrier_id, metadata_obj in ref.PLUGIN_METADATA.items():
        system_config = metadata_obj.get("system_config")
        if not system_config:
            continue

        # Group env vars by production/sandbox
        prod_vars = [k for k in system_config.keys() if "SANDBOX" not in k]
        sandbox_vars = [k for k in system_config.keys() if "SANDBOX" in k]

        # Check if production credentials are set (all vars must be non-empty)
        prod_configured = False
        if prod_vars:
            prod_configured = all(
                bool(getattr(config, var, None))
                for var in prod_vars
            )

        # Check if sandbox credentials are set (all vars must be non-empty)
        sandbox_configured = False
        if sandbox_vars:
            sandbox_configured = all(
                bool(getattr(config, var, None))
                for var in sandbox_vars
            )

        if prod_configured or sandbox_configured:
            result[carrier_id] = {
                "production": prod_configured,
                "sandbox": sandbox_configured,
            }

    return result


def contextual_reference(request: Request = None, reduced: bool = True):
    import karrio.server.core.gateway as gateway
    import karrio.server.core.validators as validators
    import karrio.server.core.middleware as middleware
    import karrio.server.providers.models as providers

    request = request or middleware.SessionContext.get_current_request()
    is_authenticated = lib.identity(
        request.user.is_authenticated if hasattr(request, "user") else False
    )

    # Compute system credentials availability
    system_credentials_carriers = lib.failsafe(
        lambda: _get_system_credentials_status(),
        {},
    )

    references = {
        **contextual_metadata(request),
        "ADDRESS_AUTO_COMPLETE": lib.failsafe(
            lambda: validators.Address.get_info(is_authenticated),
            None,
        ),
        "system_credentials_carriers": system_credentials_carriers,
        **{
            k: v
            for k, v in REFERENCE_MODELS.items()
            if k not in (REFERENCE_EXCLUSIONS if reduced else [])
        },
    }

    def _get_generic_carriers():
        # Get all carriers, then filter by extension instead of hardcoded slug
        system_custom_carriers = [
            c for c in gateway.Carriers.list(system_only=True)
            if c.ext == "generic"
        ]
        # Filter to only Carrier instances (user-owned connections, not brokered)
        custom_carriers = [
            c
            for c in (
                gateway.Carriers.list(context=request)
                if is_authenticated
                else []
            )
            if c.ext == "generic" and isinstance(c, providers.CarrierConnection)
        ]

        extra_carriers = {
            c.carrier_code: c.display_name
            for c in custom_carriers
        }
        system_carriers = {
            c.carrier_code: c.display_name
            for c in system_custom_carriers
        }
        extra_services = {
            c.carrier_code: {
                s.service_code: s.service_code
                for s in c.services
                or [
                    lib.to_object(lib.models.ServiceLevel, _)
                    for _ in references["service_levels"][c.ext]
                ]
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
                carriers={**references["carriers"], **system_carriers},
                service_names={**references["service_names"], **extra_service_names},
            )
        )

    if request is not None and "generic" in CARRIER_NAMES:
        _get_generic_carriers()

    return references


def get_carrier_details(
    carrier_name: str,
    contextual_reference: dict = None,
) -> dict:
    return ref.get_carrier_details(
        carrier_name,
        contextual_reference=contextual_reference or contextual_reference(),
    )
