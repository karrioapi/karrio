"""ParcelOne tracking tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestParcelOneTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertListEqual(request.serialize(), TrackingRequestJSON)

    def test_get_tracking(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            # Verify tracking URL format
            self.assertIn(
                f"{gateway.settings.tracking_url}/tracking/",
                mock.call_args[1]["url"],
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_tracking_no_events_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = TrackingNoEventsResponseJSON
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedTrackingNoEventsResponse
            )


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["123456789012"],
    "options": {
        "carrier_id": "PA1",
    },
}

TrackingRequestJSON = [
    {
        "tracking_id": "123456789012",
        "carrier_id": "PA1",
    }
]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "parcelone",
            "carrier_name": "parcelone",
            "delivered": True,
            "events": [
                {
                    "code": "DELIVERED",
                    "date": "2024-01-15",
                    "description": "Package delivered",
                    "location": "Munich, Germany",
                    "status": "delivered",
                    "time": "14:30 PM",
                    "timestamp": "2024-01-15T14:30:00.000Z",
                },
                {
                    "code": "OUT_FOR_DELIVERY",
                    "date": "2024-01-15",
                    "description": "Out for delivery",
                    "location": "Munich, Germany",
                    "status": "out_for_delivery",
                    "time": "08:00 AM",
                    "timestamp": "2024-01-15T08:00:00.000Z",
                },
                {
                    "code": "ARRIVED",
                    "date": "2024-01-14",
                    "description": "Arrived at destination facility",
                    "location": "Munich Hub",
                    "status": "in_transit",
                    "time": "22:00 PM",
                    "timestamp": "2024-01-14T22:00:00.000Z",
                },
                {
                    "code": "IN_TRANSIT",
                    "date": "2024-01-14",
                    "description": "Shipment in transit",
                    "location": "Berlin Hub",
                    "status": "in_transit",
                    "time": "10:00 AM",
                    "timestamp": "2024-01-14T10:00:00.000Z",
                },
                {
                    "code": "REGISTERED",
                    "date": "2024-01-13",
                    "description": "Shipment picked up",
                    "location": "Berlin",
                    "status": "pending",
                    "time": "16:00 PM",
                    "timestamp": "2024-01-13T16:00:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://tracking.parcel.one/?trackingNumber=123456789012",
                "signed_by": "John Doe",
            },
            "meta": {
                "carrier_tracking_id": "DHL123456",
                "last_mile_carrier": "DHL",
            },
            "status": "delivered",
            "tracking_number": "123456789012",
        }
    ],
    [],
]

ParsedTrackingNoEventsResponse = [[], []]


TrackingResponseJSON = """{
    "success": 1,
    "results": {
        "StatusCode": "DELIVERED",
        "CarrierTrackingID": "DHL123456",
        "CarrierIDLMC": "DHL",
        "SignedBy": "John Doe",
        "Events": [
            {
                "DateTime": "2024-01-15T14:30:00",
                "Location": "Munich, Germany",
                "Description": "Package delivered",
                "StatusCode": "DELIVERED"
            },
            {
                "DateTime": "2024-01-15T08:00:00",
                "Location": "Munich, Germany",
                "Description": "Out for delivery",
                "StatusCode": "OUT_FOR_DELIVERY"
            },
            {
                "DateTime": "2024-01-14T22:00:00",
                "Location": "Munich Hub",
                "Description": "Arrived at destination facility",
                "StatusCode": "ARRIVED"
            },
            {
                "DateTime": "2024-01-14T10:00:00",
                "Location": "Berlin Hub",
                "Description": "Shipment in transit",
                "StatusCode": "IN_TRANSIT"
            },
            {
                "DateTime": "2024-01-13T16:00:00",
                "Location": "Berlin",
                "Description": "Shipment picked up",
                "StatusCode": "REGISTERED"
            }
        ]
    }
}"""

TrackingNoEventsResponseJSON = """{
    "success": 1,
    "results": {
        "StatusCode": "UNKNOWN",
        "Events": []
    }
}"""
