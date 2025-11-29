"""Teleship carrier pickup tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTeleshipPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)

        self.assertEqual(lib.to_dict(request.serialize()), PickupRequest)

    def test_schedule_pickup(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/pickups",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_create_pickup_cancel_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)

        self.assertEqual(lib.to_dict(request.serialize()), PickupCancelRequest)

    def test_cancel_pickup(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/pickups/PKP-12345/cancel",
            )

    def test_parse_pickup_cancel_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = PickupCancelResponse
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupCancelResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "pickup_date": "2025-01-20",
    "ready_time": "2025-01-20T09:00:00",
    "closing_time": "2025-01-20T18:00:00",
    "instruction": "Ring doorbell for pickup",
    "shipment_identifiers": ["SHP-UK-US-98765", "SHP-UK-US-98766"],
    "address": {
        "address_line1": "123 Business Park",
        "city": "London",
        "postal_code": "SW1A 1AA",
        "country_code": "GB",
        "state_code": "LDN",
        "person_name": "John Smith",
        "company_name": "UK Exports Ltd",
        "phone_number": "+442071234567",
        "email": "shipping@ukexports.co.uk",
    },
}

PickupCancelPayload = {"confirmation_number": "PKP-12345"}

PickupRequest = {
    "address": {
        "address": {
            "city": "London",
            "country": "GB",
            "line1": "123 Business Park",
            "postcode": "SW1A 1AA",
            "state": "LDN",
        },
        "company": "UK Exports Ltd",
        "email": "shipping@ukexports.co.uk",
        "name": "John Smith",
        "phone": "+442071234567",
    },
    "endAt": "2025-01-20T18:00:00",
    "reference": "Ring doorbell for pickup",
    "shipmentIds": ["SHP-UK-US-98765", "SHP-UK-US-98766"],
    "startAt": "2025-01-20",
}

PickupCancelRequest = {"pickupId": "PKP-12345"}

PickupResponse = """{
    "pickup": {
        "id": "PKP-12345",
        "status": "scheduled",
        "startAt": "2025-01-20T09:00:00.000Z",
        "endAt": "2025-01-20T18:00:00.000Z",
        "address": {
            "name": "John Smith",
            "company": "UK Exports Ltd",
            "phone": "+442071234567",
            "email": "shipping@ukexports.co.uk",
            "address": {
                "line1": "123 Business Park",
                "city": "London",
                "state": "LDN",
                "postcode": "SW1A 1AA",
                "country": "GB"
            }
        },
        "reference": "Ring doorbell for pickup",
        "createdAt": "2025-01-15T10:30:00.000Z"
    }
}"""

PickupCancelResponse = """{
    "success": true,
    "message": "Pickup cancelled successfully"
}"""

ErrorResponse = """{
    "messages": [
        {
            "code": 400,
            "timestamp": "2025-01-15T10:30:45Z",
            "message": "Invalid pickup request",
            "details": [
                "Pickup date must be in the future",
                "At least one shipment ID is required"
            ]
        }
    ]
}"""

ParsedPickupResponse = [
    {
        "carrier_id": "teleship",
        "carrier_name": "teleship",
        "confirmation_number": "PKP-12345",
        "meta": {
            "address": {
                "address": {
                    "city": "London",
                    "country": "GB",
                    "line1": "123 Business Park",
                    "postcode": "SW1A 1AA",
                    "state": "LDN",
                },
                "company": "UK Exports Ltd",
                "email": "shipping@ukexports.co.uk",
                "name": "John Smith",
                "phone": "+442071234567",
            },
            "createdAt": "2025-01-15T10:30:00.000Z",
            "endAt": "2025-01-20T18:00:00.000Z",
            "id": "PKP-12345",
            "reference": "Ring doorbell for pickup",
            "startAt": "2025-01-20T09:00:00.000Z",
            "status": "scheduled",
        },
        "pickup_date": "2025-01-20",
    },
    [],
]

ParsedPickupCancelResponse = [
    {
        "carrier_id": "teleship",
        "carrier_name": "teleship",
        "success": True,
        "operation": "pickup_cancellation",
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "code": "400",
            "message": "Invalid pickup request",
            "details": {
                "timestamp": "2025-01-15T10:30:45Z",
                "details": [
                    "Pickup date must be in the future",
                    "At least one shipment ID is required",
                ],
            },
        }
    ],
]
