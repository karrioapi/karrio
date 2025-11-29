"""DUTIES CALCULATION TEMPLATES"""
from jinja2 import Template


DUTIES_TEMPLATE = Template("""\"\"\"Karrio {{name}} duties and taxes calculation implementation.\"\"\"

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract duties/taxes details from the response to populate DutiesCalculationDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., DutiesRequestType),
# while XML schema types don't have this suffix (e.g., DutiesRequest).

import karrio.schemas.{{id}}.duties_taxes_request as {{id}}_req
import karrio.schemas.{{id}}.duties_taxes_response as {{id}}_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils


def parse_duties_calculation_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DutiesCalculationDetails, typing.List[models.Message]]:
    \"\"\"
    Parse duties/taxes calculation response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (DutiesCalculationDetails, List[Message])
    \"\"\"
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract duties details
    duties = _extract_details(response, settings)

    return duties, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.DutiesCalculationDetails:
    \"\"\"
    Extract duties/taxes details from carrier response data

    data: The carrier-specific duties response data
    settings: The carrier connection settings

    Returns a DutiesCalculationDetails object with the duties/taxes information
    \"\"\"
    {% if is_xml_api %}
    # For XML APIs, convert Element to proper response object
    details = lib.to_object({{id}}_res.DutiesResponse, data)

    # Extract duties details
    total_charge = float(details.total) if hasattr(details, 'total') else 0.0
    currency = details.currency if hasattr(details, 'currency') else "USD"

    # Extract individual charges
    charges = []
    if hasattr(details, 'charges') and details.charges:
        for charge in details.charges.charge:
            charges.append({
                "name": charge.name if hasattr(charge, 'name') else "",
                "amount": float(charge.amount) if hasattr(charge, 'amount') else 0.0,
                "currency": charge.currency if hasattr(charge, 'currency') else currency,
            })
    {% else %}
    # For JSON APIs, convert dict to proper response object
    details = lib.to_object({{id}}_res.DutiesResponseType, data)

    # Extract duties details
    total_charge = float(details.price) if hasattr(details, 'price') else 0.0
    currency = details.currency if hasattr(details, 'currency') else "USD"

    # Extract individual charges
    charges = []
    if hasattr(details, 'charges') and details.charges:
        for charge in details.charges:
            charges.append({
                "name": charge.name if hasattr(charge, 'name') else "",
                "amount": float(charge.amount) if hasattr(charge, 'amount') else 0.0,
                "currency": charge.currency if hasattr(charge, 'currency') else currency,
            })
    {% endif %}

    return models.DutiesCalculationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        total_charge=lib.to_decimal(total_charge),
        currency=currency,
        charges=[
            models.ChargeDetails(
                name=charge["name"],
                amount=lib.to_decimal(charge["amount"]),
                currency=charge["currency"],
            )
            for charge in charges
        ],
    ) if total_charge else None


def duties_calculation_request(
    payload: models.DutiesCalculationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    \"\"\"
    Create a duties/taxes calculation request for the carrier API

    payload: The standardized DutiesCalculationRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    \"\"\"
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    customs = lib.to_customs_info(payload.customs)
    commodities = lib.to_commodities(customs.commodities or [])

    {% if is_xml_api %}
    # For XML API request
    request = {{id}}_req.DutiesRequest(
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
        commodities=[
            {{id}}_req.Commodity(
                description=commodity.description,
                hs_code=commodity.hs_code,
                quantity=commodity.quantity,
                value=commodity.value_amount,
                currency=commodity.value_currency or settings.default_currency,
                weight=commodity.weight,
                weight_unit=commodity.weight_unit or "KG",
                country_of_origin=commodity.origin_country,
            )
            for commodity in commodities
        ],
        currency=payload.options.get("currency") if payload.options else None,
    )
    {% else %}
    # For JSON API request
    request = {{id}}_req.DutiesRequestType(
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
        commodities=[
            {
                "description": commodity.description,
                "hsCode": commodity.hs_code,
                "quantity": commodity.quantity,
                "value": {
                    "amount": commodity.value_amount,
                    "currency": commodity.value_currency or settings.default_currency,
                },
                "weight": {
                    "value": commodity.weight,
                    "unit": commodity.weight_unit or "kg",
                },
                "countryOfOrigin": commodity.origin_country,
            }
            for commodity in commodities
        ],
        currency=payload.options.get("currency") if payload.options else None,
    )
    {% endif %}

    return lib.Serializable(request, {% if is_xml_api %}lib.to_xml{% else %}lib.to_dict{% endif %})
""")


DUTIES_INIT_TEMPLATE = Template("""from karrio.providers.{{id}}.duties import (
    duties_calculation_request,
    parse_duties_calculation_response,
)
""")


JSON_SCHEMA_DUTIES_REQUEST_TEMPLATE = Template("""{
  "shipTo": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+49 89 123456",
    "company": "German Imports GmbH",
    "address": {
      "line1": "Leopoldstrasse 119",
      "line2": "2nd Floor",
      "city": "Munich",
      "state": "Bavaria",
      "postcode": "80804",
      "country": "DE"
    }
  },
  "shipFrom": {
    "name": "Jane Smith",
    "email": "jane@ukexports.com",
    "phone": "+44 20 7946 0958",
    "company": "UK Exports Ltd",
    "address": {
      "line1": "3 Belvedere Pl",
      "line2": "",
      "city": "London",
      "state": "England",
      "postcode": "SE1 0AD",
      "country": "GB"
    }
  },
  "commodities": [
    {
      "title": "Gold Earrings",
      "description": "Gold-plated jewelry earrings",
      "hsCode": "7117190090",
      "sku": "stock-1",
      "quantity": 1,
      "value": {
        "amount": 136.74,
        "currency": "GBP"
      },
      "unitWeight": {
        "unit": "kg",
        "value": 0.18
      },
      "countryOfOrigin": "GR",
      "category": "Jewelry"
    }
  ],
  "customs": {
    "contentType": "CommercialGoods",
    "incoterms": "DDP",
    "invoiceNumber": "INV-2024-001",
    "invoiceDate": "2024-01-15T00:00:00.000Z",
    "EORI": "GB078617476000",
    "VAT": "GB123456789"
  },
  "currency": "EUR",
  "orderTrackingReference": "ORDER-12345"
}
""")


JSON_SCHEMA_DUTIES_RESPONSE_TEMPLATE = Template("""{
  "messages": [],
  "price": 41.58,
  "currency": "EUR",
  "charges": [
    {
      "name": "Duty",
      "amount": 15.50,
      "currency": "EUR",
      "rate": 0.04
    },
    {
      "name": "VAT",
      "amount": 26.08,
      "currency": "EUR",
      "rate": 0.19
    }
  ],
  "commodities": [
    {
      "itemNumber": 1,
      "title": "Gold Earrings",
      "charges": [
        {
          "name": "Duty",
          "amount": 5.47,
          "currency": "EUR",
          "rate": 0.04
        }
      ],
      "restrictions": []
    }
  ]
}
""")

# XML schema templates for duties/taxes operations
XML_SCHEMA_DUTIES_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/duties-request" xmlns="http://{{id}}.com/ws/duties-request" elementFormDefault="qualified">
    <xsd:element name="duties-request">
        <xsd:complexType>
            <xsd:all>
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
                <xsd:element name="commodities">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="commodity" maxOccurs="unbounded">
                                <xsd:complexType>
                                    <xsd:all>
                                        <xsd:element name="description" type="xsd:string" />
                                        <xsd:element name="hs-code" type="xsd:string" />
                                        <xsd:element name="quantity" type="xsd:integer" />
                                        <xsd:element name="value" type="xsd:decimal" />
                                        <xsd:element name="currency" type="xsd:string" />
                                        <xsd:element name="weight" type="xsd:decimal" />
                                        <xsd:element name="weight-unit" type="xsd:string" />
                                        <xsd:element name="country-of-origin" type="xsd:string" minOccurs="0" />
                                    </xsd:all>
                                </xsd:complexType>
                            </xsd:element>
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="currency" type="xsd:string" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
""")

XML_SCHEMA_DUTIES_RESPONSE_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/duties-response" xmlns="http://{{id}}.com/ws/duties-response" elementFormDefault="qualified">
    <xsd:element name="duties-response">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="total" type="xsd:decimal" />
                <xsd:element name="currency" type="xsd:string" />
                <xsd:element name="charges">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="charge" maxOccurs="unbounded">
                                <xsd:complexType>
                                    <xsd:all>
                                        <xsd:element name="name" type="xsd:string" />
                                        <xsd:element name="amount" type="xsd:decimal" />
                                        <xsd:element name="currency" type="xsd:string" />
                                        <xsd:element name="rate" type="xsd:decimal" minOccurs="0" />
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
""")


TEST_DUTIES_TEMPLATE = Template('''"""{{name}} carrier duties/taxes calculation tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}Duties(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.DutiesRequest = models.DutiesCalculationRequest(**DutiesPayload)

    def test_create_duties_request(self):
        request = gateway.mapper.create_duties_calculation_request(self.DutiesRequest)
        self.assertEqual(lib.to_dict(request.serialize()), DutiesRequest)

    def test_calculate_duties(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Duties.calculate(self.DutiesRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/duties"
            )

    def test_parse_duties_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = DutiesResponse
            parsed_response = (
                karrio.Duties.calculate(self.DutiesRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedDutiesResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Duties.calculate(self.DutiesRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


DutiesPayload = {
    "shipper": {
        "address_line1": "123 Main St",
        "city": "London",
        "postal_code": "SW1A 1AA",
        "country_code": "GB",
        "person_name": "John Smith",
        "company_name": "UK Exports Ltd",
    },
    "recipient": {
        "address_line1": "456 Oak Ave",
        "city": "Munich",
        "postal_code": "80804",
        "country_code": "DE",
        "person_name": "Jane Doe",
        "company_name": "German Imports GmbH",
    },
    "customs": {
        "commodities": [
            {
                "description": "Gold Earrings",
                "hs_code": "7117190090",
                "quantity": 1,
                "value_amount": 136.74,
                "value_currency": "GBP",
                "weight": 0.18,
                "weight_unit": "KG",
                "origin_country": "GR",
            }
        ],
    },
    "options": {"currency": "EUR"},
}

DutiesRequest = {% if is_xml_api %}{
    "shipper": {
        "person_name": "John Smith",
        "company_name": "UK Exports Ltd",
        "address_line1": "123 Main St",
        "city": "London",
        "postal_code": "SW1A 1AA",
        "country_code": "GB"
    },
    "recipient": {
        "person_name": "Jane Doe",
        "company_name": "German Imports GmbH",
        "address_line1": "456 Oak Ave",
        "city": "Munich",
        "postal_code": "80804",
        "country_code": "DE"
    },
    "commodities": [
        {
            "description": "Gold Earrings",
            "hs_code": "7117190090",
            "quantity": 1,
            "value": 136.74,
            "currency": "GBP",
            "weight": 0.18,
            "weight_unit": "KG",
            "country_of_origin": "GR"
        }
    ],
    "currency": "EUR"
}{% else %}{
    "shipFrom": {
        "name": "John Smith",
        "company": "UK Exports Ltd",
        "address": {
            "line1": "123 Main St",
            "city": "London",
            "postcode": "SW1A 1AA",
            "country": "GB"
        }
    },
    "shipTo": {
        "name": "Jane Doe",
        "company": "German Imports GmbH",
        "address": {
            "line1": "456 Oak Ave",
            "city": "Munich",
            "postcode": "80804",
            "country": "DE"
        }
    },
    "commodities": [
        {
            "description": "Gold Earrings",
            "hsCode": "7117190090",
            "quantity": 1,
            "value": {
                "amount": 136.74,
                "currency": "GBP"
            },
            "weight": {
                "value": 0.18,
                "unit": "kg"
            },
            "countryOfOrigin": "GR"
        }
    ],
    "currency": "EUR"
}{% endif %}

DutiesResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<duties-response>
    <total>41.58</total>
    <currency>EUR</currency>
    <charges>
        <charge>
            <name>Duty</name>
            <amount>15.50</amount>
            <currency>EUR</currency>
            <rate>0.04</rate>
        </charge>
        <charge>
            <name>VAT</name>
            <amount>26.08</amount>
            <currency>EUR</currency>
            <rate>0.19</rate>
        </charge>
    </charges>
</duties-response>"""{% else %}"""{
  "price": 41.58,
  "currency": "EUR",
  "charges": [
    {
      "name": "Duty",
      "amount": 15.50,
      "currency": "EUR",
      "rate": 0.04
    },
    {
      "name": "VAT",
      "amount": 26.08,
      "currency": "EUR",
      "rate": 0.19
    }
  ]
}"""{% endif %}

ErrorResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<error-response>
    <e>
        <code>duties_error</code>
        <message>Unable to calculate duties</message>
        <details>Invalid HS code provided</details>
    </e>
</error-response>"""{% else %}"""{
  "error": {
    "code": "duties_error",
    "message": "Unable to calculate duties",
    "details": "Invalid HS code provided"
  }
}"""{% endif %}

ParsedDutiesResponse = [
    {
        "carrier_id": "{{id}}",
        "carrier_name": "{{id}}",
        "total_charge": 41.58,
        "currency": "EUR",
        "charges": [
            {"name": "Duty", "amount": 15.50, "currency": "EUR"},
            {"name": "VAT", "amount": 26.08, "currency": "EUR"},
        ],
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "code": "duties_error",
            "message": "Unable to calculate duties",
            "details": {
                "details": "Invalid HS code provided"
            },
        }
    ],
]
''')
