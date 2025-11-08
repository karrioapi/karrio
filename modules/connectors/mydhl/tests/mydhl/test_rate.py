"""MyDHL carrier rate tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestMyDHLRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rates"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
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


RatePayload = {
    "shipper": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "parcels": [{
        "weight": 10.0,
        "width": 10.0,
        "height": 10.0,
        "length": 10.0,
        "weight_unit": "KG",
        "dimension_unit": "CM",
        "packaging_type": "BOX"
    }]
}

RateRequest = {
    "customerDetails": {
        "shipperDetails": {
            "postalCode": "12345",
            "cityName": "Test City",
            "countryCode": "US"
        },
        "receiverDetails": {
            "postalCode": "12345",
            "cityName": "Test City",
            "countryCode": "US"
        }
    },
    "accounts": [
        {
            "typeCode": "shipper",
            "number": 123456789
        }
    ],
    "productCode": None,
    "plannedShippingDateAndTime": ANY,
    "unitOfMeasurement": "metric",
    "isCustomsDeclarable": False,
    "packages": [
        {
            "typeCode": None,
            "weight": 10.0,
            "dimensions": {
                "length": 10,
                "width": 10,
                "height": 10
            }
        }
    ]
}

RateResponse = """{
  "products": [
    {
      "productName": "EXPRESS WORLDWIDE",
      "productCode": "P",
      "localProductCode": "P",
      "networkTypeCode": "TD",
      "isCustomerAgreement": false,
      "totalPrice": [
        {
          "currencyType": "BILLC",
          "priceCurrency": "USD",
          "price": 25.99
        }
      ],
      "totalPriceBreakdown": [
        {
          "currencyType": "BILLC",
          "priceCurrency": "USD",
          "priceBreakdown": [
            {
              "typeCode": "SPRQT",
              "price": 23.50
            }
          ]
        }
      ],
      "deliveryCapabilities": {
        "deliveryTypeCode": "QDDC",
        "estimatedDeliveryDateAndTime": "2024-01-15T17:00:00"
      }
    },
    {
      "productName": "EXPRESS 12:00",
      "productCode": "Y",
      "localProductCode": "Y",
      "networkTypeCode": "TD",
      "isCustomerAgreement": false,
      "totalPrice": [
        {
          "currencyType": "BILLC",
          "priceCurrency": "USD",
          "price": 35.99
        }
      ],
      "deliveryCapabilities": {
        "estimatedDeliveryDateAndTime": "2024-01-14T12:00:00"
      }
    }
  ]
}"""

ErrorResponse = """{
  "status": 400,
  "title": "Bad Request",
  "detail": "Invalid postal code provided",
  "instance": "/rates"
}"""

ParsedRateResponse = [
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "service": "P",
            "currency": "USD",
            "total_charge": "25.99",
            "transit_days": ANY,
            "extra_charges": [
                {
                    "name": "SPRQT",
                    "amount": "23.50",
                    "currency": "USD"
                }
            ],
            "meta": {
                "service_name": "EXPRESS WORLDWIDE",
                "network_type_code": "TD",
                "local_product_code": "P"
            }
        },
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "service": "Y",
            "currency": "USD",
            "total_charge": "35.99",
            "transit_days": ANY,
            "extra_charges": None,
            "meta": {
                "service_name": "EXPRESS 12:00",
                "network_type_code": "TD",
                "local_product_code": "Y"
            }
        }
    ],
    []
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "code": "400",
            "message": "Invalid postal code provided",
            "details": {
                "instance": "/rates",
                "title": "Bad Request"
            }
        }
    ]
]