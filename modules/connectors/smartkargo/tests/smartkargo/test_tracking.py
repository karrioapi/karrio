"""SmartKargo carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSmartKargoTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        serialized = request.serialize()
        self.assertEqual(len(serialized), 1)
        self.assertEqual(serialized[0]["tracking_number"], "yogi045")

    def test_get_tracking(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            self.assertIn(
                "tracking?packageReference=yogi045",
                mock.call_args[1]["url"]
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            print(parsed_response)
            self.assertEqual(len(parsed_response[0]), 1)
            self.assertEqual(parsed_response[0][0].tracking_number, "yogi045")
            self.assertEqual(parsed_response[0][0].status, "delivered")
            self.assertEqual(len(parsed_response[0][0].events), 2)

    def test_parse_error_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            print(parsed_response)
            # No tracking details when error
            self.assertEqual(len(parsed_response[0]), 0)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["yogi045"],
}

# SmartKargo returns an array of tracking events
TrackingResponse = """[
  {
    "prefix": "AXB",
    "airWaybill": "00006510",
    "headerReference": "yogi045",
    "packageReference": "yogi045",
    "pieceReference": "yogi045-001",
    "eventType": "BKD",
    "eventDate": "2021-01-25T13:03:17",
    "flightNumber": "AC123",
    "flightDate": "2021-01-26T13:30:00",
    "eventLocation": "BOS",
    "flightSegmentOrigin": null,
    "flightSegmentDestination": "LAX",
    "pieces": 1.00,
    "weight": 2.8400,
    "description": "Electronic information submitted by shipper Boston Logan."
  },
  {
    "prefix": "AXB",
    "airWaybill": "00006510",
    "headerReference": "yogi045",
    "packageReference": "yogi045",
    "pieceReference": "yogi045-002",
    "eventType": "DDL",
    "eventDate": "2021-01-26T14:30:00",
    "flightNumber": "AC123",
    "flightDate": "2021-01-26T13:30:00",
    "eventLocation": "LAX",
    "flightSegmentOrigin": "BOS",
    "flightSegmentDestination": "LAX",
    "pieces": 1.00,
    "weight": 2.8400,
    "description": "Package has been successfully delivered to the consignee."
  }
]"""

ErrorResponse = """{
  "error": {
    "code": "NOT_FOUND",
    "message": "Tracking information not found"
  }
}"""
