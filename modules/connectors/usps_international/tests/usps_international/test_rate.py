import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging as logger

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUSPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments/v3/options/search",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "company_name": "ABC Corp.",
        "address_line1": "1098 N Fraser Street",
        "city": "Georgetown",
        "postal_code": "29440",
        "country_code": "US",
        "person_name": "Tall Tom",
        "phone_number": "8005554526",
        "state_code": "SC",
    },
    "recipient": {
        "company_name": "Coffee Five",
        "address_line1": "R. da Quitanda, 86 - quiosque 01",
        "city": "Centro",
        "postal_code": "29440",
        "country_code": "BR",
        "person_name": "John",
        "phone_number": "8005554526",
        "state_code": "Rio de Janeiro",
    },
    "parcels": [
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "options": {
        "usps_mail_class": "usps_first_class_package_international_service",
        "usps_label_delivery_service": True,
        "usps_return_receipt": True,
        "usps_price_type": "RETAIL",
        "shipment_date": "2024-07-28",
    },
    "services": [],
    "reference": "REF-001",
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [
                {"amount": 31.95, "currency": "USD", "name": "Base Price"},
                {
                    "amount": 0.0,
                    "currency": "USD",
                    "name": "Class 7 Radioactive Materials Package",
                },
            ],
            "meta": {
                "rate_zone": "20",
                "service_name": "USPS FIRST CLASS PACKAGE INTERNATIONAL SERVICE MACHINABLE ISC SINGLE PIECE",
                "usps_mail_class": "FIRST-CLASS_PACKAGE_INTERNATIONAL_SERVICE",
                "usps_optimal_dimensional_weight": 0,
                "usps_price_type": "RETAIL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SP",
                "usps_zone": "20",
            },
            "service": "usps_first_class_package_international_service_machinable_isc_single_piece",
            "total_charge": 31.95,
        }
    ],
    [],
]

RateRequest = [
    {
        "destinationCountryCode": "BR",
        "foreignPostalCode": "29440",
        "originZIPCode": "29440",
        "packageDescription": {
            "extraServices": [955],
            "girth": 124.0,
            "height": 19.69,
            "length": 19.69,
            "mailClass": "FIRST-CLASS_PACKAGE_INTERNATIONAL_SERVICE",
            "mailingDate": "2024-07-28",
            "weight": 44.1,
            "width": 4.72,
        },
        "pricingOptions": [
            {
                "paymentAccount": {
                    "accountNumber": "Your Account Number",
                    "accountType": "EPS",
                },
                "priceType": "RETAIL",
            }
        ],
        "shippingFilter": "PRICE",
    }
]


RateResponse = """{
  "originZIPCode": "10001",
  "foreignPostalCode": "W1A 1AA",
  "destinationCountryCode": "GB",
  "pricingOptions": [
    {
      "shippingOptions": [
        {
          "mailClass": "FIRST-CLASS_PACKAGE_INTERNATIONAL_SERVICE",
          "rateOptions": [
            {
              "totalPrice": 31.95,
              "totalBasePrice": 31.95,
              "rates": [
                {
                  "description": "First-Class Package International Service Machinable ISC Single-piece",
                  "startDate": "2025-01-19",
                  "endDate": "",
                  "price": 31.95,
                  "zone": "20",
                  "weight": 1.2,
                  "dimensionalWeight": 0,
                  "dimWeight": 0,
                  "fees": [],
                  "priceType": "RETAIL",
                  "mailClass": "FIRST-CLASS_PACKAGE_INTERNATIONAL_SERVICE",
                  "productName": "",
                  "productDefinition": "",
                  "processingCategory": "MACHINABLE",
                  "rateIndicator": "SP",
                  "destinationEntryFacilityType": "INTERNATIONAL_SERVICE_CENTER",
                  "SKU": "IFXP0XXXXR20200"
                }
              ],
              "extraServices": [
                {
                  "name": "Class 7 Radioactive Materials Package",
                  "price": 0,
                  "extraService": "813",
                  "priceType": "COMMERCIAL",
                  "warnings": [],
                  "SKU": "NA"
                }
              ]
            }
          ]
        }
      ],
      "priceType": "RETAIL",
      "paymentAccount": {
        "accountType": "EPS",
        "accountNumber": "1000115566"
      }
    }
  ]
}
"""
