import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio import Tracking
from karrio.core.models import TrackingRequest
from .fixture import gateway


class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequestJSON)

    def test_get_tracking(self):
        with patch("karrio.mappers.yanwen.proxy.http") as mock:
            mock.return_value = "{}"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                "http://trackapi.yanwentech.com/api/tracking?nums=6A16723741816",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.yanwen.proxy.http") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["6A16723741816"]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "yanwen",
            "carrier_name": "yanwen",
            "delivered": False,
            "events": [
                {
                    "code": "PU10",
                    "date": "1900-01-01",
                    "description": "Yanwen Acceptance",
                    "time": "00:00",
                }
            ],
            "tracking_number": "00340434281410767138",
        }
    ],
    [],
]

TrackingRequestJSON = {"nums": "6A16723741816"}

TrackingResponseJSON = """{
    "code": 0,
    "message": "success",
    "result": [
        {
            "tracking_number": "00340434281410767138",
            "tracking_status": "SC20",
            "last_mile_tracking_expected": false,
            "checkpoints": [
                {
                    "time_stamp": "2019-08-15T18:52:19",
                    "time_zone": "+8",
                    "tracking_status": "PU10",
                    "message": "Yanwen Acceptance",
                    "location": ""
                }
            ]
        }
    ],
    "elapsedMilliseconds": 56
}
"""
