"""Spring carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSpringTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(lib.to_dict(request.serialize()), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.spring.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/tracking"
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.spring.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.spring.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["TRACK123"],
    "reference": "ORDER123"
}

TrackingRequest = {
  "trackingNumbers": [
    "TRACK123"
  ],
  "reference": "ORDER123"
}

TrackingResponse = """{
  "trackingInfo": [
    {
      "trackingNumber": "TRACK123",
      "status": "in_transit",
      "statusDetails": "Package is in transit",
      "estimatedDelivery": "2024-04-15",
      "events": [
        {
          "date": "2024-04-12",
          "time": "14:30:00",
          "code": "PU",
          "description": "Package picked up",
          "location": "San Francisco, CA"
        }
      ]
    }
  ]
}"""

ErrorResponse = """{
  "error": {
    "code": "tracking_error",
    "message": "Unable to track shipment",
    "details": "Invalid tracking number"
  }
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "spring",
            "carrier_name": "spring",
            "tracking_number": "TRACK123",
            "events": [
                {
                    "date": "2024-04-12",
                    "time": "14:30:00",
                    "code": "PU",
                    "description": "Package picked up",
                    "location": "San Francisco, CA"
                }
            ],
            "estimated_delivery": "2024-04-15",
            "status": "in_transit"
        }
    ],
    []
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "spring",
            "carrier_name": "spring",
            "code": "tracking_error",
            "message": "Unable to track shipment",
            "details": {
                "details": "Invalid tracking number"
            }
        }
    ]
]