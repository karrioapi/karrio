"""DPD Group carrier pickup tests."""

import unittest
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models
from unittest.mock import patch
from .fixture import gateway


class TestPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        self.assertEqual(lib.to_dict(request.serialize()), PickupRequest)

    def test_schedule_pickup(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups"
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.update(self.PickupRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups/123/update"
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups/123/cancel"
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "address": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "pickup_date": "2024-01-01",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "confirmation_number": "123"
}

PickupRequest = {
    "address": {
        "addressLine1": "123 Test Street",
        "city": "Test City",
        "postalCode": "12345",
        "countryCode": "US",
        "stateCode": "CA",
        "personName": "Test Person",
        "companyName": "Test Company",
        "phoneNumber": "1234567890",
        "email": "test@example.com"
    },
    "pickupDate": "2024-01-01",
    "readyTime": "09:00",
    "closingTime": "17:00"
}

PickupResponse = """{
  "confirmationNumber": "PICKUP123",
  "pickupDate": "2024-01-01",
  "readyTime": "09:00",
  "closingTime": "17:00",
  "status": "scheduled"
}"""

PickupUpdateResponse = """{
  "confirmationNumber": "PICKUP123",
  "pickupDate": "2024-01-02",
  "readyTime": "10:00",
  "closingTime": "18:00",
  "status": "updated"
}"""

PickupCancelResponse = """{
  "success": true,
  "message": "Pickup successfully cancelled"
}"""

ErrorResponse = """{
  "error": {
    "code": "pickup_error",
    "message": "Unable to schedule pickup",
    "details": "Invalid pickup date provided"
  }
}"""

ParsedPickupResponse = [
    {
        "carrier_id": "dpd_group",
        "carrier_name": "dpd_group",
        "confirmation_number": "PICKUP123",
        "pickup_date": "2024-01-01",
        "ready_time": "09:00",
        "closing_time": "17:00",
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "dpd_group",
            "carrier_name": "dpd_group",
            "code": "pickup_error",
            "message": "Unable to schedule pickup",
            "details": {
                "details": "Invalid pickup date provided"
            }
        }
    ]
]