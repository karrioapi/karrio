# Karrio Plugin System

## Overview

The Karrio Plugin System provides a flexible, modular architecture for extending Karrio's functionality with custom carriers, address validators, and other integrations. This system allows developers to create and distribute carrier integrations that seamlessly integrate with the Karrio shipping platform.

## Architecture

Karrio's plugin architecture consists of several key components:

### 1. Plugin Discovery

The system scans specific directories for valid Karrio plugin structures at startup. This includes:
- Default plugins directory (usually `./plugins`)
- Custom plugin directories specified via the `KARRIO_PLUGINS` environment variable
- Programmatically added directories via `add_plugin_directory()`

### 2. Plugin Structure

A valid plugin can follow either the new structure (recommended) or the legacy structure:

#### New Structure (Recommended)
```
/your_plugin_directory/
├── plugin_name/
│   └── karrio/
│       ├── plugins/           # Main plugin entry point (contains METADATA)
│       │   └── plugin_name/
│       │       └── __init__.py # Contains METADATA
│       ├── mappers/           # For carrier integrations
│       │   └── plugin_name/
│       │       ├── __init__.py # Simple imports only
│       │       ├── mapper.py   # Implementation of the mapper
│       │       ├── proxy.py    # Implementation of the proxy
│       │       └── settings.py # Settings schema
│       ├── validators/        # For address validators
│       │   └── plugin_name/
│       │       ├── __init__.py # Simple imports only
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
```

#### Legacy Structure (Supported for backward compatibility)
```
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
│       │       └── implementation files...
│       └── schemas/          # API schema definitions
│           └── plugin_name/
│               ├── __init__.py
│               └── schema files...
```

### 3. Plugin Metadata

Every plugin must define a `METADATA` object in its `__init__.py` file, with the following structure:

```python
from karrio.core.metadata import PluginMetadata

METADATA = PluginMetadata(
    id="plugin_name",              # Unique identifier for the plugin
    label="Human Readable Name",   # Display name for the plugin
    description="Plugin description", # Optional description
    status="beta",                 # Status: "beta", "production-ready", etc.

    # Components that define capabilities
    Mapper=Mapper,                 # For carrier integration
    Proxy=Proxy,                   # For carrier integration
    Settings=Settings,             # For carrier integration
    Validator=Validator,           # For address validation

    # Optional metadata
    website="https://plugin-website.com",
    documentation="https://docs.plugin-website.com",
    readme="Markdown content or path to README file",

    # Additional carrier-specific units
    options=ShippingOption,        # Custom shipping options
    services=ShippingService,      # Available shipping services
    packaging_types=PackagingType, # Packaging options

    # Extended functionality flags
    is_hub=False,                 # Whether this is a multi-carrier hub
    has_intl_accounts=False,      # Whether international accounts are supported
)
```

### 4. Plugin Registration & Loading

The system loads plugins in the following order:
1. Plugins from file system directories (using `load_local_plugins()`)
2. Plugins from the `karrio.plugins` namespace (new structure)
3. Plugins from the `karrio.mappers` namespace (legacy structure)
4. Built-in address validators from `karrio.validators`
5. Built-in carrier integrations from `karrio.providers`

### 5. Plugin Capabilities

Capabilities are automatically determined based on registered components:
- **Carrier Integration**: Requires `Mapper`, `Proxy`, and `Settings` components
- **Address Validation**: Requires `Validator` component
- **Dual Purpose**: When both carrier integration and address validation components are present

## Implementing a Plugin

### Creating a New Plugin

The recommended approach is to use the Karrio CLI:

```bash
kcli sdk add-extension --path ./your-plugins-dir
```

This will prompt for details and generate the appropriate structure. The Karrio CLI (`kcli`) now automatically creates the new plugin structure with the METADATA in the `plugins/[plugin_name]/__init__.py` file, while still maintaining the legacy structure for backward compatibility.

For existing plugins, you can add the new plugin structure with:

```bash
kcli sdk add-features carrier_name "Carrier Name" --path ./your-plugins-dir
```

This will detect the existing carrier and add the new plugin structure alongside the legacy one.

### Manual Implementation

1. Create the directory structure following the new structure format
2. Implement the required components (Mapper, Proxy, Settings, etc.)
3. Define the METADATA object in the `plugins/plugin_name/__init__.py` file
4. Register your plugin directory with Karrio

### Plugin Testing

The generated structure includes test directories with fixtures for testing your implementation:

```
/your_plugin_directory/
├── tests/
│   ├── __init__.py
│   └── plugin_name/
│       ├── __init__.py
│       ├── fixture.py
│       └── test_*.py
```

## Integration with Karrio

Plugins are automatically discovered and loaded by Karrio at startup. The system maintains references to all discovered plugins, making them available through:

- Gateway access: `karrio.gateway["plugin_name"].create(Settings(...))`
- References: `karrio.references.collect_references()`
- Plugin listings: `karrio.references.get_plugin_metadata()`

## Best Practices

1. **Use the new structure** for all new plugins
2. **Place METADATA in the plugins directory** (`karrio/plugins/plugin_name/__init__.py`)
3. **Use attrs for Settings classes** to ensure proper introspection
4. **Keep mappers simple** with minimal business logic
5. **Implement thorough error handling** in provider modules
6. **Provide comprehensive documentation** in your plugin's README.md

## Distributing Plugins

Plugins can be distributed as Python packages, allowing for easy installation via pip:

```bash
pip install karrio.plugin_name
```

Or directly from a Git repository:

```bash
pip install git+https://github.com/username/karrio-plugin-name.git
```

## Troubleshooting

Common issues:
- Missing METADATA object
- Incorrect directory structure
- Missing required components
- Settings class not decorated with attrs

The system maintains detailed logs of plugin loading issues in `FAILED_PLUGIN_MODULES`, which can be accessed for debugging.
