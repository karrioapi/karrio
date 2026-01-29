"""Karrio Interface references.

This module provides references to carrier integrations, LSP plugins,
and other plugin-related functionality in the Karrio system.
"""

import os
import attr
import pydoc
import typing
import pkgutil
import functools

import karrio.lib as lib
import karrio.core.units as units
import karrio.core.plugins as plugins
import karrio.core.metadata as metadata
from karrio.core.utils.logger import logger
from karrio.core.utils.transformer import transform_to_shared_zones_format

# Configure logger with a higher default level to reduce noise
ENABLE_ALL_PLUGINS_BY_DEFAULT = bool(
    os.environ.get("ENABLE_ALL_PLUGINS_BY_DEFAULT", True)
)

# Global references
PROVIDERS: typing.Dict[str, metadata.PluginMetadata] = {}  # Shipping carriers only
LSP_PLUGINS: typing.Dict[str, metadata.PluginMetadata] = (
    {}
)  # Logistics Service Providers
MAPPERS: typing.Dict[str, typing.Any] = {}
HOOKS: typing.Dict[str, typing.Any] = {}
SCHEMAS: typing.Dict[str, typing.Any] = {}
FAILED_IMPORTS: typing.Dict[str, typing.Any] = {}
PLUGIN_METADATA: typing.Dict[str, metadata.PluginMetadata] = {}
REFERENCES: typing.Dict[str, typing.Any] = {}
SYSTEM_CONFIGS: typing.Dict[str, typing.Tuple[typing.Any, str, type]] = (
    {}
)  # Plugin system configs


def import_extensions() -> None:
    """
    Import extensions from main modules and plugins.

    This method collects carriers, LSP plugins and mappers from
    built-in modules and plugins through multiple discovery methods with
    priority-based hierarchy (higher priority sources take precedence):

    Priority order (highest to lowest):
    1. Entrypoint-based plugins (setuptools entry_points) - most explicit
    2. karrio.plugins namespace packages - new plugin architecture
    3. karrio.mappers namespace packages - legacy architecture
    4. Directory-based plugins - local development plugins

    Plugins already loaded from a higher-priority source are skipped in
    lower-priority sources to avoid duplication and conflicts.
    """
    global PROVIDERS, LSP_PLUGINS, MAPPERS, HOOKS, SCHEMAS, FAILED_IMPORTS, PLUGIN_METADATA, REFERENCES, SYSTEM_CONFIGS
    # Reset collections
    PROVIDERS = {}
    LSP_PLUGINS = {}
    MAPPERS = {}
    HOOKS = {}
    SCHEMAS = {}
    FAILED_IMPORTS = {}
    PLUGIN_METADATA = {}
    REFERENCES = {}
    SYSTEM_CONFIGS = {}

    # Load local plugins to extend karrio namespaces (but don't process metadata yet)
    plugins.load_local_plugins()

    # =========================================================================
    # STEP 1: Load from entrypoints (highest priority - most explicit)
    # =========================================================================
    entrypoint_plugins = plugins.discover_entrypoint_plugins()
    entrypoint_metadata, entrypoint_failed = plugins.collect_plugin_metadata(
        entrypoint_plugins
    )
    PLUGIN_METADATA.update(entrypoint_metadata)

    # Only record failures for plugins not already loaded
    for key, value in entrypoint_failed.items():
        plugin_name = value.get("plugin", key)
        if plugin_name not in PLUGIN_METADATA:
            FAILED_IMPORTS[f"entrypoint.{key}"] = value

    # =========================================================================
    # STEP 2: Load from karrio.plugins namespace (new plugin architecture)
    # =========================================================================
    try:
        import karrio.plugins as karrio_plugins_module

        for _, name, ispkg in pkgutil.iter_modules(karrio_plugins_module.__path__):
            if name.startswith("_"):
                continue
            # Skip if already loaded from entrypoints
            if name in PLUGIN_METADATA:
                continue
            try:
                module = __import__(f"karrio.plugins.{name}", fromlist=[name])
                metadata_obj = getattr(module, "METADATA", None)
                if metadata_obj and isinstance(metadata_obj, metadata.PluginMetadata):
                    PLUGIN_METADATA[name] = metadata_obj
            except (AttributeError, ImportError) as e:
                # Only log error if not already loaded
                if name not in PLUGIN_METADATA:
                    logger.error(
                        "Failed to import plugin from karrio.plugins",
                        plugin_name=name,
                        error=str(e),
                    )
    except ImportError:
        pass  # karrio.plugins module may not exist

    # =========================================================================
    # STEP 3: Load from karrio.mappers namespace (legacy architecture)
    # =========================================================================
    try:
        import karrio.mappers as karrio_mappers_module

        for _, name, ispkg in pkgutil.iter_modules(karrio_mappers_module.__path__):
            if name.startswith("_"):
                continue
            # Skip if already loaded from higher priority sources
            if name in PLUGIN_METADATA:
                continue
            try:
                module = __import__(f"karrio.mappers.{name}", fromlist=[name])
                metadata_obj = getattr(module, "METADATA", None)
                if metadata_obj and isinstance(metadata_obj, metadata.PluginMetadata):
                    PLUGIN_METADATA[name] = metadata_obj
            except (AttributeError, ImportError) as e:
                # Only log error if not already loaded
                if name not in PLUGIN_METADATA:
                    logger.error(
                        "Failed to import mapper from karrio.mappers",
                        mapper_name=name,
                        error=str(e),
                    )
    except ImportError:
        pass  # karrio.mappers module may not exist

    # =========================================================================
    # STEP 4: Load from directory-based plugins (lowest priority - local dev)
    # =========================================================================
    plugin_modules = plugins.discover_plugin_modules()
    metadata_dict, failed_metadata = plugins.collect_plugin_metadata(plugin_modules)

    # Only add plugins not already loaded from higher priority sources
    for plugin_name, metadata_obj in metadata_dict.items():
        if plugin_name not in PLUGIN_METADATA:
            PLUGIN_METADATA[plugin_name] = metadata_obj

    # Only record failures for plugins not already loaded
    for key, value in failed_metadata.items():
        plugin_name = value.get("plugin", key)
        if plugin_name not in PLUGIN_METADATA:
            FAILED_IMPORTS[f"local.{key}"] = value

    # Update failed imports from plugin module loading
    for key, value in plugins.get_failed_plugin_modules().items():
        plugin_name = value.get("plugin", key)
        if plugin_name not in PLUGIN_METADATA:
            FAILED_IMPORTS[key] = value

    # =========================================================================
    # Process all collected metadata and register carriers/LSPs
    # =========================================================================
    for plugin_name, metadata_obj in PLUGIN_METADATA.items():
        if not isinstance(metadata_obj, metadata.PluginMetadata):
            logger.error(
                "Invalid metadata type, expected PluginMetadata",
                plugin_name=plugin_name,
            )
            continue

        # Process the plugin based on its service_type
        if metadata_obj.is_carrier():
            _register_carrier(metadata_obj, plugin_name)
        elif metadata_obj.is_lsp():
            _register_lsp(metadata_obj, plugin_name)

    # Sort PLUGIN_METADATA, PROVIDERS, and LSP_PLUGINS alphabetically by their keys
    PLUGIN_METADATA = dict(sorted(PLUGIN_METADATA.items()))
    PROVIDERS = dict(sorted(PROVIDERS.items()))
    LSP_PLUGINS = dict(sorted(LSP_PLUGINS.items()))

    # Collect system configs from all plugins
    for _, metadata_obj in PLUGIN_METADATA.items():
        system_config = metadata_obj.get("system_config")
        if system_config and isinstance(system_config, dict):
            SYSTEM_CONFIGS.update(system_config)

    logger.info("Plugins loaded", count=len(PLUGIN_METADATA))


def _register_carrier(metadata_obj: metadata.PluginMetadata, carrier_name: str) -> None:
    """
    Register a shipping carrier from its metadata.

    This adds the carrier to PROVIDERS and imports any mappers/callbacks/schemas.

    Args:
        metadata_obj: The carrier plugin metadata
        carrier_name: The name of the carrier
    """
    carrier_id = metadata_obj.get("id")

    if not carrier_id:
        logger.error("Carrier metadata missing ID", carrier_name=carrier_name)
        return

    if not hasattr(metadata_obj, "Mapper") or not metadata_obj.Mapper:
        logger.error("Carrier has no Mapper defined", carrier_id=carrier_id)
        return

    # Register carrier
    PROVIDERS[carrier_id] = metadata_obj

    # Register mapper
    MAPPERS[carrier_id] = metadata_obj.Mapper

    # Register hooks if available
    if hasattr(metadata_obj, "Hooks") and metadata_obj.Hooks:
        HOOKS[carrier_id] = metadata_obj.Hooks

    # Register schemas if available
    if hasattr(metadata_obj, "Settings") and metadata_obj.Settings:
        SCHEMAS[carrier_id] = metadata_obj.Settings


def _register_lsp(metadata_obj: metadata.PluginMetadata, plugin_name: str) -> None:
    """
    Register a Logistics Service Provider (LSP) plugin from its metadata.

    LSP plugins provide services like address validation, geocoding, duties calculation, etc.

    Args:
        metadata_obj: The LSP plugin metadata
        plugin_name: The name of the plugin
    """
    plugin_id = metadata_obj.get("id")

    if not plugin_id:
        logger.error("LSP plugin metadata missing ID", plugin_name=plugin_name)
        return

    if not hasattr(metadata_obj, "Mapper") or not metadata_obj.Mapper:
        logger.error("LSP plugin has no Mapper defined", plugin_id=plugin_id)
        return

    # Register LSP plugin
    LSP_PLUGINS[plugin_id] = metadata_obj

    # Register mapper
    MAPPERS[plugin_id] = metadata_obj.Mapper

    # Register hooks if available
    if hasattr(metadata_obj, "Hooks") and metadata_obj.Hooks:
        HOOKS[plugin_id] = metadata_obj.Hooks

    # Register schemas if available
    if hasattr(metadata_obj, "Settings") and metadata_obj.Settings:
        SCHEMAS[plugin_id] = metadata_obj.Settings


@functools.lru_cache(maxsize=1)
def get_providers() -> typing.Dict[str, metadata.PluginMetadata]:
    """
    Get all available carrier provider metadata.

    Returns:
        Dictionary of carrier ID to carrier metadata
    """
    return PROVIDERS


@functools.lru_cache(maxsize=1)
def get_lsp_plugins() -> typing.Dict[str, metadata.PluginMetadata]:
    """
    Get all available LSP (Logistics Service Provider) plugin metadata.

    Returns:
        Dictionary of plugin ID to plugin metadata
    """
    return LSP_PLUGINS


@functools.lru_cache(maxsize=1)
def get_mappers() -> typing.Dict[str, typing.Any]:
    """
    Get all available mappers (both carriers and LSP plugins).

    Returns:
        Dictionary of plugin ID to mapper class
    """
    return MAPPERS


@functools.lru_cache(maxsize=1)
def get_hooks() -> typing.Dict[str, typing.Any]:
    """
    Get all available hooks handlers.

    Returns:
        Dictionary of plugin ID to hooks class
    """
    return HOOKS


@functools.lru_cache(maxsize=1)
def get_schemas() -> typing.Dict[str, typing.Any]:
    """
    Get all available settings schemas.

    Returns:
        Dictionary of plugin ID to settings schema
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
        carrier_name: metadata_obj for carrier_name, metadata_obj in PROVIDERS.items()
    }


def collect_lsp_plugins_data() -> typing.Dict[str, dict]:
    """
    Collect LSP plugin metadata from loaded plugins.

    Returns:
        Dict mapping plugin names to their metadata
    """
    if not LSP_PLUGINS:
        import_extensions()

    return {
        plugin_name: attr.asdict(metadata_obj)
        for plugin_name, metadata_obj in LSP_PLUGINS.items()
    }


def detect_capabilities(
    proxy_methods: typing.List[str],
    hooks_methods: typing.List[str] = None,
) -> typing.List[str]:
    """
    Map proxy methods and hooks methods to carrier capabilities.

    Args:
        proxy_methods: List of method names from a Proxy class
        hooks_methods: Optional list of method names from a Hooks class

    Returns:
        List of capability identifiers
    """
    all_methods = proxy_methods + (hooks_methods or [])
    capabilities = [
        units.CarrierCapabilities.map_capability(prop) for prop in all_methods
    ]
    # Filter out None values from unmapped methods
    return list(set(cap for cap in capabilities if cap is not None))


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


def detect_hooks_methods(hooks_type: object) -> typing.List[str]:
    """
    Extract all public methods from a hooks type that are actually implemented.

    Args:
        hooks_type: A Hooks class

    Returns:
        List of method names that are implemented (not just inherited from base)
    """
    return [
        prop
        for prop in hooks_type.__dict__.keys()
        if "_" not in prop[0] and prop != "settings"
    ]


# Fields to exclude when collecting connection fields
COMMON_FIELDS = ["id", "carrier_id", "test_mode", "carrier_name", "services"]


def _normalize_option_meta(meta: typing.Optional[dict]) -> typing.Optional[dict]:
    """
    Normalize option meta to ensure configurable defaults to True.

    This ensures all options are configurable in the shipping method editor by default,
    unless explicitly set to False.
    """
    if meta is None:
        return {"configurable": True}

    normalized = dict(meta)
    if "configurable" not in normalized:
        normalized["configurable"] = True

    return normalized


def extract_nested_fields(_type: type) -> typing.Optional[typing.Dict[str, typing.Any]]:
    """
    Extract nested field definitions from an attrs class type.

    Args:
        _type: A type that may be an attrs class with __attrs_attrs__

    Returns:
        Dictionary of field definitions or None if not an attrs class
    """
    if not hasattr(_type, "__attrs_attrs__"):
        return None

    fields = {}
    for attr_field in _type.__attrs_attrs__:
        field_type = attr_field.type
        # Handle Optional types
        field_type_str = str(field_type)
        actual_type = field_type

        # Extract the inner type from Optional[X] or typing.Optional[X]
        if "Optional" in field_type_str:
            # Try to get the actual type from __args__
            if hasattr(field_type, "__args__") and field_type.__args__:
                actual_type = field_type.__args__[0]

        # Check for nested object types recursively
        nested_fields = None
        if hasattr(actual_type, "__attrs_attrs__"):
            nested_fields = extract_nested_fields(actual_type)

        # Extract enum values if the type is an enum
        enum_values = None
        if "enum" in str(actual_type).lower():
            try:
                enum_values = [e.name for e in actual_type]
            except Exception:
                pass

        field_def = lib.to_dict(
            dict(
                name=attr_field.name,
                type=parse_type(actual_type),
                required="NOTHING" in str(attr_field.default),
                default=lib.identity(
                    lib.to_dict(lib.to_json(attr_field.default))
                    if "NOTHING" not in str(attr_field.default)
                    else None
                ),
                enum=enum_values,
                fields=nested_fields,
            )
        )
        fields[attr_field.name] = field_def

    return fields if fields else None


def extract_list_item_type(_type: type) -> typing.Optional[str]:
    """
    Extract the item type name from a List type.

    Args:
        _type: A type that may be a List[X]

    Returns:
        String name of the item type or None if not a list with attrs class items
    """
    type_str = str(_type)

    # Check if it's a List type
    if "List" not in type_str and "list" not in type_str:
        return None

    # Try to get the inner type from __args__
    if hasattr(_type, "__args__") and _type.__args__:
        inner_type = _type.__args__[0]
        if hasattr(inner_type, "__attrs_attrs__"):
            return getattr(inner_type, "__name__", str(inner_type))

    return None


def extract_list_item_fields(_type: type) -> typing.Optional[typing.Dict[str, typing.Any]]:
    """
    Extract nested field definitions from the item type of a List.

    Args:
        _type: A type that may be a List[X] where X is an attrs class

    Returns:
        Dictionary of field definitions or None if not a list with attrs class items
    """
    type_str = str(_type)

    # Check if it's a List type
    if "List" not in type_str and "list" not in type_str:
        return None

    # Try to get the inner type from __args__
    if hasattr(_type, "__args__") and _type.__args__:
        inner_type = _type.__args__[0]
        if hasattr(inner_type, "__attrs_attrs__"):
            return extract_nested_fields(inner_type)

    return None


def collect_references(
    plugin_registry: dict = None,
) -> dict:
    """
    Collect all references from carriers, LSP plugins, and other plugins.

    This function builds a comprehensive dictionary of all available
    references in the system, including services, options, countries,
    currencies, carriers, LSP plugins, etc.

    Returns:
        Dictionary containing all reference data
    """
    global REFERENCES, PROVIDERS, LSP_PLUGINS
    if not PROVIDERS:
        import_extensions()

    # If references have already been computed, return them
    if REFERENCES and not plugin_registry:
        return REFERENCES

    registry = Registry(plugin_registry)

    # Determine enabled carriers
    enabled_carrier_ids = set(
        carrier_id
        for carrier_id in PROVIDERS.keys()
        if registry.get(
            f"{carrier_id.upper()}_ENABLED",
            registry.get("ENABLE_ALL_PLUGINS_BY_DEFAULT"),
        )
    )

    # Determine enabled LSP plugins
    enabled_lsp_ids = set(
        plugin_id
        for plugin_id in LSP_PLUGINS.keys()
        if registry.get(
            f"{plugin_id.upper()}_ENABLED",
            registry.get("ENABLE_ALL_PLUGINS_BY_DEFAULT"),
        )
    )

    services = {
        key: {c.name: c.value for c in list(mapper.get("services", []))}
        for key, mapper in PROVIDERS.items()
        if key in enabled_carrier_ids and mapper.get("services") is not None
    }
    options = {
        key: {
            c.name: lib.to_dict(
                dict(
                    code=c.value.code,
                    type=parse_type(c.value.type),
                    default=c.value.default,
                    help=c.value.help,
                    meta=_normalize_option_meta(c.value.meta),
                    enum=lib.identity(
                        None
                        if "enum" not in str(c.value.type).lower()
                        else [e.name for e in c.value.type]
                    ),
                    fields=extract_nested_fields(c.value.type),
                )
            )
            for c in list(mapper.get("options", []))
        }
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
                    # Extract item schema for list types (e.g., List[ServiceBillingNumberType])
                    item_type=extract_list_item_type(c.value.type),
                    fields=extract_list_item_fields(c.value.type),
                )
            )
            for c in list(mapper.get("connection_configs", []))
        }
        for key, mapper in PROVIDERS.items()
        if key in enabled_carrier_ids and mapper.get("connection_configs") is not None
    }

    # Build connection_fields with proper attrs class checking
    connection_fields = {
        key: (
            {
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
                or (
                    mapper.get("has_intl_accounts") and _.name == "account_country_code"
                )
            }
            if mapper.get("Settings") is not None
            and hasattr(mapper.get("Settings"), "__attrs_attrs__")
            else {}
        )
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
            carrier_id: metadata_obj.label
            for carrier_id, metadata_obj in PROVIDERS.items()
            if carrier_id in enabled_carrier_ids
        },
        "carrier_hubs": {
            carrier_id: metadata_obj.label
            for carrier_id, metadata_obj in PROVIDERS.items()
            if carrier_id in enabled_carrier_ids and metadata_obj.is_hub
        },
        "lsp_plugins": {
            plugin_id: metadata_obj.get("label", "")
            for plugin_id, metadata_obj in collect_lsp_plugins_data().items()
        },
        "services": services,
        "options": options,
        "connection_fields": connection_fields,
        "connection_configs": connection_configs,
        "carrier_capabilities": {
            key: detect_capabilities(
                (
                    detect_proxy_methods(mapper.get("Proxy"))
                    if mapper.get("Proxy")
                    else []
                ),
                (
                    detect_hooks_methods(mapper.get("Hooks"))
                    if mapper.get("Hooks")
                    else []
                ),
            )
            for key, mapper in PROVIDERS.items()
            if key in enabled_carrier_ids and mapper.get("Proxy") is not None
        },
        "lsp_capabilities": {
            key: detect_capabilities(
                (
                    detect_proxy_methods(mapper.get("Proxy"))
                    if mapper.get("Proxy")
                    else []
                ),
                (
                    detect_hooks_methods(mapper.get("Hooks"))
                    if mapper.get("Hooks")
                    else []
                ),
            )
            for key, mapper in LSP_PLUGINS.items()
            if key in enabled_lsp_ids and mapper.get("Proxy") is not None
        },
        "packaging_types": {
            key: {c.name: c.value for c in list(mapper.get("packaging_types", []))}
            for key, mapper in PROVIDERS.items()
            if key in enabled_carrier_ids and mapper.get("packaging_types") is not None
        },
        "package_presets": {
            key: {
                c.name: lib.to_dict(c.value)
                for c in list(mapper.get("package_presets", []))
            }
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
        # ratesheets - carrier default rate sheet configurations
        # Contains shared zones, services with zone_ids, and service_rates mappings
        # All enabled carriers are included - those without service_levels get empty defaults
        "ratesheets": {
            key: transform_to_shared_zones_format(mapper.get("service_levels") or [])
            for key, mapper in PROVIDERS.items()
            if key in enabled_carrier_ids
        },
        "integration_status": {
            carrier_id: metadata_obj.status
            for carrier_id, metadata_obj in PROVIDERS.items()
            if carrier_id in enabled_carrier_ids
        },
        "lsp_plugin_details": {
            plugin_id: {
                "id": plugin_id,
                "display_name": metadata_obj.get("label", ""),
                "service_type": metadata_obj.get("service_type", "LSP"),
                "integration_status": metadata_obj.get("status", ""),
                "website": metadata_obj.get("website", ""),
                "description": metadata_obj.get("description", ""),
                "documentation": metadata_obj.get("documentation", ""),
                "readme": metadata_obj.get("readme", ""),
            }
            for plugin_id, metadata_obj in collect_lsp_plugins_data().items()
        },
        "plugins": {
            name: {
                "id": metadata_obj.get("id", ""),
                "name": name,
                "display_name": metadata_obj.get("label", ""),
                "service_type": metadata_obj.get("service_type", "carrier"),
                "integration_status": metadata_obj.get("status", ""),
                "website": metadata_obj.get("website", ""),
                "description": metadata_obj.get("description", ""),
                "documentation": metadata_obj.get("documentation", ""),
                "readme": metadata_obj.get("readme", ""),
                "type": metadata_obj.plugin_type,
                "types": metadata_obj.plugin_types,
            }
            for name, metadata_obj in PLUGIN_METADATA.items()
        },
        "failed_plugins": collect_failed_plugins_data(),
    }

    logger.info("Karrio references loaded", plugin_count=len(PLUGIN_METADATA.keys()))
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
    hooks_class = pydoc.locate(f"karrio.mappers.{carrier_name}.Hooks")
    proxy_methods = detect_proxy_methods(proxy_class) if proxy_class else []
    hooks_methods = detect_hooks_methods(hooks_class) if hooks_class else []
    return detect_capabilities(proxy_methods, hooks_methods)


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
    # Check if it's a nested object type (attrs class)
    if hasattr(_type, "__attrs_attrs__"):
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
        is_enabled=registry.get(
            f"{plugin_code.upper()}_ENABLED",
            registry.get("ENABLE_ALL_PLUGINS_BY_DEFAULT"),
        ),
        capabilities=references["carrier_capabilities"].get(plugin_code, {}),
        connection_fields=references["connection_fields"].get(plugin_code, {}),
        config_fields=references["connection_configs"].get(plugin_code, {}),
        shipping_services=references["services"].get(plugin_code, {}),
        shipping_options=references["options"].get(plugin_code, {}),
        readme=metadata_obj.readme,
    )


def get_lsp_plugin_details(plugin_id: str, contextual_reference: dict = None) -> dict:
    """
    Get detailed information about an LSP plugin.

    Args:
        plugin_id: The ID of the LSP plugin
        contextual_reference: Optional pre-computed references dictionary

    Returns:
        Dictionary with detailed LSP plugin information
    """
    references = contextual_reference or collect_references()
    return references["lsp_plugin_details"].get(plugin_id, {})


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
            logger.error("Failed to set item in registry", key=key, error=str(e))
