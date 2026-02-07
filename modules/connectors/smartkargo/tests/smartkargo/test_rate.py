"""SmartKargo carrier rate tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSmartKargoRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        serialized = request.serialize()
        # Check key fields are present
        self.assertIn("reference", serialized)
        self.assertIn("packages", serialized)
        self.assertEqual(len(serialized["packages"]), 1)
        self.assertEqual(serialized["packages"][0]["grossWeightUnitMeasure"], "KG")

    def test_get_rates(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/quotation"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            # Should have 3 rates
            self.assertEqual(len(parsed_response[0]), 3)
            # Check first rate
            self.assertEqual(parsed_response[0][0].service, "smartkargo_express")
            self.assertEqual(parsed_response[0][0].transit_days, 3)

    def test_parse_error_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            # No rates when error
            self.assertEqual(len(parsed_response[0]), 0)
            # Should have error messages
            self.assertTrue(len(parsed_response[1]) > 0)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "address_line1": "1 Broadway",
        "city": "Boston",
        "postal_code": "02142",
        "country_code": "US",
        "state_code": "MA",
        "person_name": "TESTER TEST",
        "company_name": "Test Company",
        "phone_number": "19999999999",
        "email": "test@test.com"
    },
    "recipient": {
        "address_line1": "124 Main St",
        "city": "Los Angeles",
        "postal_code": "98148",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Tester Tester",
        "phone_number": "8888347867",
        "email": "test2@test.com"
    },
    "parcels": [{
        "weight": 10.0,
        "width": 20.0,
        "height": 20.0,
        "length": 20.0,
        "weight_unit": "KG",
        "dimension_unit": "CM",
        "reference_number": "PKG-TEST-001",
    }],
    "reference": "RATE-REQ-001",
}

RateResponse = """{
  "headerReference": "30068480254",
  "packageReference": "PKG-36780746",
  "status": "Quoted",
  "details": [
    {
      "slaInDays": 3,
      "deliveryDateBasedOnShipment": "2021-06-07T21:00:00+00:00",
      "serviceType": "EXP",
      "total": 12.00,
      "totalTax": 1.15
    },
    {
      "slaInDays": 5,
      "deliveryDateBasedOnShipment": "2021-06-09T21:00:00+00:00",
      "serviceType": "EPR",
      "total": 10.00,
      "totalTax": 1.19
    },
    {
      "slaInDays": 6,
      "deliveryDateBasedOnShipment": "2021-06-10T21:00:00+00:00",
      "serviceType": "EST",
      "total": 8.00,
      "totalTax": 1.15
    }
  ],
  "validations": null
}"""

ErrorResponse = """{
  "status": "Failed",
  "validations": [
    {
      "code": "VAL001",
      "message": "Invalid origin address"
    }
  ]
}"""
