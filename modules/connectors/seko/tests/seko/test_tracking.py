import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSEKOLogisticsTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/labels/statusv2",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)

    def test_parse_tracking_response_multiple(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse2
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse2)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["6994008906", "6994008907"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "delivered": True,
            "events": [
                {
                    "code": "OP-72",
                    "date": "2024-12-24",
                    "description": "DELIVERED",
                    "location": "NL",
                    "time": "13:31 PM",
                },
                {
                    "code": "OP-21",
                    "date": "2024-12-24",
                    "description": "The parcel is expected to be delivered during the day.",
                    "location": "NL",
                    "time": "07:37 AM",
                },
                {
                    "code": "OP-50",
                    "date": "2024-12-24",
                    "description": "The parcel has reached the parcel center.",
                    "location": "NL",
                    "time": "06:13 AM",
                },
                {
                    "code": "OP-50",
                    "date": "2024-12-23",
                    "description": "The parcel has reached the parcel center.",
                    "location": "Essen, DE",
                    "time": "15:29 PM",
                },
                {
                    "code": "OP-79",
                    "date": "2024-12-23",
                    "description": "The parcel has left the parcel center.",
                    "location": "Essen, DE",
                    "time": "15:29 PM",
                },
                {
                    "code": "OP-4",
                    "date": "2024-12-23",
                    "description": "The parcel was handed over to GLS.",
                    "location": "Essen, DE",
                    "time": "15:29 PM",
                },
                {
                    "code": "OP-4",
                    "date": "2024-12-17",
                    "description": "International transit to destination country ",
                    "location": "EGHAM, SURREY,GB",
                    "time": "11:06 AM",
                },
                {
                    "code": "OP-3",
                    "date": "2024-12-17",
                    "description": "Processed through Export Hub",
                    "location": "Egham, Surrey,GB",
                    "time": "09:18 AM",
                },
                {
                    "code": "OP-8",
                    "date": "2024-12-13",
                    "description": "The parcel data was entered into the GLS IT system; the parcel was not yet handed over to GLS.",
                    "location": "GB",
                    "time": "10:55 AM",
                },
                {
                    "code": "OP-1",
                    "date": "2024-12-13",
                    "description": "Tracking number allocated & order ready",
                    "location": "LONDON,EGHAM,GB",
                    "time": "09:55 AM",
                },
            ],
            "info": {
                "carrier_tracking_link": "http://track.omniparcel.com/999880931315",
                "expected_delivery": "2024-12-24",
                "shipping_date": "2024-12-24",
            },
            "meta": {"reference": "#N30080"},
            "status": "delivered",
            "tracking_number": "999880931315",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "code": "Error",
            "details": {
                "Key": "CountryCode",
                "Property": "Destination.Address.CountryCode",
            },
            "level": "error",
            "message": "CountryCode is required",
        }
    ],
]

ParsedTrackingResponse2 = [
    [
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "delivered": False,
            "events": [
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Pre-advice received",
                    "time": "11:28 AM",
                },
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Tracking number allocated & order ready",
                    "location": "LONDON,EGHAM,GB",
                    "time": "10:28 AM",
                },
            ],
            "status": "pending",
            "tracking_number": "DG30754101650",
            "info": {
                "carrier_tracking_link": "http://track.omniparcel.com/DG30754101650"
            },
            "meta": {},
        },
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "delivered": False,
            "events": [
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Pre-advice received",
                    "time": "11:56 AM",
                },
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Tracking number allocated & order ready",
                    "location": "LONDON,EGHAM,GB",
                    "time": "10:56 AM",
                },
            ],
            "status": "pending",
            "tracking_number": "DG30754101664",
            "info": {
                "carrier_tracking_link": "http://track.omniparcel.com/DG30754101664"
            },
            "meta": {},
        },
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "delivered": False,
            "events": [
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Pre-advice received",
                    "time": "11:57 AM",
                },
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Tracking number allocated & order ready",
                    "location": "LONDON,EGHAM,GB",
                    "time": "10:57 AM",
                },
            ],
            "status": "pending",
            "tracking_number": "DG30754101665",
            "info": {
                "carrier_tracking_link": "http://track.omniparcel.com/DG30754101665"
            },
            "meta": {},
        },
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "delivered": False,
            "events": [
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Pre-advice received",
                    "time": "12:02 PM",
                },
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Tracking number allocated & order ready",
                    "location": "LONDON,EGHAM,GB",
                    "time": "11:02 AM",
                },
            ],
            "status": "pending",
            "tracking_number": "DG30754101666",
            "info": {
                "carrier_tracking_link": "http://track.omniparcel.com/DG30754101666"
            },
            "meta": {},
        },
    ],
    [],
]

TrackingRequest = ["6994008906", "6994008907"]

TrackingResponse = """[
  {
    "ConsignmentNo": "999880931315",
    "Status": "DELIVERED",
    "Picked": "2024-12-24T13:31:47",
    "Delivered": "2024-12-24T13:31:47",
    "Tracking": "http://track.omniparcel.com/999880931315",
    "Reference1": "#N30080",
    "Events": [
      {
        "EventDT": "2024-12-13T09:55:23.043",
        "Code": null,
        "OmniCode": "OP-1",
        "Description": "Tracking number allocated & order ready",
        "Location": "LONDON,EGHAM,GB",
        "Part": 1
      },
      {
        "EventDT": "2024-12-13T10:55:24",
        "Code": "0.100",
        "OmniCode": "OP-8",
        "Description": "The parcel data was entered into the GLS IT system; the parcel was not yet handed over to GLS.",
        "Location": "GB",
        "Part": 1
      },
      {
        "EventDT": "2024-12-17T09:18:01.733",
        "Code": null,
        "OmniCode": "OP-3",
        "Description": "Processed through Export Hub",
        "Location": "Egham, Surrey,GB",
        "Part": 1
      },
      {
        "EventDT": "2024-12-17T11:06:29.043",
        "Code": null,
        "OmniCode": "OP-4",
        "Description": "International transit to destination country ",
        "Location": "EGHAM, SURREY,GB",
        "Part": 1
      },
      {
        "EventDT": "2024-12-23T15:29:00",
        "Code": "0.0",
        "OmniCode": "OP-4",
        "Description": "The parcel was handed over to GLS.",
        "Location": "Essen, DE",
        "Part": 1
      },
      {
        "EventDT": "2024-12-23T15:29:00",
        "Code": "1.0",
        "OmniCode": "OP-79",
        "Description": "The parcel has left the parcel center.",
        "Location": "Essen, DE",
        "Part": 1
      },
      {
        "EventDT": "2024-12-23T15:29:00",
        "Code": "2.0",
        "OmniCode": "OP-50",
        "Description": "The parcel has reached the parcel center.",
        "Location": "Essen, DE",
        "Part": 1
      },
      {
        "EventDT": "2024-12-24T06:13:10",
        "Code": "2.0",
        "OmniCode": "OP-50",
        "Description": "The parcel has reached the parcel center.",
        "Location": "NL",
        "Part": 1
      },
      {
        "EventDT": "2024-12-24T07:37:54",
        "Code": "11.0",
        "OmniCode": "OP-21",
        "Description": "The parcel is expected to be delivered during the day.",
        "Location": "NL",
        "Part": 1
      },
      {
        "EventDT": "2024-12-24T13:31:47",
        "Code": "3.0",
        "OmniCode": "OP-72",
        "Description": "DELIVERED",
        "Location": "NL",
        "Part": 1
      }
    ]
  }
]
"""

TrackingResponse2 = """[
  {
    "ConsignmentNo": "DG30754101650",
    "Status": "Pre-advice received",
    "Picked": null,
    "Delivered": null,
    "Tracking": "http://track.omniparcel.com/DG30754101650",
    "Reference1": "",
    "Events": [
      {
        "EventDT": "2024-10-25T10:28:47.677",
        "Code": null,
        "OmniCode": "OP-1",
        "Description": "Tracking number allocated & order ready",
        "Location": "LONDON,EGHAM,GB",
        "Part": 1
      },
      {
        "EventDT": "2024-10-25T11:28:49",
        "Code": "AAY",
        "OmniCode": "OP-1",
        "Description": "Pre-advice received",
        "Location": "",
        "Part": 1
      }
    ]
  },
  {
    "ConsignmentNo": "DG30754101664",
    "Status": "Pre-advice received",
    "Picked": null,
    "Delivered": null,
    "Tracking": "http://track.omniparcel.com/DG30754101664",
    "Reference1": "",
    "Events": [
      {
        "EventDT": "2024-10-25T10:56:28.603",
        "Code": null,
        "OmniCode": "OP-1",
        "Description": "Tracking number allocated & order ready",
        "Location": "LONDON,EGHAM,GB",
        "Part": 1
      },
      {
        "EventDT": "2024-10-25T11:56:30",
        "Code": "AAY",
        "OmniCode": "OP-1",
        "Description": "Pre-advice received",
        "Location": "",
        "Part": 1
      }
    ]
  },
  {
    "ConsignmentNo": "DG30754101665",
    "Status": "Pre-advice received",
    "Picked": null,
    "Delivered": null,
    "Tracking": "http://track.omniparcel.com/DG30754101665",
    "Reference1": "",
    "Events": [
      {
        "EventDT": "2024-10-25T10:57:24.197",
        "Code": null,
        "OmniCode": "OP-1",
        "Description": "Tracking number allocated & order ready",
        "Location": "LONDON,EGHAM,GB",
        "Part": 1
      },
      {
        "EventDT": "2024-10-25T11:57:25",
        "Code": "AAY",
        "OmniCode": "OP-1",
        "Description": "Pre-advice received",
        "Location": "",
        "Part": 1
      }
    ]
  },
  {
    "ConsignmentNo": "DG30754101666",
    "Status": "Pre-advice received",
    "Picked": null,
    "Delivered": null,
    "Tracking": "http://track.omniparcel.com/DG30754101666",
    "Reference1": "",
    "Events": [
      {
        "EventDT": "2024-10-25T11:02:19.387",
        "Code": null,
        "OmniCode": "OP-1",
        "Description": "Tracking number allocated & order ready",
        "Location": "LONDON,EGHAM,GB",
        "Part": 1
      },
      {
        "EventDT": "2024-10-25T12:02:20",
        "Code": "AAY",
        "OmniCode": "OP-1",
        "Description": "Pre-advice received",
        "Location": "",
        "Part": 1
      }
    ]
  }
]
"""

ErrorResponse = """{
  "Errors": [
    {
      "Property": "Destination.Address.CountryCode",
      "Message": "CountryCode is required",
      "Key": "CountryCode",
      "Value": ""
    }
  ]
}
"""
