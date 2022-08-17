
import unittest
from unittest.mock import patch, ANY
from tests.ups_freight.fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUPSFreightPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**PickupPayload)
        self.PickupUpdateRequest = models.PickupUpdateRequest(**PickupUpdatePayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)

        self.assertEqual(request.serialize(), PickupRequest)

    def test_create_update_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)

        self.assertEqual(request.serialize(), PickupUpdateRequest)

    def test_create_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(
            self.PickupCancelRequest
        )

        self.assertEqual(request.serialize(), PickupCancelRequest)

    def test_create_pickup(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = ""
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelPickupResponse
            )


if __name__ == "__main__":
    unittest.main()


PickupPayload = {}

PickupUpdatePayload = {}

PickupCancelPayload = {"confirmation_number": "0074698052"}

ParsedPickupResponse = []

ParsedCancelPickupResponse = []


PickupRequest = {}

PickupUpdateRequest = {}

PickupCancelRequest = {}


PickupResponse = """{}
"""

PickupUpdateResponse = """{}
"""

PickupCancelResponse = """{}
"""
