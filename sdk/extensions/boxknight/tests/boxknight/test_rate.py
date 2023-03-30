import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestBoxKnightRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.boxknight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rates",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.boxknight.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {"postal_code": "H4R2A4", "country_code": "CA"},
    "recipient": {"postal_code": "H4X1Z5", "country_code": "CA"},
    "parcels": [
        {
            "height": 15.0,
            "length": 20.0,
            "width": 15.0,
            "weight": 1.5,
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "reference_number": "12345",
        }
    ],
}


ParsedRateResponse = [
    [
        {
            "carrier_id": "boxknight",
            "carrier_name": "boxknight",
            "currency": "CAD",
            "meta": {"service_name": "BoxKnight Next-Day Delivery"},
            "service": "boxknight_nextday",
            "total_charge": 10.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "boxknight",
            "carrier_name": "boxknight",
            "currency": "CAD",
            "meta": {"service_name": "BoxKnight Same-Day Delivery"},
            "service": "boxknight_sameday",
            "total_charge": 12.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "boxknight",
            "carrier_name": "boxknight",
            "currency": "CAD",
            "meta": {"service_name": "Boxknight Scheduled Delivery"},
            "service": "boxknight_scheduled",
            "total_charge": 12.0,
            "transit_days": 13,
        },
    ],
    [],
]


RateRequest = {
    "postalCode": "H4X1Z5",
    "originPostalCode": "H4R2A4",
    "packages": [
        {
            "refNumber": "12345",
            "weightOptions": {
                "weight": 1.5,
                "unit": "lb",
            },
            "sizeOptions": {
                "length": 20,
                "width": 15,
                "height": 15,
                "unit": "inch",
            },
        }
    ],
}

RateResponse = """[
    {
      "price": 10,
      "service": "NEXTDAY",
      "name": "BoxKnight Next-Day Delivery",
      "description": "Get your package the next opening day of the merchant (2019-10-30)",
      "estimateDay": "2019-10-30",
      "estimateFrom": "2019-10-30",
      "estimateTo": "2019-10-30"
    },
    {
      "price": 12,
      "service": "SAMEDAY",
      "name": "BoxKnight Same-Day Delivery",
      "description": "Get your package before the end of the day (2019-10-29)",
      "estimateDay": "2019-10-29",
      "estimateFrom": "2019-10-29",
      "estimateTo": "2019-10-29"
    },
    {
      "price": 12,
      "service": "SCHEDULED",
      "name": "Boxknight Scheduled Delivery",
      "description": "Get your package in a 3h window within the next 2 weeks (2019-10-29 to 2019-11-11)",
      "estimateDay": "2019-10-29 to 2019-11-11",
      "estimateFrom": "2019-10-29",
      "estimateTo": "2019-11-11"
    }
]
"""
