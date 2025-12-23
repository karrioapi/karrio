"""Teleship carrier tracking tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTeleshipTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/tracking/TELESHIP12345678901",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["TELESHIP12345678901"],
}

TrackingRequest = ["TELESHIP12345678901"]

TrackingResponse = """{
    "trackingNumber": "TELESHIP12345678901",
    "shipmentId": "SHP-UK-US-98765",
    "status": "in_transit",
    "customerReference": "UK-US-12345",
    "shipDate": "2025-01-15",
    "estimatedDelivery": "2025-01-20",
    "shipFrom": {
        "name": "UK Exports Ltd",
        "address": {
            "city": "London",
            "state": "LDN",
            "postcode": "SW1A 1AA",
            "country": "GB"
        }
    },
    "shipTo": {
        "name": "US Imports Inc",
        "address": {
            "city": "Los Angeles",
            "state": "CA",
            "postcode": "90001",
            "country": "US"
        }
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
            "code": "collected",
            "description": "Package collected from sender",
            "location": "London, GB"
        },
        {
            "timestamp": "2025-01-15T14:30:00Z",
            "code": "in_hub",
            "description": "Arrived at UK sorting hub",
            "location": "Heathrow Hub, GB"
        },
        {
            "timestamp": "2025-01-16T02:45:00Z",
            "code": "in_transit",
            "description": "In transit to destination country",
            "location": "International Transit"
        },
        {
            "timestamp": "2025-01-17T18:20:00Z",
            "code": "customs_cleared",
            "description": "Cleared customs",
            "location": "Los Angeles ISC, US"
        },
        {
            "timestamp": "2025-01-18T08:00:00Z",
            "code": "in_transit",
            "description": "Out for delivery",
            "location": "Los Angeles, CA, US"
        }
    ]
}"""

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

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "delivered": False,
            "estimated_delivery": "2025-01-20",
            "events": [
                {
                    "code": "collected",
                    "date": "2025-01-15",
                    "description": "Package collected from sender",
                    "location": "London, GB",
                    "status": "in_transit",
                    "time": "09:15 AM",
                    "timestamp": "2025-01-15T09:15:00.000Z",
                },
                {
                    "code": "in_hub",
                    "date": "2025-01-15",
                    "description": "Arrived at UK sorting hub",
                    "location": "Heathrow Hub, GB",
                    "status": "in_transit",
                    "time": "14:30 PM",
                    "timestamp": "2025-01-15T14:30:00.000Z",
                },
                {
                    "code": "in_transit",
                    "date": "2025-01-16",
                    "description": "In transit to destination country",
                    "location": "International Transit",
                    "status": "in_transit",
                    "time": "02:45 AM",
                    "timestamp": "2025-01-16T02:45:00.000Z",
                },
                {
                    "code": "customs_cleared",
                    "date": "2025-01-17",
                    "description": "Cleared customs",
                    "location": "Los Angeles ISC, US",
                    "status": "in_transit",
                    "time": "18:20 PM",
                    "timestamp": "2025-01-17T18:20:00.000Z",
                },
                {
                    "code": "in_transit",
                    "date": "2025-01-18",
                    "description": "Out for delivery",
                    "location": "Los Angeles, CA, US",
                    "status": "in_transit",
                    "time": "08:00 AM",
                    "timestamp": "2025-01-18T08:00:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.teleship.com/TELESHIP12345678901",
                "customer_name": "Los Angeles",
                "shipment_destination_country": "US",
                "shipment_origin_country": "GB",
                "shipment_service": "DPD UK",
            },
            "meta": {
                "customer_reference": "UK-US-12345",
                "last_mile_carrier": "USPS",
                "last_mile_tracking": "9400111899223456789012",
                "ship_date": "2025-01-15",
                "shipment_id": "SHP-UK-US-98765",
            },
            "status": "in_transit",
            "tracking_number": "TELESHIP12345678901",
        }
    ],
    [],
]

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
                    "Please verify the tracking number is correct",
                ],
            },
        }
    ],
]
