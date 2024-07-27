import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
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
                f"{gateway.settings.server_url}",
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
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "person_name": "TEST USER",
        "state_code": "WA",
        "email": "test@gmail.com",
        "phone_number": "(07) 3114 1499",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "k1k 4t3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
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
    "options": {},
    "reference": "REF-001",
}

ParsedRateResponse = []


RateRequest = {
    "originZIPCode": "string",
    "destinationZIPCode": "string",
    "weight": 5,
    "length": 0,
    "width": 0,
    "height": 0,
    "mailClass": "PARCEL_SELECT",
    "mailClasses": ["USPS_GROUND_ADVANTAGE", "USPS_RETAIL_GROUND"],
    "priceType": "RETAIL",
    "mailingDate": "2021-07-01",
    "accountType": "EPS",
    "accountNumber": "string",
    "itemValue": 0,
    "extraServices": [415],
}


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
          "mailClass": "string",
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
