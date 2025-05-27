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
        self.MachinableRateRequest = models.RateRequest(**MachinableRatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments/v3/options/search",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_machinable_rate_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.MachinableRateRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), MachinableParsedRateResponse
            )


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
        "company_name": "Horizon",
        "address_line1": "1309 S Agnew Avenue",
        "address_line2": "Apt 303",
        "city": "Oklahoma City",
        "postal_code": "73108",
        "country_code": "US",
        "person_name": "Lina Smith",
        "phone_number": "+1 123 456 7890",
        "state_code": "OK",
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
        "usps_label_delivery_service": True,
        "usps_price_type": "COMMERCIAL",
        "shipment_date": "2024-07-28",
    },
    "services": ["usps_parcel_select"],
    "reference": "REF-001",
}

MachinableRatePayload = {
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
        "company_name": "Horizon",
        "address_line1": "1309 S Agnew Avenue",
        "address_line2": "Apt 303",
        "city": "Oklahoma City",
        "postal_code": "73108",
        "country_code": "US",
        "person_name": "Lina Smith",
        "phone_number": "+1 123 456 7890",
        "state_code": "OK",
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
        "shipment_date": "2024-07-28",
        "usps_machinable_piece": True,
    },
}


ParsedRateResponse = [
    [
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 5.82, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
                {"amount": 0.0, "currency": "USD", "name": "Global Direct Entry"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS LIBRARY MAIL MACHINABLE SINGLE PIECE",
                "usps_extra_services": [920, 365],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "LIBRARY_MAIL",
                "usps_optimal_dimensional_weight": 0,
                "usps_price_type": "RETAIL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SP",
                "usps_zone": "08",
            },
            "service": "usps_library_mail_machinable_single_piece",
            "total_charge": 5.82,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 5.82, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
                {"amount": 0.0, "currency": "USD", "name": "Global Direct Entry"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS LIBRARY MAIL NONSTANDARD SINGLE PIECE",
                "usps_extra_services": [920, 365],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "LIBRARY_MAIL",
                "usps_optimal_dimensional_weight": 0,
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "SP",
                "usps_zone": "08",
            },
            "service": "usps_library_mail_nonstandard_single_piece",
            "total_charge": 5.82,
        },
    ],
    [],
]

MachinableParsedRateResponse = [
    [
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 5.82, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
                {"amount": 0.0, "currency": "USD", "name": "Global Direct Entry"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS LIBRARY MAIL MACHINABLE SINGLE PIECE",
                "usps_extra_services": [920, 365],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "LIBRARY_MAIL",
                "usps_optimal_dimensional_weight": 0,
                "usps_price_type": "RETAIL",
                "usps_processing_category": "MACHINABLE",
                "usps_rate_indicator": "SP",
                "usps_zone": "08",
            },
            "service": "usps_library_mail_machinable_single_piece",
            "total_charge": 5.82,
        },
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 5.82, "currency": "USD", "name": "Base Price"},
                {"amount": 0.0, "currency": "USD", "name": "USPS Tracking"},
                {"amount": 0.0, "currency": "USD", "name": "Global Direct Entry"},
            ],
            "meta": {
                "rate_zone": "08",
                "service_name": "USPS LIBRARY MAIL NONSTANDARD SINGLE PIECE",
                "usps_extra_services": [920, 365],
                "usps_guaranteed_delivery": False,
                "usps_mail_class": "LIBRARY_MAIL",
                "usps_optimal_dimensional_weight": 0,
                "usps_price_type": "RETAIL",
                "usps_processing_category": "NONSTANDARD",
                "usps_rate_indicator": "SP",
                "usps_zone": "08",
            },
            "service": "usps_library_mail_nonstandard_single_piece",
            "total_charge": 5.82,
        },
    ],
    [],
]

RateRequest = [
    {
        "destinationEntryFacilityType": "NONE",
        "destinationZIPCode": "73108",
        "originZIPCode": "29440",
        "packageDescription": {
            "extraServices": [415],
            "height": 19.69,
            "length": 19.69,
            "mailClass": "PARCEL_SELECT",
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
                "priceType": "COMMERCIAL",
            }
        ],
        "shippingFilter": "PRICE",
    }
]

RateResponse = """{
  "originZIPCode": "10001",
  "destinationZIPCode": "90210",
  "pricingOptions": [
    {
      "shippingOptions": [
        {
          "mailClass": "LIBRARY_MAIL",
          "rateOptions": [
            {
              "commitment": {
                "name": "7 Days",
                "scheduleDeliveryDate": "2025-06-04",
                "guaranteedDelivery": false
              },
              "totalPrice": 5.82,
              "totalBasePrice": 5.82,
              "rates": [
                {
                  "description": "Library Mail Machinable Single-piece",
                  "startDate": "2025-01-19",
                  "endDate": "",
                  "price": 5.82,
                  "zone": "08",
                  "weight": 2.5,
                  "dimensionalWeight": 0,
                  "dimWeight": 0,
                  "fees": [],
                  "priceType": "RETAIL",
                  "mailClass": "LIBRARY_MAIL",
                  "productName": "",
                  "productDefinition": "",
                  "processingCategory": "MACHINABLE",
                  "rateIndicator": "SP",
                  "destinationEntryFacilityType": "NONE",
                  "SKU": "DLXX0XXXUR00030"
                }
              ],
              "extraServices": [
                {
                  "name": "USPS Tracking",
                  "price": 0,
                  "extraService": "920",
                  "priceType": "RETAIL",
                  "warnings": [],
                  "SKU": "DXTL0EXXXRX0000"
                },
                {
                  "name": "Global Direct Entry",
                  "price": 0,
                  "extraService": "365",
                  "priceType": "COMMERCIAL",
                  "warnings": [],
                  "SKU": "NA"
                }
              ]
            },
            {
              "commitment": {
                "name": "7 Days",
                "scheduleDeliveryDate": "2025-06-04",
                "guaranteedDelivery": false
              },
              "totalPrice": 5.82,
              "totalBasePrice": 5.82,
              "rates": [
                {
                  "description": "Library Mail Nonstandard Single-piece",
                  "startDate": "2025-01-19",
                  "endDate": "",
                  "price": 5.82,
                  "zone": "08",
                  "weight": 2.5,
                  "dimensionalWeight": 0,
                  "dimWeight": 0,
                  "fees": [],
                  "priceType": "RETAIL",
                  "mailClass": "LIBRARY_MAIL",
                  "productName": "",
                  "productDefinition": "",
                  "processingCategory": "NONSTANDARD",
                  "rateIndicator": "SP",
                  "destinationEntryFacilityType": "NONE",
                  "SKU": "DLXX0XXXUR00030"
                }
              ],
              "extraServices": [
                {
                  "name": "USPS Tracking",
                  "price": 0,
                  "extraService": "920",
                  "priceType": "RETAIL",
                  "warnings": [],
                  "SKU": "DXTL0EXXXRX0000"
                },
                {
                  "name": "Global Direct Entry",
                  "price": 0,
                  "extraService": "365",
                  "priceType": "COMMERCIAL",
                  "warnings": [],
                  "SKU": "NA"
                }
              ]
            }
          ]
        }
      ],
      "priceType": "RETAIL"
    }
  ]
}
"""
