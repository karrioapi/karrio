# Karrio CLI Improvements

This document details the recent improvements made to the Karrio CLI tools to enhance developer experience and productivity.

## Interactive Terminal Interface

All CLI commands now support interactive prompts when parameters are not provided. This makes the CLI more user-friendly and reduces the need to remember all command options.

### How it works:

-   When you run a command without all required parameters, the CLI will prompt you for the missing information
-   You can skip prompts by using the `--no-prompt` flag and providing all required parameters

Example:

```bash
# Interactive mode
kcli create-plugin

# Non-interactive mode
kcli create-plugin --plugin-name my-plugin --display-name "My Plugin" --description "A custom plugin" --author "Your Name"
```

## Commands with Interactive Support

### Carrier Management

-   `create-carrier` - Create a new carrier integration with interactive prompts for carrier name and display name
-   `add-extension` - Add a new carrier extension following Karrio's official format
-   `troubleshoot` - Diagnose common issues with carrier integrations
-   `migrate-structure` - Migrate a carrier to the new structure
-   `start-docs` - Start the documentation server
-   `run-tests` - Run tests for carrier integrations
-   `generate-api` - Generate API code from JSON schemas

### Plugin Management

-   `create-plugin` - Create a new plugin with interactive prompts for all configuration options

## Usability Improvements

-   Added `--dry-run` option to carrier creation commands to show what would be done without making changes
-   Added validation to ensure required parameters are provided when using `--no-prompt`
-   Improved error messages when required information is missing
-   Consistent parameter naming across all commands

## Understanding Karrio Plugins

### What is a Karrio Plugin?

A Karrio plugin is a modular extension that adds functionality to the Karrio shipping platform without modifying the core codebase. Plugins enable you to:

-   Add custom business logic for shipping operations
-   Integrate with third-party services or APIs
-   Extend carrier functionality with custom features
-   Implement specialized validation or data processing

Plugins use a standardized interface to interact with the Karrio core, making them easy to develop, test, and maintain independently.

### Plugin Architecture

Each plugin follows a standard structure:

-   Python package with its own setup.py and dependencies
-   Well-defined entry points and interfaces
-   Optional carrier-specific integrations
-   Standardized testing framework

## Creating Your First Plugin

### Step-by-Step Guide

1. **Plan your plugin**:

    - Define the purpose and functionality
    - Identify required carrier integrations (if any)
    - Determine input/output data structures

2. **Bootstrap the plugin using the CLI**:

    ```bash
    kcli create-plugin
    ```

    The interactive CLI will prompt you for:

    - Plugin name (e.g., `address_validator`)
    - Display name (e.g., "Address Validator")
    - Description
    - Author information
    - Version
    - Carrier integration (if needed)

3. **Implement your plugin logic**:

    - Edit the generated plugin.py file
    - Implement the required methods
    - Add validation logic

4. **Test your plugin**:

    - Run the included test file:
        ```bash
        python -m unittest discover -v plugins/your_plugin_name/tests
        ```
    - Add additional test cases for your functionality

5. **Install your plugin**:

    ```bash
    pip install -e ./plugins/your_plugin_name
    ```

6. **Use your plugin in your Karrio application**:

    ```python
    from karrio.plugins.your_plugin_name import plugin

    # Initialize plugin with settings
    my_plugin = plugin.YourPluginNamePlugin(settings={...})

    # Execute plugin
    result = my_plugin.execute(data={...})
    ```

### Plugin Structure Breakdown

When you create a plugin using the CLI, the following structure is generated:

```
plugins/your_plugin_name/
├── README.md                    # Documentation
├── setup.py                     # Package configuration
├── src/
│   └── karrio/
│       └── plugins/
│           └── your_plugin_name/
│               ├── __init__.py  # Version and metadata
│               ├── plugin.py    # Main plugin implementation
│               └── carriers/    # (Optional) Carrier-specific code
│                   └── carrier_name/
│                       └── __init__.py
└── tests/
    └── test_plugin.py           # Basic tests
```

### Important Files

**plugin.py**: Core plugin implementation containing the main class with:

-   `__init__`: Initialize plugin with settings
-   `execute`: Main entry point for plugin execution
-   `validate`: Data validation method

**carriers/**init**.py**: Carrier-specific implementation for plugins that integrate with specific carriers.

## Advanced Topics

### Authentication Methods

#### Basic Authentication

```python
# In settings.py
class Settings:
    def __init__(self, settings):
        self.username = settings.get('username')
        self.password = settings.get('password')
        self.carrier_settings = {
            'auth': {
                'username': self.username,
                'password': self.password
            }
        }

# In utils.py
def get_auth_header(settings):
    import base64
    credentials = f"{settings['auth']['username']}:{settings['auth']['password']}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {'Authorization': f'Basic {encoded}'}
```

#### OAuth 2.0

```python
# In settings.py
class Settings:
    def __init__(self, settings):
        self.client_id = settings.get('client_id')
        self.client_secret = settings.get('client_secret')
        self.carrier_settings = {
            'auth': {
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
        }

# In utils.py
def get_access_token(settings):
    import requests
    token_url = "https://api.example.com/oauth/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings['auth']['client_id'],
        'client_secret': settings['auth']['client_secret']
    }
    response = requests.post(token_url, data=data)
    return response.json()['access_token']
```

#### API Key

```python
# In settings.py
class Settings:
    def __init__(self, settings):
        self.api_key = settings.get('api_key')
        self.carrier_settings = {
            'auth': {
                'api_key': self.api_key
            }
        }

# In utils.py
def get_auth_header(settings):
    return {'X-API-Key': settings['auth']['api_key']}
```

### Custom Carrier Configuration

Define custom carrier configuration with enums and validation:

```python
# In settings.py
from enum import Enum

class ServiceLevel(str, Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    PRIORITY = "priority"

class PackageType(str, Enum):
    PARCEL = "parcel"
    ENVELOPE = "envelope"
    PALLET = "pallet"

class Settings:
    def __init__(self, settings):
        self.api_key = settings.get('api_key')
        self.service_level = settings.get('service_level', ServiceLevel.STANDARD)
        self.package_type = settings.get('package_type', PackageType.PARCEL)

        # Validate enum types
        if self.service_level not in ServiceLevel:
            raise ValueError(f"Invalid service level: {self.service_level}. Must be one of {[e.value for e in ServiceLevel]}")

        if self.package_type not in PackageType:
            raise ValueError(f"Invalid package type: {self.package_type}. Must be one of {[e.value for e in PackageType]}")

        self.carrier_settings = {
            'auth': {'api_key': self.api_key},
            'service_level': self.service_level,
            'package_type': self.package_type
        }
```

### Request Context and Serialization

Adding context to requests and implementing serializer functions:

```python
# Request context
def rate_request(payload, settings):
    # Add additional context to the request
    context = {
        'transaction_id': generate_transaction_id(),
        'timestamp': datetime.now().isoformat(),
        'service_level': settings.get('service_level'),
        'customer_number': settings.get('customer_number')
    }

    # Merge context with payload
    request_data = {**payload, **context}

    # Serialize to carrier-specific format
    return serialize_rate_request(request_data, settings)

# Serialization function
def serialize_rate_request(request_data, settings):
    # Transform Karrio request format to carrier-specific format
    carrier_request = {
        "shipment": {
            "sender": {
                "name": request_data["shipper"]["name"],
                "address": {
                    "street": request_data["shipper"]["address_line1"],
                    "city": request_data["shipper"]["city"],
                    "state": request_data["shipper"]["state_code"],
                    "postalCode": request_data["shipper"]["postal_code"],
                    "country": request_data["shipper"]["country_code"]
                }
            },
            "recipient": {
                "name": request_data["recipient"]["name"],
                "address": {
                    "street": request_data["recipient"]["address_line1"],
                    "city": request_data["recipient"]["city"],
                    "state": request_data["recipient"]["state_code"],
                    "postalCode": request_data["recipient"]["postal_code"],
                    "country": request_data["recipient"]["country_code"]
                }
            },
            "package": {
                "weight": {
                    "value": request_data["parcels"][0]["weight"],
                    "unit": request_data["parcels"][0]["weight_unit"]
                },
                "dimensions": {
                    "length": request_data["parcels"][0].get("length", 0),
                    "width": request_data["parcels"][0].get("width", 0),
                    "height": request_data["parcels"][0].get("height", 0),
                    "unit": request_data["parcels"][0].get("dimension_unit", "CM")
                }
            },
            "service": settings.get("service_level", "standard")
        },
        "auth": {
            "api_key": settings["auth"]["api_key"]
        },
        "transaction_id": request_data["transaction_id"]
    }

    return carrier_request
```

## Quick Reference

```bash
# Create a carrier interactively
kcli create-carrier

# Create a plugin interactively
kcli create-plugin

# Add a carrier extension with specific features
kcli add-extension --carrier-slug mycarrier --display-name "My Carrier" --features "tracking,rating,shipping"

# Troubleshoot a carrier
kcli troubleshoot

# Run tests
kcli run-tests
```
