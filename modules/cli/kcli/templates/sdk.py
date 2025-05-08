"""CARRIER EXTENSION TEMPLATES SECTION"""
from jinja2 import Template

README_TEMPLATE = Template("""# karrio.{{id}}

This package is a {{name}} extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.{{id}}
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.{{id}}.settings import Settings


# Initialize a carrier gateway
{{id}} = karrio.gateway["{{id}}"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests

"""
)

PYPROJECT_TEMPLATE = Template('''[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "karrio_{{id}}"
version = "{{version}}"
description = "Karrio - {{name}} Shipping Extension"
readme = "README.md"
requires-python = ">=3.11"
license = "Apache-2.0"
authors = [
    {name = "karrio", email = "hello@karrio.io"}
]
classifiers = [
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]
dependencies = [
    "karrio",
]

[project.urls]
Homepage = "https://github.com/karrioapi/karrio"

[project.entry-points."karrio.plugins"]
{{id}} = "karrio.plugins.{{id}}"

[tool.setuptools]
zip-safe = false
include-package-data = true

[tool.setuptools.package-dir]
"" = "."

[tool.setuptools.packages.find]
exclude = ["tests.*", "tests"]
namespaces = true
''')

SETUP_TEMPLATE = Template('''
"""Warning: This setup.py is only there for git install until poetry support git subdirectory"""
from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="karrio.{{id}}",
    version="{{version}}",
    description="Karrio - {{name}} Shipping Extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karrioapi/karrio",
    author="karrio",
    author_email="hello@karrio.io",
    license="Apache-2.0",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=["karrio"],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    include_package_data=True,
)

'''
)

XML_GENERATE_TEMPLATE = Template("""SCHEMAS=./schemas
LIB_MODULES=./karrio/schemas/{{id}}
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \\;
touch "${LIB_MODULES}/__init__.py"

generateDS --no-namespace-defs -o "${LIB_MODULES}/error.py" $SCHEMAS/error_response.xsd{% if "address" in features %}
generateDS --no-namespace-defs -o "${LIB_MODULES}/address_validation_request.py" $SCHEMAS/address_validation_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/address_validation_response.py" $SCHEMAS/address_validation_response.xsd{% endif %}{% if "rating" in features %}
generateDS --no-namespace-defs -o "${LIB_MODULES}/rate_request.py" $SCHEMAS/rate_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/rate_response.py" $SCHEMAS/rate_response.xsd{% endif %}{% if "pickup" in features %}
generateDS --no-namespace-defs -o "${LIB_MODULES}/pickup_create_request.py" $SCHEMAS/pickup_create_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/pickup_create_response.py" $SCHEMAS/pickup_create_response.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/pickup_update_request.py" $SCHEMAS/pickup_update_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/pickup_update_response.py" $SCHEMAS/pickup_update_response.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/pickup_cancel_request.py" $SCHEMAS/pickup_cancel_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/pickup_cancel_response.py" $SCHEMAS/pickup_cancel_response.xsd{% endif %}{% if "manifest" in features %}
generateDS --no-namespace-defs -o "${LIB_MODULES}/manifest_request.py" $SCHEMAS/manifest_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/manifest_response.py" $SCHEMAS/manifest_response.xsd{% endif %}{% if "shipping" in features %}
generateDS --no-namespace-defs -o "${LIB_MODULES}/shipment_request.py" $SCHEMAS/shipment_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/shipment_response.py" $SCHEMAS/shipment_response.xsd{% endif %}{% if "tracking" in features %}
generateDS --no-namespace-defs -o "${LIB_MODULES}/tracking_request.py" $SCHEMAS/tracking_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/tracking_response.py" $SCHEMAS/tracking_response.xsd{% endif %}{% if "document" in features %}
generateDS --no-namespace-defs -o "${LIB_MODULES}/document_upload_request.py" $SCHEMAS/document_upload_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/document_upload_response.py" $SCHEMAS/document_upload_response.xsd{% endif %}
"""
)

JSON_GENERATE_TEMPLATE = Template("""SCHEMAS=./schemas
LIB_MODULES=./karrio/schemas/{{id}}
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \\;
touch "${LIB_MODULES}/__init__.py"

kcli codegen generate "${SCHEMAS}/error_response.json" "${LIB_MODULES}/error_response.py"{% if "address" in features %}
kcli codegen generate "${SCHEMAS}/address_validation_request.json" "${LIB_MODULES}/address_validation_request.py"
kcli codegen generate "${SCHEMAS}/address_validation_response.json" "${LIB_MODULES}/address_validation_response.py"{% endif %}{% if "rating" in features %}
kcli codegen generate "${SCHEMAS}/rate_request.json" "${LIB_MODULES}/rate_request.py"
kcli codegen generate "${SCHEMAS}/rate_response.json" "${LIB_MODULES}/rate_response.py"{% endif %}{% if "pickup" in features %}
kcli codegen generate "${SCHEMAS}/pickup_create_request.json" "${LIB_MODULES}/pickup_create_request.py"
kcli codegen generate "${SCHEMAS}/pickup_create_response.json" "${LIB_MODULES}/pickup_create_response.py"
kcli codegen generate "${SCHEMAS}/pickup_update_request.json" "${LIB_MODULES}/pickup_update_request.py"
kcli codegen generate "${SCHEMAS}/pickup_update_response.json" "${LIB_MODULES}/pickup_update_response.py"
kcli codegen generate "${SCHEMAS}/pickup_cancel_request.json" "${LIB_MODULES}/pickup_cancel_request.py"
kcli codegen generate "${SCHEMAS}/pickup_cancel_response.json" "${LIB_MODULES}/pickup_cancel_response.py"{% endif %}{% if "manifest" in features %}
kcli codegen generate "${SCHEMAS}/manifest_request.json" "${LIB_MODULES}/manifest_request.py"
kcli codegen generate "${SCHEMAS}/manifest_response.json" "${LIB_MODULES}/manifest_response.py"{% endif %}{% if "shipping" in features %}
kcli codegen generate "${SCHEMAS}/shipment_request.json" "${LIB_MODULES}/shipment_request.py"
kcli codegen generate "${SCHEMAS}/shipment_response.json" "${LIB_MODULES}/shipment_response.py"{% endif %}{% if "tracking" in features %}
kcli codegen generate "${SCHEMAS}/tracking_request.json" "${LIB_MODULES}/tracking_request.py"
kcli codegen generate "${SCHEMAS}/tracking_response.json" "${LIB_MODULES}/tracking_response.py"{% endif %}{% if "document" in features %}
kcli codegen generate "${SCHEMAS}/document_upload_request.json" "${LIB_MODULES}/document_upload_request.py"
kcli codegen generate "${SCHEMAS}/document_upload_response.json" "${LIB_MODULES}/document_upload_response.py"{% endif %}


"""
)

MAPPER_IMPORTS_TEMPLATE = Template(
    """from karrio.mappers.{{id}}.mapper import Mapper
from karrio.mappers.{{id}}.proxy import Proxy
from karrio.mappers.{{id}}.settings import Settings
"""
)

MAPPER_METADATA_TEMPLATE = Template(
    """from karrio.core.metadata import Metadata

from karrio.mappers.{{id}}.mapper import Mapper
from karrio.mappers.{{id}}.proxy import Proxy
from karrio.mappers.{{id}}.settings import Settings
import karrio.providers.{{id}}.units as units
import karrio.providers.{{id}}.utils as utils


METADATA = Metadata(
    id="{{id}}",
    label="{{name}}",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    # options=units.ShippingOption,
    # services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
)

"""
)

PLUGIN_METADATA_TEMPLATE = Template(
    """from karrio.core.metadata import PluginMetadata

from karrio.mappers.{{id}}.mapper import Mapper
from karrio.mappers.{{id}}.proxy import Proxy
from karrio.mappers.{{id}}.settings import Settings
import karrio.providers.{{id}}.units as units
import karrio.providers.{{id}}.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="{{id}}",
    label="{{name}}",
    description="{{name}} shipping integration for Karrio",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    # options=units.ShippingOption,
    # services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
    # Extra info
    website="",
    documentation="",
)

"""
)

MAPPER_TEMPLATE = Template('''"""Karrio {{name}} client mapper."""

import typing
import karrio.lib as lib
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.providers.{{id}} as provider
import karrio.mappers.{{id}}.settings as provider_settings


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings{% if "rating" in features %}

    def create_rate_request(
        self, payload: models.RateRequest
    ) -> lib.Serializable:
        return provider.rate_request(payload, self.settings)
    {% endif %}{% if "tracking" in features %}
    def create_tracking_request(
        self, payload: models.TrackingRequest
    ) -> lib.Serializable:
        return provider.tracking_request(payload, self.settings)
    {% endif %}{% if "shipping" in features %}
    def create_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        return provider.shipment_request(payload, self.settings)
    {% endif %}{% if "pickup" in features %}
    def create_pickup_request(
        self, payload: models.PickupRequest
    ) -> lib.Serializable:
        return provider.pickup_request(payload, self.settings)
    {% endif %}{% if "pickup" in features %}
    def create_pickup_update_request(
        self, payload: models.PickupUpdateRequest
    ) -> lib.Serializable:
        return provider.pickup_update_request(payload, self.settings)
    {% endif %}{% if "pickup" in features %}
    def create_cancel_pickup_request(
        self, payload: models.PickupCancelRequest
    ) -> lib.Serializable:
        return provider.pickup_cancel_request(payload, self.settings)
    {% endif %}{% if "shipping" in features %}
    def create_cancel_shipment_request(
        self, payload: models.ShipmentCancelRequest
    ) -> lib.Serializable[str]:
        return provider.shipment_cancel_request(payload, self.settings)
    {% endif %}{% if "document" in features %}
    def create_document_upload_request(
        self, payload: models.DocumentUploadRequest
    ) -> lib.Serializable[str]:
        return provider.document_upload_request(payload, self.settings)
    {% endif %}{% if "address" in features %}
    def create_address_validation_request(
        self, payload: models.AddressValidationRequest
    ) -> lib.Serializable:
        return provider.address_validation_request(payload, self.settings)
    {% endif %}{% if "manifest" in features %}
    def create_manifest_request(
        self, payload: models.ManifestRequest
    ) -> lib.Serializable:
        return provider.manifest_request(payload, self.settings)
    {% endif %}
    {% if "pickup" in features %}
    def parse_cancel_pickup_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_pickup_cancel_response(response, self.settings)
    {% endif %}{% if "shipping" in features %}
    def parse_cancel_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_shipment_cancel_response(response, self.settings)
    {% endif %}{% if "pickup" in features %}
    def parse_pickup_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
        return provider.parse_pickup_response(response, self.settings)
    {% endif %}{% if "pickup" in features %}
    def parse_pickup_update_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
        return provider.parse_pickup_update_response(response, self.settings)
    {% endif %}{% if "rating" in features %}
    def parse_rate_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
        return provider.parse_rate_response(response, self.settings)
    {% endif %}{% if "shipping" in features %}
    def parse_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return provider.parse_shipment_response(response, self.settings)
    {% endif %}{% if "tracking" in features %}
    def parse_tracking_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
        return provider.parse_tracking_response(response, self.settings)
    {% endif %}{% if "document" in features %}
    def parse_document_upload_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
        return provider.parse_document_upload_response(response, self.settings)
    {% endif %}{% if "manifest" in features %}
    def parse_manifest_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
        return provider.parse_manifest_response(response, self.settings)
    {% endif %}{% if "address" in features %}
    def parse_address_validation_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.AddressValidationDetails], typing.List[models.Message]]:
        return provider.parse_address_validation_response(response, self.settings)
    {% endif %}

'''
)

MAPPER_PROXY_TEMPLATE = Template('''"""Karrio {{name}} client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.{{id}}.settings as provider_settings

# IMPLEMENTATION INSTRUCTIONS:
# 1. Import the schema types specific to your carrier API
# 2. Uncomment and adapt the request examples below to work with your carrier API
# 3. Replace the stub responses with actual API calls once you've tested with the example data
# 4. Update URLs, headers, and authentication methods as required by your carrier API


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings{% if "rating" in features %}

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/rates",
        #     data={% if is_xml_api %}request.serialize(){% else %}lib.to_json(request.serialize()){% endif %},
        #     trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
        #     method="POST",
        #     headers={
        #         "Content-Type": {% if is_xml_api %}"application/xml"{% else %}"application/json"{% endif %},
        #         {% if is_xml_api %}"Authorization": f"Basic {self.settings.authorization}"{% else %}"Authorization": f"Bearer {self.settings.api_key}"{% endif %}
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        {% if is_xml_api %}response = '<r></r>'{% else %}response = lib.to_json({}){% endif %}

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "shipping" in features %}
    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/shipments",
        #     data={% if is_xml_api %}request.serialize(){% else %}lib.to_json(request.serialize()){% endif %},
        #     trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
        #     method="POST",
        #     headers={
        #         "Content-Type": {% if is_xml_api %}"application/xml"{% else %}"application/json"{% endif %},
        #         {% if is_xml_api %}"Authorization": f"Basic {self.settings.authorization}"{% else %}"Authorization": f"Bearer {self.settings.api_key}"{% endif %}
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        {% if is_xml_api %}response = '<r></r>'{% else %}response = lib.to_json({}){% endif %}

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "shipping" in features %}
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/shipments/cancel",
        #     data={% if is_xml_api %}request.serialize(){% else %}lib.to_json(request.serialize()){% endif %},
        #     trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
        #     method="POST",
        #     headers={
        #         "Content-Type": {% if is_xml_api %}"application/xml"{% else %}"application/json"{% endif %},
        #         {% if is_xml_api %}"Authorization": f"Basic {self.settings.authorization}"{% else %}"Authorization": f"Bearer {self.settings.api_key}"{% endif %}
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        {% if is_xml_api %}response = '<r></r>'{% else %}response = lib.to_json({}){% endif %}

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "tracking" in features %}
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/tracking",
        #     data={% if is_xml_api %}request.serialize(){% else %}lib.to_json(request.serialize()){% endif %},
        #     trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
        #     method="POST",
        #     headers={
        #         "Content-Type": {% if is_xml_api %}"application/xml"{% else %}"application/json"{% endif %},
        #         {% if is_xml_api %}"Authorization": f"Basic {self.settings.authorization}"{% else %}"Authorization": f"Bearer {self.settings.api_key}"{% endif %}
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        {% if is_xml_api %}response = '<r></r>'{% else %}response = lib.to_json({}){% endif %}

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "pickup" in features %}
    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/pickups",
        #     data={% if is_xml_api %}request.serialize(){% else %}lib.to_json(request.serialize()){% endif %},
        #     trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
        #     method="POST",
        #     headers={
        #         "Content-Type": {% if is_xml_api %}"application/xml"{% else %}"application/json"{% endif %},
        #         {% if is_xml_api %}"Authorization": f"Basic {self.settings.authorization}"{% else %}"Authorization": f"Bearer {self.settings.api_key}"{% endif %}
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        {% if is_xml_api %}response = '<r></r>'{% else %}response = lib.to_json({}){% endif %}

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "pickup" in features %}
    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/pickups/modify",
        #     data={% if is_xml_api %}request.serialize(){% else %}lib.to_json(request.serialize()){% endif %},
        #     trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
        #     method="POST",
        #     headers={
        #         "Content-Type": {% if is_xml_api %}"application/xml"{% else %}"application/json"{% endif %},
        #         {% if is_xml_api %}"Authorization": f"Basic {self.settings.authorization}"{% else %}"Authorization": f"Bearer {self.settings.api_key}"{% endif %}
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        {% if is_xml_api %}response = '<r></r>'{% else %}response = lib.to_json({}){% endif %}

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "pickup" in features %}
    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/pickups/cancel",
        #     data={% if is_xml_api %}request.serialize(){% else %}lib.to_json(request.serialize()){% endif %},
        #     trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
        #     method="POST",
        #     headers={
        #         "Content-Type": {% if is_xml_api %}"application/xml"{% else %}"application/json"{% endif %},
        #         {% if is_xml_api %}"Authorization": f"Basic {self.settings.authorization}"{% else %}"Authorization": f"Bearer {self.settings.api_key}"{% endif %}
        #     },
        # )

        # During development, use stub response from schema examples
        {% if is_xml_api %}response = '<r></r>'{% else %}response = lib.to_json({}){% endif %}

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "address" in features %}
    def validate_address(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/address/validate",
        #     data={% if is_xml_api %}request.serialize(){% else %}lib.to_json(request.serialize()){% endif %},
        #     trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
        #     method="POST",
        #     headers={
        #         "Content-Type": {% if is_xml_api %}"application/xml"{% else %}"application/json"{% endif %},
        #         {% if is_xml_api %}"Authorization": f"Basic {self.settings.authorization}"{% else %}"Authorization": f"Bearer {self.settings.api_key}"{% endif %}
        #     },
        # )

        # During development, use stub response from schema examples
        {% if is_xml_api %}response = '<r></r>'{% else %}response = lib.to_json({}){% endif %}

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "document" in features %}
    def upload_document(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/documents",
        #     data={% if is_xml_api %}request.serialize(){% else %}lib.to_json(request.serialize()){% endif %},
        #     trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
        #     method="POST",
        #     headers={
        #         "Content-Type": {% if is_xml_api %}"application/xml"{% else %}"application/json"{% endif %},
        #         {% if is_xml_api %}"Authorization": f"Basic {self.settings.authorization}"{% else %}"Authorization": f"Bearer {self.settings.api_key}"{% endif %}
        #     },
        # )

        # During development, use stub response from schema examples
        {% if is_xml_api %}response = '<r></r>'{% else %}response = lib.to_json({}){% endif %}

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "manifest" in features %}
    def create_manifest(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/manifests",
        #     data={% if is_xml_api %}request.serialize(){% else %}lib.to_json(request.serialize()){% endif %},
        #     trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
        #     method="POST",
        #     headers={
        #         "Content-Type": {% if is_xml_api %}"application/xml"{% else %}"application/json"{% endif %},
        #         {% if is_xml_api %}"Authorization": f"Basic {self.settings.authorization}"{% else %}"Authorization": f"Bearer {self.settings.api_key}"{% endif %}
        #     },
        # )

        # During development, use stub response from schema examples
        {% if is_xml_api %}response = '<r></r>'{% else %}response = lib.to_json({}){% endif %}

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}
'''
)

MAPPER_SETTINGS_TEMPLATE = Template('''"""Karrio {{name}} client settings."""

import attr
import karrio.providers.{{id}}.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """{{name}} connection settings."""

    # Add carrier specific API connection properties here
    {% if is_xml_api %}username: str
    password: str
    account_number: str = None{% else %}api_key: str
    account_number: str = None{% endif %}

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "{{id}}"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

'''
)

PROVIDER_IMPORTS_TEMPLATE = Template(
    '''"""Karrio {{name}} provider imports."""
from karrio.providers.{{id}}.utils import Settings{% if "rating" in features %}
from karrio.providers.{{id}}.rate import (
    parse_rate_response,
    rate_request,
){% endif %}{% if "shipping" in features %}
from karrio.providers.{{id}}.shipment import (
    parse_shipment_cancel_response,
    parse_shipment_response,
    shipment_cancel_request,
    shipment_request,
){% endif %}{% if "pickup" in features %}
from karrio.providers.{{id}}.pickup import (
    parse_pickup_cancel_response,
    parse_pickup_update_response,
    parse_pickup_response,
    pickup_update_request,
    pickup_cancel_request,
    pickup_request,
){% endif %}{% if "tracking" in features %}
from karrio.providers.{{id}}.tracking import (
    parse_tracking_response,
    tracking_request,
){% endif %}{% if "address" in features %}
from karrio.providers.{{id}}.address import (
    parse_address_validation_response,
    address_validation_request,
){% endif %}{% if "document" in features %}
from karrio.providers.{{id}}.document import (
    parse_document_upload_response,
    document_upload_request,
){% endif %}{% if "manifest" in features %}
from karrio.providers.{{id}}.manifest import (
    parse_manifest_response,
    manifest_request,
)
{% endif %}
'''
)

PROVIDER_ERROR_TEMPLATE = Template('''"""Karrio {{name}} error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.utils as provider_utils


def parse_error_response(
    response: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors: list = []  # compute the carrier error object list

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code="",
            message="",
            details={**kwargs},
        )
        for error in errors
    ]

'''
)

PROVIDER_UNITS_TEMPLATE = Template('''
import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """ Carrier specific packaging type """
    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingService(lib.StrEnum):
    """ Carrier specific services """
    {{id}}_standard_service = "{{name}} Standard Service"


class ShippingOption(lib.Enum):
    """ Carrier specific options """
    # {{id}}_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = {{id}}_coverage  #  maps unified karrio option to carrier specific

    pass


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]

'''
)

PROVIDER_UTILS_TEMPLATE = Template('''
import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """{{name}} connection settings."""

    # Add carrier specific api connection properties here
    {% if is_xml_api %}username: str
    password: str
    account_number: str = None{% else %}api_key: str
    account_number: str = None{% endif %}

    @property
    def carrier_name(self):
        return "{{id}}"

    @property
    def server_url(self):
        return (
            "https://carrier.api"
            if self.test_mode
            else "https://sandbox.carrier.api"
        )

    # """uncomment the following code block to expose a carrier tracking url."""
    # @property
    # def tracking_url(self):
    #     return "https://www.carrier.com/tracking?tracking-id={}"

    {% if is_xml_api %}@property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii"){% endif %}

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

#     """uncomment the following code block to implement the oauth login."""
#     @property
#     def access_token(self):
#         """Retrieve the access_token using the client_id|client_secret pair
#         or collect it from the cache if an unexpired access_token exist.
#         """
#         cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"
#         now = datetime.datetime.now() + datetime.timedelta(minutes=30)

#         auth = self.connection_cache.get(cache_key) or {}
#         token = auth.get("access_token")
#         expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

#         if token is not None and expiry is not None and expiry > now:
#             return token

#         self.connection_cache.set(cache_key, lambda: login(self))
#         new_auth = self.connection_cache.get(cache_key)

#         return new_auth["access_token"]

# """uncomment the following code block to implement the oauth login."""
# def login(settings: Settings):
#     import karrio.providers.{{id}}.error as error

#     result = lib.request(
#         url=f"{settings.server_url}/oauth/token",
#         method="POST",
#         headers={"content-Type": "application/x-www-form-urlencoded"},
#         data=lib.to_query_string(
#             dict(
#                 grant_type="client_credentials",
#                 client_id=settings.client_id,
#                 client_secret=settings.client_secret,
#             )
#         ),
#     )

#     response = lib.to_dict(result)
#     messages = error.parse_error_response(response, settings)

#     if any(messages):
#         raise errors.ParsedMessagesError(messages)

#     expiry = datetime.datetime.now() + datetime.timedelta(
#         seconds=float(response.get("expires_in", 0))
#     )
#     return {**response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, "PDF")  # Example of label type config with PDF default

'''
)


TEST_FIXTURE_TEMPLATE = Template(
    '''"""{{name}} carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["{{id}}"].create(
    dict(
        id="123456789",
        test_mode=True,
        carrier_id="{{id}}",
        account_number="123456789",
        {% if is_xml_api %}username="username",
        password="password",{% else %}api_key="TEST_API_KEY",{% endif %}
    )
)
'''
)

TEST_IMPORTS_TEMPLATE = Template(
    """{% if "rating" in features %}
from {{id}}.test_rate import *{% endif %}{% if "pickup" in features %}
from {{id}}.test_pickup import *{% endif %}{% if "address" in features %}
from {{id}}.test_address import *{% endif %}{% if "tracking" in features %}
from {{id}}.test_tracking import *{% endif %}{% if "shipping" in features %}
from {{id}}.test_shipment import *{% endif %}{% if "document" in features %}
from {{id}}.test_document import *{% endif %}{% if "manifest" in features %}
from {{id}}.test_manifest import *
{% endif %}
"""
)

TEST_PROVIDER_IMPORTS_TEMPLATE = Template(
    """from .fixture import gateway
"""
)

XML_SCHEMA_ERROR_TEMPLATE = Template(
    """<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/error" xmlns="http://{{id}}.com/ws/error" elementFormDefault="qualified">
    <xsd:element name="error-response">
        <xsd:complexType>
            <xsd:sequence>
                <xsd:element name="error" maxOccurs="unbounded">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="code" type="xsd:string" />
                            <xsd:element name="message" type="xsd:string" />
                            <xsd:element name="details" type="xsd:string" minOccurs="0" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
            </xsd:sequence>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

JSON_SCHEMA_ERROR_TEMPLATE = Template(
    """{
  "errorResponse": {
    "errors": [
      {
        "code": "ERROR_CODE",
        "message": "Error message description",
        "details": "Additional error details"
      }
    ]
  }
}
"""
)

VALIDATOR_IMPORTS_TEMPLATE = Template(
    """from karrio.validators.{{id}}.validator import Validator
"""
)

VALIDATOR_TEMPLATE = Template('''"""{{name}} address validator."""

import typing
import karrio.lib as lib
import karrio.api.validator as validator
import karrio.core.models as models
import karrio.providers.{{id}} as provider
from karrio.providers.{{id}}.utils import Settings


class Validator(validator.Validator):
    """{{name}} address validator."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def validate_address(self, payload: models.Address) -> models.AddressValidation:
        """
        Validate a shipping address using {{name}}'s API.

        Args:
            payload: The address to validate

        Returns:
            AddressValidation object with validation results
        """
        request = provider.address_validation_request(payload, self.settings)
        response = provider.validation_call(request, self.settings)
        result = provider.parse_address_validation_response(response, self.settings)

        return result
'''
)
