import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship import Tracking
from purplship.core.models import TrackingRequest
from tests.australiapost.fixture import gateway


class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequestJSON)

    def test_get_tracking(self):
        with patch("purplship.mappers.australiapost.proxy.http") as mock:
            mock.return_value = "{}"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v1/track?tracking_ids=7XX1000%2C7XX1000634011427",
            )

    def test_parse_tracking_response(self):
        with patch("purplship.mappers.australiapost.proxy.http") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )

    def test_parse_tracking_error_response(self):
        with patch("purplship.mappers.australiapost.proxy.http") as mock:
            mock.return_value = TrackingErrorResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingErrorResponse)
            )

    def test_parse_error_response(self):
        with patch("purplship.mappers.australiapost.proxy.http") as mock:
            mock.return_value = ErrorResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedErrorResponse)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["7XX1000,7XX1000634011427"]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "delivered": True,
            "events": [
                {
                    "date": "2014-05-30",
                    "description": "Delivered",
                    "location": "ALEXANDRIA NSW",
                    "time": "14:43",
                },
                {
                    "date": "2014-05-30",
                    "description": "With Australia Post for delivery today",
                    "location": "ALEXANDRIA NSW",
                    "time": "06:08",
                },
                {
                    "date": "2014-05-29",
                    "description": "Processed through Australia Post facility",
                    "location": "CHULLORA NSW",
                    "time": "19:40",
                },
                {
                    "date": "2014-05-29",
                    "description": "Arrived at facility in destination country",
                    "location": "SYDNEY (AU)",
                    "time": "10:16",
                },
                {
                    "date": "2014-05-26",
                    "description": "Departed facility",
                    "location": "JOHN F. KENNEDY APT/NEW YORK (US)",
                    "time": "05:00",
                },
                {
                    "date": "2014-05-26",
                    "description": "Departed facility",
                    "location": "JOHN F. KENNEDY APT/NEW YORK (US)",
                    "time": "05:00",
                },
                {
                    "date": "2014-05-23",
                    "description": "Shipping information approved by Australia Post",
                    "time": "14:27",
                },
            ],
            "tracking_number": "7XX1000634011427",
        }
    ],
    [
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "code": "ESB-10001",
            "details": {"tracking_number": "7XX1000"},
        }
    ],
]

ParsedTrackingErrorResponse = [
    [],
    [
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "code": "51101",
            "details": {"name": "TOO_MANY_AP_TRACKING_IDS"},
            "message": "The request must contain 10 or less AP article ids, consignment ids, or barcode ids.",
        }
    ],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "code": "API_002",
            "details": {"name": "Too many requests"},
            "message": "Too many requests",
        }
    ],
]


# Serialized sample

TrackingRequestJSON = {"tracking_ids": "7XX1000,7XX1000634011427"}

TrackingResponseJSON = """{
  "tracking_results": [
    {
      "tracking_id": "7XX1000",
      "errors": [
        {
          "code": "ESB-10001",
          "name": "Invalid tracking ID"
        }
      ]
    },
    {
      "tracking_id": "7XX1000634011427",
      "status": "Delivered",
      "trackable_items": [
        {
          "article_id": "7XX1000634011427",
          "product_type": "eParcel",
          "events": [
            {
              "location": "ALEXANDRIA NSW",
              "description": "Delivered",
              "date": "2014-05-30T14:43:09+10:00"
            },
            {
              "location": "ALEXANDRIA NSW",
              "description": "With Australia Post for delivery today",
              "date": "2014-05-30T06:08:51+10:00"
            },
            {
              "location": "CHULLORA NSW",
              "description": "Processed through Australia Post facility",
              "date": "2014-05-29T19:40:19+10:00"
            },
            {
              "location": "SYDNEY (AU)",
              "description": "Arrived at facility in destination country",
              "date": "2014-05-29T10:16:00+10:00"
            },
            {
              "location": "JOHN F. KENNEDY APT\/NEW YORK (US)",
              "description": "Departed facility",
              "date": "2014-05-26T05:00:00+10:00"
            },
            {
              "location": "JOHN F. KENNEDY APT\/NEW YORK (US)",
              "description": "Departed facility",
              "date": "2014-05-26T05:00:00+10:00"
            },
            {
              "description": "Shipping information approved by Australia Post",
              "date": "2014-05-23T14:27:15+10:00"
            }
          ],
          "status": "Delivered"
        }
      ]
    }
  ]
}
"""

TrackingErrorResponseJSON = """{
  "errors": [
    {
      "code": "51101",
      "name": "TOO_MANY_AP_TRACKING_IDS",
      "message": "The request must contain 10 or less AP article ids, consignment ids, or barcode ids."
    }
  ]
}
"""

ErrorResponseJSON = """{
  "errors": [
    {
      "message": "Too many requests",
      "error_code": "API_002",
      "error_name": "Too many requests"
    }
  ]
}
"""
