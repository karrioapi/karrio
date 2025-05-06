from jinja2 import Template

PROVIDER_MANIFEST_TEMPLATE = Template(
    '''"""Karrio {{name}} manifest API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract manifest details from the response

import typing
import base64
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_manifest_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    """
    Parse manifest response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (ManifestDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.ManifestDetails:
    """
    Extract manifest details from carrier response data

    data: The carrier-specific manifest response data
    settings: The carrier connection settings

    Returns a ManifestDetails object with the manifest information
    """
    {% if is_xml_api %}
    # Example implementation for XML response:
    # Extract manifest ID and document from the response
    # manifest_id = lib.find_element("manifest-id", data, first=True).text
    # manifest_content = lib.find_element("manifest-document", data, first=True).text
    # shipments = []
    # for shipment_elem in lib.find_element("shipment", data):
    #     shipments.append(lib.find_element("tracking-number", shipment_elem, first=True).text)

    # For development, return sample data
    manifest_id = "MAN123456"
    manifest_content = "base64_encoded_manifest_pdf"
    shipments = ["TRACK123456", "TRACK789012"]
    {% else %}
    # Example implementation for JSON response:
    # manifest_id = data.get("manifestId", "")
    # manifest_content = data.get("manifestDocument", "")
    # shipments = []
    # for shipment in data.get("shipments", []):
    #     shipments.append(shipment.get("trackingNumber", ""))

    # For development, return sample data
    manifest_id = "MAN123456"
    manifest_content = "base64_encoded_manifest_pdf"
    shipments = ["TRACK123456", "TRACK789012"]
    {% endif %}

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        manifest_id=manifest_id,
        shipments=shipments,
        doc=models.ManifestDocument(manifest=manifest_content),
        meta=dict(
            # Additional carrier-specific metadata
            created_at="2023-07-01T12:00:00Z",
            submission_id="SUB123456"
        ),
    )


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a manifest request for the carrier API

    payload: The standardized ManifestRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Extract tracking numbers (shipments) to be included in the manifest
    tracking_numbers = payload.shipments

    {% if is_xml_api %}
    # Example implementation for XML manifest request:
    # import karrio.schemas.{{id}}.manifest_request as {{id}}_req
    #
    # shipment_list = []
    # for tracking_number in tracking_numbers:
    #     shipment_list.append({{id}}_req.Shipment(
    #         tracking_number=tracking_number
    #     ))
    #
    # request = {{id}}_req.ManifestRequest(
    #     account_number=settings.account_number,
    #     close_date=payload.close_date or lib.today(),
    #     shipments=shipment_list
    # )
    #
    # return lib.Serializable(
    #     request,
    #     lambda _: lib.to_xml(
    #         _,
    #         name_="ManifestRequest",
    #         namespacedef_='xmlns="http://{{id}}.com/schema/manifest"'
    #     )
    # )

    # For development, return a simple XML request
    close_date = payload.close_date or lib.today()
    shipments_xml = ""
    for tracking_number in tracking_numbers:
        shipments_xml += f"  <shipment>\n    <tracking-number>{tracking_number}</tracking-number>\n  </shipment>\n"

    request = f"""<?xml version="1.0"?>
<manifest-request>
  <account-number>{settings.account_number}</account-number>
  <close-date>{close_date}</close-date>
  <shipments>
{shipments_xml}  </shipments>
</manifest-request>"""

    return lib.Serializable(request, lambda r: r)
    {% else %}
    # Example implementation for JSON manifest request:
    # import karrio.schemas.{{id}}.manifest_request as {{id}}_req
    #
    # shipment_list = []
    # for tracking_number in tracking_numbers:
    #     shipment_list.append({
    #         "trackingNumber": tracking_number
    #     })
    #
    # request = {{id}}_req.ManifestRequestType(
    #     accountNumber=settings.account_number,
    #     closeDate=payload.close_date or lib.today(),
    #     shipments=shipment_list
    # )
    #
    # return lib.Serializable(request, lib.to_dict)

    # For development, return a simple JSON request
    shipment_list = []
    for tracking_number in tracking_numbers:
        shipment_list.append({
            "trackingNumber": tracking_number
        })

    request = {
        "accountNumber": settings.account_number,
        "closeDate": str(payload.close_date or lib.today()),
        "shipments": shipment_list
    }

    return lib.Serializable(request, lib.to_dict)
    {% endif %}
'''
)

# XML schema templates for manifest operations
XML_SCHEMA_MANIFEST_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/manifest-request" xmlns="http://{{id}}.com/ws/manifest-request" elementFormDefault="qualified">
    <xsd:element name="manifest-request">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="account-number" type="xsd:string" minOccurs="0" />
                <xsd:element name="close-date" type="xsd:date" />
                <xsd:element name="shipments">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="shipment" maxOccurs="unbounded">
                                <xsd:complexType>
                                    <xsd:all>
                                        <xsd:element name="tracking-number" type="xsd:string" />
                                    </xsd:all>
                                </xsd:complexType>
                            </xsd:element>
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

XML_SCHEMA_MANIFEST_RESPONSE_TEMPLATE = Template(
    """<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/manifest-response" xmlns="http://{{id}}.com/ws/manifest-response" elementFormDefault="qualified">
    <xsd:element name="manifest-response">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="manifest-id" type="xsd:string" />
                <xsd:element name="manifest-url" type="xsd:string" minOccurs="0" />
                <xsd:element name="manifest-document" type="xsd:base64Binary" minOccurs="0" />
                <xsd:element name="status" type="xsd:string" />
                <xsd:element name="shipment-count" type="xsd:integer" minOccurs="0" />
                <xsd:element name="creation-date" type="xsd:dateTime" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

# JSON schema templates for manifest operations
JSON_SCHEMA_MANIFEST_REQUEST_TEMPLATE = Template(
    """{
  "manifestRequest": {
    "accountNumber": "123456",
    "closeDate": "2023-06-01",
    "shipments": [
      {
        "trackingNumber": "1Z12345E0205271688"
      },
      {
        "trackingNumber": "1Z12345E0205271689"
      }
    ]
  }
}
"""
)

JSON_SCHEMA_MANIFEST_RESPONSE_TEMPLATE = Template(
    """{
  "manifestResponse": {
    "manifestId": "MAN123456",
    "manifestUrl": "https://example.com/manifest/MAN123456",
    "manifestData": "base64_encoded_manifest_data",
    "status": "completed",
    "shipmentCount": 2,
    "creationDate": "2023-06-01T15:30:00Z"
  }
}
"""
)

TEST_MANIFEST_TEMPLATE = Template('''"""{{name}} carrier manifest tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)

class Test{{compact_name}}Manifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(
            shipments=["SHIP123456", "SHIP789012"]
        )

    def test_create_manifest_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)
        self.assertEqual(request.serialize(), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/manifests"
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ManifestResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest)
                .from_(gateway)
                .parse()
            )
            self.assertIsNotNone(parsed_response[0])
            self.assertEqual(len(parsed_response[1]), 0)
            self.assertEqual(parsed_response[0].carrier_name, "{{id}}")

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest)
                .from_(gateway)
                .parse()
            )
            self.assertIsNone(parsed_response[0])
            self.assertEqual(len(parsed_response[1]), 1)
            self.assertEqual(parsed_response[1][0].code, "manifest_error")


if __name__ == "__main__":
    unittest.main()


ManifestResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<manifest-response>
    <carrier-id>{{id}}</carrier-id>
    <carrier-name>{{id}}</carrier-name>
    <manifest>JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwogIC9QYWdlcyAyIDAgUgo+PgplbmRvYmoKCjIgMCBvYmoKPDwKICAvVHlwZSAvUGFnZXMKICAvTWVkaWFCb3ggWyAwIDAgMjAwIDIwMCBdCiAgL0NvdW50IDEKICAvS2lkcyBbIDMgMCBSIF0KPj4KZW5kb2JqCgozIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2UKICAvUGFyZW50IDIgMCBSCiAgL1Jlc291cmNlcyA8PAogICAgL0ZvbnQgPDwKICAgICAgL0YxIDQgMCBSIAogICAgPj4KICA+PgogIC9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKCjQgMCBvYmoKPDwKICAvVHlwZSAvRm9udAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvVGltZXMtUm9tYW4KPj4KZW5kb2JqCgo1IDAgb2JqICAlIHBhZ2UgY29udGVudAo8PAogIC9MZW5ndGggNDQKPj4Kc3RyZWFtCkJUCjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8sIHdvcmxkISkgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4gCjAwMDAwMDAwNzkgMDAwMDAgbiAKMDAwMDAwMDE3MyAwMDAwMCBuIAowMDAwMDAwMzAxIDAwMDAwIG4gCjAwMDAwMDAzODAgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9TaXplIDYKICAvUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKNDkyCiUlRU9G</manifest>
</manifest-response>"""{% else %}"""{
  "carrier_id": "{{id}}",
  "carrier_name": "{{id}}",
  "manifest": "JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwogIC9QYWdlcyAyIDAgUgo+PgplbmRvYmoKCjIgMCBvYmoKPDwKICAvVHlwZSAvUGFnZXMKICAvTWVkaWFCb3ggWyAwIDAgMjAwIDIwMCBdCiAgL0NvdW50IDEKICAvS2lkcyBbIDMgMCBSIF0KPj4KZW5kb2JqCgozIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2UKICAvUGFyZW50IDIgMCBSCiAgL1Jlc291cmNlcyA8PAogICAgL0ZvbnQgPDwKICAgICAgL0YxIDQgMCBSIAogICAgPj4KICA+PgogIC9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKCjQgMCBvYmoKPDwKICAvVHlwZSAvRm9udAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvVGltZXMtUm9tYW4KPj4KZW5kb2JqCgo1IDAgb2JqICAlIHBhZ2UgY29udGVudAo8PAogIC9MZW5ndGggNDQKPj4Kc3RyZWFtCkJUCjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8sIHdvcmxkISkgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4gCjAwMDAwMDAwNzkgMDAwMDAgbiAKMDAwMDAwMDE3MyAwMDAwMCBuIAowMDAwMDAwMzAxIDAwMDAwIG4gCjAwMDAwMDAzODAgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9TaXplIDYKICAvUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKNDkyCiUlRU9G"
}"""{% endif %}

ManifestRequest = {% if is_xml_api %}"""<?xml version="1.0"?>
<manifest-request>
  <shipment-identifiers>
    <shipment-identifier>SHIP123456</shipment-identifier>
    <shipment-identifier>SHIP789012</shipment-identifier>
  </shipment-identifiers>
  <address>
    <address-line1>123 Main Street</address-line1>
    <city>Los Angeles</city>
    <postal-code>90001</postal-code>
    <country-code>US</country-code>
    <state-code>CA</state-code>
    <person-name>John Doe</person-name>
    <company-name>Test Company</company-name>
    <phone-number>555-123-4567</phone-number>
    <email>john.doe@example.com</email>
  </address>
  <reference>REF123</reference>
  <options>
    <option>
      <key>close_date</key>
      <value>2023-07-01</value>
    </option>
  </options>
</manifest-request>"""{% else %}"""{
  "shipmentIdentifiers": [
    "SHIP123456",
    "SHIP789012"
  ],
  "address": {
    "addressLine1": "123 Main Street",
    "city": "Los Angeles",
    "postalCode": "90001",
    "countryCode": "US",
    "stateCode": "CA",
    "personName": "John Doe",
    "companyName": "Test Company",
    "phoneNumber": "555-123-4567",
    "email": "john.doe@example.com"
  },
  "reference": "REF123",
  "options": {
    "close_date": "2023-07-01"
  }
}"""{% endif %}

ErrorResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<error-response>
    <e>
        <code>manifest_error</code>
        <message>Unable to create manifest</message>
        <details>Invalid shipment identifiers provided</details>
    </e>
</error-response>"""{% else %}"""{
  "error": {
    "code": "manifest_error",
    "message": "Unable to create manifest",
    "details": "Invalid shipment identifiers provided"
  }
}"""{% endif %}'''
)
