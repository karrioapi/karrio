import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUSPSTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
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

ParsedTrackingResponse = ["89108749065090"]

ParsedErrorResponse = []


TrackingRequest = {}

TrackingResponse = """{
  "trackingNumber": "string",
  "additionalInfo": "string",
  "ADPScripting": "string",
  "archiveRestoreInfo": "string",
  "associatedLabel": "string",
  "carrierRelease": true,
  "mailClass": "BOUND_PRINTED_MATTER",
  "destinationCity": "string",
  "destinationCountryCode": "string",
  "destinationState": "st",
  "destinationZIP": "string",
  "editedLabelId": "string",
  "emailEnabled": true,
  "endOfDay": "string",
  "eSOFEligible": true,
  "expectedDeliveryTimeStamp": "2019-08-24T14:15:22Z",
  "expectedDeliveryType": "string",
  "guaranteedDeliveryTimeStamp": "2019-08-24T14:15:22Z",
  "guaranteedDetails": "string",
  "itemShape": "LETTER",
  "kahalaIndicator": true,
  "mailType": "INTERNATIONAL_INBOUND",
  "approximateIntakeDate": "string",
  "uniqueTrackingId": "string",
  "onTime": true,
  "originCity": "string",
  "originCountry": "st",
  "originState": "str",
  "originZIP": "strin",
  "proofOfDeliveryEnabled": true,
  "predictedDeliveryTimeStamp": "2019-08-24T14:15:22Z",
  "predictedDeliveryDate": "2019-08-24",
  "predictedDeliveryWindowStartTime": "string",
  "predictedDeliveryWindowEndTime": "string",
  "relatedReturnReceiptID": "string",
  "redeliveryEnabled": true,
  "enabledNotificationRequests": {
    "SMS": {
      "futureDelivery": true,
      "alertDelivery": true,
      "todayDelivery": true,
      "UP": true,
      "DND": true
    },
    "EMail": {
      "futureDelivery": true,
      "alertDelivery": true,
      "todayDelivery": true,
      "UP": true,
      "DND": true,
      "firstDisplayable": true,
      "otherActivity": true
    }
  },
  "restoreEnabled": true,
  "returnDateNotice": "2019-08-24",
  "RRAMenabled": true,
  "RREEnabled": true,
  "services": ["string"],
  "serviceTypeCode": "string",
  "status": "string",
  "statusCategory": "string",
  "statusSummary": "Your item was delivered at 12:55 pm on April 05, 2010 in FALMOUTH, MA 02540",
  "trackingProofOfDeliveryEnabled": true,
  "valueofArticle": "string",
  "extendRetentionPurchasedCode": "string",
  "extendRetentionExtraServiceCodeOptions": [{}],
  "trackingEvents": [
    {
      "eventType": "string",
      "eventTimestamp": "2019-08-24T14:15:22Z",
      "GMTTimestamp": "2024-04-04T14:03:12.041Z",
      "GMTOffset": "-7:00",
      "eventCountry": "string",
      "eventCity": "string",
      "eventState": "string",
      "eventZIP": "string",
      "firm": "string",
      "name": "string",
      "authorizedAgent": true,
      "eventCode": "string",
      "actionCode": "string",
      "reasonCode": "string"
    }
  ]
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
