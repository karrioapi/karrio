import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TesteShipperTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.eshipper.proxy.lib.request") as mock:
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

ParsedTrackingResponse = []

ParsedErrorResponse = []


TrackingRequest = [{"trackingNumber": "S34WER4S"}]

TrackingResponse = """{
  "trackingUrl": "string",
  "brandedTrackingUrl": "string",
  "lmcCarrierTrackingUrl": "string",
  "carbonNeutral": true,
  "remarks": "string",
  "trackingDetails": [
    {
      "carrier": "string",
      "carrierEventCode": "string",
      "dateTime": "2024-05-13T03:18:15.315Z",
      "location": "string",
      "postalCode": "string",
      "proofOfDelivery": "string",
      "signatoryName": "string",
      "description": "string",
      "additionalInfo": "string",
      "awbNumber": "string",
      "vehicleId": "string",
      "vehicleType": "Flight",
      "eshipperOrderStatus": "string"
    }
  ],
  "status": {
    "labelGenerated": true,
    "reachedAtWarehouse": true,
    "inTransit": true,
    "delivered": true,
    "exception": true
  },
  "orderDetails": {
    "carrier": {
      "carrierName": "string",
      "serviceName": "string",
      "carrierLogoPath": "string"
    },
    "from": {
      "attention": "string",
      "company": "string",
      "address1": "string",
      "address2": "string",
      "city": "string",
      "province": "string",
      "country": "string",
      "zip": "string",
      "email": "string",
      "phone": "\\\\ddd\\-\\ddd\\dddd",
      "instructions": "string",
      "residential": true,
      "tailgateRequired": true,
      "confirmDelivery": true,
      "notifyRecipient": true
    },
    "to": {
      "attention": "string",
      "company": "string",
      "address1": "string",
      "address2": "string",
      "city": "string",
      "province": "string",
      "country": "string",
      "zip": "string",
      "email": "string",
      "phone": "\\\\\\dd \\ddd \\ddd\\dddd",
      "instructions": "string",
      "residential": true,
      "tailgateRequired": true,
      "confirmDelivery": true,
      "notifyRecipient": true
    },
    "packages": {
      "type": "string",
      "quantity": 0,
      "weightUnit": "string",
      "packages": [
        {
          "height": 0,
          "length": 0,
          "width": 0,
          "dimensionUnit": "string",
          "weight": 0,
          "weightUnit": "string",
          "type": "string",
          "freightClass": "string",
          "nmfcCode": "string",
          "insuranceAmount": 0,
          "codAmount": 0,
          "description": "string",
          "harmonizedCode": "string",
          "skuCode": "string"
        }
      ],
      "totalWeight": 0
    }
  }
}
"""

ErrorResponse = """{
  "type": "Success",
  "message": "string",
  "code": "string",
  "fieldErrors": [
    {
      "objectName": "string",
      "field": "string",
      "message": "string"
    }
  ],
  "thirdPartyMessage": "string"
}
"""
