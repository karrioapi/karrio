"""Teleship carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestTeleshipTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch.object(type(gateway.settings), 'access_token', new_callable=lambda: property(lambda self: "test_token_123")):
            with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
                mock.return_value = "{}"
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
                self.assertEqual(
                    mock.call_args[1]["url"],
                    f"{gateway.settings.server_url}/api/tracking/TELESHIP12345678901"
                )

    def test_parse_tracking_response(self):
        with patch.object(type(gateway.settings), 'access_token', new_callable=lambda: property(lambda self: "test_token_123")):
            with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
                mock.return_value = TrackingResponse
                parsed_response = (
                    karrio.Tracking.fetch(self.TrackingRequest)
                    .from_(gateway)
                    .parse()
                )
                self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch.object(type(gateway.settings), 'access_token', new_callable=lambda: property(lambda self: "test_token_123")):
            with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
                mock.return_value = ErrorResponse
                parsed_response = (
                    karrio.Tracking.fetch(self.TrackingRequest)
                    .from_(gateway)
                    .parse()
                )
                self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


# 1. Karrio Input Payload
TrackingPayload = {
    "tracking_numbers": ["TELESHIP12345678901"],
}

# 2. Carrier Request Format (from generated schemas)
TrackingRequest = ["TELESHIP12345678901"]

# 3. Carrier Response Mock (actual API format)
TrackingResponse = """{
    "trackingNumber": "TELESHIP12345678901",
    "shipmentId": "SHP-UK-US-98765",
    "status": "in_transit",
    "customerReference": "UK-US-12345",
    "shipDate": "2025-01-15",
    "estimatedDelivery": "2025-01-20",
    "shipFrom": {
        "name": "UK Exports Ltd",
        "city": "London",
        "state": "LDN",
        "postcode": "SW1A 1AA",
        "country": "GB"
    },
    "shipTo": {
        "name": "US Imports Inc",
        "city": "Los Angeles",
        "state": "CA",
        "postcode": "90001",
        "country": "US"
    },
    "firstMile": {
        "carrier": "DPD UK",
        "trackingNumber": "DPD987654321GB"
    },
    "lastMile": {
        "carrier": "USPS",
        "trackingNumber": "9400111899223456789012"
    },
    "events": [
        {
            "timestamp": "2025-01-15T09:15:00Z",
            "status": "collected",
            "description": "Package collected from sender",
            "location": "London, GB"
        },
        {
            "timestamp": "2025-01-15T14:30:00Z",
            "status": "in_hub",
            "description": "Arrived at UK sorting hub",
            "location": "Heathrow Hub, GB"
        },
        {
            "timestamp": "2025-01-16T02:45:00Z",
            "status": "in_transit",
            "description": "In transit to destination country",
            "location": "International Transit"
        },
        {
            "timestamp": "2025-01-17T18:20:00Z",
            "status": "customs_cleared",
            "description": "Cleared customs",
            "location": "Los Angeles ISC, US"
        },
        {
            "timestamp": "2025-01-18T08:00:00Z",
            "status": "in_transit",
            "description": "Out for delivery",
            "location": "Los Angeles, CA, US"
        }
    ]
}"""

# 4. Error Response Mock
ErrorResponse = """{
    "messages": [
        {
            "code": 404,
            "timestamp": "2025-01-18T12:00:00Z",
            "message": "Tracking number not found",
            "details": [
                "No shipment found with tracking number: TELESHIP12345678901",
                "Please verify the tracking number is correct"
            ]
        }
    ]
}"""

# 5. Parsed Success Response (Karrio format)
ParsedTrackingResponse = [
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "tracking_number": "TELESHIP12345678901",
            "events": [
                {
                    "date": "2025-01-15",
                    "description": "Package collected from sender",
                    "code": "collected",
                    "time": "09:15:00",
                    "location": "London, GB"
                },
                {
                    "date": "2025-01-15",
                    "description": "Arrived at UK sorting hub",
                    "code": "in_hub",
                    "time": "14:30:00",
                    "location": "Heathrow Hub, GB"
                },
                {
                    "date": "2025-01-16",
                    "description": "In transit to destination country",
                    "code": "in_transit",
                    "time": "02:45:00",
                    "location": "International Transit"
                },
                {
                    "date": "2025-01-17",
                    "description": "Cleared customs",
                    "code": "customs_cleared",
                    "time": "18:20:00",
                    "location": "Los Angeles ISC, US"
                },
                {
                    "date": "2025-01-18",
                    "description": "Out for delivery",
                    "code": "in_transit",
                    "time": "08:00:00",
                    "location": "Los Angeles, CA, US"
                }
            ],
            "delivered": False,
            "estimated_delivery": "2025-01-20",
            "status": "in_transit",
            "info": {
                "carrier_tracking_link": "https://track.teleship.com/TELESHIP12345678901",
                "customer_name": "Los Angeles",
                "shipment_service": "DPD UK",
                "shipment_origin_country": "GB",
                "shipment_destination_country": "US"
            },
            "meta": {
                "shipment_id": "SHP-UK-US-98765",
                "customer_reference": "UK-US-12345",
                "ship_date": "2025-01-15",
                "ship_from": "London, GB",
                "ship_to": "Los Angeles, CA, US",
                "first_mile_carrier": "DPD UK",
                "first_mile_tracking": "DPD987654321GB",
                "last_mile_carrier": "USPS",
                "last_mile_tracking": "9400111899223456789012"
            }
        }
    ],
    []
]

# 6. Parsed Error Response
ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "code": "404",
            "message": "Tracking number not found",
            "details": {
                "timestamp": "2025-01-18T12:00:00Z",
                "tracking_number": "TELESHIP12345678901",
                "details": [
                    "No shipment found with tracking number: TELESHIP12345678901",
                    "Please verify the tracking number is correct"
                ]
            }
        }
    ]
]
