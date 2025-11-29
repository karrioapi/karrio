"""Teleship carrier rate tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTeleshipRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/rates/quotes",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
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
    "parcels": [
        {
            "weight": 1.2,
            "width": 20.0,
            "height": 15.0,
            "length": 30.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "packaging_type": "parcel",
        }
    ],
    "reference": "UK-US-12345",
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
            }
        ],
        "options": {"eori_number": "GB123456789000"},
    },
}

RateRequest = [
    {
        "commercialInvoiceReference": "INV-2025-001",
        "commodities": [
            {
                "countryOfOrigin": "GB",
                "description": "Consumer electronics widget",
                "quantity": 2,
                "sku": "WIDGET-001",
                "title": "Electronic Widget",
                "unitWeight": {"unit": "kg", "value": 0.6},
                "value": {"amount": 150.0, "currency": "GBP"},
            }
        ],
        "customerReference": "UK-US-12345",
        "customs": {
            "EORI": "GB123456789000",
            "contentType": "CommercialGoods",
            "invoiceDate": "2025-01-15",
            "invoiceNumber": "INV-2025-001",
        },
        "dimensions": {"height": 15.0, "length": 30.0, "unit": "cm", "width": 20.0},
        "packageType": "parcel",
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
        "weight": {"unit": "kg", "value": 1.2},
    }
]

RateResponse = """{
    "rates": [
        {
            "price": 106.56,
            "currency": "GBP",
            "transit": 3,
            "service": {
                "code": "TELESHIP-EXPEDITED-DROPOFF",
                "name": "Teleship Expedited Drop-off"
            },
            "charges": [
                {
                    "name": "Base Freight",
                    "amount": 85.00,
                    "rate": 85.00,
                    "currency": "GBP"
                },
                {
                    "name": "Fuel Surcharge",
                    "amount": 12.75,
                    "rate": 0.15,
                    "currency": "GBP"
                },
                {
                    "name": "Customs Clearance",
                    "amount": 8.81,
                    "rate": 8.81,
                    "currency": "GBP"
                }
            ],
            "estimatedDelivery": "2025-12-10T07:59:59.999Z"
        },
        {
            "price": 78.95,
            "currency": "GBP",
            "transit": 7,
            "service": {
                "code": "TELESHIP-STANDARD-DROPOFF",
                "name": "Teleship Standard Drop-off"
            },
            "charges": [
                {
                    "name": "Base Freight",
                    "amount": 65.00,
                    "rate": 65.00,
                    "currency": "GBP"
                },
                {
                    "name": "Fuel Surcharge",
                    "amount": 9.75,
                    "rate": 0.15,
                    "currency": "GBP"
                },
                {
                    "name": "Customs Clearance",
                    "amount": 4.20,
                    "rate": 4.20,
                    "currency": "GBP"
                }
            ],
            "estimatedDelivery": "2025-01-27T00:00:00.000Z"
        },
        {
            "price": 142.30,
            "currency": "GBP",
            "transit": 2,
            "service": {
                "code": "TELESHIP-EXPEDITED-PICKUP",
                "name": "Teleship Expedited Pickup"
            },
            "charges": [
                {
                    "name": "Base Freight",
                    "amount": 105.00,
                    "rate": 105.00,
                    "currency": "GBP"
                },
                {
                    "name": "Fuel Surcharge",
                    "amount": 15.75,
                    "rate": 0.15,
                    "currency": "GBP"
                },
                {
                    "name": "Pickup Fee",
                    "amount": 12.00,
                    "rate": 12.00,
                    "currency": "GBP"
                },
                {
                    "name": "Customs Clearance",
                    "amount": 9.55,
                    "rate": 9.55,
                    "currency": "GBP"
                }
            ],
            "estimatedDelivery": "2025-01-19T00:00:00.000Z"
        }
    ],
    "commodities": [
        {
            "itemNumber": 1,
            "title": "Electronic Widget",
            "charges": [
                {
                    "name": "Duty",
                    "amount": 15.00,
                    "rate": 0.10,
                    "currency": "GBP"
                },
                {
                    "name": "VAT",
                    "amount": 33.00,
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
            "message": "Invalid shipment data",
            "details": [
                "Weight exceeds maximum for selected service",
                "Postal code format invalid for destination country"
            ]
        }
    ]
}"""

ParsedRateResponse = [
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "service": "teleship_expedited_dropoff",
            "total_charge": 106.56,
            "currency": "GBP",
            "transit_days": 3,
            "extra_charges": [
                {"name": "Base Freight", "amount": 85.0, "currency": "GBP"},
                {"name": "Fuel Surcharge", "amount": 12.75, "currency": "GBP"},
                {"name": "Customs Clearance", "amount": 8.81, "currency": "GBP"},
            ],
            "meta": {
                "service_name": "teleship_expedited_dropoff",
                "estimated_delivery": "2025-12-10",
            },
        },
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "service": "teleship_standard_dropoff",
            "total_charge": 78.95,
            "currency": "GBP",
            "transit_days": 7,
            "extra_charges": [
                {"name": "Base Freight", "amount": 65.0, "currency": "GBP"},
                {"name": "Fuel Surcharge", "amount": 9.75, "currency": "GBP"},
                {"name": "Customs Clearance", "amount": 4.2, "currency": "GBP"},
            ],
            "meta": {
                "service_name": "teleship_standard_dropoff",
                "estimated_delivery": "2025-01-27",
            },
        },
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "service": "teleship_expedited_pickup",
            "total_charge": 142.3,
            "currency": "GBP",
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base Freight", "amount": 105.0, "currency": "GBP"},
                {"name": "Fuel Surcharge", "amount": 15.75, "currency": "GBP"},
                {"name": "Pickup Fee", "amount": 12.0, "currency": "GBP"},
                {"name": "Customs Clearance", "amount": 9.55, "currency": "GBP"},
            ],
            "meta": {
                "service_name": "teleship_expedited_pickup",
                "estimated_delivery": "2025-01-19",
            },
        },
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "code": "400",
            "message": "Invalid shipment data",
            "details": {
                "timestamp": "2025-01-15T10:30:45Z",
                "details": [
                    "Weight exceeds maximum for selected service",
                    "Postal code format invalid for destination country",
                ],
            },
        }
    ],
]
