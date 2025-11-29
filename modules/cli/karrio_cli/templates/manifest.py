from jinja2 import Template

PROVIDER_MANIFEST_TEMPLATE = Template(
    '''"""Karrio {{name}} manifest creation implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract manifest details from the response to populate ManifestDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., ManifestRequestType),
# while XML schema types don't have this suffix (e.g., ManifestRequest).

import karrio.schemas.{{id}}.manifest_request as {{id}}_req
import karrio.schemas.{{id}}.manifest_response as {{id}}_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils


def parse_manifest_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    """
    Parse manifest creation response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (ManifestDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract manifest details
    manifest = _extract_details(response, settings)

    return manifest, messages


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
    # For XML APIs, convert Element to proper response object
    manifest = lib.to_object({{id}}_res.ManifestResponse, data)

    # Extract manifest details
    manifest_id = manifest.manifest_id if hasattr(manifest, 'manifest_id') else ""
    manifest_url = manifest.manifest_url if hasattr(manifest, 'manifest_url') else ""
    manifest_document = manifest.manifest_document if hasattr(manifest, 'manifest_document') else ""
    status = manifest.status if hasattr(manifest, 'status') else ""
    {% else %}
    # For JSON APIs, convert dict to proper response object
    manifest = lib.to_object({{id}}_res.ManifestResponseType, data)

    # Extract manifest details
    manifest_id = manifest.manifestId if hasattr(manifest, 'manifestId') else ""
    manifest_url = manifest.manifestUrl if hasattr(manifest, 'manifestUrl') else ""
    manifest_document = manifest.manifestData if hasattr(manifest, 'manifestData') else ""
    status = manifest.status if hasattr(manifest, 'status') else ""
    {% endif %}

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        manifest_id=manifest_id,
        doc=models.ManifestDocument(manifest=manifest_document) if manifest_document else None,
        meta=dict(
            status=status,
            manifest_url=manifest_url,
        ),
    ) if manifest_id else None


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
    # Convert karrio models to carrier-specific format
    address = lib.to_address(payload.address) if payload.address else None

    {% if is_xml_api %}
    # For XML API request
    request = {{id}}_req.ManifestRequest(
        account_number=settings.account_number,
        close_date=payload.options.get("close_date") if payload.options else None,
        shipments=[
            {{id}}_req.Shipment(tracking_number=identifier)
            for identifier in payload.shipment_identifiers
        ],
    )
    {% else %}
    # For JSON API request
    request = {{id}}_req.ManifestRequestType(
        accountNumber=settings.account_number,
        closeDate=payload.options.get("closeDate") if payload.options else None,
        shipments=[
            {"trackingNumber": identifier}
            for identifier in payload.shipment_identifiers
        ],
    )
    {% endif %}

    return lib.Serializable(request, {% if is_xml_api %}lib.to_xml{% else %}lib.to_dict{% endif %})
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
