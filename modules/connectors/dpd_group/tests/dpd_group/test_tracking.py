"""DPD Group carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestDPDGroupTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        print(f"Generated request: {request.serialize()}")
        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertTrue(
                mock.call_args[1]["url"].startswith(
                    f"{gateway.settings.server_url}/tracking/"
                )
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertEqual(len(parsed_response[1]), 1)


if __name__ == "__main__":
    unittest.main()


# Test Data

TrackingPayload = {
    "tracking_numbers": ["05300000011267"],
}

TrackingRequest = ["05300000011267"]

TrackingResponse = """{
  "trackingNumber": "05300000011267",
  "shipmentId": "SHIP123456789",
  "status": "DELIVERED",
  "statusDescription": "Package has been delivered",
  "events": [
    {
      "timestamp": "2024-01-20T14:30:00Z",
      "status": "DELIVERED",
      "description": "Package delivered to recipient",
      "location": {
        "city": "Munich",
        "country": "DE",
        "postalCode": "54321"
      },
      "signedBy": "John Doe"
    },
    {
      "timestamp": "2024-01-20T08:15:00Z",
      "status": "OUT_FOR_DELIVERY",
      "description": "Out for delivery",
      "location": {
        "city": "Munich",
        "country": "DE"
      }
    },
    {
      "timestamp": "2024-01-19T22:45:00Z",
      "status": "IN_TRANSIT",
      "description": "Arrived at delivery depot",
      "location": {
        "city": "Munich",
        "country": "DE"
      }
    }
  ],
  "estimatedDelivery": "2024-01-20",
  "recipient": {
    "name": "John Doe",
    "city": "Munich",
    "country": "DE"
  }
}"""

ErrorResponse = """{
  "error": {
    "code": "NOT_FOUND",
    "message": "Tracking number not found"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/v1.1/tracking/05300000011267",
  "status": 404
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dpd_group",
            "carrier_name": "dpd_group",
            "tracking_number": "05300000011267",
            "status": "delivered",
            "events": [
                {
                    "date": "2024-01-20",
                    "description": "Package delivered to recipient",
                    "code": "DELIVERED",
                    "time": "14:30",
                    "location": "Munich, 54321, DE",
                },
                {
                    "date": "2024-01-20",
                    "description": "Out for delivery",
                    "code": "OUT_FOR_DELIVERY",
                    "time": "08:15",
                    "location": "Munich, DE",
                },
                {
                    "date": "2024-01-19",
                    "description": "Arrived at delivery depot",
                    "code": "IN_TRANSIT",
                    "time": "22:45",
                    "location": "Munich, DE",
                },
            ],
            "estimated_delivery": "2024-01-20",
            "info": {
                "carrier_tracking_link": "https://tracking.dpdgroup.com/track/05300000011267",
            },
        }
    ],
    []
]
