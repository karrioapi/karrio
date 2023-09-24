import unittest
import urllib.parse
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAsendiaUSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/A1/v1.0/ShippingPlatform/ShippingRate?{urllib.parse.urlencode(lib.to_dict(RateRequest))}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {"postal_code": "44106", "country_code": "US"},
    "recipient": {"postal_code": "20770", "country_code": "US"},
    "parcels": [
        {
            "width": 5,
            "height": 5,
            "length": 3,
            "weight": 1.0,
            "weight_unit": "LB",
            "dimension_unit": "IN",
        }
    ],
    "options": {
        "asendia_us_processing_location": "SFO",
    },
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "asendia_us",
            "carrier_name": "asendia_us",
            "currency": "string",
            "meta": {"service_name": "string"},
            "service": "string",
            "total_charge": 0.0,
        }
    ],
    [
        {
            "carrier_id": "asendia_us",
            "carrier_name": "asendia_us",
            "code": "Continue",
            "details": {},
            "message": "string",
        }
    ],
]


RateRequest = {
    "accountNumber": "account_number",
    "processingLocation": "SFO",
    "recipientPostalCode": "20770",
    "recipientCountryCode": "US",
    "totalPackageWeight": 1.0,
    "weightUnit": "Lb",
    "dimLength": 3.0,
    "dimWidth": 5.0,
    "dimHeight": 5.0,
    "dimUnit": "IN",
    "productCode": "*",
}

RateResponse = """{
  "shippingRates": [
    {
      "productCode": "string",
      "rate": 0.0,
      "currencyType": "string"
    }
  ],
  "responseStatus": {
    "responseStatusCode": "Continue",
    "responseStatusMessage": "string"
  }
}
"""
