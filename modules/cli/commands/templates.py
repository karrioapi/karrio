from jinja2 import Template


EMPTY_FILE_TEMPLATE = Template("")


MODELS_TEMPLATE = Template(
    """
{% for name, cls in classes.items() %}
#### {{ name }}

| Name | Type | Description
| --- | --- | --- |
{% for prop in cls.__attrs_attrs__ %}| `{{ prop.name }}` | {{ prop.type }} | {{ '**required**' if str(prop.default) == 'NOTHING' else '' }}
{% endfor %}
{% endfor %}
"""
)

SETTINGS_TEMPLATE = Template(
    """
{% for k, val in settings.items() %}
#### {{ val['label'] }} Settings `[carrier_name = {{k}}]`

| Name | Type | Description
| --- | --- | --- |
{% for prop in val['Settings'].__attrs_attrs__ %}| `{{ prop.name }}` | {{ prop.type }} | {{ '**required**' if str(prop.default) == 'NOTHING' else '' }}
{% endfor %}
{% endfor %}
"""
)

SERVICES_TEMPLATE = Template(
    """
{% for key, value in service_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Identifier
| --- | ---
{% for code, name in value.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}
"""
)

SHIPMENT_OPTIONS_TEMPLATE = Template(
    """
{% for key, value in option_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Identifier | Description
| --- | --- | ---
{% for code, spec in value.items() %}| `{{ code }}` | {{ spec.get('key') }} | {{ spec.get('type') }}
{% endfor %}
{% endfor %}
"""
)

PACKAGING_TYPES_TEMPLATE = Template(
    """
{% for key, value in packaging_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Identifier
| --- | ---
{% for code, name in value.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}
"""
)

SHIPMENT_PRESETS_TEMPLATE = Template(
    """
{% for key, value in preset_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Dimensions | Note
| --- | --- | ---
{% for code, dim in value.items() %}{{ format_dimension(code, dim) }}
{% endfor %}
{% endfor %}
"""
)

UTILS_TOOLS_TEMPLATE = Template(
    """
{% for tool, import in utils %}
- `{{ tool.__name__ }}`

Usage:
```python
{{ import }}
```

```text
{{ doc(tool) }}
```

{% endfor %}
"""
)

COUNTRY_INFO_TEMPLATES = Template(
    """
## Countries

| Code | Name
| --- | ---
{% for code, name in countries.items() %}| `{{ code }}` | {{ name }}
{% endfor %}

## States and Provinces

{% for country, states in country_states.items() %}

### {{ countries[country] }}

| Code | Name
| --- | ---
{% for code, name in states.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}

## Currencies

| Code | Name
| --- | ---
{% for code, name in currencies.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
"""
)

UNITS_TEMPLATES = Template(
    """
## WEIGHT UNITS

| Code | Identifier
| --- | ---
{% for code, name in weight_units.items() %}| `{{ code }}` | {{ name }}
{% endfor %}

## DIMENSION UNITS

| Code | Identifier
| --- | ---
{% for code, name in dimension_units.items() %}| `{{ code }}` | {{ name }}
{% endfor %}

"""
)

"""CARRIER EXTENSTION TEMPLATES SECTION"""

README_TEMPLATE = Template(
    """
# karrio.{{id}}

This package is a {{name}} extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.{{id}}
```

## Usage

```python
import karrio
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

SETUP_TEMPLATE = Template(
    '''
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

XML_GENERATE_TEMPLATE = Template(
    """SCHEMAS=./schemas
LIB_MODULES=./karrio/schemas/{{id}}
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \\;
touch "${LIB_MODULES}/__init__.py"


generateDS --no-namespace-defs -o "${LIB_MODULES}/error.py" $SCHEMAS/error.xsd

"""
)

JSON_GENERATE_TEMPLATE = Template(
    """SCHEMAS=./schemas
LIB_MODULES=./karrio/schemas/{{id}}
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \\;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it --rm --name quicktype -v $PWD:/app-e SCHEMAS=/app/schemas -e LIB_MODULES=/app/karrio/schemas/{{id}} \\
    karrio/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums --src-lang json --lang jstruct \\
    --no-nice-property-names --all-properties-optional --type-as-suffix $@
}

quicktype --src="${SCHEMAS}/error.json" --out="${LIB_MODULES}/error.py"

"""
)

MAPPER_METADATA_TEMPLATE = Template(
    """
from karrio.core.metadata import Metadata

from karrio.mappers.{{id}}.mapper import Mapper
from karrio.mappers.{{id}}.proxy import Proxy
from karrio.mappers.{{id}}.settings import Settings
import karrio.providers.{{id}}.units as units


METADATA = Metadata(
    id="{{id}}",
    label="{{name}}",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False
)

"""
)

MAPPER_TEMPLATE = Template(
    '''
"""Karrio {{name}} client mapper."""

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
    {% endif %}

'''
)

MAPPER_PROXY_TEMPLATE = Template(
    '''
"""Karrio {{name}} client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.{{id}}.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings{% if "rating" in features %}

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=request.serialize(),
            trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "shipping" in features %}
    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=request.serialize(),
            trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "shipping" in features %}
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=request.serialize(),
            trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "tracking" in features %}
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=request.serialize(),
            trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "pickup" in features %}
    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=request.serialize(),
            trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "pickup" in features %}
    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=request.serialize(),
            trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "pickup" in features %}
    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=request.serialize(),
            trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "document" in features %}
    def upload_document(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=request.serialize(),
            trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}{% if "manifest" in features %}
    def create_manifest(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=request.serialize(),
            trace=self.trace_as({% if is_xml_api %}"xml"{% else %}"json"{% endif %}),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, {% if is_xml_api %}lib.to_element{% else %}lib.to_dict{% endif %})
    {% endif %}
'''
)

MAPPER_SETTINGS_TEMPLATE = Template(
    '''
"""Karrio {{name}} client settings."""

import attr
import karrio.providers.{{id}}.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """{{name}} connection settings."""

    # required carrier specific properties

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
    """
from karrio.providers.{{id}}.utils import Settings{% if "rating" in features %}
from karrio.providers.{{id}}.rate import parse_rate_response, rate_request{% endif %}{% if "shipping" in features %}
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
){% endif %}{% if "document" in features %}
from karrio.providers.{{id}}.document import (
    parse_document_upload_response,
    document_upload_request,
){% endif %}{% if "manifest" in features %}
from karrio.providers.{{id}}.manifest import (
    parse_manifest_response,
    create_manifest_request,
){% endif %}

"""
)

PROVIDER_ERROR_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.utils as provider_utils


def parse_error_response(
    response: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors = []  # compute the carrier error object list

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

"""
)

PROVIDER_RATE_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [_extract_details(rate, settings) for rate in response]

    return rates, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = None  # parse carrier rate type

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service="",  # extract service from rate
        total_charge=0.0,  # extract the rate total rate cost
        currency="",  # extract the rate pricing currency
        transit_days=0,  # extract the rate transit days
        meta=dict(
            service_name="",  # extract the rate service human readable name
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    packages = lib.to_packages(payload.parcels)  # preprocess the request parcels
    services = lib.to_services(payload.services, provider_units.ShippingService)  # preprocess the request services
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
    )   # preprocess the request options

    request = None  # map data to convert karrio model to {{id}} specific type

    return lib.Serializable(request)

"""
)

PROVIDER_TRACKING_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, {% if is_xml_api %}lib.Element{% else %}dict{% endif %}]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
        ],
        start=[],
    )
    tracking_details = [_extract_details(details, settings) for _, details in responses]

    return tracking_details, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking = None  # parse carrier tracking object type

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="",  # extract tracking number from tracking
        events=[
            models.TrackingEvent(
                date=lib.fdate(""), # extract tracking event date
                description="",  # extract tracking event description or code
                code="",  # extract tracking event code
                time=lib.ftime(""), # extract tracking event time
                location="",  # extract tracking event address
            )
            for event in []  # extract tracking events
        ],
        estimated_delivery=lib.fdate(""), # extract tracking estimated date if provided
        delivered=False,  # compute tracking delivered status
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = None  # map data to convert karrio model to {{id}} specific type

    return lib.Serializable(request)

"""
)

PROVIDER_UNITS_TEMPLATE = Template(
    '''
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

PROVIDER_UTILS_TEMPLATE = Template(
    '''
import karrio.core as core


class Settings(core.Settings):
    """{{name}} connection settings."""

    # username: str  # carrier specific api credential key

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

'''
)

PROVIDER_ADDRESS_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_address_validation_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.AddressValidationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = True  # compute address validation success state

    validation_details = (
        models.AddressValidationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
        )
        if success else None
    )

    return validation_details, messages


def address_validation_request(
    payload: models.AddressValidationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[lib.Envelope]:

    request = None  # map data to convert karrio model to {{id}} specific type

    return lib.Serializable(request)

"""
)

PROVIDER_SHIPMENT_IMPORTS_TEMPLATE = Template(
    """
from karrio.providers.{{id}}.shipment.create import (
    parse_shipment_response,
    shipment_request,
)
from karrio.providers.{{id}}.shipment.cancel import (
    parse_shipment_cancel_response,
    shipment_cancel_request,
)

"""
)

PROVIDER_SHIPMENT_CANCEL_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = True  # compute shipment cancel success state

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        ) if success else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    request = None  # map data to convert karrio model to {{id}} specific type

    return lib.Serializable(request)

"""
)

PROVIDER_SHIPMENT_CREATE_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings)
        if "tracking_number" in response
        else None
    )

    return shipment, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = None  # parse carrier shipment type from "data"
    label = ""  # extract and process the shipment label to a valid base64 text
    # invoice = ""  # extract and process the shipment invoice to a valid base64 text if applies

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="",  # extract tracking number from shipment
        shipment_identifier="",  # extract shipment identifier from shipment
        label_type="PDF",  # extract shipment label file format
        docs=models.Documents(
            label=label,  # pass label base64 text
            # invoice=invoice,  # pass invoice base64 text if applies
        ),
        meta=dict(
            # any relevent meta
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    packages = lib.to_packages(payload.parcels)  # preprocess the request parcels
    service = provider_units.ShippingService.map(payload.service).value_or_key  # preprocess the request services
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
    )   # preprocess the request options

    request = None  # map data to convert karrio model to {{id}} specific type

    return lib.Serializable(request)

"""
)

PROVIDER_DOCUMENT_UPLOAD_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_document_upload_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.DocumentUploadDetails:
    documents = []  # documents ids and name extraction

    return models.DocumentUploadDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        documents=[
            models.DocumentDetails(
                document_id="doc_id",
                file_name="file_name",
            )
            for doc in documents
        ],
        meta=dict(),
    )


def document_upload_request(
    payload: models.DocumentUploadRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    request = None  # map data to convert karrio model to {{id}} specific type

    return lib.Serializable(request)

"""
)

PROVIDER_MANIFEST_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_manifest_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.ManifestDetails:
    details = None  # manifest details parsing
    manifest = None  # extract carrier manifest file

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        doc=models.ManifestDocument(manifest=manifest),
        meta=dict(),
    )


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    request = None  # map data to convert karrio model to {{id}} specific type

    return lib.Serializable(request)

"""
)

PROVIDER_PICKUP_IMPORTS_TEMPLATE = Template(
    """
from karrio.providers.{{id}}.pickup.create import parse_pickup_response, pickup_request
from karrio.providers.{{id}}.pickup.update import parse_pickup_update_response, pickup_update_request
from karrio.providers.{{id}}.pickup.cancel import parse_pickup_cancel_response, pickup_cancel_request

"""
)

PROVIDER_PICKUP_CANCEL_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_pickup_cancel_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = True  # compute address validation success state

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Pickup",
            success=success,
        ) if success else None
    )

    return confirmation, messages


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    request = None  # map data to convert karrio model to {{id}} specific type

    return lib.Serializable(request)

"""
)

PROVIDER_PICKUP_CREATE_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_pickup_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    pickup = (
        _extract_details(response, settings)
        if "confirmation_number" in response
        else None
    )

    return pickup, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    pickup = None  # parse carrier pickup type from "data"

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number="",  # extract confirmation number from pickup
        pickup_date=lib.fdate(""), # extract tracking event date
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings
) -> lib.Serializable:
    request = None  # map data to convert karrio model to {{id}} specific type

    return lib.Serializable(request)

"""
)

PROVIDER_PICKUP_UPDATE_TEMPLATE = Template(
    """
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_pickup_update_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    pickup = (
        _extract_details(response, settings)
        if "confirmation_number" in response
        else None
    )

    return pickup, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    pickup = None  # parse carrier pickup type from "data"

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number="",  # extract confirmation number from pickup
        pickup_date=lib.fdate(""), # extract tracking event date
    )


def pickup_update_request(
    payload: models.PickupUpdateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = None  # map data to convert karrio model to {{id}} specific type

    return lib.Serializable(request)

"""
)


TEST_IMPORTS_TEMPLATE = Template(
    """{% if "rating" in features %}
from tests.{{id}}.test_rate import *{% endif %}{% if "pickup" in features %}
from tests.{{id}}.test_pickup import *{% endif %}{% if "address" in features %}
from tests.{{id}}.test_address import *{% endif %}{% if "tracking" in features %}
from tests.{{id}}.test_tracking import *{% endif %}{% if "shipping" in features %}
from tests.{{id}}.test_shipment import *{% endif %}{% if "document" in features %}
from tests.{{id}}.test_document import *{% endif %}{% if "manifest" in features %}
from tests.{{id}}.test_manifest import *
{% endif %}
"""
)

TEST_PROVIDER_IMPORTS_TEMPLATE = Template("")

TEST_FIXTURE_TEMPLATE = Template(
    """
import karrio

gateway = karrio.gateway["{{id}}"].create(
    dict(
        # add required carrier API setting key/value here
    )
)

"""
)

XML_SCHEMA_TEMPLATE = Template(
    """<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://targetNamespace" xmlns="http://xmlns" elementFormDefault="qualified">
</xsd:schema>

"""
)

JSON_SCHEMA_TEMPLATE = Template(
    """{}
"""
)

TEST_RATE_TEMPLATE = Template(
    '''
import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}Rating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{% if is_xml_api %}<a></a>{% else %}{}{% endif %}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {}

ParsedRateResponse = []


RateRequest = {% if is_xml_api %}"""<a></a>
"""{% else %}{}{% endif %}

RateResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

'''
)

TEST_TRACKING_TEMPLATE = Template(
    '''
import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}Tracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{% if is_xml_api %}<a></a>{% else %}{}{% endif %}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedTrackingResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedErrorResponse
            )


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["89108749065090"],
}

ParsedTrackingResponse = []

ParsedErrorResponse = []


TrackingRequest = {% if is_xml_api %}"""<a></a>
"""{% else %}{}{% endif %}

TrackingResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

ErrorResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

'''
)

TEST_SHIPMENT_TEMPLATE = Template(
    '''
import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}Shipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{% if is_xml_api %}<a></a>{% else %}{}{% endif %}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{% if is_xml_api %}<a></a>{% else %}{}{% endif %}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = []

ParsedCancelShipmentResponse = []


ShipmentRequest = {% if is_xml_api %}"""<a></a>
"""{% else %}{}{% endif %}

ShipmentCancelRequest = {% if is_xml_api %}"""<a></a>
"""{% else %}{}{% endif %}

ShipmentResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

ShipmentCancelResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

'''
)

TEST_DOCUMENT_UPLOAD_TEMPLATE = Template(
    '''
import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}DocumentUpload(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.DocumentUploadRequest = models.DocumentUploadRequest(**DocumentUploadPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_document_upload_request(
            self.DocumentUploadRequest
        )

        self.assertEqual(request.serialize(), DocumentUploadRequest)

    def test_upload_document(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{% if is_xml_api %}<a></a>{% else %}{}{% endif %}"
            karrio.Document.upload(self.DocumentUploadRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_document_upload_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = DocumentUploadResponse
            parsed_response = (
                karrio.Document.upload(self.DocumentUploadRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedDocumentUploadResponse
            )


if __name__ == "__main__":
    unittest.main()


DocumentUploadPayload = {
    "document_files": [
        {
            "doc_format": "txt",
            "doc_name": "TestFile.txt",
            "doc_type": "other",
            "doc_file": "R0lGODdhIAOwBPAAAA==",
        }
    ],
}

ParsedDocumentUploadResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "carrier_id",
        "documents": [
            {
                "document_id": "090493e1815c194e",
                "file_name": "TestFile.txt",
            }
        ],
        "meta": {},
    },
    [],
]


DocumentUploadRequest = {% if is_xml_api %}"""<a></a>
"""{% else %}{}{% endif %}

DocumentUploadResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

'''
)

TEST_MANIFEST_TEMPLATE = Template(
    '''
import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}Manifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(**ManifestPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_manifest_request(
            self.ManifestRequest
        )

        self.assertEqual(request.serialize(), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{% if is_xml_api %}<a></a>{% else %}{}{% endif %}"
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ManifestResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedManifestResponse
            )


if __name__ == "__main__":
    unittest.main()


ManifestPayload = {
    "shipment_identifiers": ["794947717776"],
    "address": {
        "city": "Los Angeles",
        "state_code": "CA",
        "postal_code": "90001",
        "country_code": "US",
    },
    "options": {},
}

ParsedManifestResponse = [
    {
        "carrier_id": "{{id}}",
        "carrier_name": "{{id}}",
        "doc": {"manifest": ANY},
        "meta": {},
    },
    [],
]


ManifestRequest = {% if is_xml_api %}"""<a></a>
"""{% else %}{}{% endif %}

ManifestResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

'''
)

TEST_PICKUP_TEMPLATE = Template(
    '''
import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}Pickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**PickupPayload)
        self.PickupUpdateRequest = models.PickupUpdateRequest(**PickupUpdatePayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)

        self.assertEqual(request.serialize(), PickupRequest)

    def test_create_update_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)

        self.assertEqual(request.serialize(), PickupUpdateRequest)

    def test_create_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(
            self.PickupCancelRequest
        )

        self.assertEqual(request.serialize(), PickupCancelRequest)

    def test_create_pickup(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{% if is_xml_api %}<a></a>{% else %}{}{% endif %}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{% if is_xml_api %}<a></a>{% else %}{}{% endif %}"
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{% if is_xml_api %}<a></a>{% else %}{}{% endif %}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ""
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelPickupResponse
            )


if __name__ == "__main__":
    unittest.main()


PickupPayload = {}

PickupUpdatePayload = {}

PickupCancelPayload = {"confirmation_number": "0074698052"}

ParsedPickupResponse = []

ParsedCancelPickupResponse = []


PickupRequest = {% if is_xml_api %}"""<a></a>
"""{% else %}{}{% endif %}

PickupUpdateRequest = {% if is_xml_api %}"""<a></a>
"""{% else %}{}{% endif %}

PickupCancelRequest = {% if is_xml_api %}"""<a></a>
"""{% else %}{}{% endif %}


PickupResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

PickupUpdateResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

PickupCancelResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

'''
)

TEST_ADDRESS_TEMPLATE = Template(
    '''
import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}Rating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = models.AddressValidationRequest(**AddressValidationPayload)

    def test_create_AddressValidation_request(self):
        request = gateway.mapper.create_address_validation_request(
            self.AddressValidationRequest
        )

        self.assertEqual(request.serialize(), AddressValidationRequest)

    def test_validate_address(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{% if is_xml_api %}<a></a>{% else %}{}{% endif %}"
            karrio.Address.validate(self.AddressValidationRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_address_validation_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = AddressValidationResponse
            parsed_response = karrio.Address.validate(self.RateRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedAddressValidationResponse)


if __name__ == "__main__":
    unittest.main()


AddressValidationPayload = {}

ParsedAddressValidationResponse = []


AddressValidationRequest = {% if is_xml_api %}"""<a></a>
"""{% else %}{}{% endif %}

AddressValidationResponse = """{% if is_xml_api %}<a></a>{% else %}{}{% endif %}
"""

'''
)
