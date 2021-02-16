import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship import Tracking
from purplship.core.models import TrackingRequest
from tests.sendle.fixture import gateway


class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequestJSON)

    def test_get_tracking(self):
        with patch("purplship.mappers.sendle.proxy.http") as mock:
            mock.return_value = "{}"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/tracking/S3ND73",
            )

    def test_parse_tracking_response(self):
        with patch("purplship.mappers.sendle.proxy.http") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )

    def test_parse_error_response(self):
        with patch("purplship.mappers.sendle.proxy.http") as mock:
            mock.return_value = ErrorResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedErrorResponse)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["S3ND73"]

ParsedTrackingResponse = [[{'carrier_id': 'sendle', 'carrier_name': 'sendle', 'delivered': True, 'events': [{'code': 'Info', 'date': '2015-11-27', 'description': 'Your parcel was signed for by JIMMY', 'time': '23:47'}, {'code': 'Delivered', 'date': '2015-11-27', 'description': 'Parcel delivered', 'time': '23:46'}, {'code': 'Info', 'date': '2015-11-26', 'description': 'Parcel is loaded for delivery', 'time': '23:00'}, {'code': 'Info', 'date': '2015-11-26', 'description': 'Arrived at the depot for processing', 'time': '19:46'}, {'code': 'In Transit', 'date': '2015-11-25', 'description': 'In transit', 'time': '01:14'}, {'code': 'Info', 'date': '2015-11-25', 'description': 'In transit between locations', 'time': '01:04'}, {'code': 'Pickup', 'date': '2015-11-24', 'description': 'Parcel picked up', 'time': '20:31'}, {'code': 'Pickup Attempted', 'date': '2015-11-23', 'description': 'We attempted to pick up the parcel but were unsuccessful', 'time': '01:04'}], 'tracking_number': 'S3ND73'}], []]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "sendle",
            "carrier_name": "sendle",
            "code": "payment_required",
            "message": "The account associated with this API key has no method of payment. Please go to your Account Settings in your Sendle Dashboard and add a payment method.",
        }
    ],
]


TrackingRequestJSON = ["S3ND73"]

TrackingResponseJSON = """{
  "state": "Delivered",
  "tracking_events": [
    {
      "event_type": "Pickup Attempted",
      "scan_time": "2015-11-23T01:04:00Z",
      "description": "We attempted to pick up the parcel but were unsuccessful",
      "reason": "Parcel not ready"
    },
    {
      "event_type": "Pickup",
      "scan_time": "2015-11-24T20:31:00Z",
      "description": "Parcel picked up"
    },
    {
      "event_type": "Info",
      "scan_time": "2015-11-25T01:04:00Z",
      "description": "In transit between locations"
    },
    {
      "event_type": "In Transit",
      "scan_time": "2015-11-25T01:14:00Z",
      "description": "In transit",
      "origin_location": "Sydney",
      "destination_location": "Brisbane"
    },
    {
      "event_type": "Info",
      "scan_time": "2015-11-26T19:46:00Z",
      "description": "Arrived at the depot for processing"
    },
    {
      "event_type": "Info",
      "scan_time": "2015-11-26T23:00:00Z",
      "description": "Parcel is loaded for delivery"
    },
    {
      "event_type": "Delivered",
      "scan_time": "2015-11-27T23:46:00Z",
      "description": "Parcel delivered"
    },
    {
      "event_type": "Info",
      "scan_time": "2015-11-27T23:47:00Z",
      "description": "Your parcel was signed for by JIMMY"
    }
  ],
  "origin": {
    "country": "AU"
  },
  "destination": {
    "country": "AU"
  }
}
"""

ErrorResponseJSON = """{
    "error": "payment_required",
    "error_description": "The account associated with this API key has no method of payment. Please go to your Account Settings in your Sendle Dashboard and add a payment method."
}
"""
