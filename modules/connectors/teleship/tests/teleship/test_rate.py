"""Teleship carrier rate tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestTeleshipRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/rates/quotes"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


# 1. Karrio Input Payload
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
        "email": "shipping@ukexports.co.uk"
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
        "email": "receiving@usimports.com"
    },
    "parcels": [
        {
            "weight": 1.2,
            "width": 20.0,
            "height": 15.0,
            "length": 30.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "packaging_type": "parcel"
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
                "origin_country": "GB"
            }
        ],
        "options": {
            "eori_number": "GB123456789000"
        }
    }
}

# 2. Carrier Request Format (from generated schemas)
RateRequest = {
    "customerReference": "UK-US-12345",
    "packageType": "parcel",
    "shipTo": {
        "name": "Jane Doe",
        "email": "receiving@usimports.com",
        "phone": "+13105551234",
        "address": {
            "line1": "555 Industrial Blvd",
            "city": "Los Angeles",
            "state": "CA",
            "postcode": "90001",
            "country": "US"
        }
    },
    "shipFrom": {
        "name": "John Smith",
        "company": "UK Exports Ltd",
        "address": {
            "line1": "123 Business Park",
            "city": "London",
            "state": "LDN",
            "postcode": "SW1A 1AA",
            "country": "GB"
        }
    },
    "weight": {
        "value": 1.2,
        "unit": "KG"
    },
    "dimensions": {
        "unit": "CM",
        "length": 30,
        "width": 20,
        "height": 15
    },
    "commodities": [
        {
            "sku": "WIDGET-001",
            "title": "Electronic Widget",
            "value": {
                "amount": 150,
                "currency": "GBP"
            },
            "quantity": 2,
            "unitWeight": {
                "value": 0.6,
                "unit": "KG"
            },
            "description": "Consumer electronics widget",
            "countryOfOrigin": "GB"
        }
    ],
    "customs": {
        "EORI": "GB123456789000",
        "contentType": "merchandise",
        "invoiceDate": "2025-01-15",
        "invoiceNumber": "INV-2025-001"
    }
}

# 3. Carrier Response Mock (actual API format)
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
            "estimatedDelivery": "2025-01-20"
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
            "estimatedDelivery": "2025-01-27"
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
            "estimatedDelivery": "2025-01-19"
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

# 4. Error Response Mock
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

# 5. Parsed Success Response (Karrio format)
ParsedRateResponse = [
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "service": "TELESHIP-EXPEDITED-DROPOFF",
            "total_charge": 106.56,
            "currency": "GBP",
            "transit_days": 3,
            "extra_charges": [
                {
                    "name": "Base Freight",
                    "amount": 85.0,
                    "currency": "GBP"
                },
                {
                    "name": "Fuel Surcharge",
                    "amount": 12.75,
                    "currency": "GBP"
                },
                {
                    "name": "Customs Clearance",
                    "amount": 8.81,
                    "currency": "GBP"
                }
            ],
            "meta": {
                "service_name": "Teleship Expedited Drop-off",
                "estimated_delivery": "2025-01-20"
            }
        },
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "service": "TELESHIP-STANDARD-DROPOFF",
            "total_charge": 78.95,
            "currency": "GBP",
            "transit_days": 7,
            "extra_charges": [
                {
                    "name": "Base Freight",
                    "amount": 65.0,
                    "currency": "GBP"
                },
                {
                    "name": "Fuel Surcharge",
                    "amount": 9.75,
                    "currency": "GBP"
                },
                {
                    "name": "Customs Clearance",
                    "amount": 4.2,
                    "currency": "GBP"
                }
            ],
            "meta": {
                "service_name": "Teleship Standard Drop-off",
                "estimated_delivery": "2025-01-27"
            }
        },
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "service": "TELESHIP-EXPEDITED-PICKUP",
            "total_charge": 142.3,
            "currency": "GBP",
            "transit_days": 2,
            "extra_charges": [
                {
                    "name": "Base Freight",
                    "amount": 105.0,
                    "currency": "GBP"
                },
                {
                    "name": "Fuel Surcharge",
                    "amount": 15.75,
                    "currency": "GBP"
                },
                {
                    "name": "Pickup Fee",
                    "amount": 12.0,
                    "currency": "GBP"
                },
                {
                    "name": "Customs Clearance",
                    "amount": 9.55,
                    "currency": "GBP"
                }
            ],
            "meta": {
                "service_name": "Teleship Expedited Pickup",
                "estimated_delivery": "2025-01-19"
            }
        }
    ],
    []
]

# 6. Parsed Error Response
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
                    "Postal code format invalid for destination country"
                ]
            }
        }
    ]
]
