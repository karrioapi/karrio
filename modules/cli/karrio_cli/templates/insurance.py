"""INSURANCE TEMPLATES"""
from jinja2 import Template


INSURANCE_APPLY_TEMPLATE = Template("""\"\"\"Karrio {{name}} insurance coverage implementation.\"\"\"

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract insurance details from the response to populate InsuranceDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., InsuranceRequestType),
# while XML schema types don't have this suffix (e.g., InsuranceRequest).

import karrio.schemas.{{id}}.insurance_request as {{id}}_req
import karrio.schemas.{{id}}.insurance_response as {{id}}_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils


def parse_insurance_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.InsuranceDetails, typing.List[models.Message]]:
    \"\"\"
    Parse insurance response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (InsuranceDetails, List[Message])
    \"\"\"
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract insurance details
    insurance = _extract_details(response, settings)

    return insurance, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.InsuranceDetails:
    \"\"\"
    Extract insurance details from carrier response data

    data: The carrier-specific insurance response data
    settings: The carrier connection settings

    Returns an InsuranceDetails object with the insurance information
    \"\"\"
    {% if is_xml_api %}
    # For XML APIs, convert Element to proper response object
    insurance = lib.to_object({{id}}_res.InsuranceResponse, data)

    # Extract insurance details
    insurance_id = insurance.insurance_id if hasattr(insurance, 'insurance_id') else ""
    premium = insurance.premium if hasattr(insurance, 'premium') else 0.0
    currency = insurance.currency if hasattr(insurance, 'currency') else "USD"
    status = insurance.status if hasattr(insurance, 'status') else ""
    {% else %}
    # For JSON APIs, convert dict to proper response object
    insurance = lib.to_object({{id}}_res.InsuranceResponseType, data)

    # Extract insurance details
    insurance_id = insurance.id if hasattr(insurance, 'id') else ""
    premium = insurance.premium if hasattr(insurance, 'premium') else 0.0
    currency = insurance.currency if hasattr(insurance, 'currency') else "USD"
    status = insurance.status if hasattr(insurance, 'status') else ""
    {% endif %}

    return models.InsuranceDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        insurance_id=insurance_id,
        insurance_charge=models.ChargeDetails(
            name="Insurance",
            amount=lib.to_decimal(premium),
            currency=currency,
        ),
        meta=dict(status=status),
    ) if insurance_id else None


def insurance_request(
    payload: models.InsuranceRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    \"\"\"
    Create an insurance request for the carrier API

    payload: The standardized InsuranceRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    \"\"\"
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    parcel = lib.to_packages([payload.parcel]).single if payload.parcel else None

    {% if is_xml_api %}
    # For XML API request
    request = {{id}}_req.InsuranceRequest(
        shipment_id=payload.shipment_identifier,
        coverage_amount=lib.to_decimal(payload.coverage_amount),
        coverage_currency=payload.coverage_currency or settings.default_currency,
        shipper={{id}}_req.Address(
            person_name=shipper.person_name,
            company_name=shipper.company_name,
            address_line1=shipper.address_line1,
            city=shipper.city,
            state_code=shipper.state_code,
            postal_code=shipper.postal_code,
            country_code=shipper.country_code,
        ),
        recipient={{id}}_req.Address(
            person_name=recipient.person_name,
            company_name=recipient.company_name,
            address_line1=recipient.address_line1,
            city=recipient.city,
            state_code=recipient.state_code,
            postal_code=recipient.postal_code,
            country_code=recipient.country_code,
        ),
    )
    {% else %}
    # For JSON API request
    request = {{id}}_req.InsuranceRequestType(
        shipmentId=payload.shipment_identifier,
        coverage={
            "value": lib.to_decimal(payload.coverage_amount),
            "currency": payload.coverage_currency or settings.default_currency,
        },
        shipFrom={
            "name": shipper.person_name,
            "company": shipper.company_name,
            "address": {
                "line1": shipper.address_line1,
                "line2": shipper.address_line2,
                "city": shipper.city,
                "state": shipper.state_code,
                "postcode": shipper.postal_code,
                "country": shipper.country_code,
            },
        },
        shipTo={
            "name": recipient.person_name,
            "company": recipient.company_name,
            "address": {
                "line1": recipient.address_line1,
                "line2": recipient.address_line2,
                "city": recipient.city,
                "state": recipient.state_code,
                "postcode": recipient.postal_code,
                "country": recipient.country_code,
            },
        },
    )
    {% endif %}

    return lib.Serializable(request, {% if is_xml_api %}lib.to_xml{% else %}lib.to_dict{% endif %})
""")


INSURANCE_INIT_TEMPLATE = Template("""from karrio.providers.{{id}}.insurance.apply import (
    insurance_request,
    parse_insurance_response,
)
""")


JSON_SCHEMA_INSURANCE_REQUEST_TEMPLATE = Template("""{
  "shipmentId": "shp_1234567890",
  "coverage": {
    "value": 1000.00,
    "currency": "USD"
  },
  "shipFrom": {
    "name": "John Doe",
    "company": "ACME Corp",
    "address": {
      "line1": "123 Main St",
      "line2": "Suite 100",
      "city": "Los Angeles",
      "state": "CA",
      "postcode": "90001",
      "country": "US"
    }
  },
  "shipTo": {
    "name": "Jane Smith",
    "company": "XYZ Inc",
    "address": {
      "line1": "456 Oak Ave",
      "line2": "",
      "city": "New York",
      "state": "NY",
      "postcode": "10001",
      "country": "US"
    }
  },
  "parcel": {
    "weight": {
      "value": 2.5,
      "unit": "kg"
    },
    "dimensions": {
      "length": 30,
      "width": 20,
      "height": 15,
      "unit": "cm"
    }
  }
}
""")


JSON_SCHEMA_INSURANCE_RESPONSE_TEMPLATE = Template("""{
  "id": "ins_abc123xyz",
  "status": "active",
  "premium": 15.50,
  "currency": "USD",
  "coverage": {
    "value": 1000.00,
    "currency": "USD"
  },
  "shipmentId": "shp_1234567890",
  "createdAt": "2024-01-15T10:30:00Z",
  "expiresAt": "2024-02-15T10:30:00Z"
}
""")

# XML schema templates for insurance operations
XML_SCHEMA_INSURANCE_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/insurance-request" xmlns="http://{{id}}.com/ws/insurance-request" elementFormDefault="qualified">
    <xsd:element name="insurance-request">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="shipment-id" type="xsd:string" />
                <xsd:element name="coverage-amount" type="xsd:decimal" />
                <xsd:element name="coverage-currency" type="xsd:string" />
                <xsd:element name="shipper">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="person-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="company-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="address-line1" type="xsd:string" />
                            <xsd:element name="city" type="xsd:string" />
                            <xsd:element name="state-code" type="xsd:string" minOccurs="0" />
                            <xsd:element name="postal-code" type="xsd:string" />
                            <xsd:element name="country-code" type="xsd:string" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="recipient">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="person-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="company-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="address-line1" type="xsd:string" />
                            <xsd:element name="city" type="xsd:string" />
                            <xsd:element name="state-code" type="xsd:string" minOccurs="0" />
                            <xsd:element name="postal-code" type="xsd:string" />
                            <xsd:element name="country-code" type="xsd:string" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
""")

XML_SCHEMA_INSURANCE_RESPONSE_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/insurance-response" xmlns="http://{{id}}.com/ws/insurance-response" elementFormDefault="qualified">
    <xsd:element name="insurance-response">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="insurance-id" type="xsd:string" />
                <xsd:element name="status" type="xsd:string" />
                <xsd:element name="premium" type="xsd:decimal" />
                <xsd:element name="currency" type="xsd:string" />
                <xsd:element name="shipment-id" type="xsd:string" minOccurs="0" />
                <xsd:element name="created-at" type="xsd:dateTime" minOccurs="0" />
                <xsd:element name="expires-at" type="xsd:dateTime" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
""")


TEST_INSURANCE_TEMPLATE = Template('''"""{{name}} carrier insurance tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}Insurance(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.InsuranceRequest = models.InsuranceRequest(**InsurancePayload)

    def test_create_insurance_request(self):
        request = gateway.mapper.create_insurance_request(self.InsuranceRequest)
        self.assertEqual(lib.to_dict(request.serialize()), InsuranceRequest)

    def test_apply_insurance(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Insurance.apply(self.InsuranceRequest).from_(gateway)
            # Verify the request was made - adjust URL to match carrier API
            self.assertIsNotNone(mock.call_args)

    def test_parse_insurance_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = InsuranceResponse
            parsed_response = (
                karrio.Insurance.apply(self.InsuranceRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedInsuranceResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Insurance.apply(self.InsuranceRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


InsurancePayload = {
    "shipment_identifier": "shp_1234567890",
    "coverage_amount": 1000.00,
    "coverage_currency": "USD",
    "shipper": {
        "address_line1": "123 Main St",
        "city": "Los Angeles",
        "postal_code": "90001",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "John Doe",
        "company_name": "ACME Corp",
    },
    "recipient": {
        "address_line1": "456 Oak Ave",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "state_code": "NY",
        "person_name": "Jane Smith",
        "company_name": "XYZ Inc",
    },
}

InsuranceRequest = {% if is_xml_api %}{
    "shipment_id": "shp_1234567890",
    "coverage_amount": 1000.00,
    "coverage_currency": "USD",
    "shipper": {
        "person_name": "John Doe",
        "company_name": "ACME Corp",
        "address_line1": "123 Main St",
        "city": "Los Angeles",
        "state_code": "CA",
        "postal_code": "90001",
        "country_code": "US"
    },
    "recipient": {
        "person_name": "Jane Smith",
        "company_name": "XYZ Inc",
        "address_line1": "456 Oak Ave",
        "city": "New York",
        "state_code": "NY",
        "postal_code": "10001",
        "country_code": "US"
    }
}{% else %}{
    "shipmentId": "shp_1234567890",
    "coverage": {
        "value": 1000.00,
        "currency": "USD"
    },
    "shipFrom": {
        "name": "John Doe",
        "company": "ACME Corp",
        "address": {
            "line1": "123 Main St",
            "city": "Los Angeles",
            "state": "CA",
            "postcode": "90001",
            "country": "US"
        }
    },
    "shipTo": {
        "name": "Jane Smith",
        "company": "XYZ Inc",
        "address": {
            "line1": "456 Oak Ave",
            "city": "New York",
            "state": "NY",
            "postcode": "10001",
            "country": "US"
        }
    }
}{% endif %}

InsuranceResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<insurance-response>
    <insurance-id>ins_abc123xyz</insurance-id>
    <status>active</status>
    <premium>15.50</premium>
    <currency>USD</currency>
    <shipment-id>shp_1234567890</shipment-id>
    <created-at>2024-01-15T10:30:00Z</created-at>
    <expires-at>2024-02-15T10:30:00Z</expires-at>
</insurance-response>"""{% else %}"""{
  "id": "ins_abc123xyz",
  "status": "active",
  "premium": 15.50,
  "currency": "USD",
  "coverage": {
    "value": 1000.00,
    "currency": "USD"
  },
  "shipmentId": "shp_1234567890",
  "createdAt": "2024-01-15T10:30:00Z",
  "expiresAt": "2024-02-15T10:30:00Z"
}"""{% endif %}

ErrorResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<error-response>
    <e>
        <code>insurance_error</code>
        <message>Unable to apply insurance</message>
        <details>Coverage amount exceeds maximum limit</details>
    </e>
</error-response>"""{% else %}"""{
  "error": {
    "code": "insurance_error",
    "message": "Unable to apply insurance",
    "details": "Coverage amount exceeds maximum limit"
  }
}"""{% endif %}

ParsedInsuranceResponse = [
    {
        "carrier_id": "{{id}}",
        "carrier_name": "{{id}}",
        "insurance_id": "ins_abc123xyz",
        "insurance_charge": {
            "name": "Insurance",
            "amount": 15.50,
            "currency": "USD",
        },
        "meta": {"status": "active"},
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "code": "insurance_error",
            "message": "Unable to apply insurance",
            "details": {
                "details": "Coverage amount exceeds maximum limit"
            },
        }
    ],
]
''')
