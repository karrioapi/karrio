import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio import Tracking
from karrio.core.models import TrackingRequest
from .fixture import gateway


class TestAmazonShippingTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(**TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequestJSON)

    def test_get_tracking(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = "{}"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v1/tracking/89108749065090",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = ErrorResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedErrorResponse)
            )


if __name__ == "__main__":
    unittest.main()


TRACKING_PAYLOAD = {
    "tracking_numbers": ["89108749065090"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "amazon_shipping",
            "carrier_name": "amazon_shipping",
            "delivered": True,
            "estimated_delivery": "2019-04-04",
            "events": [
                {
                    "code": "Delivered",
                    "date": "2019-04-04",
                    "description": "Delivered",
                    "location": "San Bernardino, CA, 92404, US",
                    "time": "06:45",
                }
            ],
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
            "code": "incididunt qui",
            "details": {"note": "sint est", "tracking_number": "89108749065090"},
            "message": "officia cillum ut",
        },
        {
            "carrier_id": "amazon_shipping",
            "carrier_name": "amazon_shipping",
            "code": "nostrud laboris ex culpa do",
            "details": {"note": "incididunt", "tracking_number": "89108749065090"},
            "message": "consequat quis ut minim voluptate",
        },
    ],
]


TrackingRequestJSON = ["89108749065090"]

TrackingResponseJSON = """{
    "trackingId": "89108749065090",
    "eventHistory": [
        {
            "eventCode": "Delivered",
            "location": {
                "city": "San Bernardino",
                "countryCode": "US",
                "stateOrRegion": "CA",
                "postalCode": "92404"
            },
            "eventTime": "2019-04-04T06:45:12Z"
        }
    ],
    "promisedDeliveryDate": "2019-04-04T07:05:06Z",
    "summary": {
        "status": "Delivered"
    }
}
"""

ErrorResponseJSON = """{
    "errors": [
        {
            "code": "incididunt qui",
            "message": "officia cillum ut",
            "details": "sint est"
        },
        {
            "code": "nostrud laboris ex culpa do",
            "message": "consequat quis ut minim voluptate",
            "details": "incididunt"
        }
    ]
}
"""
