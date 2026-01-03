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
        with patch("karrio.mappers.dpd_meta.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickupscheduling",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.dpd_meta.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd_meta.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "address": {
        "address_line1": "Main Street",
        "street_number": "42",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "person_name": "John Smith",
        "company_name": "ABC Logistics",
        "phone_number": "+4930123456",
        "email": "pickup@abclogistics.com",
    },
    "pickup_date": "2025-12-01",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "instruction": "Ground floor delivery preferred",
    "parcels": [{"weight": 5.0, "weight_unit": "KG"}],
}

PickupRequest = {
    "comment": "Ground floor delivery preferred",
    "customerInfos": {
        "customerAccountNumber": "ACC123456",
        "customerID": "123456789",
    },
    "numberOfParcels": 1,
    "pickup": {"date": "2025-12-01", "fromTime": "09:00", "toTime": "17:00"},
    "pickupAddress": {
        "city": "Berlin",
        "companyName": "ABC Logistics",
        "country": "DE",
        "houseNumber": "42",
        "name1": "John Smith",
        "street": "Main Street",
        "zipCode": "10115",
    },
    "pickupContact": {
        "contactPerson": "John Smith",
        "email": "pickup@abclogistics.com",
        "phone1": "+4930123456",
    },
}

PickupResponse = """{
  "scheduledPickupResponse": [
    {
      "pickupreference": "PU20251201001",
      "statusCode": "SUCCESS",
      "statusDescription": "Pickup scheduled successfully"
    }
  ]
}"""

ErrorResponse = """{
  "errorCode": "ERR002",
  "errorMessage": "Invalid pickup request",
  "errorOrigin": "META-API"
}"""

ParsedPickupResponse = [
    {
        "carrier_id": "dpd_meta",
        "carrier_name": "dpd_meta",
        "confirmation_number": "PU20251201001",
        "meta": {
            "status_code": "SUCCESS",
            "status_description": "Pickup scheduled successfully",
        },
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "dpd_meta",
            "carrier_name": "dpd_meta",
            "code": "ERR002",
            "details": {"errorOrigin": "META-API"},
            "message": "Error Code ERR002: Invalid pickup request",
        }
    ],
]
