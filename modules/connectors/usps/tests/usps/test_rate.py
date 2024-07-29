import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUSPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v3/total-rates/search",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            logger.debug(lib.to_dict(parsed_response))
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
        "usps_price_type": "RETAIL",
        "shipment_date": "2024-07-28",
    },
    "services": ["usps_parcel_select"],
    "reference": "REF-001",
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "extra_charges": [
                {"amount": 3.35, "currency": "USD", "name": "Base Charge"},
                {"amount": 3.35, "currency": "USD", "name": "string"},
                {"amount": 3.35, "currency": "USD", "name": "Adult Signature Required"},
            ],
            "meta": {"service_name": "usps_parcel_select", "zone": "01"},
            "service": "usps_parcel_select",
            "total_charge": 3.35,
        }
    ],
    [],
]


RateRequest = [
    {
        "accountNumber": "Your Account Number",
        "accountType": "EPS",
        "destinationZIPCode": "73108",
        "extraServices": [415],
        "height": 19.69,
        "length": 19.69,
        "mailClasses": ["PARCEL_SELECT"],
        "mailingDate": "2024-07-28",
        "originZIPCode": "29440",
        "priceType": "RETAIL",
        "weight": 44.1,
        "width": 4.72,
    }
]


RateResponse = """{
  "rateOptions": [
    {
      "totalBasePrice": 3.35,
      "rates": [
        {
          "SKU": "DPXX0XXXXX07200",
          "description": "string",
          "priceType": "RETAIL",
          "price": 3.35,
          "weight": 5,
          "dimWeight": 5,
          "fees": [
            {
              "name": "string",
              "SKU": "string",
              "price": 0
            }
          ],
          "startDate": "2021-07-16",
          "endDate": "2021-07-16",
          "mailClass": "PARCEL_SELECT",
          "zone": "01"
        }
      ],
      "extraServices": [
        {
          "extraService": "922",
          "name": "Adult Signature Required",
          "SKU": "DPXX0XXXXX07200",
          "priceType": "RETAIL",
          "price": 3.35,
          "warnings": [
            {
              "warningCode": "string",
              "warningDescription": "string"
            }
          ]
        }
      ],
      "totalPrice": 3.35
    }
  ]
}
"""
