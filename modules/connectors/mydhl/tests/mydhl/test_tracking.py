"""MyDHL carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestMyDHLTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments/9356579890/tracking"
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["9356579890"]
}

TrackingRequest = ["9356579890"]

TrackingResponse = """{
  "shipments": [
    {
      "shipmentTrackingNumber": 9356579890,
      "status": "delivered",
      "shipmentTimestamp": "2024-01-10T10:00:00",
      "productCode": "P",
      "description": "EXPRESS WORLDWIDE",
      "estimatedTimeOfDelivery": "2024-01-15T17:00:00",
      "events": [
        {
          "date": "2024-01-15",
          "time": "17:00:00",
          "typeCode": "OK",
          "description": "Shipment delivered",
          "serviceArea": [
            {
              "code": "NYC",
              "description": "New York, NY"
            }
          ]
        },
        {
          "date": "2024-01-15",
          "time": "08:00:00",
          "typeCode": "PU",
          "description": "Shipment picked up",
          "serviceArea": [
            {
              "code": "LAX",
              "description": "Los Angeles, CA"
            }
          ]
        }
      ]
    }
  ]
}"""

ErrorResponse = """{
  "status": 404,
  "title": "Not Found",
  "detail": "No shipments found for the given tracking number",
  "instance": "/shipments/9356579890/tracking"
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "tracking_number": "9356579890",
            "events": [
                {
                    "date": "2024-01-15",
                    "time": "17:00:00",
                    "code": "OK",
                    "description": "Shipment delivered",
                    "location": "New York, NY"
                },
                {
                    "date": "2024-01-15",
                    "time": "08:00:00",
                    "code": "PU",
                    "description": "Shipment picked up",
                    "location": "Los Angeles, CA"
                }
            ],
            "estimated_delivery": "2024-01-15",
            "delivered": True,
            "status": "delivered",
            "meta": {
                "product_code": "P",
                "shipment_timestamp": "2024-01-10T10:00:00"
            }
        }
    ],
    []
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "code": "404",
            "message": "No shipments found for the given tracking number",
            "details": {
                "instance": "/shipments/9356579890/tracking",
                "title": "Not Found"
            }
        }
    ]
]