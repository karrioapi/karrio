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
                f"{gateway.settings.server_url}/v4/collections/RM/fa3bb603-2687-4b38-ba18-3264208446c6",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.side_effect = [PickupCancelResponse, "{}"]
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v4/collections/RM/fa3bb603-2687-4b38-ba18-3264208446c6",
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v4/collections/RM/fa3bb603-2687-4b38-ba18-3264208446c6/cancel",
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
    "options": {
        "sapient_slot_reservation_id": "1f3c991f-a6ff-4ffb-9292-17690d745992",
        "sapient_shipment_id": "fa3bb603-2687-4b38-ba18-3264208446c6",
        "sapient_carrier_code": "RM",
    },
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
    "options": {
        "sapient_shipment_id": "fa3bb603-2687-4b38-ba18-3264208446c6",
        "sapient_carrier_code": "RM",
        "sapient_bring_my_label": True,
    },
}

PickupCancelPayload = {
    "confirmation_number": "0074698052",
    "options": {
        "sapient_shipment_id": "fa3bb603-2687-4b38-ba18-3264208446c6",
        "sapient_carrier_code": "RM",
    },
}

ParsedPickupResponse = [
    {
        "carrier_id": "sapient",
        "carrier_name": "sapient",
        "confirmation_number": "CC-W307-028741033",
        "pickup_date": "2023-07-04",
        "meta": {
            "sapient_shipment_id": "fa3bb603-2687-4b38-ba18-3264208446c6",
            "sapient_carrier_code": "RM",
        },
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
    "SlotDate": "2013-10-19",
    "BringMyLabel": False,
}


PickupUpdateRequest = {
    "SlotDate": "2013-10-19",
    "BringMyLabel": True,
}


PickupCancelRequest = {
    "carrier_code": "RM",
    "shipmentId": "fa3bb603-2687-4b38-ba18-3264208446c6",
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
