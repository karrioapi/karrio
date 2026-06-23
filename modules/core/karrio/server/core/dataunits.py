import karrio.core.units as units
import karrio.lib as lib
import karrio.references as ref
import karrio.server.conf as conf
import karrio.server.core.utils as utils
from django.urls import reverse
from rest_framework.request import Request

PACKAGE_MAPPERS = ref.collect_providers_data()
# Full installed catalog (never stale); the enabled gate is applied live at the
# request edge — see contextual_reference(include_disabled=...).
REFERENCE_MODELS = {
    **ref.collect_references(include_disabled=True),
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
NON_HUBS_CARRIERS = [carrier_name for carrier_name in CARRIER_NAMES if carrier_name not in CARRIER_HUBS]


def _plugin_flag_default(constance_config: dict, key: str) -> bool:
    """Default for an untoggled flag: its CONSTANCE_CONFIG value, matching getattr(config, key)."""
    spec = constance_config.get(key)
    if spec is not None:
        return bool(spec[0])
    return bool(ref.ENABLE_ALL_PLUGINS_BY_DEFAULT)


def get_enabled_plugin_ids() -> tuple:
    """Live (carriers, lsp) enabled sets from a single batched constance read (no per-plugin N+1)."""
    carrier_keys = {f"{c.upper()}_ENABLED": c for c in REFERENCE_MODELS["carriers"]}
    lsp_keys = {f"{p.upper()}_ENABLED": p for p in REFERENCE_MODELS.get("lsp_capabilities", {})}
    constance_config = getattr(conf.settings, "CONSTANCE_CONFIG", {})

    if conf.settings.MULTI_TENANTS:
        tenant = getattr(conf.settings, "tenant", None)
        source = getattr(tenant, "feature_flags", {}) if tenant else {}
    else:
        source = utils.batch_get_constance_values([*carrier_keys, *lsp_keys])

    def _enabled(keys: dict) -> set:
        return {pid for key, pid in keys.items() if source.get(key, _plugin_flag_default(constance_config, key))}

    enabled_carriers = _enabled(carrier_keys)
    enabled_carriers.add("generic")
    return enabled_carriers, _enabled(lsp_keys)


def get_enabled_carrier_ids() -> set:
    """Carrier ids whose plugin is currently enabled (``generic`` always in)."""
    return get_enabled_plugin_ids()[0]


def get_enabled_lsp_ids() -> set:
    return get_enabled_plugin_ids()[1]


def is_admin_surface(request) -> bool:
    """Surface-based (not role-based): staff on the normal app still get the tenant view."""
    return "/admin/" in getattr(request, "path", "") if request is not None else False


def _is_staff_request(request) -> bool:
    """Staff check that also works on /v1/references, which disables DRF auth (request.user is anonymous)."""
    user = getattr(request, "user", None)
    if getattr(user, "is_authenticated", False):
        return bool(getattr(user, "is_staff", False))

    from rest_framework.settings import api_settings

    # Run the configured authenticators read-only; never raises, never affects the response.
    for authenticator in api_settings.DEFAULT_AUTHENTICATION_CLASSES:
        result = lib.failsafe(lambda a=authenticator: a().authenticate(request))
        if result is not None:
            authed_user, _ = result
            return bool(getattr(authed_user, "is_staff", False))
    return False


def includes_disabled_carriers(request) -> bool:
    """Full catalog only for staff that explicitly ask (``?include_disabled=true``) — the admin app does, the normal app never."""
    if request is None:
        return False
    if is_admin_surface(request):
        return True
    raw = request.query_params.get("include_disabled") if hasattr(request, "query_params") else None
    if str(raw).lower() not in ("1", "true", "yes"):
        return False
    return _is_staff_request(request)


def ensure_carrier_enabled(carrier_name: str, request=None) -> None:
    """Reject tenant use of a not-enabled carrier; admin surfaces exempt. Request resolved from session context for serializers."""
    import karrio.server.core.middleware as middleware
    from django.utils.translation import gettext_lazy as _
    from rest_framework.exceptions import ValidationError

    request = request or middleware.SessionContext.get_current_request()
    if is_admin_surface(request):
        return
    if carrier_name not in get_enabled_carrier_ids():
        raise ValidationError({"carrier_name": _("This carrier is not available.")})


def contextual_metadata(request: Request):
    # Detect HTTPS from headers (for proxied environments like Caddy/ALB)
    is_https = False
    if hasattr(request, "META"):
        # Check X-Forwarded-Proto header (set by load balancers/proxies)
        forwarded_proto = request.META.get("HTTP_X_FORWARDED_PROTO", "").lower()
        # Check if request is secure (Django's built-in HTTPS detection)
        is_secure = getattr(request, "is_secure", lambda: False)()
        is_https = forwarded_proto == "https" or is_secure

    if hasattr(request, "build_absolute_uri"):
        _host: str = request.build_absolute_uri(reverse("karrio.server.core:metadata", kwargs={}))
        # Override protocol if we detected HTTPS but build_absolute_uri returned HTTP
        if is_https and _host.startswith("http://"):
            _host = _host.replace("http://", "https://", 1)
    else:
        _host = "/"

    host = _host[:-1] if _host[-1] == "/" else _host
    if conf.settings.MULTI_TENANTS:
        name = getattr(conf.settings.tenant, "name", conf.settings.APP_NAME)
        website = getattr(conf.settings.tenant, "website", conf.settings.APP_WEBSITE)
    else:
        # Batch fetch APP_NAME and APP_WEBSITE in a single query
        _app_config = utils.batch_get_constance_values(["APP_NAME", "APP_WEBSITE"])
        name = _app_config.get("APP_NAME") or conf.settings.APP_NAME
        website = _app_config.get("APP_WEBSITE") or conf.settings.APP_WEBSITE

    # Batch fetch all feature flags
    flag_names = [flag for flag, _ in conf.settings.FEATURE_FLAGS]

    if conf.settings.MULTI_TENANTS:
        # In multi-tenancy mode, feature flags come from tenant.feature_flags (JSON field)
        # No N+1 issue since it's a single field access on an already-loaded tenant object
        tenant = conf.settings.tenant
        tenant_flags = getattr(tenant, "feature_flags", {}) if tenant else {}
        feature_flags = {flag: tenant_flags.get(flag, getattr(conf.settings, flag, None)) for flag in flag_names}
    else:
        # In single-tenant mode, batch fetch from Constance to avoid N+1 queries
        constance_values = utils.batch_get_constance_values(flag_names)
        feature_flags = {
            flag: (constance_values.get(flag) if flag in constance_values else getattr(conf.settings, flag, None))
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


def _get_system_credentials_status(test_mode: bool = None) -> dict:
    """Compute which carriers have system credentials configured.

    Args:
        test_mode: If provided, adds a 'configured' field indicating whether
            credentials are available for the current mode (sandbox if test_mode
            is True, production if False).

    Returns dict like:
    {
        "dhl_parcel_de": {"production": True, "sandbox": False, "configured": True},
        "teleship": {"production": True, "sandbox": True, "configured": True},
    }
    """
    result = {}

    # Collect all config keys needed across all carriers to batch-fetch
    all_config_keys = set()
    carrier_vars = {}  # carrier_id -> (prod_vars, sandbox_vars)

    for carrier_id, metadata_obj in ref.PLUGIN_METADATA.items():
        system_config = metadata_obj.get("system_config")
        if not system_config:
            continue

        prod_vars = [k for k in system_config if "SANDBOX" not in k]
        sandbox_vars = [k for k in system_config if "SANDBOX" in k]
        carrier_vars[carrier_id] = (prod_vars, sandbox_vars)
        all_config_keys.update(prod_vars)
        all_config_keys.update(sandbox_vars)

    if not all_config_keys:
        return result

    # Batch fetch all config values in a single query
    config_values = utils.batch_get_constance_values(list(all_config_keys))

    for carrier_id, (prod_vars, sandbox_vars) in carrier_vars.items():
        prod_configured = bool(prod_vars) and all(bool(config_values.get(var)) for var in prod_vars)
        sandbox_configured = bool(sandbox_vars) and all(bool(config_values.get(var)) for var in sandbox_vars)

        if prod_configured or sandbox_configured:
            entry = {
                "production": prod_configured,
                "sandbox": sandbox_configured,
            }

            # Add mode-aware 'configured' field
            if test_mode is not None:
                entry["configured"] = sandbox_configured if test_mode else prod_configured

            # Extract field names from system config keys
            # e.g., DHL_PARCEL_DE_CLIENT_ID -> client_id
            prefix = carrier_id.upper() + "_"
            sandbox_prefix = carrier_id.upper() + "_SANDBOX_"
            system_fields = set()
            for var in prod_vars + sandbox_vars:
                name = var.upper()
                if name.startswith(sandbox_prefix):
                    name = name[len(sandbox_prefix) :]
                elif name.startswith(prefix):
                    name = name[len(prefix) :]
                system_fields.add(name.lower())
            entry["fields"] = list(system_fields)

            result[carrier_id] = entry

    return result


def _get_platform_references() -> dict:
    """Get JTL platform-specific references (template variables, etc.).

    Reads from constance config. Returns empty defaults when constance
    keys are not configured (e.g. non-JTL deployments).
    """
    import json

    result = {}

    try:
        from constance import config as constance_config

        raw = getattr(constance_config, "WAWI_TEMPLATE_VARIABLES", "{}")
        result["wawi_template_variables"] = json.loads(raw) if isinstance(raw, str) else raw
    except (ImportError, Exception):
        result["wawi_template_variables"] = {}

    return result


def contextual_reference(request: Request = None, reduced: bool = True, include_disabled: bool = False):
    import karrio.server.core.gateway as gateway
    import karrio.server.core.middleware as middleware
    import karrio.server.core.validators as validators
    import karrio.server.providers.models as providers

    request = request or middleware.SessionContext.get_current_request()
    is_authenticated = lib.identity(request.user.is_authenticated if hasattr(request, "user") else False)

    # Compute system credentials availability (mode-aware)
    _test_mode = getattr(request, "test_mode", None)
    system_credentials_carriers = lib.failsafe(
        lambda: _get_system_credentials_status(test_mode=_test_mode),
        {},
    )

    references = {
        **contextual_metadata(request),
        "ADDRESS_AUTO_COMPLETE": lib.failsafe(
            lambda: validators.Address.get_info(is_authenticated),
            None,
        ),
        "system_credentials_carriers": system_credentials_carriers,
        **{k: v for k, v in REFERENCE_MODELS.items() if k not in (REFERENCE_EXCLUSIONS if reduced else [])},
        **_get_platform_references(),
    }

    # Prune to the live enabled set for tenants (one batched read); admin keeps the full catalog.
    if not include_disabled:
        enabled_carriers, enabled_lsp = get_enabled_plugin_ids()
        references = ref.filter_references_to_enabled(references, enabled_carriers, enabled_lsp)
        references["system_credentials_carriers"] = {
            carrier_id: status
            for carrier_id, status in (references.get("system_credentials_carriers") or {}).items()
            if carrier_id in enabled_carriers
        }

    def _get_generic_carriers():
        # Get all carriers, then filter by extension instead of hardcoded slug
        system_custom_carriers = [c for c in gateway.Carriers.list(system_only=True) if c.ext == "generic"]
        # Filter to only Carrier instances (user-owned connections, not brokered)
        custom_carriers = [
            c
            for c in (gateway.Carriers.list(context=request) if is_authenticated else [])
            if c.ext == "generic" and isinstance(c, providers.CarrierConnection)
        ]

        extra_carriers = {c.carrier_code: c.display_name for c in custom_carriers}
        system_carriers = {c.carrier_code: c.display_name for c in system_custom_carriers}
        extra_services = {
            c.carrier_code: {
                s.service_code: s.service_code
                for s in c.services
                or [
                    lib.to_object(lib.models.ServiceLevel, _)
                    for _ in (references.get("ratesheets", {}).get(c.ext, {}).get("services", []))
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

    # Tell clients which carriers expose dynamic metadata so the shipping app
    # only attempts `?connection_id=` for those — non-dynamic carriers serve
    # the same static catalog regardless. See PRDs/CARRIER_DYNAMIC_METADATA.md.
    import karrio.server.core.dynamic as core_dynamic

    references["carriers_with_dynamic_metadata"] = sorted(core_dynamic.carriers_with_dynamic_metadata())

    return references


def get_carrier_details(
    carrier_name: str,
    contextual_reference: dict = None,
) -> dict:
    details = ref.get_carrier_details(
        carrier_name,
        contextual_reference=contextual_reference or contextual_reference(),
    )
    # Per-carrier flag mirrors the references-level list so callers fetching a
    # single carrier don't need a separate references round-trip to decide
    # whether passing ?connection_id= is worthwhile.
    dynamic_carriers = (contextual_reference or {}).get("carriers_with_dynamic_metadata") or []
    details["has_dynamic_metadata"] = carrier_name in dynamic_carriers
    return details
