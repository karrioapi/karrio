import unittest
from unittest.mock import patch
from tests.sendle.fixture import proxy
from gds_helpers import to_dict
from purplship.core.models import TrackingRequest


class TestSendleTracking(unittest.TestCase):
    def test_create_tracking_request(self):
        payload = TrackingRequest(tracking_numbers=TRACKING_REQUEST)

        tracking_request = proxy.mapper.create_tracking_request(payload)
        self.assertEqual(to_dict(tracking_request), to_dict(TRACKING_REQUEST))

    @patch("purplship.carriers.sendle.sendle_proxy.http", return_value="{}")
    def test_get_tracking(self, http_mock):
        proxy.get_tracking(TRACKING_REQUEST)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, TRACKING_REQUEST_QUERY_STR)

    def test_parse_tracking_response(self):
        parsed_response = proxy.mapper.parse_tracking_response(TRACKING_RESPONSE)
        self.assertEqual(to_dict(parsed_response), to_dict(PARSED_TRACKING_RESPONSE))

    def test_parse_tracking_response_with_errors(self):
        parsed_response = proxy.mapper.parse_tracking_response(
            TRACKING_RESPONSE_WITH_ERROR
        )
        self.assertEqual(
            to_dict(parsed_response), to_dict(PARSED_TRACKING_RESPONSE_WITH_ERROR)
        )


if __name__ == "__main__":
    unittest.main()


TRACKING_REQUEST = ["S3ND73"]

PARSED_TRACKING_RESPONSE = [
    [
        {
            "carrier": "Sendle",
            "events": [
                {
                    "code": "Pickup Attempted",
                    "date": "2015-11-23T01:04:00Z",
                    "description": "We attempted to pick up the parcel but were unsuccessful",
                },
                {
                    "code": "Pickup",
                    "date": "2015-11-24T20:31:00Z",
                    "description": "Parcel picked up",
                },
                {
                    "code": "Info",
                    "date": "2015-11-25T01:04:00Z",
                    "description": "In transit between locations",
                },
                {
                    "code": "In Transit",
                    "date": "2015-11-25T01:14:00Z",
                    "description": "In transit",
                    "location": "Brisbane",
                },
                {
                    "code": "Info",
                    "date": "2015-11-26T19:46:00Z",
                    "description": "Arrived at the depot for processing",
                },
                {
                    "code": "Info",
                    "date": "2015-11-26T23:00:00Z",
                    "description": "Parcel is loaded for delivery",
                },
                {
                    "code": "Delivered",
                    "date": "2015-11-27T23:46:00Z",
                    "description": "Parcel delivered",
                },
                {
                    "code": "Info",
                    "date": "2015-11-27T23:47:00Z",
                    "description": "Your parcel was signed for by JIMMY",
                },
            ],
            "tracking_number": "S3ND73",
        }
    ],
    [],
]

PARSED_TRACKING_RESPONSE_WITH_ERROR = [
    [],
    [
        {
            "carrier": "Sendle",
            "code": "unprocessable_entity",
            "message": "The data you supplied is invalid. Error messages are in the messages section. Please fix those fields and try again.",
        }
    ],
]


TRACKING_REQUEST_QUERY_STR = "https://sandbox.sendle.com/tracking/S3ND73"

TRACKING_RESPONSE = [
    {
        "ref": "S3ND73",
        "response": {
            "state": "Delivered",
            "tracking_events": [
                {
                    "event_type": "Pickup Attempted",
                    "scan_time": "2015-11-23T01:04:00Z",
                    "description": "We attempted to pick up the parcel but were unsuccessful",
                    "reason": "Parcel not ready",
                },
                {
                    "event_type": "Pickup",
                    "scan_time": "2015-11-24T20:31:00Z",
                    "description": "Parcel picked up",
                },
                {
                    "event_type": "Info",
                    "scan_time": "2015-11-25T01:04:00Z",
                    "description": "In transit between locations",
                },
                {
                    "event_type": "In Transit",
                    "scan_time": "2015-11-25T01:14:00Z",
                    "description": "In transit",
                    "origin_location": "Sydney",
                    "destination_location": "Brisbane",
                },
                {
                    "event_type": "Info",
                    "scan_time": "2015-11-26T19:46:00Z",
                    "description": "Arrived at the depot for processing",
                },
                {
                    "event_type": "Info",
                    "scan_time": "2015-11-26T23:00:00Z",
                    "description": "Parcel is loaded for delivery",
                },
                {
                    "event_type": "Delivered",
                    "scan_time": "2015-11-27T23:46:00Z",
                    "description": "Parcel delivered",
                },
                {
                    "event_type": "Info",
                    "scan_time": "2015-11-27T23:47:00Z",
                    "description": "Your parcel was signed for by JIMMY",
                },
            ],
        },
    }
]

TRACKING_RESPONSE_WITH_ERROR = [
    {
        "ref": "S3ND73",
        "response": {
            "error": "unprocessable_entity",
            "error_description": "The data you supplied is invalid. Error messages are in the messages section. Please fix those fields and try again.",
        },
    }
]
