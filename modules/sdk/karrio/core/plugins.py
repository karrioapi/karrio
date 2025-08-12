"""
Karrio Plugins Module.

This module provides functionality for loading and managing Karrio plugins.
Plugins allow extending Karrio's functionality with custom carriers, mappers,
and address validators.

Usage:
    There are several ways to use plugins with Karrio:

    1. Default plugins directory:
       By default, Karrio looks for plugins in a 'plugins' directory in the current working directory.

    2. Custom plugin directory via environment variable:
       Set the KARRIO_PLUGINS environment variable to the path of your plugins directory:

       export KARRIO_PLUGINS=/path/to/your/plugins

    3. Programmatically add plugin directories:

       import karrio.plugins as plugins
       plugins.add_plugin_directory('/path/to/your/plugins')

Plugin Directory Structure:
    A valid plugin directory can have either of the following structures:

    1. New Structure (Recommended):
    /your_plugin_directory/
    ├── plugin_name/
    │   └── karrio/
    │       ├── plugins/           # For plugins (carrier integrations, address validators, etc...)
    │       │   └── plugin_name/
    │       │       └── __init__.py # Contains METADATA
    │       ├── mappers/           # For carrier integrations
    │       │   └── plugin_name/
    │       │       ├── __init__.py # Contains METADATA
    │       │       ├── mapper.py   # Implementation of the mapper
    │       │       ├── proxy.py    # Implementation of the proxy
    │       │       └── settings.py # Settings schema
    │       ├── validators/        # For address validators
    │       │   └── plugin_name/
    │       │       ├── __init__.py # Contains METADATA
    │       │       └── validator.py # Implementation of the validator
    │       ├── providers/         # Provider-specific implementations
    │       │   └── plugin_name/
    │       │       ├── __init__.py
    │       │       ├── error.py    # Error handling
    │       │       ├── units.py    # Units and enums
    │       │       ├── utils.py    # Utility functions
    │       │       ├── rate.py     # Rating functionality
    │       │       ├── tracking.py # Tracking functionality
    │       │       ├── manifest.py # Manifest functionality
    │       │       ├── shipment/   # Shipment operations
    │       │       │   ├── __init__.py
    │       │       │   ├── create.py
    │       │       │   └── cancel.py
    │       │       └── pickup/     # Pickup operations
    │       │           ├── __init__.py
    │       │           ├── create.py
    │       │           ├── update.py
    │       │           └── cancel.py
    │       └── schemas/          # API schema definitions
    │           └── plugin_name/
    │               ├── __init__.py
    │               └── various schema files...

    2. Legacy Structure (Supported for backward compatibility):
    /your_plugin_directory/
    ├── plugin_name/
    │   └── karrio/
    │       ├── mappers/           # For carrier integrations
    │       │   └── plugin_name/
    │       │       ├── __init__.py # Contains METADATA
    │       │       ├── mapper.py   # Implementation of the mapper
    │       │       ├── proxy.py    # Implementation of the proxy
    │       │       └── settings.py # Settings schema
    │       ├── validators/        # For address validators
    │       │   └── plugin_name/
    │       │       ├── __init__.py # Contains METADATA
    │       │       └── validator.py # Implementation of the validator
    │       ├── providers/         # Provider-specific implementations
    │       │   └── plugin_name/
    │       │       ├── __init__.py
    │       │       ├── error.py    # Error handling
    │       │       ├── units.py    # Units and enums
    │       │       ├── utils.py    # Utility functions
    │       │       ├── rate.py     # Rating functionality
    │       │       ├── tracking.py # Tracking functionality
    │       │       ├── manifest.py # Manifest functionality
    │       │       ├── shipment/   # Shipment operations
    │       │       │   ├── __init__.py
    │       │       │   ├── create.py
    │       │       │   └── cancel.py
    │       │       └── pickup/     # Pickup operations
    │       │           ├── __init__.py
    │       │           ├── create.py
    │       │           ├── update.py
    │       │           └── cancel.py
    │       └── schemas/          # API schema definitions
    │           └── plugin_name/
    │               ├── __init__.py
    │               └── various schema files...

Plugin Metadata:
    Each plugin must define a METADATA object of type PluginMetadata in its __init__.py file.
    The metadata should specify the plugin's capabilities, features, and other relevant information.

    The plugin's capabilities (carrier integration, address validation, etc.) are automatically
    determined based on the components defined in the metadata and registered modules.
"""

import os
import sys
import inspect
import logging
import importlib
import traceback
import pkgutil
from typing import List, Optional, Dict, Any, Tuple
import importlib.metadata as importlib_metadata

# Configure logger with a higher default level to reduce noise
logger = logging.getLogger(__name__)
if not logger.level:
    logger.setLevel(logging.INFO)

# Default plugin directories to scan
DEFAULT_PLUGINS = [
    os.path.join(os.getcwd(), "plugins"),  # Local plugins directory
    os.path.join(os.getcwd(), "community/plugins"),  # Community plugins directory
]

# Track failed plugin loads
FAILED_PLUGIN_MODULES: Dict[str, Any] = {}

# Entrypoint group for Karrio plugins
ENTRYPOINT_GROUP = "karrio.plugins"

# Ensure the karrio.plugins module exists
try:
    import karrio.plugins
except ImportError:
    # Create an empty module for plugins if it doesn't exist
    try:
        import types
        import karrio

        karrio.plugins = types.ModuleType("karrio.plugins")
        karrio.plugins.__path__ = []
        sys.modules["karrio.plugins"] = karrio.plugins
        logger.debug("Created karrio.plugins module")
    except (ImportError, AttributeError) as e:
        logger.error(f"Failed to create karrio.plugins module: {e}")


def get_custom_plugin_dirs() -> List[str]:
    """
    Get custom plugin directory from environment variable.

    Checks if the KARRIO_PLUGINS environment variable is defined
    and if the directory exists. Returns a list containing the
    custom plugin directory if it's valid.

    Returns:
        List[str]: List of valid custom plugin directories from environment variables
    """
    custom_dirs = []
    env_plugins = os.environ.get("KARRIO_PLUGINS", "")

    if env_plugins and os.path.exists(env_plugins):
        custom_dirs.append(env_plugins)

    return custom_dirs


# Initialize DEFAULT_PLUGINS with environment variable directories
custom_dirs = get_custom_plugin_dirs()
for directory in custom_dirs:
    if directory not in DEFAULT_PLUGINS:
        DEFAULT_PLUGINS.append(directory)


def add_plugin_directory(directory: str) -> None:
    """
    Add a custom plugin directory programmatically.

    This function checks if the directory exists and if it's not already
    in the DEFAULT_PLUGINS list. If it passes these checks, the directory
    is added to the list and the extensions are reloaded.

    Args:
        directory (str): Path to the plugin directory to add

    Example:
        >>> import karrio.plugins as plugins
        >>> plugins.add_plugin_directory('/path/to/your/plugins')
    """
    global DEFAULT_PLUGINS
    if os.path.exists(directory) and directory not in DEFAULT_PLUGINS:
        DEFAULT_PLUGINS.append(directory)
        # Trigger a reload of plugins when a new directory is added
        try:
            import karrio.references

            if hasattr(karrio.references, "import_extensions"):
                karrio.references.import_extensions()
        except (ImportError, AttributeError):
            pass  # Silently ignore if references module can't be imported


def discover_plugins(plugin_dirs: Optional[List[str]] = None) -> List[str]:
    """
    Discover available plugins in the specified directories.

    Scans the given directories (or DEFAULT_PLUGINS if none specified)
    for valid Karrio plugin structures. A valid plugin structure must
    have a 'karrio' subdirectory with plugins, mappers and/or validators.

    Args:
        plugin_dirs: List of directories to scan for plugins.
                     If None, uses DEFAULT_PLUGINS.

    Returns:
        List of paths to valid plugin directories
    """
    if plugin_dirs is None:
        plugin_dirs = DEFAULT_PLUGINS
    else:
        # Ensure plugin_dirs has unique entries
        plugin_dirs = list(dict.fromkeys(plugin_dirs))

    plugins = []
    for plugin_dir in plugin_dirs:
        if not os.path.exists(plugin_dir):
            continue

        # Look for directories that might be plugins
        for item in os.listdir(plugin_dir):
            item_path = os.path.join(plugin_dir, item)
            if os.path.isdir(item_path):
                # Check if this directory has a karrio subdirectory
                karrio_dir = os.path.join(item_path, "karrio")

                # Skip if karrio directory doesn't exist
                if not os.path.isdir(karrio_dir):
                    continue

                # Check for plugins, mappers or validators subdirectories
                plugins_dir = os.path.join(karrio_dir, "plugins")
                mappers_dir = os.path.join(karrio_dir, "mappers")
                validators_dir = os.path.join(karrio_dir, "validators")

                if (
                    os.path.isdir(plugins_dir)
                    or os.path.isdir(mappers_dir)
                    or os.path.isdir(validators_dir)
                ):
                    plugins.append(item_path)

    # Ensure returned plugin paths are unique
    return list(dict.fromkeys(plugins))


def discover_plugin_modules(
    plugin_dirs: Optional[List[str]] = None, module_types: List[str] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Discover and collect modules from plugins by type.

    Scans plugin directories for modules of specified types (plugins, mappers, validators, etc.)
    and returns them organized by plugin name and module type.

    Args:
        plugin_dirs: List of plugin directories to scan (uses DEFAULT_PLUGINS if None)
        module_types: List of module types to discover (defaults to ["plugins", "mappers", "validators"])

    Returns:
        Dict mapping plugin names to a dict of module types and their module objects
    """
    global FAILED_PLUGIN_MODULES
    FAILED_PLUGIN_MODULES = {}

    if module_types is None:
        module_types = ["plugins", "mappers", "validators"]

    plugin_paths = discover_plugins(plugin_dirs)
    plugin_modules: Dict[str, Dict[str, Any]] = {}

    for plugin_path in plugin_paths:
        plugin_name = os.path.basename(plugin_path)
        karrio_dir = os.path.join(plugin_path, "karrio")

        # Skip if karrio directory doesn't exist
        if not os.path.isdir(karrio_dir):
            continue

        plugin_modules[plugin_name] = {}

        # Check for each module type
        for module_type in module_types:
            module_dir = os.path.join(karrio_dir, module_type)

            # Skip if this module type doesn't exist in the plugin
            if not os.path.isdir(module_dir):
                continue

            # Look for plugin-specific submodules (e.g., plugins/plugin_name or mappers/plugin_name)
            for subitem in os.listdir(module_dir):
                subitem_path = os.path.join(module_dir, subitem)
                submodule_init = os.path.join(subitem_path, "__init__.py")

                if os.path.isdir(subitem_path) and os.path.exists(submodule_init):
                    submodule_name = subitem

                    # Try to import the module
                    try:
                        # Add the plugin's parent dir to sys.path if not already there
                        plugin_parent = os.path.dirname(plugin_path)
                        if plugin_parent not in sys.path:
                            sys.path.insert(0, plugin_parent)

                        # Import the module
                        module_path = f"karrio.{module_type}.{submodule_name}"
                        module = importlib.import_module(module_path)

                        # Store successful imports
                        if module_type not in plugin_modules[plugin_name]:
                            plugin_modules[plugin_name][module_type] = {}

                        plugin_modules[plugin_name][module_type][
                            submodule_name
                        ] = module

                    except Exception as e:
                        # Track failed module imports
                        logger.error(
                            f"Error importing {module_type}.{submodule_name} from {plugin_name}: {str(e)}"
                        )
                        key = f"{plugin_name}.{module_type}.{submodule_name}"
                        FAILED_PLUGIN_MODULES[key] = {
                            "plugin": plugin_name,
                            "module_type": module_type,
                            "submodule": submodule_name,
                            "error": str(e),
                            "traceback": traceback.format_exc(),
                        }

    return plugin_modules


def collect_plugin_metadata(
    plugin_modules: Dict[str, Dict[str, Any]],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Collect metadata from discovered plugin modules.

    Args:
        plugin_modules: Dictionary of plugin modules organized by plugin name and module type

    Returns:
        Tuple containing:
        - Dictionary of successful plugin metadata
        - Dictionary of failed plugin metadata attempts
    """
    plugin_metadata = {}
    failed_metadata = {}

    for plugin_name, modules_by_type in plugin_modules.items():
        metadata_found = False

        # First try to find metadata in plugins (new structure)
        if "plugins" in modules_by_type:
            for submodule_name, module in modules_by_type["plugins"].items():
                try:
                    if hasattr(module, "METADATA"):
                        plugin_metadata[plugin_name] = module.METADATA
                        metadata_found = True
                        break
                except Exception as e:
                    key = f"{plugin_name}.plugins.{submodule_name}"
                    failed_metadata[key] = {
                        "plugin": plugin_name,
                        "module_type": "plugins",
                        "submodule": submodule_name,
                        "error": str(e),
                    }

        # If not found in plugins, try mappers (legacy structure)
        if not metadata_found and "mappers" in modules_by_type:
            for submodule_name, module in modules_by_type["mappers"].items():
                try:
                    if hasattr(module, "METADATA"):
                        plugin_metadata[plugin_name] = module.METADATA
                        metadata_found = True
                        break
                except Exception as e:
                    key = f"{plugin_name}.mappers.{submodule_name}"
                    failed_metadata[key] = {
                        "plugin": plugin_name,
                        "module_type": "mappers",
                        "submodule": submodule_name,
                        "error": str(e),
                    }

        # If not found in mappers, try validators (legacy structure)
        if not metadata_found and "validators" in modules_by_type:
            for submodule_name, module in modules_by_type["validators"].items():
                try:
                    if hasattr(module, "METADATA"):
                        plugin_metadata[plugin_name] = module.METADATA
                        metadata_found = True
                        break
                except Exception as e:
                    key = f"{plugin_name}.validators.{submodule_name}"
                    failed_metadata[key] = {
                        "plugin": plugin_name,
                        "module_type": "validators",
                        "submodule": submodule_name,
                        "error": str(e),
                    }

        if not metadata_found and modules_by_type:
            # Record error only if we have some modules but no metadata
            failed_metadata[plugin_name] = {
                "plugin": plugin_name,
                "error": "No METADATA found in any module",
            }

        # NEW: Try direct import of karrio.plugins.[plugin_name] and karrio.mappers.[plugin_name] if not found
        if not metadata_found:
            for modtype in ["plugins", "mappers"]:
                try:
                    module_path = f"karrio.{modtype}.{plugin_name}"
                    module = importlib.import_module(module_path)
                    if hasattr(module, "METADATA"):
                        plugin_metadata[plugin_name] = module.METADATA
                        metadata_found = True
                        break
                except Exception as e:
                    key = f"{plugin_name}.{modtype}.__init__"
                    failed_metadata[key] = {
                        "plugin": plugin_name,
                        "module_type": modtype,
                        "submodule": "__init__",
                        "error": str(e),
                    }

    return plugin_metadata, failed_metadata


def load_local_plugins(plugin_dirs: Optional[List[str]] = None) -> List[str]:
    """
    Load plugins from local directories into the karrio namespace.

    This function:
    1. Discovers plugins in the specified directories
    2. Adds the plugin parent directory to sys.path
    3. Extends the karrio namespace to include the plugin modules
    4. Refreshes karrio.references (if not called from references)

    Args:
        plugin_dirs: List of directories to scan for plugins.
                     If None, uses DEFAULT_PLUGINS.

    Returns:
        List of plugin names that were successfully loaded
    """

    plugins = discover_plugins(plugin_dirs)
    loaded_plugins = []
    already_processed = (
        set()
    )  # Track which plugins have been processed to avoid duplicates

    # Ensure all required namespaces exist
    required_namespaces = ["plugins", "mappers", "providers", "schemas", "validators"]
    for namespace in required_namespaces:
        module_name = f"karrio.{namespace}"
        try:
            # Try to import the module
            importlib.import_module(module_name)
        except ImportError:
            # Create the module if it doesn't exist
            try:
                import types
                import karrio

                module = types.ModuleType(module_name)
                module.__path__ = []
                setattr(karrio, namespace, module)
                sys.modules[module_name] = module
                logger.debug(f"Created {module_name} module")
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to create {module_name} module: {e}")

    for plugin_path in plugins:
        # Skip if we've already processed this plugin path
        if plugin_path in already_processed:
            continue

        already_processed.add(plugin_path)
        plugin_name = os.path.basename(plugin_path)

        # Add the plugin's parent directory to sys.path
        plugin_parent = os.path.dirname(plugin_path)
        if plugin_parent not in sys.path:
            sys.path.insert(0, plugin_parent)

        # Check if the plugin has the necessary structure
        karrio_dir = os.path.join(plugin_path, "karrio")

        # Skip if karrio directory doesn't exist
        if not os.path.isdir(karrio_dir):
            logger.error(
                f"Invalid plugin structure: missing karrio directory in {plugin_path}"
            )
            continue

        # Look for plugins, mappers, providers, schemas, and validators directories
        for module_name in required_namespaces:
            module_dir = os.path.join(karrio_dir, module_name)

            # Skip if directory doesn't exist
            if not os.path.isdir(module_dir):
                continue

            # Try to extend the corresponding karrio namespace
            try:
                target_module_name = f"karrio.{module_name}"
                target_module = importlib.import_module(target_module_name)

                # Extend the module's __path__ to include our plugin directory
                if hasattr(target_module, "__path__"):
                    extended_path = pkgutil.extend_path(
                        target_module.__path__, target_module.__name__
                    )
                    if module_dir not in extended_path:
                        extended_path.append(module_dir)
                    target_module.__path__ = extended_path
            except ImportError as e:
                logger.error(f"Could not import {target_module_name}: {e}")
                continue

        # Mark plugin as loaded
        loaded_plugins.append(plugin_name)

    # To prevent recursion, only refresh references if we're not being called from references
    # This check uses the stack frame inspection to see if we're being called from import_extensions
    calling_module = ""
    frame = inspect.currentframe()
    if frame and frame.f_back:
        calling_module = frame.f_back.f_globals.get("__name__", "")
    if "karrio.references" not in calling_module:
        try:
            import karrio.references

            if hasattr(karrio.references, "import_extensions"):
                karrio.references.import_extensions()
                logger.info("Refreshed karrio.references providers")
        except (ImportError, AttributeError) as e:
            logger.error(f"Could not refresh karrio.references: {e}")

    return loaded_plugins


def get_failed_plugin_modules() -> Dict[str, Any]:
    """
    Get information about plugin modules that failed to load.

    Returns:
        Dict containing information about failed plugin module loads
    """
    return FAILED_PLUGIN_MODULES  # type: ignore


def discover_entrypoint_plugins() -> Dict[str, Dict[str, Any]]:
    """
    Discover plugins registered via setuptools entrypoints.

    This function looks for plugins registered under the 'karrio.plugins'
    entrypoint group. Each entrypoint should point to a module with a METADATA
    object that defines the plugin's capabilities.

    Returns:
        Dict mapping plugin names to a dict containing the plugin module
    """
    global FAILED_PLUGIN_MODULES
    entrypoint_plugins = {}

    try:
        # Find all entry points in the karrio.plugins group
        entry_points = importlib_metadata.entry_points()

        # Handle different entry_points behavior in different versions of importlib_metadata
        if hasattr(entry_points, "select"):  # Python 3.10+
            plugin_entry_points = entry_points.select(group=ENTRYPOINT_GROUP)
        elif hasattr(entry_points, "get"):  # Python 3.8, 3.9
            plugin_entry_points = entry_points.get(ENTRYPOINT_GROUP, [])  # type: ignore
        else:  # Older versions or different implementation
            plugin_entry_points = [
                ep
                for ep in entry_points
                if getattr(ep, "group", None) == ENTRYPOINT_GROUP
            ]  # type: ignore

        for entry_point in plugin_entry_points:
            plugin_name = entry_point.name

            try:
                # Load the plugin module
                plugin_module = entry_point.load()

                # Create a structured dict similar to discover_plugin_modules output
                if plugin_name not in entrypoint_plugins:
                    entrypoint_plugins[plugin_name] = {
                        "entrypoint": {plugin_name: plugin_module}
                    }

            except Exception as e:
                # Track failed entrypoint loads
                logger.error(f"Error loading entrypoint plugin {plugin_name}: {str(e)}")
                key = f"entrypoint.{plugin_name}"
                FAILED_PLUGIN_MODULES[key] = {
                    "plugin": plugin_name,
                    "module_type": "entrypoint",
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }

    except Exception as e:
        logger.error(f"Error discovering entrypoint plugins: {str(e)}")

    return entrypoint_plugins
