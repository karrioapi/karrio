"""GLS Group carrier tracking tests."""

import unittest
from unittest.mock import patch
from tests.fixture import gateway
import logging
import karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestGLSGroupTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        print(f"Generated request: {request.serialize()}")
        self.assertIsInstance(request.serialize(), list)

    def test_get_tracking(self):
        with patch("karrio.mappers.gls_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            print(f"Called URL: {mock.call_args}")
            # Verify that the URL contains the tracking number
            self.assertIn("/rs/tracking/", str(mock.call_args))

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.gls_group.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.gls_group.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingErrorResponse)


if __name__ == "__main__":
    unittest.main()

# Test data
TrackingPayload = {
    "tracking_numbers": ["12345678901234567890"],
}

TrackingResponse = """{
  "trackingNumber": "12345678901234567890",
  "status": "IN_TRANSIT",
  "shipmentId": "GLS123456789",
  "product": "PARCEL",
  "weight": 5.5,
  "events": [
    {
      "timestamp": "2025-01-15T10:30:00Z",
      "status": "ACCEPTED",
      "description": "Shipment accepted at depot",
      "location": {
        "city": "Berlin",
        "country": "DE"
      }
    },
    {
      "timestamp": "2025-01-15T15:45:00Z",
      "status": "IN_TRANSIT",
      "description": "Shipment in transit",
      "location": {
        "city": "Leipzig",
        "country": "DE"
      }
    }
  ],
  "estimatedDelivery": "2025-01-17"
}"""

ErrorResponse = """{
  "errors": [
    {
      "code": "NOT_FOUND",
      "message": "Tracking number not found"
    }
  ]
}"""

# Parsed tracking response
ParsedTrackingResponse = [
    [
        {
            "carrier_id": "gls_group",
            "carrier_name": "gls_group",
            "tracking_number": "12345678901234567890",
            "status": "in_transit",
            "events": [
                {
                    "date": "2025-01-15",
                    "description": "Shipment accepted at depot",
                    "location": "Berlin, DE",
                    "code": "ACCEPTED",
                    "time": "10:30:00"
                },
                {
                    "date": "2025-01-15",
                    "description": "Shipment in transit",
                    "location": "Leipzig, DE",
                    "code": "IN_TRANSIT",
                    "time": "15:45:00"
                }
            ],
            "estimated_delivery": "2025-01-17",
            "meta": {
                "shipment_id": "GLS123456789",
                "product": "PARCEL",
                "weight": 5.5
            }
        }
    ],
    []
]

# Parsed error response
ParsedTrackingErrorResponse = [
    [],
    [
        {
            "carrier_id": "gls_group",
            "carrier_name": "gls_group",
            "code": "NOT_FOUND",
            "message": "Tracking number not found",
            "details": {}
        }
    ]
]
