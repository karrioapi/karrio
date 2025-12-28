"""Hermes carrier pickup tests."""

import unittest
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models
from unittest.mock import patch, PropertyMock
from .fixture import gateway


class TestPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        self.assertEqual(lib.to_dict(request.serialize()), PickupRequest)

    def test_schedule_pickup(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                mock.return_value = "{}"
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway)
                self.assertEqual(
                    mock.call_args[1]["url"],
                    f"{gateway.settings.server_url}/pickuporders"
                )

    def test_cancel_pickup(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                mock.return_value = "{}"
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)
                self.assertEqual(
                    mock.call_args[1]["url"],
                    f"{gateway.settings.server_url}/pickuporders/12345678901"
                )

    def test_parse_pickup_response(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                mock.return_value = PickupResponse
                parsed_response = (
                    karrio.Pickup.schedule(self.PickupRequest)
                    .from_(gateway)
                    .parse()
                )
                self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_pickup_cancel_response(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                mock.return_value = PickupCancelResponse
                parsed_response = (
                    karrio.Pickup.cancel(self.PickupCancelRequest)
                    .from_(gateway)
                    .parse()
                )
                self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupCancelResponse)

    def test_parse_error_response(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
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
        "address_line1": "Essener Bogen 1",
        "city": "Hamburg",
        "postal_code": "22419",
        "country_code": "DE",
        "person_name": "Max Mustermann",
        "company_name": "Test Company",
        "phone_number": "+49401234567",
    },
    "pickup_date": "2025-01-15",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "parcels": [{"weight": 5.0}]
}

PickupCancelPayload = {
    "confirmation_number": "12345678901"
}

PickupRequest = {
    "pickupAddress": {
        "street": "Essener Bogen",
        "houseNumber": "1",
        "zipCode": "22419",
        "town": "Hamburg",
        "countryCode": "DE",
        "addressAddition": "Test Company"
    },
    "pickupName": {
        "firstname": "Max",
        "lastname": "Mustermann"
    },
    "phone": "+49401234567",
    "pickupDate": "2025-01-15",
    "pickupTimeSlot": "BETWEEN_10_AND_13",
    "parcelCount": {
        "pickupParcelCountXS": 0,
        "pickupParcelCountS": 0,
        "pickupParcelCountM": 1,
        "pickupParcelCountL": 0,
        "pickupParcelCountXL": 0
    }
}

PickupCancelRequest = {
    "pickupOrderID": "12345678901"
}

PickupResponse = """{
    "listOfResultCodes": [],
    "pickupOrderID": "12345678901"
}"""

PickupCancelResponse = """{
    "listOfResultCodes": [],
    "pickupOrderID": "12345678901"
}"""

ErrorResponse = """{
    "listOfResultCodes": [
        {
            "code": "e070",
            "message": "Unable to cancel the pickup order."
        }
    ]
}"""

ParsedPickupResponse = [
    {
        "carrier_id": "hermes",
        "carrier_name": "hermes",
        "confirmation_number": "12345678901"
    },
    []
]

ParsedPickupCancelResponse = [
    {
        "carrier_id": "hermes",
        "carrier_name": "hermes",
        "success": True,
        "operation": "Cancel Pickup"
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "hermes",
            "carrier_name": "hermes",
            "code": "e070",
            "message": "Unable to cancel the pickup order.",
            "details": {}
        }
    ]
]
