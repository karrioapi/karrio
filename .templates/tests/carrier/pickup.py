import logging
import unittest
from unittest.mock import patch
import purplship
from purplship.core.utils import DP
from purplship.core.models import (
    PickupRequest,
    PickupUpdateRequest,
    PickupCancelRequest,
)
from tests.carrier.fixture import gateway

logger = logging.getLogger(__name__)


class TestCarrierPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**pickup_data)
        self.PickupUpdateRequest = PickupUpdateRequest(**pickup_update_data)
        self.PickupCancelRequest = PickupCancelRequest(**pickup_cancel_data)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)

        self.assertEqual(request.serialize(), PickupRequestXML)

    def test_create_modify_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)

        self.assertEqual(request.serialize(), PickupUpdateRequestXML)

    def test_create_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)

        self.assertEqual(request.serialize(), PickupCancelRequestXML)

    def test_request_pickup(self):
        with patch("purplship.mappers.carrier.proxy.http") as mock:
            mock.return_value = "<a></a>"
            purplship.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_modify_pickup(self):
        with patch("purplship.mappers.carrier.proxy.http") as mocks:
            mocks.side_effect = [
                PickupResponseXML,
            ]
            purplship.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            cancel_call, *_ = mocks.call_args_list

            self.assertEqual(
                cancel_call[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_pickup(self):
        with patch("purplship.mappers.carrier.proxy.http") as mock:
            mock.return_value = "<a></a>"
            purplship.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_request_pickup_response(self):
        with patch("purplship.mappers.carrier.proxy.http") as mock:
            mock.return_value = PickupResponseXML
            parsed_response = (
                purplship.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(ParsedPickupResponse))

    def test_parse_modify_pickup_response(self):
        with patch("purplship.mappers.carrier.proxy.http") as mocks:
            mocks.side_effect = [
                PickupResponseXML,
            ]
            parsed_response = (
                purplship.Pickup.update(self.PickupUpdateRequest).from_(gateway).parse()
            )

            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(ParsedPickupResponse))

    def test_parse_void_shipment_response(self):
        with patch("purplship.mappers.carrier.proxy.http") as mock:
            mock.return_value = PickupCancelResponseXML
            parsed_response = (
                purplship.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedPickupCancelResponse)
            )


if __name__ == "__main__":
    unittest.main()

pickup_data = {
    "pickup_date": "2015-01-28",
    "address": {
        "company_name": "Jim Duggan",
        "address_line1": "2271 Herring Cove",
        "city": "Halifax",
        "postal_code": "B3L2C2",
        "country_code": "CA",
        "person_name": "John Doe",
        "phone_number": "1 514 5555555",
        "state_code": "NS",
        "residential": True,
        "email": "john.doe@carrier.ca",
    },
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
}

pickup_update_data = {
    "confirmation_number": "10000696",
    "pickup_date": "2015-01-28",
    "address": {
        "person_name": "Jane Doe",
        "email": "john.doe@carrier.ca",
        "phone_number": "1 514 5555555",
    },
    "parcels": [{"weight": 4, "weight_unit": "KG"}],
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
    "options": {"LoadingDockAvailable": False, "TrailerAccessible": False},
}

pickup_cancel_data = {"confirmation_number": "10000696"}

ParsedPickupResponse = [
    {
        "carrier_id": "carrier",
        "carrier_name": "carrier",
        "confirmation_number": "10000696",
        "pickup_date": "2015-01-28 15:00:00",
    },
    [],
]

ParsedPickupCancelResponse = [
    {
        "carrier_id": "carrier",
        "carrier_name": "carrier",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupRequestXML = """
"""

PickupUpdateRequestXML = """
"""

PickupCancelRequestXML = """
"""

PickupCancelResponseXML = """
"""

PickupResponseXML = """
"""
