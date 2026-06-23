"""Amazon Shipping tracking tests."""

import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.sdk as karrio

from .fixture import gateway


class TestAmazonShippingTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertListEqual(request.serialize(), TrackingRequestJSON)

    def test_get_tracking(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v2/tracking",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = ErrorResponseJSON
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TRACKING_PAYLOAD = {
    "tracking_numbers": ["89108749065090"],
}

TrackingRequestJSON = [
    {
        "tracking_id": "89108749065090",
        "carrier_id": "AMZN_US",
    }
]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "amazon_shipping",
            "carrier_name": "amazon_shipping",
            "delivered": True,
            "estimated_delivery": "2024-01-17",
            "events": [
                {
                    "code": "Delivered",
                    "date": "2024-01-17",
                    "description": "Delivered",
                    "location": "Seattle, WA, 98101, US",
                    "status": "delivered",
                    "time": "14:30 PM",
                    "timestamp": "2024-01-17T14:30:00.000Z",
                },
                {
                    "code": "OutForDelivery",
                    "date": "2024-01-17",
                    "description": "OutForDelivery",
                    "location": "Seattle, WA, 98101, US",
                    "status": "out_for_delivery",
                    "time": "08:00 AM",
                    "timestamp": "2024-01-17T08:00:00.000Z",
                },
                {
                    "code": "InTransit",
                    "date": "2024-01-16",
                    "description": "InTransit",
                    "location": "Portland, OR, 97201, US",
                    "status": "in_transit",
                    "time": "10:00 AM",
                    "timestamp": "2024-01-16T10:00:00.000Z",
                },
            ],
            "meta": {
                "carrier_tracking_id": "89108749065090",
                "received_by": "John Doe",
            },
            "status": "delivered",
            "tracking_number": "89108749065090",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "amazon_shipping",
            "carrier_name": "amazon_shipping",
            "code": "InvalidTrackingId",
            "details": {"note": "Tracking ID not found", "tracking_number": "89108749065090"},
            "message": "The tracking ID provided is not valid",
        }
    ],
]


TrackingResponseJSON = """{
  "payload": {
    "trackingId": "89108749065090",
    "alternateLegTrackingId": null,
    "eventHistory": [
      {
        "eventCode": "Delivered",
        "location": {
          "city": "Seattle",
          "stateOrRegion": "WA",
          "countryCode": "US",
          "postalCode": "98101"
        },
        "eventTime": "2024-01-17T14:30:00Z",
        "shipmentType": "FORWARD"
      },
      {
        "eventCode": "OutForDelivery",
        "location": {
          "city": "Seattle",
          "stateOrRegion": "WA",
          "countryCode": "US",
          "postalCode": "98101"
        },
        "eventTime": "2024-01-17T08:00:00Z",
        "shipmentType": "FORWARD"
      },
      {
        "eventCode": "InTransit",
        "location": {
          "city": "Portland",
          "stateOrRegion": "OR",
          "countryCode": "US",
          "postalCode": "97201"
        },
        "eventTime": "2024-01-16T10:00:00Z",
        "shipmentType": "FORWARD"
      }
    ],
    "promisedDeliveryDate": "2024-01-17T20:00:00Z",
    "summary": {
      "status": "Delivered",
      "trackingDetailCodes": {
        "forward": ["Signed"],
        "returns": []
      },
      "proofOfDelivery": {
        "deliveryLocationCoordinates": {
          "latitude": 47.6062,
          "longitude": -122.3321
        },
        "deliveryImageURL": null,
        "receivedBy": "John Doe"
      }
    }
  }
}
"""

ErrorResponseJSON = """{
  "errors": [
    {
      "code": "InvalidTrackingId",
      "message": "The tracking ID provided is not valid",
      "details": "Tracking ID not found"
    }
  ]
}
"""
