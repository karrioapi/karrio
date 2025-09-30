from jinja2 import Template

PROVIDER_RATE_TEMPLATE = Template('''"""Karrio {{name}} rate API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract data from the response to populate the RateDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., RateRequestType),
# while XML schema types don't have this suffix (e.g., RateRequest).

import karrio.schemas.{{id}}.rate_request as {{id}}_req
import karrio.schemas.{{id}}.rate_response as {{id}}_res

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

    # Extract rate objects from the response - adjust based on carrier API structure
    {% if is_xml_api %}
    # For XML APIs, find the path to rate elements
    rate_elements = response.xpath(".//rate") if hasattr(response, 'xpath') else []
    rates = [_extract_details(rate, settings) for rate in rate_elements]
    {% else %}
    # For JSON APIs, find the path to rate objects
    rate_objects = response.get("rates", []) if hasattr(response, 'get') else []
    rates = [_extract_details(rate, settings) for rate in rate_objects]
    {% endif %}

    return rates, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """
    Extract rate details from carrier response data

    data: The carrier-specific rate data structure
    settings: The carrier connection settings

    Returns a RateDetails object with extracted rate information
    """
    # Convert the carrier data to a proper object for easy attribute access
    {% if is_xml_api %}
    # For XML APIs, convert Element to proper response object
    rate = lib.to_object({{id}}_res.Rate, data)

    # Now access data through the object attributes
    service = rate.service_code
    service_name = rate.service_name
    total = float(rate.total_charge) if hasattr(rate, 'total_charge') and rate.total_charge else 0.0
    currency = rate.currency or "USD"
    transit_days = int(rate.transit_days) if hasattr(rate, 'transit_days') and rate.transit_days else 0
    {% else %}
    # For JSON APIs, convert dict to proper response object
    rate = lib.to_object({{id}}_res.RateResponseType, data)

    # Now access data through the object attributes
    service = rate.serviceCode if hasattr(rate, 'serviceCode') else ""
    service_name = rate.serviceName if hasattr(rate, 'serviceName') else ""
    total = float(rate.totalCharge) if hasattr(rate, 'totalCharge') and rate.totalCharge else 0.0
    currency = rate.currency if hasattr(rate, 'currency') else "USD"
    transit_days = int(rate.transitDays) if hasattr(rate, 'transitDays') and rate.transitDays else 0
    {% endif %}

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service,
        total_charge=lib.to_money(total, currency),
        currency=currency,
        transit_days=transit_days,
        meta=dict(
            service_name=service_name,
            # Add any other useful metadata from the carrier response
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a rate request for the carrier API

    payload: The standardized RateRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Create the carrier-specific request object
    {% if is_xml_api %}
    # For XML API request
    request = {{id}}_req.RateRequest(
        # Map shipper details
        shipper={{id}}_req.Address(
            address_line1=shipper.address_line1,
            city=shipper.city,
            postal_code=shipper.postal_code,
            country_code=shipper.country_code,
            state_code=shipper.state_code,
            person_name=shipper.person_name,
            company_name=shipper.company_name,
            phone_number=shipper.phone_number,
            email=shipper.email,
        ),
        # Map recipient details
        recipient={{id}}_req.Address(
            address_line1=recipient.address_line1,
            city=recipient.city,
            postal_code=recipient.postal_code,
            country_code=recipient.country_code,
            state_code=recipient.state_code,
            person_name=recipient.person_name,
            company_name=recipient.company_name,
            phone_number=recipient.phone_number,
            email=recipient.email,
        ),
        # Map package details
        packages=[
            {{id}}_req.Package(
                weight=package.weight.value,
                weight_unit=provider_units.WeightUnit[package.weight.unit].value,
                length=package.length.value if package.length else None,
                width=package.width.value if package.width else None,
                height=package.height.value if package.height else None,
                dimension_unit=provider_units.DimensionUnit[package.dimension_unit].value if package.dimension_unit else None,
                packaging_type=provider_units.PackagingType[package.packaging_type or 'your_packaging'].value,
            )
            for package in packages
        ],
        # Map service codes if specified
        services=[s.value_or_key for s in services] if services else None,
        # Add customer number and other account details
        customer_number=settings.customer_number,
        # Add any other required fields for this carrier's API
    )
    {% else %}
    # For JSON API request
    request = {{id}}_req.RateRequestType(
        # Map shipper details
        shipper={
            "addressLine1": shipper.address_line1,
            "city": shipper.city,
            "postalCode": shipper.postal_code,
            "countryCode": shipper.country_code,
            "stateCode": shipper.state_code,
            "personName": shipper.person_name,
            "companyName": shipper.company_name,
            "phoneNumber": shipper.phone_number,
            "email": shipper.email,
        },
        # Map recipient details
        recipient={
            "addressLine1": recipient.address_line1,
            "city": recipient.city,
            "postalCode": recipient.postal_code,
            "countryCode": recipient.country_code,
            "stateCode": recipient.state_code,
            "personName": recipient.person_name,
            "companyName": recipient.company_name,
            "phoneNumber": recipient.phone_number,
            "email": recipient.email,
        },
        # Map package details
        packages=[
            {
                "weight": package.weight.value,
                "weightUnit": provider_units.WeightUnit[package.weight.unit].value,
                "length": package.length.value if package.length else None,
                "width": package.width.value if package.width else None,
                "height": package.height.value if package.height else None,
                "dimensionUnit": provider_units.DimensionUnit[package.dimension_unit].value if package.dimension_unit else None,
                "packagingType": provider_units.PackagingType[package.packaging_type or 'your_packaging'].value,
            }
            for package in packages
        ],
        # Add service code
        serviceCode=service,
        # Add account information
        customerNumber=settings.customer_number,
        # Add label details
        labelFormat=payload.label_type or "PDF",
        # Add any other required fields for the carrier API
    )
    {% endif %}

    return lib.Serializable(request, {% if is_xml_api %}lib.to_xml{% else %}lib.to_dict{% endif %})

'''
)


TEST_RATE_TEMPLATE = Template('''"""{{name}} carrier rate tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class Test{{compact_name}}Rating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rates"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "parcels": [{
        "weight": 10.0,
        "width": 10.0,
        "height": 10.0,
        "length": 10.0,
        "weight_unit": "KG",
        "dimension_unit": "CM",
        "packaging_type": "BOX"
    }]
}

RateRequest = {% if is_xml_api %}{
    "shipper": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "packages": [
        {
            "weight": 10.0,
            "weight_unit": "KG",
            "length": 10.0,
            "width": 10.0,
            "height": 10.0,
            "dimension_unit": "CM",
            "packaging_type": "BOX"
        }
    ]
}{% else %}{
    "shipper": {
        "addressLine1": "123 Test Street",
        "city": "Test City",
        "postalCode": "12345",
        "countryCode": "US",
        "stateCode": "CA",
        "personName": "Test Person",
        "companyName": "Test Company",
        "phoneNumber": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "addressLine1": "123 Test Street",
        "city": "Test City",
        "postalCode": "12345",
        "countryCode": "US",
        "stateCode": "CA",
        "personName": "Test Person",
        "companyName": "Test Company",
        "phoneNumber": "1234567890",
        "email": "test@example.com"
    },
    "packages": [
        {
            "weight": 10.0,
            "weightUnit": "KG",
            "length": 10.0,
            "width": 10.0,
            "height": 10.0,
            "dimensionUnit": "CM",
            "packagingType": "BOX"
        }
    ]
}{% endif %}

RateResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<rate-response>
    <rate>
        <service-code>express</service-code>
        <service-name>Express Service</service-name>
        <total-charge>25.99</total-charge>
        <currency>USD</currency>
        <transit-days>2</transit-days>
    </rate>
    <rate>
        <service-code>ground</service-code>
        <service-name>Ground Service</service-name>
        <total-charge>12.99</total-charge>
        <currency>USD</currency>
        <transit-days>5</transit-days>
    </rate>
</rate-response>"""{% else %}"""{
  "rates": [
    {
      "serviceCode": "express",
      "serviceName": "Express Service",
      "totalCharge": 25.99,
      "currency": "USD",
      "transitDays": 2
    },
    {
      "serviceCode": "ground",
      "serviceName": "Ground Service",
      "totalCharge": 12.99,
      "currency": "USD",
      "transitDays": 5
    }
  ]
}"""{% endif %}

ErrorResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<error-response>
    <e>
        <code>rate_error</code>
        <message>Unable to get rates</message>
        <details>Invalid address provided</details>
    <e>
</error-response>"""{% else %}"""{
  "error": {
    "code": "rate_error",
    "message": "Unable to get rates",
    "details": "Invalid address provided"
  }
}"""{% endif %}

ParsedRateResponse = [
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "service": "express",
            "currency": "USD",
            "total_charge": 25.99,
            "transit_days": 2,
            "meta": {
                "service_name": "Express Service"
            }
        },
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "service": "ground",
            "currency": "USD",
            "total_charge": 12.99,
            "transit_days": 5,
            "meta": {
                "service_name": "Ground Service"
            }
        }
    ],
    []
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "code": "rate_error",
            "message": "Unable to get rates",
            "details": {
                "details": "Invalid address provided"
            }
        }
    ]
]
'''
)

XML_SCHEMA_RATE_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/rate" xmlns="http://{{id}}.com/ws/rate" elementFormDefault="qualified">
    <xsd:element name="rate-request">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="shipper">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="address-line1" type="xsd:string" />
                            <xsd:element name="city" type="xsd:string" />
                            <xsd:element name="postal-code" type="xsd:string" />
                            <xsd:element name="country-code" type="xsd:string" />
                            <xsd:element name="state-code" type="xsd:string" minOccurs="0" />
                            <xsd:element name="person-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="company-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="phone-number" type="xsd:string" minOccurs="0" />
                            <xsd:element name="email" type="xsd:string" minOccurs="0" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="recipient">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="address-line1" type="xsd:string" />
                            <xsd:element name="city" type="xsd:string" />
                            <xsd:element name="postal-code" type="xsd:string" />
                            <xsd:element name="country-code" type="xsd:string" />
                            <xsd:element name="state-code" type="xsd:string" minOccurs="0" />
                            <xsd:element name="person-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="company-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="phone-number" type="xsd:string" minOccurs="0" />
                            <xsd:element name="email" type="xsd:string" minOccurs="0" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="packages">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="package" maxOccurs="unbounded">
                                <xsd:complexType>
                                    <xsd:all>
                                        <xsd:element name="weight" type="xsd:decimal" />
                                        <xsd:element name="weight-unit" type="xsd:string" />
                                        <xsd:element name="length" type="xsd:decimal" minOccurs="0" />
                                        <xsd:element name="width" type="xsd:decimal" minOccurs="0" />
                                        <xsd:element name="height" type="xsd:decimal" minOccurs="0" />
                                        <xsd:element name="dimension-unit" type="xsd:string" minOccurs="0" />
                                        <xsd:element name="packaging-type" type="xsd:string" minOccurs="0" />
                                    </xsd:all>
                                </xsd:complexType>
                            </xsd:element>
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="services" minOccurs="0">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="service" type="xsd:string" maxOccurs="unbounded" />
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="options" type="xsd:string" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

XML_SCHEMA_RATE_RESPONSE_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/rate" xmlns="http://{{id}}.com/ws/rate" elementFormDefault="qualified">
    <xsd:element name="rate-response">
        <xsd:complexType>
            <xsd:sequence>
                <xsd:element name="rate" maxOccurs="unbounded">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="service-code" type="xsd:string" />
                            <xsd:element name="service-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="total-charge" type="xsd:decimal" />
                            <xsd:element name="currency" type="xsd:string" minOccurs="0" />
                            <xsd:element name="transit-days" type="xsd:integer" minOccurs="0" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
            </xsd:sequence>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

JSON_SCHEMA_RATE_REQUEST_TEMPLATE = Template(
    """{
  "rateRequest": {
    "shipper": {
      "addressLine1": "123 Main St",
      "city": "Anytown",
      "postalCode": "12345",
      "countryCode": "US",
      "stateCode": "CA",
      "personName": "John Doe",
      "companyName": "ACME Corp",
      "phoneNumber": "555-123-4567",
      "email": "john@example.com"
    },
    "recipient": {
      "addressLine1": "456 Oak St",
      "city": "Somewhere",
      "postalCode": "67890",
      "countryCode": "US",
      "stateCode": "NY",
      "personName": "Jane Smith",
      "companyName": "XYZ Inc",
      "phoneNumber": "555-987-6543",
      "email": "jane@example.com"
    },
    "packages": [
      {
        "weight": 10.5,
        "weightUnit": "KG",
        "length": 20.0,
        "width": 15.0,
        "height": 10.0,
        "dimensionUnit": "CM",
        "packagingType": "BOX"
      }
    ],
    "services": ["EXPRESS", "GROUND"],
    "options": {
      "insurance": true,
      "signature_required": false
    }
  }
}
"""
)

JSON_SCHEMA_RATE_RESPONSE_TEMPLATE = Template(
    """{
  "rateResponse": {
    "rates": [
      {
        "serviceCode": "EXPRESS",
        "serviceName": "Express Shipping",
        "totalCharge": 25.99,
        "currency": "USD",
        "transitDays": 2
      },
      {
        "serviceCode": "GROUND",
        "serviceName": "Ground Shipping",
        "totalCharge": 12.99,
        "currency": "USD",
        "transitDays": 5
      }
    ]
  }
}
"""
)
