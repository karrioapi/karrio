"""Asendia carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAsendiaTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            with patch(
                "karrio.providers.asendia.utils.Settings.access_token",
                new_callable=lambda: property(lambda self: "test_token"),
            ):
                mock.return_value = TrackingResponse
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
                self.assertEqual(
                    mock.call_args[1]["url"],
                    f"{gateway.settings.server_url}/api/customers/CUST123/tracking/ASENDIA123456789",
                )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            with patch(
                "karrio.providers.asendia.utils.Settings.access_token",
                new_callable=lambda: property(lambda self: "test_token"),
            ):
                mock.return_value = TrackingResponse
                parsed_response = (
                    karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
                )
                self.assertListEqual(
                    lib.to_dict(parsed_response), ParsedTrackingResponse
                )

    def test_parse_error_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            with patch(
                "karrio.providers.asendia.utils.Settings.access_token",
                new_callable=lambda: property(lambda self: "test_token"),
            ):
                mock.return_value = ErrorResponse
                parsed_response = (
                    karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
                )
                self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["ASENDIA123456789"],
}

TrackingRequest = ["ASENDIA123456789"]

TrackingResponse = """{
  "trackingNumber": "ASENDIA123456789",
  "trackingEvents": [
    {
      "id": 1,
      "code": "PU",
      "time": "2024-04-12T14:30:00Z",
      "locationName": "Bern",
      "carrierEventDescription": "Package picked up",
      "locationCountry": "CH"
    },
    {
      "id": 2,
      "code": "IT",
      "time": "2024-04-13T09:15:00Z",
      "locationName": "Zurich Airport",
      "carrierEventDescription": "In transit to destination",
      "locationCountry": "CH"
    },
    {
      "id": 3,
      "code": "DL",
      "time": "2024-04-15T11:00:00Z",
      "locationName": "New York",
      "carrierEventDescription": "Delivered",
      "locationCountry": "US"
    }
  ]
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "delivered": True,
            "events": [
                {
                    "code": "DL",
                    "date": "2024-04-15",
                    "description": "Delivered",
                    "location": "New York, US",
                    "status": "delivered",
                    "time": "11:00 AM",
                    "timestamp": "2024-04-15T11:00:00.000Z",
                },
                {
                    "code": "IT",
                    "date": "2024-04-13",
                    "description": "In transit to destination",
                    "location": "Zurich Airport, CH",
                    "status": "in_transit",
                    "time": "09:15 AM",
                    "timestamp": "2024-04-13T09:15:00.000Z",
                },
                {
                    "code": "PU",
                    "date": "2024-04-12",
                    "description": "Package picked up",
                    "location": "Bern, CH",
                    "status": "picked_up",
                    "time": "14:30 PM",
                    "timestamp": "2024-04-12T14:30:00.000Z",
                },
            ],
            "status": "delivered",
            "tracking_number": "ASENDIA123456789",
        }
    ],
    [],
]

ErrorResponse = """{
  "type": "https://www.asendia-sync.com/problem/constraint-violation",
  "title": "Not Found",
  "status": 404,
  "detail": "Tracking number not found",
  "path": "/api/customers/CUST123/tracking/INVALID123",
  "message": "error.tracking.not_found"
}"""

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "code": "404",
            "details": {
                "path": "/api/customers/CUST123/tracking/INVALID123",
                "tracking_number": "ASENDIA123456789",
                "type": "https://www.asendia-sync.com/problem/constraint-violation",
            },
            "message": "Tracking number not found",
        }
    ],
]
