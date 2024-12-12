import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
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
            "delivered": False,
            "events": [
                {
                    "code": "OP-1",
                    "date": "2021-03-01",
                    "description": "Tracking number allocated & order ready",
                    "location": "SAN BERNARDINO,CA,US",
                    "time": "21:47 PM",
                },
                {
                    "code": "OP-3",
                    "date": "2021-03-05",
                    "description": "Processed through Export Hub",
                    "location": "Carson, CA,US",
                    "time": "08:56 AM",
                },
                {
                    "code": "OP-4",
                    "date": "2021-03-05",
                    "description": "International transit to destination country ",
                    "location": "CARSON, CA,US",
                    "time": "13:53 PM",
                },
            ],
            "status": "in_transit",
            "tracking_number": "WFY9001843",
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
                    "description": "Tracking number allocated & order ready",
                    "location": "LONDON,EGHAM,GB",
                    "time": "10:28 AM",
                },
                {
                    "code": "AAY",
                    "date": "2024-10-25",
                    "description": "Pre-advice received",
                    "time": "11:28 AM",
                },
            ],
            "status": "in_transit",
            "tracking_number": "DG30754101650",
        },
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "delivered": False,
            "events": [
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Tracking number allocated & order ready",
                    "location": "LONDON,EGHAM,GB",
                    "time": "10:56 AM",
                },
                {
                    "code": "AAY",
                    "date": "2024-10-25",
                    "description": "Pre-advice received",
                    "time": "11:56 AM",
                },
            ],
            "status": "in_transit",
            "tracking_number": "DG30754101664",
        },
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "delivered": False,
            "events": [
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Tracking number allocated & order ready",
                    "location": "LONDON,EGHAM,GB",
                    "time": "10:57 AM",
                },
                {
                    "code": "AAY",
                    "date": "2024-10-25",
                    "description": "Pre-advice received",
                    "time": "11:57 AM",
                },
            ],
            "status": "in_transit",
            "tracking_number": "DG30754101665",
        },
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "delivered": False,
            "events": [
                {
                    "code": "OP-1",
                    "date": "2024-10-25",
                    "description": "Tracking number allocated & order ready",
                    "location": "LONDON,EGHAM,GB",
                    "time": "11:02 AM",
                },
                {
                    "code": "AAY",
                    "date": "2024-10-25",
                    "description": "Pre-advice received",
                    "time": "12:02 PM",
                },
            ],
            "status": "in_transit",
            "tracking_number": "DG30754101666",
        },
    ],
    [],
]

TrackingRequest = ["6994008906", "6994008907"]

TrackingResponse = """[
  {
    "ConsignmentNo": "WFY9001843",
    "Status": "International transit to destination country ",
    "Picked": null,
    "Delivered": null,
    "Tracking": "http://track.omniparcel.com/1481576-WFY9001843",
    "Reference1": "S5828797:0",
    "Events": [
      {
        "EventDT": "2021-03-01T21:47:50.643",
        "Code": null,
        "OmniCode": "OP-1",
        "Description": "Tracking number allocated & order ready",
        "Location": "SAN BERNARDINO,CA,US",
        "Part": 1
      },
      {
        "EventDT": "2021-03-05T08:56:22.287",
        "Code": null,
        "OmniCode": "OP-3",
        "Description": "Processed through Export Hub",
        "Location": "Carson, CA,US",
        "Part": 1
      },
      {
        "EventDT": "2021-03-05T13:53:00.55",
        "Code": null,
        "OmniCode": "OP-4",
        "Description": "International transit to destination country ",
        "Location": "CARSON, CA,US",
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
