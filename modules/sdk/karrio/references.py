"""Karrio Interface references.

This module provides references to carrier integrations, address validators,
and other plugin-related functionality in the Karrio system.
"""

import os
import attr
import pydoc
import typing
import logging
import pkgutil
import functools

import karrio.lib as lib
import karrio.core.units as units
import karrio.core.plugins as plugins
import karrio.core.metadata as metadata

# Configure logger with a higher default level to reduce noise
ENABLE_ALL_PLUGINS_BY_DEFAULT = bool(
    os.environ.get("ENABLE_ALL_PLUGINS_BY_DEFAULT", True)
)
logger = logging.getLogger(__name__)
if not logger.level:
    logger.setLevel(logging.INFO)

# Global references - DO NOT RENAME (used for backward compatibility)
PROVIDERS: typing.Dict[str, metadata.PluginMetadata] = {}
ADDRESS_VALIDATORS: typing.Dict[str, metadata.PluginMetadata] = {}
MAPPERS: typing.Dict[str, typing.Any] = {}
SCHEMAS: typing.Dict[str, typing.Any] = {}
FAILED_IMPORTS: typing.Dict[str, typing.Any] = {}
PLUGIN_METADATA: typing.Dict[str, metadata.PluginMetadata] = {}
REFERENCES: typing.Dict[str, typing.Any] = {}


def import_extensions() -> None:
    """
    Import extensions from main modules and plugins.

    This method collects carriers, address validators and mappers from
    built-in modules and plugins through multiple discovery methods:

    1. Directory-based plugins
    2. Entrypoint-based plugins (setuptools entry_points)
    3. Built-in modules
    """
    global PROVIDERS, ADDRESS_VALIDATORS, MAPPERS, SCHEMAS, FAILED_IMPORTS, PLUGIN_METADATA, REFERENCES
    # Reset collections
    PROVIDERS = {}
    ADDRESS_VALIDATORS = {}
    MAPPERS = {}
    SCHEMAS = {}
    FAILED_IMPORTS = {}
    PLUGIN_METADATA = {}
    REFERENCES = {}

    # Load plugins (if not already loaded)
    plugins.load_local_plugins()

    # Discover and import modules from directory-based plugins
    plugin_modules = plugins.discover_plugin_modules()
    metadata_dict, failed_metadata = plugins.collect_plugin_metadata(plugin_modules)
    PLUGIN_METADATA.update(metadata_dict)

    # Discover and import modules from entrypoint-based plugins
    entrypoint_plugins = plugins.discover_entrypoint_plugins()
    entrypoint_metadata, entrypoint_failed = plugins.collect_plugin_metadata(entrypoint_plugins)
    PLUGIN_METADATA.update(entrypoint_metadata)

    # Update failed imports
    FAILED_IMPORTS.update(plugins.get_failed_plugin_modules())
    for key, value in failed_metadata.items():
        FAILED_IMPORTS[f"metadata.{key}"] = value
    for key, value in entrypoint_failed.items():
        FAILED_IMPORTS[f"entrypoint.metadata.{key}"] = value

    # Process collected metadata to find carriers, validators, and mappers
    for plugin_name, metadata_obj in PLUGIN_METADATA.items():
        if not isinstance(metadata_obj, metadata.PluginMetadata):
            logger.error(f"Invalid metadata type in {plugin_name}, expected PluginMetadata")
            continue

        # Process the plugin based on its capabilities
        # Capabilities are now automatically determined from registered components
        if metadata_obj.is_carrier_integration():
            _register_carrier(metadata_obj, plugin_name)

        if metadata_obj.is_address_validator():
            _register_validator(metadata_obj)

    # Import packages from karrio.plugins (new plugin architecture)
    try:
        import karrio.plugins
        # Use pkgutil to find all modules within karrio.plugins
        for _, name, ispkg in pkgutil.iter_modules(karrio.plugins.__path__):
            if name.startswith('_'):
                continue
            try:
                module = __import__(f"karrio.plugins.{name}", fromlist=[name])
                metadata_obj = getattr(module, 'METADATA', None)
                if metadata_obj and isinstance(metadata_obj, metadata.PluginMetadata):
                    # Add to PLUGIN_METADATA so it's accessible via plugin management interfaces
                    PLUGIN_METADATA[name] = metadata_obj
                    if metadata_obj.is_carrier_integration():
                        _register_carrier(metadata_obj, name)
                    if metadata_obj.is_address_validator():
                        _register_validator(metadata_obj)
            except (AttributeError, ImportError) as e:
                logger.error(f"Failed to import plugin {name}: {str(e)}")
    except ImportError:
        logger.error("Could not import karrio.plugins")

    # Import carriers from built-in karrio mappers (legacy approach for backward compatibility)
    try:
        import karrio.mappers
        # Use pkgutil to find all modules within karrio.mappers
        for _, name, ispkg in pkgutil.iter_modules(karrio.mappers.__path__):
            if name.startswith('_'):
                continue
            try:
                module = __import__(f"karrio.mappers.{name}", fromlist=[name])
                metadata_obj = getattr(module, 'METADATA', None)
                if metadata_obj and isinstance(metadata_obj, metadata.PluginMetadata):
                    # Add to PLUGIN_METADATA so it's accessible via plugin management interfaces
                    PLUGIN_METADATA[name] = metadata_obj
                    _register_carrier(metadata_obj, name)
            except (AttributeError, ImportError) as e:
                logger.error(f"Failed to import mapper {name}: {str(e)}")
    except ImportError:
        logger.error("Could not import karrio.mappers")

    # Import address validators from built-in modules
    try:
        import karrio.validators
        _import_validators_from_module(karrio.validators)
    except ImportError:
        logger.error("Could not import karrio.validators")

    # Import carriers from built-in modules
    try:
        import karrio.providers
        for provider_name in dir(karrio.providers):
            if provider_name.startswith('_'):
                continue
            try:
                provider = getattr(karrio.providers, provider_name)
                metadata_obj = getattr(provider, 'METADATA', None)
                if metadata_obj and isinstance(metadata_obj, metadata.PluginMetadata):
                    # Add to PLUGIN_METADATA so it's accessible via plugin management interfaces
                    PLUGIN_METADATA[provider_name] = metadata_obj
                    _register_carrier(metadata_obj, provider_name)
            except (AttributeError, ImportError) as e:
                logger.error(f"Failed to import provider {provider_name}: {str(e)}")
                continue
    except ImportError:
        logger.error("Could not import karrio.providers")

    # Sort PLUGIN_METADATA and PROVIDERS alphabetically by their keys
    PLUGIN_METADATA = dict(sorted(PLUGIN_METADATA.items()))
    PROVIDERS = dict(sorted(PROVIDERS.items()))

    logger.info(f"> Loaded {len(PLUGIN_METADATA)} plugins")


def _import_validators_from_module(module):
    """
    Import validators from a module by looking for METADATA in submodules.
    """
    for validator_name in dir(module):
        if validator_name.startswith('_'):
            continue
        try:
            validator_module = getattr(module, validator_name)
            metadata_obj = getattr(validator_module, 'METADATA', None)
            if metadata_obj and isinstance(metadata_obj, metadata.PluginMetadata):
                # Add to PLUGIN_METADATA so it's accessible via plugin management interfaces
                PLUGIN_METADATA[validator_name] = metadata_obj
                _register_validator(metadata_obj)
        except (AttributeError, ImportError) as e:
            logger.error(f"Failed to import validator {validator_name}: {str(e)}")
            continue


def _register_carrier(metadata_obj: metadata.PluginMetadata, carrier_name: str) -> None:
    """
    Register a carrier from its metadata.

    This adds the carrier to providers and imports any mappers/schemas.

    Args:
        metadata_obj: The carrier plugin metadata
        carrier_name: The name of the carrier
    """
    carrier_id = metadata_obj.get("id")

    if not carrier_id:
        logger.error(f"Carrier metadata missing ID")
        return

    if not hasattr(metadata_obj, 'Mapper') or not metadata_obj.Mapper:
        logger.error(f"Carrier {carrier_id} has no Mapper defined")
        return

    # Register carrier
    PROVIDERS[carrier_id] = metadata_obj

    # Register mapper
    MAPPERS[carrier_id] = metadata_obj.Mapper

    # Register schemas if available
    if hasattr(metadata_obj, 'Settings'):
        SCHEMAS[carrier_id] = metadata_obj.Settings


def _register_validator(metadata_obj: metadata.PluginMetadata) -> None:
    """
    Register an address validator from its metadata.

    Args:
        metadata_obj: The validator plugin metadata
    """
    validator_id = metadata_obj.get("id")

    if not validator_id:
        logger.error(f"Validator metadata missing ID")
        return

    if not hasattr(metadata_obj, 'Validator') or not metadata_obj.Validator:
        logger.error(f"Address validator {validator_id} has no Validator defined")
        return

    # Register address validator
    ADDRESS_VALIDATORS[validator_id] = metadata_obj


@functools.lru_cache(maxsize=1)
def get_providers() -> typing.Dict[str, metadata.PluginMetadata]:
    """
    Get all available provider metadata.

    Returns:
        Dictionary of carrier ID to carrier metadata
    """
    return PROVIDERS


@functools.lru_cache(maxsize=1)
def get_address_validators() -> typing.Dict[str, metadata.PluginMetadata]:
    """
    Get all available address validator metadata.

    Returns:
        Dictionary of validator ID to validator metadata
    """
    return ADDRESS_VALIDATORS


@functools.lru_cache(maxsize=1)
def get_mappers() -> typing.Dict[str, typing.Any]:
    """
    Get all available carrier mappers.

    Returns:
        Dictionary of carrier ID to mapper class
    """
    return MAPPERS


@functools.lru_cache(maxsize=1)
def get_schemas() -> typing.Dict[str, typing.Any]:
    """
    Get all available carrier settings schemas.

    Returns:
        Dictionary of carrier ID to settings schema
    """
    return SCHEMAS


@functools.lru_cache(maxsize=1)
def get_failed_imports() -> typing.Dict[str, typing.Any]:
    """
    Get information about import failures.

    Returns:
        Dictionary containing error information for failed imports
    """
    return FAILED_IMPORTS


def get_plugin_metadata() -> typing.Dict[str, metadata.PluginMetadata]:
    """
    Get metadata for all discovered plugins.

    Returns:
        Dictionary of plugin name to plugin metadata
    """
    return PLUGIN_METADATA


def collect_plugins_data() -> typing.Dict[str, dict]:
    """
    Collect metadata for all plugins.

    Returns:
        Dict mapping plugin names to their metadata as dictionaries
    """
    if not PLUGIN_METADATA:
        import_extensions()

    return {
        plugin_name: attr.asdict(plugin_metadata)
        for plugin_name, plugin_metadata in PLUGIN_METADATA.items()
    }


def collect_failed_plugins_data() -> typing.Dict[str, dict]:
    """
    Collect information about plugins that failed to load.

    Returns:
        Dict mapping plugin names to error information
    """
    if not PLUGIN_METADATA:
        import_extensions()

    return FAILED_IMPORTS


def collect_providers_data() -> typing.Dict[str, metadata.PluginMetadata]:
    """
    Collect metadata for carrier integration plugins.

    Returns:
        Dict mapping carrier names to their metadata as dictionaries
    """
    if not PROVIDERS:
        import_extensions()

    return {
        carrier_name: metadata_obj
        for carrier_name, metadata_obj in PROVIDERS.items()
    }


def collect_address_validators_data() -> typing.Dict[str, dict]:
    """
    Collect address validator metadata from loaded validators.

    Returns:
        Dict mapping validator names to their metadata
    """
    if not ADDRESS_VALIDATORS:
        import_extensions()

    return {
        validator_name: attr.asdict(metadata_obj)
        for validator_name, metadata_obj in ADDRESS_VALIDATORS.items()
    }


def detect_capabilities(proxy_methods: typing.List[str]) -> typing.List[str]:
    """
    Map proxy methods to carrier capabilities.

    Args:
        proxy_methods: List of method names from a Proxy class

    Returns:
        List of capability identifiers
    """
    return list(set([units.CarrierCapabilities.map_capability(prop) for prop in proxy_methods]))


def detect_proxy_methods(proxy_type: object) -> typing.List[str]:
    """
    Extract all public methods from a proxy type.

    Args:
        proxy_type: A Proxy class

    Returns:
        List of method names
    """
    return [
        prop
        for prop in proxy_type.__dict__.keys()
        if "_" not in prop[0] and prop != "settings"
    ]

# Fields to exclude when collecting connection fields
COMMON_FIELDS = ["id", "carrier_id", "test_mode", "carrier_name"]


def collect_references(
    plugin_registry: dict = None,
) -> dict:
    """
    Collect all references from carriers, validators, and plugins.

    This function builds a comprehensive dictionary of all available
    references in the system, including services, options, countries,
    currencies, carriers, etc.

    Returns:
        Dictionary containing all reference data
    """
    global REFERENCES, PROVIDERS
    if not PROVIDERS:
        import_extensions()

    # If references have already been computed, return them
    if REFERENCES and not plugin_registry:
        return REFERENCES

    registry = Registry(plugin_registry)

    # Determine enabled carriers
    enabled_carrier_ids = set(
        carrier_id for carrier_id in PROVIDERS.keys()
        if registry.get(f"{carrier_id.upper()}_ENABLED", registry.get("ENABLE_ALL_PLUGINS_BY_DEFAULT"))
    )

    services = {
        key: {c.name: c.value for c in list(mapper.get("services", []))}
        for key, mapper in PROVIDERS.items()
        if key in enabled_carrier_ids and mapper.get("services") is not None
    }
    options = {
        key: {c.name: dict(code=c.value.code, type=parse_type(c.value.type), default=c.value.default) for c in list(mapper.get("options", []))}
        for key, mapper in PROVIDERS.items()
        if key in enabled_carrier_ids and mapper.get("options") is not None
    }
    connection_configs = {
        key: {
            c.name: lib.to_dict(
                dict(
                    name=c.name,
                    code=c.value.code,
                    required=False,
                    type=parse_type(c.value.type),
                    default=c.value.default,
                    enum=lib.identity(
                        None
                        if "enum" not in str(c.value.type).lower()
                        else [c.name for c in c.value.type]
                    ),
                )
            )
            for c in list(mapper.get("connection_configs", []))
        }
        for key, mapper in PROVIDERS.items()
        if key in enabled_carrier_ids and mapper.get("connection_configs") is not None
    }

    # Build connection_fields with proper attrs class checking
    connection_fields = {
        key: {
            _.name: lib.to_dict(
                dict(
                    name=_.name,
                    type=parse_type(_.type),
                    required="NOTHING" in str(_.default),
                    default=lib.identity(
                        lib.to_dict(lib.to_json(_.default))
                        if ("NOTHING" not in str(_.default))
                        else None
                    ),
                    enum=lib.identity(
                        None
                        if "enum" not in str(_.type).lower()
                        else [c.name for c in _.type]
                    ),
                )
            )
            for _ in getattr(mapper.get("Settings"), "__attrs_attrs__", [])
            if (_.name not in COMMON_FIELDS)
            or (mapper.get("has_intl_accounts") and _.name == "account_country_code")
        } if mapper.get("Settings") is not None and hasattr(mapper.get("Settings"), "__attrs_attrs__") else {}
        for key, mapper in PROVIDERS.items()
        if key in enabled_carrier_ids
    }

    REFERENCES = {
        "countries": {c.name: c.value for c in list(units.Country)},  # type: ignore
        "currencies": {c.name: c.value for c in list(units.Currency)},  # type: ignore
        "weight_units": {c.name: c.value for c in list(units.WeightUnit)},  # type: ignore
        "dimension_units": {c.name: c.value for c in list(units.DimensionUnit)},  # type: ignore
        "states": {
            c.name: {s.name: s.value for s in list(c.value)}  # type: ignore
            for c in list(units.CountryState)  # type: ignore
        },
        "payment_types": {c.name: c.value for c in list(units.PaymentType)},  # type: ignore
        "customs_content_type": {
            c.name: c.value for c in list(units.CustomsContentType)  # type: ignore
        },
        "incoterms": {c.name: c.value for c in list(units.Incoterm)},  # type: ignore
        "carriers": {
            carrier_id: metadata_obj.label for carrier_id, metadata_obj in PROVIDERS.items() if carrier_id in enabled_carrier_ids
        },
        "carrier_hubs": {
            carrier_id: metadata_obj.label
            for carrier_id, metadata_obj in PROVIDERS.items()
            if carrier_id in enabled_carrier_ids and metadata_obj.is_hub
        },
        "address_validators": {
            validator_id: metadata_obj.get("label", "")
            for validator_id, metadata_obj in collect_address_validators_data().items()
        },
        "services": services,
        "options": options,
        "connection_fields": connection_fields,
        "connection_configs": connection_configs,
        "carrier_capabilities": {
            key: detect_capabilities(detect_proxy_methods(mapper.get("Proxy")))
            for key, mapper in PROVIDERS.items()
            if key in enabled_carrier_ids and mapper.get("Proxy") is not None
        },
        "packaging_types": {
            key: {c.name: c.value for c in list(mapper.get("packaging_types", []))}
            for key, mapper in PROVIDERS.items()
            if key in enabled_carrier_ids and mapper.get("packaging_types") is not None
        },
        "package_presets": {
            key: {c.name: lib.to_dict(c.value) for c in list(mapper.get("package_presets", []))}
            for key, mapper in PROVIDERS.items()
            if key in enabled_carrier_ids and mapper.get("package_presets") is not None
        },
        "option_names": {
            name: {key: key.upper().replace("_", " ") for key, _ in value.items()}
            for name, value in options.items()
        },
        "service_names": {
            name: {key: key.upper().replace("_", " ") for key, _ in value.items()}
            for name, value in services.items()
        },
        "service_levels": {
            key: lib.to_dict(mapper.get("service_levels"))
            for key, mapper in PROVIDERS.items()
            if key in enabled_carrier_ids and mapper.get("service_levels") is not None
        },
        "integration_status": {
            carrier_id: metadata_obj.status for carrier_id, metadata_obj in PROVIDERS.items() if carrier_id in enabled_carrier_ids
        },
        "address_validator_details": {
            validator_id: {
                "id": validator_id,
                "provider": validator_id,
                "display_name": metadata_obj.get("label", ""),
                "integration_status": metadata_obj.get("status", ""),
                "website": metadata_obj.get("website", ""),
                "description": metadata_obj.get("description", ""),
                "documentation": metadata_obj.get("documentation", ""),
                "readme": metadata_obj.get("readme", ""),
            }
            for validator_id, metadata_obj in collect_address_validators_data().items()
        },
        "plugins": {
            name: {
                "id": metadata_obj.get("id", ""),
                "name": name,
                "display_name": metadata_obj.get("label", ""),
                "integration_status": metadata_obj.get("status", ""),
                "website": metadata_obj.get("website", ""),
                "description": metadata_obj.get("description", ""),
                "documentation": metadata_obj.get("documentation", ""),
                "readme": metadata_obj.get("readme", ""),
                "type": metadata_obj.plugin_type,
                "types": metadata_obj.plugin_types,
                "is_dual_purpose": metadata_obj.is_dual_purpose()
            }
            for name, metadata_obj in PLUGIN_METADATA.items()
        },
        "failed_plugins": collect_failed_plugins_data(),
    }

    logger.info(f"> Karrio references loaded. {len(PLUGIN_METADATA.keys())} plugins")
    return REFERENCES


def get_carrier_capabilities(carrier_name) -> typing.List[str]:
    """
    Get the capabilities of a specific carrier.

    Args:
        carrier_name: The name of the carrier

    Returns:
        List of capability identifiers
    """
    proxy_class = pydoc.locate(f"karrio.mappers.{carrier_name}.Proxy")
    proxy_methods = detect_proxy_methods(proxy_class)
    return detect_capabilities(proxy_methods)


def parse_type(_type: type) -> str:
    """
    Parse a Python type into a string representation.

    Args:
        _type: Python type object

    Returns:
        String representation of the type
    """
    _name = getattr(_type, "__name__", None)

    if _name is not None and _name == "bool":
        return "boolean"
    if _name is not None and _name == "str":
        return "string"
    if _name is not None and (_name == "int" or "to_int" in _name):
        return "integer"
    if _name is not None and _name == "float":
        return "float"
    if _name is not None and "money" in _name:
        return "float"
    if "Address" in str(_type):
        return "Address"
    if "enum" in str(_type):
        return "string"
    if _name is not None and ("list" in _name or "List" in _name):
        return "list"
    if _name is not None and ("dict" in _name or "Dict" in _name):
        return "object"

    return str(_type)


def get_carrier_details(
    plugin_code: str,
    contextual_reference: dict = None,
    plugin_registry: dict = None,
) -> dict:
    """
    Get detailed information about a carrier.

    Args:
        carrier_id: The ID of the carrier
        contextual_reference: Optional pre-computed references dictionary
        plugin_registry: Optional plugin registry dictionary
    Returns:
        Dictionary with detailed carrier information
    """
    metadata_obj: metadata.PluginMetadata = collect_providers_data().get(plugin_code)
    references = contextual_reference or collect_references()
    registry = Registry(plugin_registry)

    return dict(
        id=plugin_code,
        carrier_name=plugin_code,
        display_name=getattr(metadata_obj, "label", ""),
        integration_status=getattr(metadata_obj, "status", ""),
        website=getattr(metadata_obj, "website", ""),
        description=getattr(metadata_obj, "description", ""),
        documentation=getattr(metadata_obj, "documentation", ""),
        is_enabled=registry.get(f"{plugin_code.upper()}_ENABLED", registry.get("ENABLE_ALL_PLUGINS_BY_DEFAULT")),
        capabilities=references["carrier_capabilities"].get(plugin_code, {}),
        connection_fields=references["connection_fields"].get(plugin_code, {}),
        config_fields=references["connection_configs"].get(plugin_code, {}),
        shipping_services=references["services"].get(plugin_code, {}),
        shipping_options=references["options"].get(plugin_code, {}),
        readme=metadata_obj.readme,
    )


def get_validator_details(validator_id: str, contextual_reference: dict = None) -> dict:
    """
    Get detailed information about an address validator plugin.

    Args:
        validator_id: The ID of the validator plugin
        contextual_reference: Optional pre-computed references dictionary

    Returns:
        Dictionary with detailed validator information
    """
    references = contextual_reference or collect_references()
    return references["address_validator_details"].get(validator_id, {})


def get_plugin_details(plugin_name: str, contextual_reference: dict = None) -> dict:
    """
    Get detailed information about any plugin by name.

    Args:
        plugin_name: The name of the plugin
        contextual_reference: Optional pre-computed references dictionary

    Returns:
        Dictionary with detailed plugin information
    """
    references = contextual_reference or collect_references()
    return references["plugins"].get(plugin_name, {})


class Registry(dict):
    def __init__(self, registry: typing.Any = None):
        self.registry = registry
        self._config_loaded = False

    def _ensure_config_loaded(self):
        if not self._config_loaded and self.registry is None:
            try:
                from constance import config
                # Don't access config.ENABLE_ALL_PLUGINS_BY_DEFAULT here
                # Just store the config object
                self.registry = config
                self._config_loaded = True
            except Exception:
                self.registry = {}
                self._config_loaded = True

    def get(self, key, default=None):
        self._ensure_config_loaded()
        try:
            if isinstance(self.registry, dict):
                return self.registry.get(key, os.environ.get(key, default))
            else:
                return getattr(self.registry, key, os.environ.get(key, default))
        except Exception:
            return os.environ.get(key, default)

    def __setitem__(self, key: str, value: typing.Any):
        try:
            if isinstance(self.registry, dict):
                self.registry[key] = value
            else:
                setattr(self.registry, key, value)
        except Exception as e:
            logger.error(f"Failed to set item {key} in registry: {e}")
