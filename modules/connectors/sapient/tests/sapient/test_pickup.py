import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSAPIENTPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupUpdateRequest = models.PickupUpdateRequest(**PickupUpdatePayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)

        self.assertEqual(request.serialize(), PickupRequest)

    def test_create_update_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)

        self.assertEqual(request.serialize(), PickupUpdateRequest)

    def test_create_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)

        self.assertEqual(request.serialize(), PickupCancelRequest)

    def test_create_pickup(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_pickup_response(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = PickupCancelResponse
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelPickupResponse
            )


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "pickup_date": "2013-10-19",
    "ready_time": "10:20",
    "closing_time": "09:20",
    "instruction": "behind the front desk",
    "address": {
        "company_name": "ABC Corp.",
        "address_line1": "1098 N Fraser Street",
        "city": "Georgetown",
        "postal_code": "29440",
        "country_code": "US",
        "person_name": "Tall Tom",
        "phone_number": "8005554526",
        "state_code": "SC",
    },
    "parcels": [{"weight": 20, "weight_unit": "LB"}],
    "options": {"usps_package_type": "FIRST-CLASS_PACKAGE_SERVICE"},
}

PickupUpdatePayload = {
    "confirmation_number": "0074698052",
    "pickup_date": "2013-10-19",
    "ready_time": "10:20",
    "closing_time": "09:20",
    "instruction": "behind the front desk",
    "address": {
        "company_name": "ABC Corp.",
        "address_line1": "1098 N Fraser Street",
        "city": "Georgetown",
        "postal_code": "29440",
        "country_code": "US",
        "person_name": "Tall Tom",
        "phone_number": "8005554526",
        "state_code": "SC",
    },
    "parcels": [{"weight": 20, "weight_unit": "LB"}],
    "options": {"usps_package_type": "FIRST-CLASS_PACKAGE_SERVICE"},
}

PickupCancelPayload = {"confirmation_number": "0074698052"}

ParsedPickupResponse = [
    {
        "carrier_id": "sapient",
        "carrier_name": "sapient",
        "confirmation_number": "string",
        "pickup_date": "2019-08-24",
    },
    [],
]

ParsedCancelPickupResponse = [
    {
        "carrier_id": "sapient",
        "carrier_name": "sapient",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupRequest = {
    "SlotReservationId": "1f3c991f-a6ff-4ffb-9292-17690d745992",
    "SlotDate": "2024-06-17",
    "BringMyLabel": False,
}


PickupUpdateRequest = {
    "SlotDate": "2024-06-17",
    "BringMyLabel": True,
}


PickupCancelRequest = {
    "shipmentId": "1f3c991f-a6ff-4ffb-9292-17690d745992",
}


PickupResponse = """{
  "CollectionOrderId": "CC-W307-028741033",
  "CollectionDate": "2023-07-04"
}
"""

PickupUpdateResponse = """{
  "CollectionOrderId": "CC-W307-028741033",
  "CollectionDate": "2023-07-04"
}
"""

PickupCancelResponse = """{"ok": true}
"""
