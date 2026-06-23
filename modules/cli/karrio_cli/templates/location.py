from jinja2 import Template

PROVIDER_LOCATION_TEMPLATE = Template(
    '''"""Karrio {{name}} location finder API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract location details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., LocationRequestType),
# while XML schema types don't have this suffix (e.g., LocationRequest).

import karrio.schemas.{{id}}.location_request as {{id}}_req
import karrio.schemas.{{id}}.location_response as {{id}}_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_location_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.LocationDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract the carrier locations from the response and map each one with
    # `_extract_location`. The exact path depends on the carrier API shape.
    locations = [
        _extract_location(location, settings)
        for location in []  # e.g. response.get("locations", [])
    ]

    return locations, messages


def _extract_location(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.LocationDetails:
    """Map a single carrier location entry to a unified LocationDetails."""
    location = lib.to_object({{id}}_res.{% if is_xml_api %}Location{% else %}LocationType{% endif %}, data)

    return models.LocationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        location_id=None,
        location_type=None,  # depot, parcel_shop, locker, pickup_point, ...
        name=None,
        address=None,
        latitude=None,
        longitude=None,
        distance=None,
    )


def location_request(
    payload: models.LocationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a location search request for the carrier API

    payload: The standardized LocationRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # The search is anchored on the unified Address abstraction
    address = lib.to_address(payload.address)

    {% if is_xml_api %}
    # For XML API request
    request = {{id}}_req.LocationRequest(
        country_code=address.country_code,
        postcode=address.postal_code,
        city_name=address.city,
        street=address.address_line1,
        location_type=payload.location_type,
        radius=payload.radius_km,
        max_results=payload.max_results,
    )
    {% else %}
    # For JSON API request - Using camelCase attribute names to match schema definition
    request = {{id}}_req.LocationRequestType(
        countryCode=address.country_code,
        postalCode=address.postal_code,
        cityLocality=address.city,
        streetAddress=address.address_line1,
        locationType=payload.location_type,
        radiusKm=payload.radius_km,
        maxResults=payload.max_results,
    )
    {% endif %}

    return lib.Serializable(request, {% if is_xml_api %}lib.to_xml{% else %}lib.to_dict{% endif %})
'''
)

JSON_SCHEMA_LOCATION_REQUEST_TEMPLATE = Template('''
{
  "countryCode": "US",
  "postalCode": "12345",
  "cityLocality": "City Name",
  "streetAddress": "123 Main St",
  "locationType": "pickup_point",
  "radiusKm": 10,
  "maxResults": 20
}
''')

JSON_SCHEMA_LOCATION_RESPONSE_TEMPLATE = Template('''
{
  "locations": [
    {
      "locationId": "LOC-001",
      "locationType": "pickup_point",
      "name": "Downtown Pickup Point",
      "address": {
        "streetAddress": "123 Main St",
        "cityLocality": "City Name",
        "postalCode": "12345",
        "countryCode": "US"
      },
      "latitude": 40.7128,
      "longitude": -74.006,
      "distanceKm": 1.2,
      "openingHours": [],
      "services": []
    }
  ]
}
''')

XML_SCHEMA_LOCATION_REQUEST_TEMPLATE = Template('''<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/location" xmlns="http://{{id}}.com/ws/location" elementFormDefault="qualified">
    <xsd:element name="location-request">
        <xsd:complexType>
            <xsd:sequence>
                <xsd:element name="country_code" type="xsd:string" />
                <xsd:element name="postcode" type="xsd:string" minOccurs="0" />
                <xsd:element name="city_name" type="xsd:string" minOccurs="0" />
                <xsd:element name="street" type="xsd:string" minOccurs="0" />
                <xsd:element name="location_type" type="xsd:string" minOccurs="0" />
                <xsd:element name="radius" type="xsd:decimal" minOccurs="0" />
                <xsd:element name="max_results" type="xsd:integer" minOccurs="0" />
            </xsd:sequence>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
''')

XML_SCHEMA_LOCATION_RESPONSE_TEMPLATE = Template('''<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/location" xmlns="http://{{id}}.com/ws/location" elementFormDefault="qualified">
    <xsd:element name="location-response">
        <xsd:complexType>
            <xsd:sequence>
                <xsd:element name="location" maxOccurs="unbounded">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="location_id" type="xsd:string" />
                            <xsd:element name="location_type" type="xsd:string" minOccurs="0" />
                            <xsd:element name="name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="street" type="xsd:string" minOccurs="0" />
                            <xsd:element name="city_name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="postcode" type="xsd:string" minOccurs="0" />
                            <xsd:element name="country_code" type="xsd:string" minOccurs="0" />
                            <xsd:element name="latitude" type="xsd:decimal" minOccurs="0" />
                            <xsd:element name="longitude" type="xsd:decimal" minOccurs="0" />
                            <xsd:element name="distance" type="xsd:decimal" minOccurs="0" />
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
            </xsd:sequence>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
''')

TEST_LOCATION_TEMPLATE = Template('''"""{{name}} carrier location finder tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)

class Test{{compact_name}}Location(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.LocationRequest = models.LocationRequest(**LocationPayload)

    def test_create_location_request(self):
        request = gateway.mapper.create_location_request(self.LocationRequest)
        self.assertEqual(lib.to_dict(request.serialize()), LocationRequest)

    def test_get_locations(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Location.search(self.LocationRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/locations"
            )

    def test_parse_location_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = LocationResponse
            parsed_response = (
                karrio.Location.search(self.LocationRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedLocationResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Location.search(self.LocationRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


LocationPayload = {
    "address": {
        "country_code": "US",
        "postal_code": "12345",
        "city": "City Name",
    },
    "location_type": "pickup_point",
}

LocationRequest = {% if is_xml_api %}"""<?xml version="1.0"?>
<location-request>
    <country_code>US</country_code>
    <postcode>12345</postcode>
    <city_name>City Name</city_name>
    <location_type>pickup_point</location_type>
</location-request>"""{% else %}{
  "countryCode": "US",
  "postalCode": "12345",
  "cityLocality": "City Name",
  "locationType": "pickup_point"
}{% endif %}

LocationResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<location-response>
    <location>
        <location_id>LOC-001</location_id>
        <location_type>pickup_point</location_type>
        <name>Downtown Pickup Point</name>
        <street>123 Main St</street>
        <city_name>City Name</city_name>
        <postcode>12345</postcode>
        <country_code>US</country_code>
    </location>
</location-response>"""{% else %}"""{
  "locations": [
    {
      "locationId": "LOC-001",
      "locationType": "pickup_point",
      "name": "Downtown Pickup Point",
      "address": {
        "streetAddress": "123 Main St",
        "cityLocality": "City Name",
        "postalCode": "12345",
        "countryCode": "US"
      }
    }
  ]
}"""{% endif %}

ErrorResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<error-response>
    <e>
        <code>location_error</code>
        <message>Unable to find locations</message>
        <details>Invalid search parameters provided</details>
    </e>
</error-response>"""{% else %}"""{
  "error": {
    "code": "location_error",
    "message": "Unable to find locations",
    "details": "Invalid search parameters provided"
  }
}"""{% endif %}

ParsedLocationResponse = [
    [],
    []
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "code": "location_error",
            "message": "Unable to find locations",
            "details": {
                "details": "Invalid search parameters provided"
            }
        }
    ]
]''')
