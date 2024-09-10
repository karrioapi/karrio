import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAsendiaUSTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/A1/v2.0/Tracking/Milestone?trackingNumberVendor=89108749065090",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["89108749065090"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "asendia_us",
            "carrier_name": "asendia_us",
            "delivered": False,
            "events": [
                {
                    "code": "s10",
                    "date": "2021-08-09",
                    "description": "Delivered",
                    "time": "11:13 AM",
                },
                {
                    "code": "s8",
                    "date": "2021-08-09",
                    "description": "Arrived at Destination Delivery Office",
                    "time": "09:07 AM",
                },
                {
                    "code": "s7",
                    "date": "2021-08-07",
                    "description": "Out of Customs",
                    "time": "13:17 PM",
                },
                {
                    "code": "s5",
                    "date": "2021-08-07",
                    "description": "Arrived in Destination Country",
                    "location": "LAKSI MAIL CENTER",
                    "time": "09:43 AM",
                },
                {
                    "code": "s4",
                    "date": "2021-07-30",
                    "description": "Departed from USA",
                    "location": "Asendia US (Philadelphia)",
                    "time": "08:08 AM",
                },
                {
                    "code": "s2d",
                    "date": "2021-07-30",
                    "description": "Shipment dispatched by Asendia",
                    "location": "Folcroft, PA 19032",
                    "time": "10:14 AM",
                },
                {
                    "code": "s2c",
                    "date": "2021-07-30",
                    "description": "Service dispatched by Asendia",
                    "location": "Folcroft, PA 19032",
                    "time": "10:10 AM",
                },
                {
                    "code": "s2b",
                    "date": "2021-07-29",
                    "description": "Sorted by Asendia",
                    "location": "Folcroft, PA 19032",
                    "time": "16:33 PM",
                },
                {
                    "code": "s2a",
                    "date": "2021-07-28",
                    "description": "Processed By Asendia",
                    "location": "Asendia US (Philadelphia)",
                    "time": "21:44 PM",
                },
                {
                    "code": "s1",
                    "date": "2021-07-24",
                    "description": "Shipment Information Received",
                    "time": "13:00 PM",
                },
            ],
            "status": "in_transit",
            "tracking_number": "RL924104146CH",
        }
    ],
    [
        {
            "carrier_id": "asendia_us",
            "carrier_name": "asendia_us",
            "code": 200,
            "details": {},
        }
    ],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "asendia_us",
            "carrier_name": "asendia_us",
            "code": 401,
            "details": {},
            "message": "Authentication to the resource has been denied: incorrect "
            "username or password.",
        }
    ],
]


TrackingRequest = ["89108749065090"]

TrackingResponse = """{
  "data": [
    {
      "trackingNumberVendor": "RL924104146CH",
      "customerReferenceNumber": "9400109205568727179826",
      "trackingMilestoneEvents": [
        {
          "eventCode": "s10",
          "eventDescription": "Delivered",
          "eventLocation": "",
          "eventOn": "2021-08-09T11:13:00+00:00"
        },
        {
          "eventCode": "s8",
          "eventDescription": "Arrived at Destination Delivery Office",
          "eventLocation": "",
          "eventOn": "2021-08-09T09:07:00+00:00"
        },
        {
          "eventCode": "s7",
          "eventDescription": "Out of Customs",
          "eventLocation": "",
          "eventOn": "2021-08-07T13:17:00+00:00"
        },
        {
          "eventCode": "s5",
          "eventDescription": "Arrived in Destination Country",
          "eventLocation": "LAKSI MAIL CENTER",
          "eventOn": "2021-08-07T09:43:00+00:00"
        },
        {
          "eventCode": "s4",
          "eventDescription": "Departed from USA",
          "eventLocation": "Asendia US (Philadelphia)",
          "eventOn": "2021-07-30T08:08:16+00:00"
        },
        {
          "eventCode": "s2d",
          "eventDescription": "Shipment dispatched by Asendia",
          "eventLocation": "Folcroft, PA 19032",
          "eventOn": "2021-07-30T10:14:50.452565+00:00"
        },
        {
          "eventCode": "s2c",
          "eventDescription": "Service dispatched by Asendia",
          "eventLocation": "Folcroft, PA 19032",
          "eventOn": "2021-07-30T10:10:51.867423+00:00"
        },
        {
          "eventCode": "s2b",
          "eventDescription": "Sorted by Asendia",
          "eventLocation": "Folcroft, PA 19032",
          "eventOn": "2021-07-29T16:33:14.998765+00:00"
        },
        {
          "eventCode": "s2a",
          "eventDescription": "Processed By Asendia",
          "eventLocation": "Asendia US (Philadelphia)",
          "eventOn": "2021-07-28T21:44:44+00:00"
        },
        {
          "eventCode": "s1",
          "eventDescription": "Shipment Information Received",
          "eventLocation": "",
          "eventOn": "2021-07-24T13:00:15.85088+00:00"
        }
      ]
    }
  ],
  "responseStatus": {
    "responseStatusCode": 200,
    "responseStatusMessage": ""
  }
}
"""

ErrorResponse = """{
	"responseStatusCode": 401,
	"responseStatusMessage": "Authentication to the resource has been denied: incorrect username or password."
}
"""
