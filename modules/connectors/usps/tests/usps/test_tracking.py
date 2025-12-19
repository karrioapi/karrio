import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging as logger

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUSPSTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/tracking/v3/tracking/89108749065090?expand=DETAIL",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)

    def test_parse_auth_error_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = AuthErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(lib.to_dict(parsed_response), ParsedAuthErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["89108749065090"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "delivered": True,
            "events": [
                {
                    "code": "01",
                    "date": "2024-11-22",
                    "description": "Delivered, Parcel Locker",
                    "location": "HERNANDO, 34442, FL",
                    "status": "delivered",
                    "time": "13:58 PM",
                    "timestamp": "2024-11-22T13:58:00.000Z",
                },
                {
                    "code": "OF",
                    "date": "2024-11-22",
                    "description": "Out for Delivery",
                    "location": "HERNANDO, 34442, FL",
                    "status": "out_for_delivery",
                    "time": "09:10 AM",
                    "timestamp": "2024-11-22T09:10:00.000Z",
                },
                {
                    "code": "07",
                    "date": "2024-11-22",
                    "description": "Arrived at Post Office",
                    "location": "LECANTO, 34461, FL",
                    "time": "08:59 AM",
                    "timestamp": "2024-11-22T08:59:00.000Z",
                },
                {
                    "code": "A1",
                    "date": "2024-11-20",
                    "description": "Arrived at USPS Regional Facility",
                    "location": "JACKSONVILLE FL DISTRIBUTION CENTER",
                    "time": "01:13 AM",
                    "timestamp": "2024-11-20T01:13:00.000Z",
                },
                {
                    "code": "TL",
                    "date": "2024-11-20",
                    "description": "In Transit to Next Facility",
                    "status": "in_transit",
                    "time": "01:11 AM",
                    "timestamp": "2024-11-20T01:11:00.000Z",
                },
                {
                    "code": "TL",
                    "date": "2024-11-19",
                    "description": "In Transit to Next Facility",
                    "status": "in_transit",
                    "time": "18:07 PM",
                    "timestamp": "2024-11-19T18:07:00.000Z",
                },
                {
                    "code": "TL",
                    "date": "2024-11-19",
                    "description": "In Transit to Next Facility",
                    "status": "in_transit",
                    "time": "12:11 PM",
                    "timestamp": "2024-11-19T12:11:00.000Z",
                },
                {
                    "code": "T1",
                    "date": "2024-11-19",
                    "description": "Departed USPS Regional Facility",
                    "location": "QUEENS NY DISTRIBUTION CENTER",
                    "time": "06:16 AM",
                    "timestamp": "2024-11-19T06:16:00.000Z",
                },
                {
                    "code": "10",
                    "date": "2024-11-18",
                    "description": "Arrived at USPS Regional Origin Facility",
                    "location": "QUEENS NY DISTRIBUTION CENTER",
                    "time": "18:02 PM",
                    "timestamp": "2024-11-18T18:02:00.000Z",
                },
                {
                    "code": "SF",
                    "date": "2024-11-18",
                    "description": "Departed Post Office",
                    "location": "JAMAICA, 11430, NY",
                    "time": "17:01 PM",
                    "timestamp": "2024-11-18T17:01:00.000Z",
                },
                {
                    "code": "03",
                    "date": "2024-11-18",
                    "description": "USPS in possession of item",
                    "location": "JAMAICA, 11430, NY",
                    "time": "11:10 AM",
                    "timestamp": "2024-11-18T11:10:00.000Z",
                },
                {
                    "code": "GX",
                    "date": "2024-11-15",
                    "description": "Shipping Label Created, USPS Awaiting Item",
                    "location": "SPRINGFIELD GARDENS, 11413, NY",
                    "time": "11:32 AM",
                    "timestamp": "2024-11-15T11:32:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://tools.usps.com/go/TrackConfirmAction?tLabels=9400109104250532908587",
                "shipment_destination_postal_code": "34442",
                "shipment_origin_postal_code": "11430",
                "shipment_service": "USPS Ground Advantage<SUP>&#153;</SUP>",
            },
            "status": "delivered",
            "tracking_number": "9400109104250532908587",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "code": "string",
            "details": {
                "source": {"example": "string", "parameter": "string"},
                "tracking_number": "89108749065090",
            },
            "message": "string",
        }
    ],
]

ParsedAuthErrorResponse = [
    [],
    [
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "code": "invalid_client",
            "message": "Client authentication failed.",
            "details": {
                "tracking_number": "89108749065090",
                "error_uri": "https://datatracker.ietf.org/doc/html/rfc6749#page-45",
            },
        }
    ],
]

TrackingRequest = ["89108749065090"]

TrackingResponse = """{
  "destinationCity": "HERNANDO",
  "destinationState": "FL",
  "destinationZIP": "34442",
  "emailEnabled": "true",
  "kahalaIndicator": "false",
  "mailClass": "USPS Ground Advantage<SUP>&#153;</SUP>",
  "mailType": "DM",
  "originCity": "JAMAICA",
  "originState": "NY",
  "originZIP": "11430",
  "proofOfDeliveryEnabled": "false",
  "restoreEnabled": "false",
  "RRAMEnabled": "false",
  "RREEnabled": "false",
  "services": [
    "USPS Tracking<SUP>&#174;</SUP>",
    "Up to $100 insurance included"
  ],
  "serviceTypeCode": "001",
  "status": "Delivered, Parcel Locker",
  "statusCategory": "Delivered",
  "statusSummary": "Your item was delivered to a parcel locker at 1:58 pm on November 22, 2024 in HERNANDO, FL 34442.",
  "tableCode": "T",
  "uniqueMailPieceID": "110158946",
  "mailPieceIntakeDate": "2024-11-15 11:09:19.000000",
  "trackingEvents": [
    {
      "eventType": "Delivered, Parcel Locker",
      "eventTimestamp": "2024-11-22T13:58:00",
      "GMTTimestamp": "2024-11-22T18:58:40Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": "HERNANDO",
      "eventState": "FL",
      "eventZIP": "34442",
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "01",
      "additionalProp": null
    },
    {
      "eventType": "Out for Delivery",
      "eventTimestamp": "2024-11-22T09:10:00",
      "GMTTimestamp": "2024-11-22T14:10:45Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": "HERNANDO",
      "eventState": "FL",
      "eventZIP": "34442",
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "OF",
      "additionalProp": null
    },
    {
      "eventType": "Arrived at Post Office",
      "eventTimestamp": "2024-11-22T08:59:00",
      "GMTTimestamp": "2024-11-22T13:59:45Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": "LECANTO",
      "eventState": "FL",
      "eventZIP": "34461",
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "07",
      "additionalProp": null
    },
    {
      "eventType": "Arrived at USPS Regional Facility",
      "eventTimestamp": "2024-11-20T01:13:00",
      "GMTTimestamp": "2024-11-20T06:13:31Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": "JACKSONVILLE FL DISTRIBUTION CENTER",
      "eventState": null,
      "eventZIP": null,
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "A1",
      "additionalProp": null
    },
    {
      "eventType": "In Transit to Next Facility",
      "eventTimestamp": "2024-11-20T01:11:00",
      "GMTTimestamp": "2024-11-20T06:11:52Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": null,
      "eventState": null,
      "eventZIP": null,
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "TL",
      "additionalProp": null
    },
    {
      "eventType": "In Transit to Next Facility",
      "eventTimestamp": "2024-11-19T18:07:00",
      "GMTTimestamp": "2024-11-19T23:07:58Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": null,
      "eventState": null,
      "eventZIP": null,
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "TL",
      "additionalProp": null
    },
    {
      "eventType": "In Transit to Next Facility",
      "eventTimestamp": "2024-11-19T12:11:00",
      "GMTTimestamp": "2024-11-19T17:11:23Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": null,
      "eventState": null,
      "eventZIP": null,
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "TL",
      "additionalProp": null
    },
    {
      "eventType": "Departed USPS Regional Facility",
      "eventTimestamp": "2024-11-19T06:16:00",
      "GMTTimestamp": "2024-11-19T11:16:41Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": "QUEENS NY DISTRIBUTION CENTER",
      "eventState": null,
      "eventZIP": null,
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "T1",
      "additionalProp": null
    },
    {
      "eventType": "Arrived at USPS Regional Origin Facility",
      "eventTimestamp": "2024-11-18T18:02:00",
      "GMTTimestamp": "2024-11-18T23:02:52Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": "QUEENS NY DISTRIBUTION CENTER",
      "eventState": null,
      "eventZIP": null,
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "10",
      "additionalProp": null
    },
    {
      "eventType": "Departed Post Office",
      "eventTimestamp": "2024-11-18T17:01:00",
      "GMTTimestamp": "2024-11-18T22:01:35Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": "JAMAICA",
      "eventState": "NY",
      "eventZIP": "11430",
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "SF",
      "additionalProp": null
    },
    {
      "eventType": "USPS in possession of item",
      "eventTimestamp": "2024-11-18T11:10:00",
      "GMTTimestamp": "2024-11-18T16:10:31Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": "JAMAICA",
      "eventState": "NY",
      "eventZIP": "11430",
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "03",
      "additionalProp": null
    },
    {
      "eventType": "Shipping Label Created, USPS Awaiting Item",
      "eventTimestamp": "2024-11-15T11:32:00",
      "GMTTimestamp": "2024-11-15T16:32:33Z",
      "GMTOffset": "-05:00",
      "eventCountry": null,
      "eventCity": "SPRINGFIELD GARDENS",
      "eventState": "NY",
      "eventZIP": "11413",
      "firm": null,
      "name": null,
      "authorizedAgent": "false",
      "eventCode": "GX",
      "additionalProp": null
    }
  ],
  "trackingNumber": "9400109104250532908587"
}
"""

ErrorResponse = """{
  "apiVersion": "string",
  "error": {
    "code": "string",
    "message": "string",
    "errors": [
      {
        "status": "string",
        "code": "string",
        "title": "string",
        "detail": "string",
        "source": {
          "parameter": "string",
          "example": "string"
        }
      }
    ]
  }
}
"""

AuthErrorResponse = """{
    "error": "invalid_client",
    "error_description": "Client authentication failed.",
    "error_uri": "https://datatracker.ietf.org/doc/html/rfc6749#page-45"
}
"""
