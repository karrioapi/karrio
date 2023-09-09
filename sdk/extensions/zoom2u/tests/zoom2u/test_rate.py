import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestZoom2uRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {}

ParsedRateResponse = []


RateRequest = {
    "PurchaseOrderNumber": "ABCD1234",
    "PackageDescription": "1 box with some cakes",
    "DeliverySpeed": "VIP",
    "ReadyDateTime": "2020-12-24T10:20:00.06Z",
    "VehicleType": "Car",
    "PackageType": "Box",
    "Pickup": {
        "ContactName": "John Smith",
        "Email": "test@test.com",
        "Phone": "0000 0000",
        "UnitNumber": "",
        "StreetNumber": "123",
        "Street": "Main St",
        "Suburb": "North Sydney",
        "State": "NSW",
        "Postcode": "2000",
        "Country": "Australia",
        "Notes": "",
    },
    "Dropoff": {
        "ContactName": "Jane Smith",
        "Email": "test@test.com",
        "Phone": "0000 0000",
        "UnitNumber": "ACME Co.",
        "StreetNumber": "123",
        "Street": "Main St",
        "Suburb": "North Sydney",
        "State": "NSW",
        "Postcode": "2000",
        "Country": "Australia",
        "Notes": "",
    },
}


RateResponse = """[
  {
    "deliverySpeed": "Same day",
    "price": 68,
    "deliveredBy": "2020-12-25T06:00:00Z",
    "earliestPickupEta": "2020-12-24T11:20:00Z",
    "earliestDropEta": "2020-12-24T11:20:00Z"
  },
  {
    "deliverySpeed": "Same day",
    "price": 68,
    "deliveredBy": "2020-12-25T09:30:00Z"
  },
  {
    "deliverySpeed": "3 hour",
    "price": 86,
    "deliveredBy": "2020-12-25T01:00:00Z"
  },
  {
    "deliverySpeed": "VIP",
    "price": 159,
    "deliveredBy": "2020-12-24T11:20:00Z"
  }
]
"""
