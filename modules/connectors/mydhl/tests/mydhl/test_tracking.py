"""MyDHL carrier tracking tests."""

import unittest
from unittest.mock import patch
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
        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/tracking?shipmentTrackingNumber=9356579890"
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock1:
            mock1.return_value = TrackingResponse
            response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            with patch("karrio.providers.mydhl.utils.lib.request") as mock2:
                mock2.return_value = ProofOfDeliveryResponse
                parsed_response = response.parse()

                self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["9356579890"]
}

TrackingRequest = "shipmentTrackingNumber=9356579890"

TrackingResponse = """{
  "shipments": [
    {
      "shipmentTrackingNumber": "9356579890",
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
  "instance": "/tracking?shipmentTrackingNumber=9356579890"
}"""

ProofOfDeliveryResponse = """{
  "documents": [
    {
      "content": "JVBERi0xLjQK",
      "format": "PDF",
      "typeCode": "POD"
    }
  ]
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "delivered": True,
            "estimated_delivery": "2024-01-15",
            "events": [
                {
                    "code": "OK",
                    "date": "2024-01-15",
                    "description": "Shipment delivered",
                    "location": "New York, NY",
                    "status": "delivered",
                    "time": "17:00",
                    "timestamp": "2024-01-15T17:00:00.000Z",
                },
                {
                    "code": "PU",
                    "date": "2024-01-15",
                    "description": "Shipment picked up",
                    "location": "Los Angeles, CA",
                    "status": "pending",
                    "time": "08:00",
                    "timestamp": "2024-01-15T08:00:00.000Z",
                }
            ],
            "images": {},
            "info": {
                "carrier_tracking_link": "https://www.dhl.com/ca-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=9356579890",
                "expected_delivery": "2024-01-15",
                "shipment_service": "mydhl_express_worldwide",
                "shipping_date": "2024-01-10",
            },
            "meta": {
                "description": "EXPRESS WORLDWIDE",
                "product_code": "P",
                "shipment_timestamp": "2024-01-10T10:00:00"
            },
            "status": "delivered",
            "tracking_number": "9356579890",
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
                "instance": "/tracking?shipmentTrackingNumber=9356579890",
                "title": "Not Found"
            }
        }
    ]
]
