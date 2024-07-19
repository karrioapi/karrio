import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSendleTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/tracking/S34WER4S",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["S34WER4S"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "sendle",
            "carrier_name": "sendle",
            "delivered": True,
            "estimated_delivery": "2023-04-05",
            "events": [
                {
                    "code": "Delivered",
                    "date": "2023-04-05",
                    "description": "Your package has been delivered to your "
                    "mailbox!",
                    "location": "NEW YORK, NY",
                    "time": "14:56 PM",
                },
                {
                    "code": "Out for Delivery",
                    "date": "2023-04-05",
                    "description": "Your package is on board for delivery!",
                    "location": "NEW YORK, NY",
                    "time": "09:10 AM",
                },
                {
                    "code": "In Transit",
                    "date": "2023-04-05",
                    "description": "Your package is in transit with the carrier.",
                    "location": "NEW YORK, NY",
                    "time": "08:59 AM",
                },
                {
                    "code": "In Transit",
                    "date": "2023-04-05",
                    "description": "Your package is in transit with the carrier.",
                    "location": "NEW YORK, NY",
                    "time": "08:04 AM",
                },
                {
                    "code": "In Transit",
                    "date": "2023-04-05",
                    "description": "Your package is in transit with the carrier.",
                    "location": "NEW YORK NY DISTRIBUTION CENTER",
                    "time": "03:14 AM",
                },
                {
                    "code": "In Transit",
                    "date": "2023-04-04",
                    "description": "Your package is in transit with the carrier.",
                    "location": "JERSEY CITY NJ NETWORK DISTRIBUTION CENTER",
                    "time": "22:43 PM",
                },
                {
                    "code": "In Transit",
                    "date": "2023-04-04",
                    "description": "Your package is in transit with the carrier.",
                    "location": "TEANECK, NJ",
                    "time": "16:55 PM",
                },
                {
                    "code": "Pickup",
                    "date": "2023-04-04",
                    "description": "Parcel picked up",
                    "time": "16:12 PM",
                },
                {
                    "code": "Pickup Attempted",
                    "date": "2023-04-03",
                    "description": "We attempted to pick up the parcel but were "
                    "unsuccessful",
                    "time": "08:20 AM",
                },
            ],
            "status": "delivered",
            "tracking_number": "S34WER4S",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "sendle",
            "carrier_name": "sendle",
            "code": "not_found",
            "details": {
                "error_description": "The resource you requested was not found. "
                "Please check the URI and try again.",
                "tracking_number": "S34WER4S",
            },
            "message": "The resource you requested was not found. Please check the URI "
            "and try again.",
        }
    ],
]


TrackingRequest = [{"ref": "S34WER4S"}]

TrackingResponse = """{
    "state": "Delivered",
    "status": {
        "description": "Your package has been delivered to your mailbox!",
        "last_changed_at": "2023-04-05 18:56:00 UTC"
    },
    "origin": {
        "country": "US"
    },
    "destination": {
        "country": "US"
    },
    "scheduling": {
        "pickup_date": "",
        "picked_up_on": "2023-04-04",
        "delivered_on": "2023-04-05",
        "estimated_delivery_date_minimum": "",
        "estimated_delivery_date_maximum": "",
        "status": ""
    },
    "tracking_events": [
        {
            "event_type": "Pickup Attempted",
            "scan_time": "2023-04-03T08:20:00Z",
            "description": "We attempted to pick up the parcel but were unsuccessful",
            "reason": "Parcel not ready",
            "display_time": "2023-04-03T08:20:00Z"
        },
        {
            "event_type": "Pickup",
            "scan_time": "2023-04-04T16:12:00Z",
            "description": "Parcel picked up",
            "display_time": "2023-04-04T16:12:00Z"
        },
        {
            "event_type": "In Transit",
            "scan_time": "2023-04-04T20:55:00Z",
            "description": "Your package is in transit with the carrier.",
            "location": "TEANECK, NJ",
            "local_scan_time": "2023-04-04T16:55:00",
            "display_time": "2023-04-04T16:55:00-04:00"
        },
        {
            "event_type": "In Transit",
            "scan_time": "2023-04-04T22:43:00Z",
            "description": "Your package is in transit with the carrier.",
            "location": "JERSEY CITY NJ NETWORK DISTRIBUTION CENTER",
            "local_scan_time": "2023-04-04T22:43:00",
            "display_time": "2023-04-04T22:43:00Z"
        },
        {
            "event_type": "In Transit",
            "scan_time": "2023-04-05T03:14:00Z",
            "description": "Your package is in transit with the carrier.",
            "location": "NEW YORK NY DISTRIBUTION CENTER",
            "local_scan_time": "2023-04-05T03:14:00",
            "display_time": "2023-04-05T03:14:00Z"
        },
        {
            "event_type": "In Transit",
            "scan_time": "2023-04-05T12:04:00Z",
            "description": "Your package is in transit with the carrier.",
            "location": "NEW YORK, NY",
            "local_scan_time": "2023-04-05T08:04:00",
            "display_time": "2023-04-05T08:04:00-04:00"
        },
        {
            "event_type": "In Transit",
            "scan_time": "2023-04-05T12:59:00Z",
            "description": "Your package is in transit with the carrier.",
            "location": "NEW YORK, NY",
            "local_scan_time": "2023-04-05T08:59:00",
            "display_time": "2023-04-05T08:59:00-04:00"
        },
        {
            "event_type": "Out for Delivery",
            "scan_time": "2023-04-05T13:10:00Z",
            "description": "Your package is on board for delivery!",
            "location": "NEW YORK, NY",
            "local_scan_time": "2023-04-05T09:10:00",
            "display_time": "2023-04-05T09:10:00-04:00"
        },
        {
            "event_type": "Delivered",
            "scan_time": "2023-04-05T18:56:00Z",
            "description": "Your package has been delivered to your mailbox!",
            "location": "NEW YORK, NY",
            "local_scan_time": "2023-04-05T14:56:00",
            "display_time": "2023-04-05T14:56:00-04:00"
        }
    ]
}
"""

ErrorResponse = """{
  "error": "not_found",
  "error_description": "The resource you requested was not found. Please check the URI and try again."
}
"""
