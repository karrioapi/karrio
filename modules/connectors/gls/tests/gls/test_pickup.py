"""GLS Group sporadic pickup tests."""

import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.sdk as karrio

from .fixture import gateway


class TestGLSGroupPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        request_dict = lib.to_dict(request.serialize())
        self.assertEqual(request_dict["ContactID"], "TEST_CONTACT_ID")
        self.assertEqual(request_dict["Product"], "PARCEL")
        self.assertEqual(request_dict["NumberOfParcels"], 1)
        self.assertIn("PreferredPickUpDate", request_dict)

    def test_schedule_pickup(self):
        with patch("karrio.mappers.gls.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.shipment_api_url}/rs/sporadiccollection",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.gls.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            pickup, _ = parsed_response
            self.assertIsNotNone(pickup)
            self.assertEqual(pickup.confirmation_number, "2025-01-15T14:00:00Z")


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "address": {
        "address_line1": "Rheinstrasse 7",
        "city": "Hueckelhoven",
        "postal_code": "41836",
        "country_code": "DE",
        "company_name": "JTL-Software-GmbH",
        "phone_number": "+4924332222",
    },
    "pickup_date": "2026-05-10",
    "ready_time": "10:00",
    "closing_time": "17:00",
    "parcels": [{"weight": 2.5, "weight_unit": "KG"}],
    "instruction": "Please collect from reception",
}

PickupResponse = """{"EstimatedPickUpDate":"2025-01-15T14:00:00Z"}"""
