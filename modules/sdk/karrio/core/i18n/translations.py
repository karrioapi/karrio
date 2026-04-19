"""
Carrier string translation infrastructure.

Provides locale-aware translations for carrier-specific strings
(service names, option names, connection field/config labels, carrier display
names, capabilities, and integration status).
Translations are applied at response time using Django's active language.
"""

import functools
import importlib
import logging

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def _get_translation_catalogs() -> dict:
    """
    Collect translation catalogs from all registered carrier plugins.
    Returns a dict keyed by carrier_id with sub-dicts for each category.
    Uses lru_cache for thread-safe memoization.
    """
    catalogs: dict = {}

    try:
        from karrio.references import collect_providers_data

        providers = collect_providers_data()

        for carrier_id, _metadata_obj in providers.items():
            i18n_module = _load_carrier_i18n(carrier_id)
            if i18n_module is None:
                continue

            catalogs[carrier_id] = {
                "service_names": getattr(i18n_module, "SERVICE_NAME_TRANSLATIONS", {}),
                "option_names": getattr(i18n_module, "OPTION_NAME_TRANSLATIONS", {}),
            }
    except (ImportError, ModuleNotFoundError, AttributeError):
        logger.warning("Could not load carrier translation catalogs", exc_info=True)

    return catalogs


def _load_carrier_i18n(carrier_id: str):
    """Attempt to import a carrier's i18n module."""
    try:
        return importlib.import_module(f"karrio.providers.{carrier_id}.i18n")
    except (ImportError, ModuleNotFoundError):
        return None


def _get_catalogs() -> dict:
    return _get_translation_catalogs()


CONNECTION_FIELD_LABELS: dict = {
    "username": "Username",
    "password": "Password",
    "api_key": "API Key",
    "api_secret": "API Secret",
    "account_number": "Account Number",
    "site_id": "Site ID",
    "secret_key": "Secret Key",
    "client_id": "Client ID",
    "client_secret": "Client Secret",
    "customer_number": "Customer Number",
    "contract_id": "Contract ID",
    "access_license_number": "Access License Number",
    "meter_number": "Meter Number",
    "account_pin": "Account PIN",
    "account_entity": "Account Entity",
    "account_country_code": "Account Country Code",
    "test_mode": "Test Mode",
    "carrier_id": "Carrier ID",
    "tracking_url": "Tracking URL",
    "server_url": "Server URL",
}

CONFIG_FIELD_LABELS: dict = {
    "label_type": "Label Type",
    "label_template": "Label Template",
    "brand_color": "Brand Color",
    "text_color": "Text Color",
    "cost_center": "Cost Center",
    "shipping_options": "Shipping Options",
    "shipping_services": "Shipping Services",
    "enforce_zpl": "Enforce ZPL",
    "skip_service_filter": "Skip Service Filter",
    "service_suffix": "Service Suffix",
    "billing_numbers": "Billing Numbers",
}

CAPABILITY_LABELS: dict = {
    "shipping": "Shipping",
    "tracking": "Tracking",
    "rating": "Rating",
    "pickup": "Pickup",
    "paperless": "Paperless",
    "manifest": "Manifest",
    "duties": "Duties",
    "insurance": "Insurance",
    "webhook": "Webhook",
    "oauth": "OAuth",
}

INTEGRATION_STATUS_LABELS: dict = {
    "production-ready": "Production Ready",
    "beta": "Beta",
    "alpha": "Alpha",
    "development": "Development",
}


def format_label(name: str) -> str:
    """
    Convert a snake_case field name to a human-readable label.
    e.g. 'site_id' -> 'Site Id', 'api_key' -> 'Api Key'
    """
    return name.replace("_", " ").title()


def _gettext(text: str) -> str:
    """Translate a string using Django's active language, with fallback."""
    try:
        from django.utils.translation import gettext  # type: ignore[import-not-found]

        return gettext(text)
    except Exception:
        return text


def _translate_service_names(service_names: dict, catalogs: dict) -> dict:
    """Apply carrier-specific translations to service names with fallback."""
    result: dict = {}
    for carrier_id, services in service_names.items():
        carrier_catalog = catalogs.get(carrier_id, {}).get("service_names", {})
        result[carrier_id] = {}
        for key, _display_name in services.items():
            catalog_label = carrier_catalog.get(key)
            if catalog_label is not None:
                result[carrier_id][key] = _gettext(str(catalog_label))
            else:
                stripped = _strip_carrier_prefix(key, carrier_id)
                result[carrier_id][key] = _gettext(format_label(stripped))
    return result


def _translate_option_names(option_names: dict, catalogs: dict) -> dict:
    """Apply carrier-specific translations to option names with fallback."""
    result: dict = {}
    for carrier_id, options in option_names.items():
        carrier_catalog = catalogs.get(carrier_id, {}).get("option_names", {})
        result[carrier_id] = {}
        for key, _display_name in options.items():
            catalog_label = carrier_catalog.get(key)
            if catalog_label is not None:
                result[carrier_id][key] = _gettext(str(catalog_label))
            else:
                stripped = _strip_carrier_prefix(key, carrier_id)
                result[carrier_id][key] = _gettext(format_label(stripped))
    return result


def _translate_field_entries(fields: dict, label_map: dict) -> dict:
    """Add translated label field to field/config entries."""
    result: dict = {}
    for carrier_id, entries in fields.items():
        result[carrier_id] = {}
        for field_name, field_data in entries.items():
            translated = dict(field_data)
            english_label = label_map.get(field_name, format_label(field_name))
            translated["label"] = _gettext(english_label)
            result[carrier_id][field_name] = translated
    return result


def _strip_carrier_prefix(name: str, carrier_id: str) -> str:
    """Strip carrier_id prefix from an option/field name."""
    prefix = f"{carrier_id}_"
    if name.lower().startswith(prefix.lower()):
        return name[len(prefix) :]
    return name


def _translate_options(options: dict, option_names: dict, catalogs: dict) -> dict:
    """Add translated label field to shipping option entries."""
    result: dict = {}
    for carrier_id, entries in options.items():
        carrier_catalog = catalogs.get(carrier_id, {}).get("option_names", {})
        result[carrier_id] = {}
        for option_code, option_data in entries.items():
            translated = dict(option_data)
            catalog_label = carrier_catalog.get(option_code)
            if catalog_label is not None:
                translated["label"] = _gettext(str(catalog_label))
            else:
                stripped = _strip_carrier_prefix(option_code, carrier_id)
                translated["label"] = _gettext(format_label(stripped))
            result[carrier_id][option_code] = translated
    return result


def _translate_carrier_names(carriers: dict) -> dict:
    """Apply translations to carrier display names with fallback."""
    return {carrier_id: _gettext(display_name) for carrier_id, display_name in carriers.items()}


def _translate_capabilities(capabilities: dict) -> dict:
    """Translate carrier capability names."""
    result: dict = {}
    for carrier_id, caps in capabilities.items():
        result[carrier_id] = [_gettext(CAPABILITY_LABELS.get(cap, format_label(cap))) for cap in caps]
    return result


def _translate_enum_values(enum_dict: dict) -> dict:
    """Translate enum display values (countries, incoterms, customs types, etc.)."""
    return {key: _gettext(value) if isinstance(value, str) else value for key, value in enum_dict.items()}


def _translate_integration_status(statuses: dict) -> dict:
    """Translate integration status values."""
    return {
        carrier_id: _gettext(INTEGRATION_STATUS_LABELS.get(status, format_label(status)))
        for carrier_id, status in statuses.items()
    }


def translate_references(references: dict) -> dict:
    """
    Apply locale-aware translations to reference data at response time.

    Translates service_names, option_names, connection_fields (adds label),
    connection_configs (adds label), carrier display names, capabilities,
    and integration status. Falls back to the original value for any
    string without a translation.
    """
    catalogs = _get_catalogs()

    translated = dict(references)

    if "service_names" in translated:
        translated["service_names"] = _translate_service_names(translated["service_names"], catalogs)

    if "option_names" in translated:
        translated["option_names"] = _translate_option_names(translated["option_names"], catalogs)

    if "connection_fields" in translated:
        translated["connection_fields"] = _translate_field_entries(
            translated["connection_fields"], CONNECTION_FIELD_LABELS
        )

    if "connection_configs" in translated:
        translated["connection_configs"] = _translate_field_entries(
            translated["connection_configs"], CONFIG_FIELD_LABELS
        )

    if "options" in translated:
        translated["options"] = _translate_options(
            translated["options"],
            translated.get("option_names", {}),
            catalogs,
        )

    if "carriers" in translated:
        translated["carriers"] = _translate_carrier_names(translated["carriers"])

    if "carrier_capabilities" in translated:
        translated["carrier_capabilities"] = _translate_capabilities(translated["carrier_capabilities"])

    if "integration_status" in translated:
        translated["integration_status"] = _translate_integration_status(translated["integration_status"])

    for key in ("countries", "customs_content_type", "incoterms", "payment_types"):
        if key in translated:
            translated[key] = _translate_enum_values(translated[key])

    return translated
