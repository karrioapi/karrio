"""SmartKargo carrier rate tests."""

import unittest
from unittest.mock import patch
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
        # Per-package pattern: serialize returns a list of requests
        self.assertIsInstance(serialized, list)
        self.assertEqual(len(serialized), 1)
        self.assertIn("reference", serialized[0])
        self.assertIn("packages", serialized[0])
        self.assertEqual(len(serialized[0]["packages"]), 1)
        self.assertEqual(serialized[0]["packages"][0]["grossWeightUnitMeasure"], "KG")

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
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedRateResponse,
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedErrorResponse,
            )


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

ParsedRateResponse = [
    [
        {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "currency": "USD",
            "extra_charges": [
                {"amount": 12.0, "currency": "USD", "name": "Base Rate"},
                {"amount": 1.15, "currency": "USD", "name": "Tax"},
            ],
            "meta": {
                "estimated_delivery": "2021-06-07T21:00:00+00:00",
                "service_name": "smartkargo_express",
                "service_type": "EXP",
            },
            "service": "smartkargo_express",
            "total_charge": 13.15,
            "transit_days": 3,
        },
        {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "currency": "USD",
            "extra_charges": [
                {"amount": 10.0, "currency": "USD", "name": "Base Rate"},
                {"amount": 1.19, "currency": "USD", "name": "Tax"},
            ],
            "meta": {
                "estimated_delivery": "2021-06-09T21:00:00+00:00",
                "service_name": "smartkargo_priority",
                "service_type": "EPR",
            },
            "service": "smartkargo_priority",
            "total_charge": 11.19,
            "transit_days": 5,
        },
        {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "currency": "USD",
            "extra_charges": [
                {"amount": 8.0, "currency": "USD", "name": "Base Rate"},
                {"amount": 1.15, "currency": "USD", "name": "Tax"},
            ],
            "meta": {
                "estimated_delivery": "2021-06-10T21:00:00+00:00",
                "service_name": "smartkargo_standard",
                "service_type": "EST",
            },
            "service": "smartkargo_standard",
            "total_charge": 9.15,
            "transit_days": 6,
        },
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "code": "VAL001",
            "details": {},
            "message": "Invalid origin address",
        },
    ],
]
