from jinja2 import Template

PROVIDER_ADDRESS_TEMPLATE = Template(
    '''"""Karrio {{name}} address validation API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract address validation details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., AddressValidationRequestType),
# while XML schema types don't have this suffix (e.g., AddressValidationRequest).

import karrio.schemas.{{id}}.address_validation_request as {{id}}_req
import karrio.schemas.{{id}}.address_validation_response as {{id}}_res

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

    validation_details = models.AddressValidationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=True,
    )

    return validation_details, messages


def address_validation_request(
    payload: models.AddressValidationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create an address validation request for the carrier API

    payload: The standardized AddressValidationRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Extract the address from payload
    address = lib.to_address(payload.address)

    {% if is_xml_api %}
    # For XML API request
    request = {{id}}_req.AddressValidationRequest(
        street=address.address_line1,
        city_name=address.city,
        postcode=address.postal_code,
        country_code=address.country_code,
        province_code=address.state_code,
    )
    {% else %}
    # For JSON API request - Using camelCase attribute names to match schema definition
    request = {{id}}_req.AddressValidationRequestType(
        streetAddress=address.address_line1,
        cityLocality=address.city,
        postalCode=address.postal_code,
        countryCode=address.country_code,
        stateProvince=address.state_code,
    )
    {% endif %}

    return lib.Serializable(request, {% if is_xml_api %}lib.to_xml{% else %}lib.to_dict{% endif %})
'''
)

JSON_SCHEMA_ADDRESS_VALIDATION_REQUEST_TEMPLATE = Template('''
{
  "streetAddress": "123 Main St",
  "cityLocality": "City Name",
  "postalCode": "12345",
  "countryCode": "US",
  "stateProvince": "CA"
}
''')

JSON_SCHEMA_ADDRESS_VALIDATION_RESPONSE_TEMPLATE = Template('''
{
  "isValid": true,
  "normalizedAddress": {
    "streetAddress": "123 Main St",
    "cityLocality": "City Name",
    "postalCode": "12345",
    "countryCode": "US",
    "stateProvince": "CA"
  },
  "validationMessages": [
    {
      "message": "Address is valid",
      "code": "SUCCESS"
    }
  ]
}
''')

XML_SCHEMA_ADDRESS_VALIDATION_REQUEST_TEMPLATE = Template('''<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/address" xmlns="http://{{id}}.com/ws/address" elementFormDefault="qualified">
    <xsd:element name="address-validation-request">
        <xsd:complexType>
            <xsd:sequence>
                <xsd:element name="street" type="xsd:string" />
                <xsd:element name="city_name" type="xsd:string" />
                <xsd:element name="postcode" type="xsd:string" />
                <xsd:element name="country_code" type="xsd:string" />
                <xsd:element name="province_code" type="xsd:string" minOccurs="0" />
            </xsd:sequence>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
''')

XML_SCHEMA_ADDRESS_VALIDATION_RESPONSE_TEMPLATE = Template('''<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/address" xmlns="http://{{id}}.com/ws/address" elementFormDefault="qualified">
    <xsd:element name="address-validation-response">
        <xsd:complexType>
            <xsd:sequence>
                <xsd:element name="valid_address" type="xsd:string" />
                <xsd:element name="normalized_address" minOccurs="0">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="street" type="xsd:string" />
                            <xsd:element name="city_name" type="xsd:string" />
                            <xsd:element name="postcode" type="xsd:string" />
                            <xsd:element name="country_code" type="xsd:string" />
                            <xsd:element name="province_code" type="xsd:string" minOccurs="0" />
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="validation_messages" minOccurs="0">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="message" maxOccurs="unbounded">
                                <xsd:complexType>
                                    <xsd:sequence>
                                        <xsd:element name="text" type="xsd:string" />
                                        <xsd:element name="code" type="xsd:string" />
                                    </xsd:sequence>
                                </xsd:complexType>
                            </xsd:element>
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
            </xsd:sequence>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
''')

TEST_ADDRESS_TEMPLATE = Template('''"""{{name}} carrier address validation tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)

class Test{{compact_name}}Address(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = models.AddressValidationRequest(**AddressValidationPayload)

    def test_create_address_validation_request(self):
        request = gateway.mapper.create_address_validation_request(self.AddressValidationRequest)
        self.assertEqual(lib.to_dict(request.serialize()), AddressValidationRequest)

    def test_validate_address(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Address.validate(self.AddressValidationRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/address/validate"
            )

    def test_parse_address_validation_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = AddressValidationResponse
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedAddressValidationResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


AddressValidationPayload = {
    "address": {
        "address_line1": "123 Main St",
        "city": "City Name",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
    }
}

AddressValidationRequest = {% if is_xml_api %}"""<?xml version="1.0"?>
<address-validation-request>
    <street>123 Main St</street>
    <city_name>City Name</city_name>
    <postcode>12345</postcode>
    <country_code>US</country_code>
    <province_code>CA</province_code>
</address-validation-request>"""{% else %}{
  "streetAddress": "123 Main St",
  "cityLocality": "City Name",
  "postalCode": "12345",
  "countryCode": "US",
  "stateProvince": "CA"
}{% endif %}

AddressValidationResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<address-validation-response>
    <valid_address>true</valid_address>
    <normalized_address>
        <street>123 MAIN ST</street>
        <city_name>CITY NAME</city_name>
        <postcode>12345</postcode>
        <country_code>US</country_code>
        <province_code>CA</province_code>
    </normalized_address>
</address-validation-response>"""{% else %}"""{
  "isValid": true,
  "normalizedAddress": {
    "streetAddress": "123 MAIN ST",
    "cityLocality": "CITY NAME",
    "postalCode": "12345",
    "countryCode": "US",
    "stateProvince": "CA"
  },
  "validationMessages": [
    {
      "message": "Address is valid",
      "code": "SUCCESS"
    }
  ]
}"""{% endif %}

ErrorResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<error-response>
    <e>
        <code>address_error</code>
        <message>Unable to validate address</message>
        <details>Invalid address information provided</details>
    </e>
</error-response>"""{% else %}"""{
  "error": {
    "code": "address_error",
    "message": "Unable to validate address",
    "details": "Invalid address information provided"
  }
}"""{% endif %}

ParsedAddressValidationResponse = [
    {
        "carrier_id": "{{id}}",
        "carrier_name": "{{id}}",
        "success": True
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "code": "address_error",
            "message": "Unable to validate address",
            "details": {
                "details": "Invalid address information provided"
            }
        }
    ]
]''')
