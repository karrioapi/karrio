import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAustraliaPostTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v1/track?tracking_ids=7XX1000634011427",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_tracking_error_response(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.return_value = TrackingErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedTrackingErrorResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["7XX1000634011427"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "delivered": False,
            "info": {
                "carrier_tracking_link": "https://auspost.com.au/mypost/beta/track/details/ET123456789AU"
            },
            "status": "in_transit",
            "tracking_number": "ET123456789AU",
        },
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "delivered": True,
            "events": [
                {
                    "date": "2021-01-21",
                    "description": "Delivered - Left in a safe place",
                    "location": "KEW VIC",
                    "time": "11:04 AM",
                },
                {
                    "date": "2021-01-21",
                    "description": "Onboard for delivery",
                    "location": "OAKLEIGH SOUTH VIC",
                    "time": "08:34 AM",
                },
                {
                    "date": "2021-01-20",
                    "description": "In transit to next facility in OAKLEIGH SOUTH VIC",
                    "time": "11:55 AM",
                },
                {
                    "date": "2021-01-20",
                    "description": "Item processed at facility",
                    "location": "SUNSHINE WEST VIC",
                    "time": "11:48 AM",
                },
                {
                    "date": "2021-01-19",
                    "description": "In transit to next facility in SUNSHINE WEST VIC",
                    "time": "22:13 PM",
                },
                {
                    "date": "2021-01-19",
                    "description": "Item processed at facility",
                    "location": "CHULLORA NSW",
                    "time": "21:17 PM",
                },
                {
                    "date": "2021-01-19",
                    "description": "Arrived awaiting clearance (Inbound)",
                    "location": "SYDNEY NSW",
                    "time": "16:09 PM",
                },
                {
                    "date": "2021-01-07",
                    "description": "Cleared and awaiting international departure",
                    "location": "CHICAGO (US)",
                    "time": "08:49 AM",
                },
                {
                    "date": "2021-01-06",
                    "description": "Received item from Sender (Outbound)",
                    "location": "US-60199, UNITED STATES",
                    "time": "08:27 AM",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://auspost.com.au/mypost/beta/track/details/LX123456789US",
                "shipment_service": "International",
            },
            "status": "delivered",
            "tracking_number": "LX123456789US",
        },
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "delivered": True,
            "events": [
                {
                    "date": "2021-02-02",
                    "description": "Delivered",
                    "location": "NZ",
                    "time": "07:38 AM",
                },
                {
                    "date": "2021-02-02",
                    "description": "Onboard for delivery",
                    "location": "NZ",
                    "time": "06:03 AM",
                },
                {
                    "date": "2021-02-02",
                    "description": "Onboard for delivery",
                    "location": "Transit Scan",
                    "time": "01:55 AM",
                },
                {
                    "date": "2021-02-02",
                    "description": "Arrived in New Zealand",
                    "location": "NZ",
                    "time": "01:51 AM",
                },
                {
                    "date": "2021-02-02",
                    "description": "Item cleared by Customs",
                    "location": "Transit Scan",
                    "time": "01:21 AM",
                },
                {
                    "date": "2021-01-31",
                    "description": "Item is in Customs",
                    "location": "Transit Scan",
                    "time": "07:57 AM",
                },
                {
                    "date": "2021-01-28",
                    "description": "Despatch Parcels from Export Facility",
                    "location": "Transit Scan",
                    "time": "03:33 AM",
                },
                {
                    "date": "2021-01-27",
                    "description": "Processed at Export Facility",
                    "location": "Transit Scan",
                    "time": "19:24 PM",
                },
                {
                    "date": "2021-01-27",
                    "description": "Shipping information approved by Australia Post",
                    "time": "13:31 PM",
                },
                {
                    "date": "2021-01-27",
                    "description": "Shipping information received by Australia Post",
                    "time": "13:31 PM",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://auspost.com.au/mypost/beta/track/details/00123456789000123400",
                "shipment_service": "International",
            },
            "status": "delivered",
            "tracking_number": "00123456789000123400",
        },
    ],
    [],
]

ParsedTrackingErrorResponse = [
    [],
    [
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "code": "ESB-10001",
            "details": {"tracking_number": "7XX1000"},
            "message": "Invalid tracking ID",
        }
    ],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "code": "51101",
            "details": {},
            "message": "The request must contain 10 or less AP article ids, consignment "
            "ids, or barcode ids.",
        }
    ],
]


TrackingRequest = {"tracking_ids": ["7XX1000634011427"]}

TrackingResponse = """{
  "tracking_results": [
    {
      "tracking_id": "ET123456789AU",
      "trackable_items": [
        {
          "consignment_id": "ET123456789AU",
          "number_of_items": 1,
          "items": [
            {
              "article_id": "ET123456789AU",
              "product_type": "International Express",
              "events": [
                {
                  "description": "Processed by air carrier",
                  "date": "2021-02-03T08:08:00+11:00"
                },
                {
                  "description": "Processed by air carrier",
                  "date": "2021-01-29T11:31:00+11:00"
                },
                {
                  "description": "Processed by air carrier",
                  "date": "2021-01-29T04:54:00+11:00"
                },
                {
                  "location": "BRISBANE QLD",
                  "description": "Cleared and awaiting international departure",
                  "date": "2021-01-28T01:59:11+11:00"
                },
                {
                  "location": "BRISBANE QLD",
                  "description": "Arrived at facility",
                  "date": "2021-01-27T23:51:48+11:00"
                },
                {
                  "location": "BEENLEIGH QLD",
                  "description": "Received by Australia Post",
                  "date": "2021-01-27T11:06:59+11:00"
                },
                {
                  "description": "Shipping information approved by Australia Post",
                  "date": "2021-01-27T03:04:03+11:00"
                },
                {
                  "description": "Shipping information received by Australia Post",
                  "date": "2021-01-27T00:22:43+11:00"
                }
              ],
              "status": "Unknown"
            }
          ]
        }
      ]
    },
    {
      "tracking_id": "LX123456789US",
      "status": "Delivered",
      "trackable_items": [
        {
          "article_id": "LX123456789US",
          "product_type": "International",
          "events": [
            {
              "location": "KEW VIC",
              "description": "Delivered - Left in a safe place",
              "date": "2021-01-21T11:04:27+11:00"
            },
            {
              "location": "OAKLEIGH SOUTH VIC",
              "description": "Onboard for delivery",
              "date": "2021-01-21T08:34:14+11:00"
            },
            {
              "description": "In transit to next facility in OAKLEIGH SOUTH VIC",
              "date": "2021-01-20T11:55:37+11:00"
            },
            {
              "location": "SUNSHINE WEST VIC",
              "description": "Item processed at facility",
              "date": "2021-01-20T11:48:23+11:00"
            },
            {
              "description": "In transit to next facility in SUNSHINE WEST VIC",
              "date": "2021-01-19T22:13:13+11:00"
            },
            {
              "location": "CHULLORA NSW",
              "description": "Item processed at facility",
              "date": "2021-01-19T21:17:09+11:00"
            },
            {
              "location": "SYDNEY NSW",
              "description": "Arrived awaiting clearance (Inbound)",
              "date": "2021-01-19T16:09:03+11:00"
            },
            {
              "location": "CHICAGO (US)",
              "description": "Cleared and awaiting international departure",
              "date": "2021-01-07T08:49:00+11:00"
            },
            {
              "location": "US-60199, UNITED STATES",
              "description": "Received item from Sender (Outbound)",
              "date": "2021-01-06T08:27:00+11:00"
            }
          ],
          "status": "Delivered"
        }
      ]
    },
    {
      "tracking_id": "00123456789000123400",
      "status": "Delivered",
      "trackable_items": [
        {
          "article_id": "00123456789000123400",
          "product_type": "International",
          "events": [
            {
              "location": "NZ",
              "description": "Delivered",
              "date": "2021-02-02T07:38:56+11:00"
            },
            {
              "location": "NZ",
              "description": "Onboard for delivery",
              "date": "2021-02-02T06:03:04+11:00"
            },
            {
              "location": "Transit Scan",
              "description": "Onboard for delivery",
              "date": "2021-02-02T01:55:11+11:00"
            },
            {
              "location": "NZ",
              "description": "Arrived in New Zealand",
              "date": "2021-02-02T01:51:00+11:00"
            },
            {
              "location": "Transit Scan",
              "description": "Item cleared by Customs",
              "date": "2021-02-02T01:21:00+11:00"
            },
            {
              "location": "Transit Scan",
              "description": "Item is in Customs",
              "date": "2021-01-31T07:57:52+11:00"
            },
            {
              "location": "Transit Scan",
              "description": "Despatch Parcels from Export Facility",
              "date": "2021-01-28T03:33:43+11:00"
            },
            {
              "location": "Transit Scan",
              "description": "Processed at Export Facility",
              "date": "2021-01-27T19:24:41+11:00"
            },
            {
              "description": "Shipping information approved by Australia Post",
              "date": "2021-01-27T13:31:54+11:00"
            },
            {
              "description": "Shipping information received by Australia Post",
              "date": "2021-01-27T13:31:07+11:00"
            }
          ],
          "status": "Delivered"
        }
      ]
    }
  ]
}
"""

TrackingErrorResponse = """{
  "tracking_results": [
    {
      "tracking_id": "7XX1000",
      "errors": [
        {
          "code": "ESB-10001",
          "name": "Invalid tracking ID"
        }
      ]
    }
  ]
}
"""

ErrorResponse = """{
  "errors": [
    {
      "code": "51101",
      "name": "TOO_MANY_AP_TRACKING_IDS",
      "message": "The request must contain 10 or less AP article ids, consignment ids, or barcode ids."
    }
  ]
}
"""
