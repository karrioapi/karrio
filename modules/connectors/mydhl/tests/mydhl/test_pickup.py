"""MyDHL carrier pickup tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestMyDHLPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupUpdateRequest = models.PickupUpdateRequest(**PickupUpdatePayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        self.assertEqual(lib.to_dict(request.serialize()), PickupRequest)

    def test_schedule_pickup(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups"
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups"
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups/PRG999123456"
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "address": {
        "address_line1": "123 Main Street",
        "city": "Los Angeles",
        "postal_code": "90001",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "John Doe",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "pickup@example.com"
    },
    "pickup_date": "2024-01-15",
    "ready_time": "09:00",
    "closing_time": "17:00"
}

PickupUpdatePayload = {
    "confirmation_number": "PRG999123456",
    "address": {
        "address_line1": "123 Main Street",
        "city": "Los Angeles",
        "postal_code": "90001",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "John Doe",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "pickup@example.com"
    },
    "pickup_date": "2024-01-16",
    "ready_time": "10:00",
    "closing_time": "18:00"
}

PickupCancelPayload = {
    "confirmation_number": "PRG999123456"
}

PickupRequest = {
    "accounts": [{"number": "123456789", "typeCode": "shipper"}],
    "closeTime": "17:00",
    "customerDetails": {
        "shipperDetails": {
            "contactInformation": {
                "companyName": "Test Company",
                "email": "pickup@example.com",
                "fullName": "John Doe",
                "mobilePhone": "1234567890",
                "phone": "1234567890"
            },
            "postalAddress": {
                "addressLine1": "123 Main Street",
                "cityName": "Los Angeles",
                "countryCode": "US",
                "countryName": "United States",
                "postalCode": "90001",
                "provinceCode": "CA"
            }
        }
    },
    "location": "reception",
    "locationType": "business",
    "plannedPickupDateAndTime": ANY,
    "shipmentDetails": [
        {
            "isCustomsDeclarable": False,
            "packages": [{"weight": 1.0}],
            "productCode": "P",
            "unitOfMeasurement": "metric"
        }
    ]
}

PickupResponse = """{
  "dispatchConfirmationNumbers": ["PRG999123456", "PRG999123457"],
  "readyByTime": "09:00",
  "nextPickupDate": "2024-01-15",
  "warnings": []
}"""

PickupUpdateResponse = """{
  "dispatchConfirmationNumber": "PRG999123456",
  "readyByTime": "10:00",
  "nextPickupDate": "2024-01-16",
  "warnings": []
}"""

PickupCancelResponse = """{
  "dispatchConfirmationNumber": "PRG999123456",
  "status": "cancelled"
}"""

ErrorResponse = """{
  "status": 400,
  "title": "Bad Request",
  "detail": "Invalid pickup request - missing required field",
  "instance": "/pickups"
}"""

ParsedPickupResponse = [
    {
        "carrier_id": "mydhl",
        "carrier_name": "mydhl",
        "confirmation_number": "PRG999123456",
        "meta": {
            "confirmation_numbers": ["PRG999123456", "PRG999123457"]
        },
        "pickup_date": "2024-01-15",
        "ready_time": "09:00"
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "code": "400",
            "message": "Invalid pickup request - missing required field",
            "details": {
                "instance": "/pickups",
                "title": "Bad Request"
            }
        }
    ]
]