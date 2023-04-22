import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestRoadieRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.roadie.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v1/estimates",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.roadie.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "street_number": "123",
        "address_line1": "Main Street",
        "city": "Atlanta",
        "state_code": "GA",
        "postal_code": "30305",
    },
    "recipient": {
        "address_line1": "456 Central Ave.",
        "city": "Atlanta",
        "state_code": "GA",
        "postal_code": "30308",
    },
    "parcels": [
        {
            "length": 1.0,
            "width": 1.0,
            "height": 1.0,
            "weight": 1.0,
            "dimension_unit": "IN",
            "weight_unit": "LB",
        }
    ],
    "options": {
        "pickup_after": "2019-01-01 13:00:00",
        "deliver_start": "2019-01-01 21:00:00",
        "deliver_end": "2019-01-01 23:00:00",
        "declared_value": 20.0,
    },
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "roadie",
            "carrier_name": "roadie",
            "currency": "USD",
            "extra_charges": [
                {"amount": 12.0, "currency": "USD", "name": "Base Price"}
            ],
            "meta": {
                "estimated_distance": 12.54,
                "service_name": "Roadie Local Delivery",
                "size": "large",
            },
            "service": "roadie_local_delivery",
            "total_charge": 12.0,
            "transit_days": 1,
        }
    ],
    [],
]


RateRequest = {
    "items": [
        {
            "length": 1.0,
            "width": 1.0,
            "height": 1.0,
            "weight": 1.0,
            "quantity": 1,
            "value": 20.0,
        }
    ],
    "pickup_location": {
        "address": {
            "street1": "123 Main Street",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30305",
        }
    },
    "delivery_location": {
        "address": {
            "street1": "456 Central Ave.",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30308",
        }
    },
    "pickup_after": "2019-01-01T13:00:00Z",
    "deliver_between": {"start": "2019-01-01T21:00:00Z", "end": "2019-01-01T23:00:00Z"},
}

RateResponse = """{
  "price": 12.00,
  "size": "large",
  "estimated_distance": 12.54
}
"""
