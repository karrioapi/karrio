"""DPD Group carrier rating tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestDPDGroupRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rates"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
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


# Test Data

RatePayload = {
    "shipper": {
        "company_name": "Acme Corporation",
        "address_line1": "Main Street 123",
        "city": "Berlin",
        "postal_code": "12345",
        "country_code": "DE",
        "person_name": "John Shipper",
    },
    "recipient": {
        "company_name": "Doe Enterprises",
        "address_line1": "Oak Avenue 456",
        "city": "Munich",
        "postal_code": "54321",
        "country_code": "DE",
        "person_name": "Jane Recipient",
    },
    "parcels": [
        {
            "weight": 5.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "length": 30,
            "width": 20,
            "height": 15,
        }
    ],
    "services": ["dpd_group_classic", "dpd_group_express_12"],
}

RateRequest = {
    "shipperAddress": {
        "postalCode": "12345",
        "city": "Berlin",
        "country": "DE",
    },
    "receiverAddress": {
        "postalCode": "54321",
        "city": "Munich",
        "country": "DE",
    },
    "parcels": [
        {
            "weight": 5.0,
            "length": 30,
            "width": 20,
            "height": 15,
        }
    ],
    "productCodes": ["dpd_group_classic", "dpd_group_express_12"],
}

RateResponse = """{
  "rates": [
    {
      "productCode": "CL",
      "productName": "DPD Classic",
      "totalAmount": 25.99,
      "currency": "EUR",
      "transitDays": 2,
      "deliveryDate": "2024-01-17"
    },
    {
      "productCode": "E12",
      "productName": "DPD Express 12",
      "totalAmount": 32.50,
      "currency": "EUR",
      "transitDays": 1,
      "deliveryDate": "2024-01-16"
    }
  ]
}"""

ErrorResponse = """{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid postal code",
    "details": [
      {
        "field": "shipper.postalCode",
        "message": "Postal code format is invalid"
      }
    ]
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/v1.1/rates",
  "status": 400
}"""

ParsedRateResponse = [
    [
        {
            "carrier_id": "dpd_group",
            "carrier_name": "dpd_group",
            "service": "dpd_group_classic",
            "total_charge": 25.99,
            "currency": "EUR",
            "transit_days": 2,
            "meta": {
                "service_name": "CL",
                "product_code": "CL",
                "product_name": "DPD Classic",
                "delivery_date": "2024-01-17",
            },
        },
        {
            "carrier_id": "dpd_group",
            "carrier_name": "dpd_group",
            "service": "dpd_group_express_12",
            "total_charge": 32.50,
            "currency": "EUR",
            "transit_days": 1,
            "meta": {
                "service_name": "E12",
                "product_code": "E12",
                "product_name": "DPD Express 12",
                "delivery_date": "2024-01-16",
            },
        },
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "dpd_group",
            "carrier_name": "dpd_group",
            "code": "VALIDATION_ERROR",
            "message": "Invalid postal code",
            "details": {
                "details": [
                    {
                        "field": "shipper.postalCode",
                        "message": "Postal code format is invalid"
                    }
                ]
            }
        }
    ]
]
