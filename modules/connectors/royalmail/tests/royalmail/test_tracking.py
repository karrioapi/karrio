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
        with patch("karrio.mappers.royalmail.proxy.http") as mock:
            mock.return_value = "{}"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/mailpieces/v2/090367574000000FE1E1B/events",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.royalmail.proxy.http") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )

    def test_parse_tracking_error_response(self):
        with patch("karrio.mappers.royalmail.proxy.http") as mock:
            mock.return_value = TrackingErrorResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingErrorResponse)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["090367574000000FE1E1B"]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "royalmail",
            "carrier_name": "royalmail",
            "delivered": False,
            "estimated_delivery": "2017-02-20",
            "events": [
                {
                    "code": "EVNMI",
                    "date": "2016-10-20",
                    "description": "Forwarded - Mis-sort",
                    "location": "Stafford DO",
                    "time": "10:04 AM",
                }
            ],
            "tracking_number": "090367574000000FE1E1B",
        }
    ],
    [],
]

ParsedTrackingErrorResponse = [
    [],
    [
        {
            "carrier_id": "royalmail",
            "carrier_name": "royalmail",
            "code": "400",
            "details": {
                "errors": [
                    {
                        "errorCause": "The submitted request was not valid against the required header definition",
                        "errorCode": "E0004",
                        "errorDescription": "Failed header validation for X-Accept-RMG-Terms",
                        "errorResolution": "Please check the API request against the required header definition and re-submit",
                    }
                ]
            },
            "message": "Bad Request",
        }
    ],
]


TrackingRequestJSON = ["090367574000000FE1E1B"]

TrackingResponseJSON = """{
  "mailPieces": {
    "mailPieceId": "090367574000000FE1E1B",
    "carrierShortName": "RM",
    "carrierFullName": "Royal Mail Group Ltd",
    "summary": {
      "uniqueItemId": "090367574000000FE1E1B",
      "oneDBarcode": "FQ087430672GB",
      "productId": "SD2",
      "productName": "Special Delivery Guaranteed",
      "productDescription": "Our guaranteed next working day service with tracking and a signature on delivery",
      "productCategory": "NON-INTERNATIONAL",
      "destinationCountryCode": "GBR",
      "destinationCountryName": "United Kingdom of Great Britain and Northern Ireland",
      "originCountryCode": "GBR",
      "originCountryName": "United Kingdom of Great Britain and Northern Ireland",
      "lastEventCode": "EVNMI",
      "lastEventName": "Forwarded - Mis-sort",
      "lastEventDateTime": "2016-10-20T10:04:00+01:00",
      "lastEventLocationName": "Stafford DO",
      "statusDescription": "It's being redirected",
      "statusCategory": "IN TRANSIT",
      "statusHelpText": "The item is in transit and a confirmation will be provided on delivery. For more information on levels of tracking by service, please see Sending Mail.",
      "summaryLine": "Item FQ087430672GB was forwarded to the Delivery Office on 2016-10-20.",
      "internationalPostalProvider": {
        "url": "https://www.royalmail.com/track-your-item",
        "title": "Royal Mail Group Ltd",
        "description": "Royal Mail Group Ltd"
      }
    },
    "signature": {
      "recipientName": "Simon",
      "signatureDateTime": "2016-10-20T10:04:00+01:00",
      "imageId": "001234"
    },
    "estimatedDelivery": {
      "date": "2017-02-20",
      "startOfEstimatedWindow": "08:00:00+01:00",
      "endOfEstimatedWindow": "11:00:00+01:00"
    },
    "events": [
      {
        "eventCode": "EVNMI",
        "eventName": "Forwarded - Mis-sort",
        "eventDateTime": "2016-10-20T10:04:00+01:00",
        "locationName": "Stafford DO"
      }
    ],
    "links": {
      "summary": {
        "href": "/mailpieces/v2/summary?mailPieceId=090367574000000FE1E1B",
        "title": "Summary",
        "description": "Get summary"
      },
      "signature": {
        "href": "/mailpieces/v2/090367574000000FE1E1B/signature",
        "title": "Signature",
        "description": "Get signature"
      },
      "redelivery": {
        "href": "/personal/receiving-mail/redelivery",
        "title": "Redelivery",
        "description": "Book a redelivery"
      }
    }
  }
}
"""

TrackingErrorResponseJSON = """{
  "httpCode": "400",
  "httpMessage": "Bad Request",
  "errors": [
    {
      "errorCode": "E0004",
      "errorDescription": "Failed header validation for X-Accept-RMG-Terms",
      "errorCause": "The submitted request was not valid against the required header definition",
      "errorResolution": "Please check the API request against the required header definition and re-submit"
    }
  ]
}
"""
