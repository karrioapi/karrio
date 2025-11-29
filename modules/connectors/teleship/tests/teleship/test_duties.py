"""Teleship carrier duties and taxes calculation tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTeleshipDuties(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.DutiesRequest = models.DutiesCalculationRequest(**DutiesPayload)

    def test_create_duties_request(self):
        request = gateway.mapper.create_duties_calculation_request(self.DutiesRequest)

        self.assertEqual(lib.to_dict(request.serialize()), DutiesRequest)

    def test_calculate_duties(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Duties.calculate(self.DutiesRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/trade-engine/duties-taxes",
            )

    def test_parse_duties_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = DutiesResponse
            parsed_response = (
                karrio.Duties.calculate(self.DutiesRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedDutiesResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Duties.calculate(self.DutiesRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


DutiesPayload = {
    "shipment_identifier": "SHP-UK-US-12345",
    "shipper": {
        "address_line1": "123 Business Park",
        "city": "London",
        "postal_code": "SW1A 1AA",
        "country_code": "GB",
        "state_code": "LDN",
        "person_name": "John Smith",
        "company_name": "UK Exports Ltd",
        "phone_number": "+442071234567",
        "email": "shipping@ukexports.co.uk",
    },
    "recipient": {
        "address_line1": "555 Industrial Blvd",
        "city": "Los Angeles",
        "postal_code": "90001",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Jane Doe",
        "company_name": "US Imports Inc",
        "phone_number": "+13105551234",
        "email": "receiving@usimports.com",
    },
    "reference": "ORDER-2025-001",
    "customs": {
        "content_type": "merchandise",
        "invoice": "INV-2025-001",
        "invoice_date": "2025-01-15",
        "commodities": [
            {
                "sku": "WIDGET-001",
                "title": "Electronic Widget",
                "description": "Consumer electronics widget",
                "quantity": 2,
                "weight": 0.6,
                "weight_unit": "KG",
                "value_amount": 150.00,
                "value_currency": "GBP",
                "origin_country": "GB",
                "hs_code": "8471.30.0100",
            },
            {
                "sku": "GADGET-002",
                "title": "Smart Gadget",
                "description": "Portable smart device",
                "quantity": 1,
                "weight": 0.3,
                "weight_unit": "KG",
                "value_amount": 250.00,
                "value_currency": "GBP",
                "origin_country": "GB",
                "hs_code": "8517.12.0000",
            },
        ],
        "options": {
            "eori_number": "GB123456789000",
            "incoterms": "DAP",
        },
    },
    "options": {"currency": "GBP"},
}

DutiesRequest = {
    "commodities": [
        {
            "countryOfOrigin": "GB",
            "description": "Consumer electronics widget",
            "hsCode": "8471.30.0100",
            "quantity": 2,
            "sku": "WIDGET-001",
            "title": "Electronic Widget",
            "unitWeight": {"unit": "KG", "value": 0.6},
            "value": {"amount": 150.0, "currency": "GBP"},
        },
        {
            "countryOfOrigin": "GB",
            "description": "Portable smart device",
            "hsCode": "8517.12.0000",
            "quantity": 1,
            "sku": "GADGET-002",
            "title": "Smart Gadget",
            "unitWeight": {"unit": "KG", "value": 0.3},
            "value": {"amount": 250.0, "currency": "GBP"},
        },
    ],
    "currency": "GBP",
    "customs": {
        "EORI": "GB123456789000",
        "contentType": "merchandise",
        "invoiceDate": "2025-01-15",
        "invoiceNumber": "INV-2025-001",
    },
    "orderTrackingReference": "ORDER-2025-001",
    "shipFrom": {
        "address": {
            "city": "London",
            "country": "GB",
            "line1": "123 Business Park",
            "postcode": "SW1A 1AA",
            "state": "LDN",
        },
        "company": "UK Exports Ltd",
        "email": "shipping@ukexports.co.uk",
        "name": "John Smith",
        "phone": "+442071234567",
    },
    "shipTo": {
        "address": {
            "city": "Los Angeles",
            "country": "US",
            "line1": "555 Industrial Blvd",
            "postcode": "90001",
            "state": "CA",
        },
        "company": "US Imports Inc",
        "email": "receiving@usimports.com",
        "name": "Jane Doe",
        "phone": "+13105551234",
    },
}

DutiesResponse = """{
    "messages": [],
    "price": 127.50,
    "currency": "GBP",
    "charges": [
        {
            "name": "Import Duty",
            "amount": 55.00,
            "rate": 0.10,
            "currency": "GBP"
        },
        {
            "name": "VAT",
            "amount": 72.50,
            "rate": 0.20,
            "currency": "GBP"
        }
    ],
    "commodities": [
        {
            "itemNumber": 1,
            "title": "Electronic Widget",
            "charges": [
                {
                    "name": "Import Duty",
                    "amount": 30.00,
                    "rate": 0.10,
                    "currency": "GBP"
                },
                {
                    "name": "VAT",
                    "amount": 36.00,
                    "rate": 0.20,
                    "currency": "GBP"
                }
            ]
        },
        {
            "itemNumber": 2,
            "title": "Smart Gadget",
            "charges": [
                {
                    "name": "Import Duty",
                    "amount": 25.00,
                    "rate": 0.10,
                    "currency": "GBP"
                },
                {
                    "name": "VAT",
                    "amount": 36.50,
                    "rate": 0.20,
                    "currency": "GBP"
                }
            ]
        }
    ]
}"""

ErrorResponse = """{
    "messages": [
        {
            "code": 400,
            "timestamp": "2025-01-15T10:30:45Z",
            "message": "Duties calculation failed",
            "details": [
                "Invalid HS code format for commodity: WIDGET-001",
                "Origin country must be provided for all commodities"
            ]
        }
    ]
}"""

ParsedDutiesResponse = [
    {
        "carrier_id": "teleship",
        "carrier_name": "teleship",
        "total_charge": 127.5,
        "currency": "GBP",
        "charges": [
            {"name": "Import Duty", "amount": 55.0, "currency": "GBP"},
            {"name": "VAT", "amount": 72.5, "currency": "GBP"},
        ],
        "meta": {
            "price": 127.5,
            "currency": "GBP",
            "charges": [
                {
                    "name": "Import Duty",
                    "amount": 55.0,
                    "rate": 0.1,
                    "currency": "GBP",
                },
                {"name": "VAT", "amount": 72.5, "rate": 0.2, "currency": "GBP"},
            ],
            "commodities": [
                {
                    "itemNumber": 1,
                    "title": "Electronic Widget",
                    "charges": [
                        {
                            "name": "Import Duty",
                            "amount": 30.0,
                            "rate": 0.1,
                            "currency": "GBP",
                        },
                        {
                            "name": "VAT",
                            "amount": 36.0,
                            "rate": 0.2,
                            "currency": "GBP",
                        },
                    ],
                },
                {
                    "itemNumber": 2,
                    "title": "Smart Gadget",
                    "charges": [
                        {
                            "name": "Import Duty",
                            "amount": 25.0,
                            "rate": 0.1,
                            "currency": "GBP",
                        },
                        {
                            "name": "VAT",
                            "amount": 36.5,
                            "rate": 0.2,
                            "currency": "GBP",
                        },
                    ],
                },
            ],
        },
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "code": "400",
            "message": "Duties calculation failed",
            "details": {
                "timestamp": "2025-01-15T10:30:45Z",
                "details": [
                    "Invalid HS code format for commodity: WIDGET-001",
                    "Origin country must be provided for all commodities",
                ],
            },
        }
    ],
]
