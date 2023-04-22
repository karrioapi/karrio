import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestBoxKnightTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.boxknight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/orders/{self.TrackingRequest.tracking_numbers[0]}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.boxknight.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.boxknight.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["93e11b39-0af8-40bb-742a-912375a09743"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "boxknight",
            "carrier_name": "boxknight",
            "delivered": False,
            "events": [
                {
                    "code": "GEOCODED",
                    "description": "GEOCODED",
                    "date": ANY,
                    "time": ANY,
                }
            ],
            "info": {
                "carrier_tracking_link": "https://www.tracking.boxknight.com/tracking?trackingNo=93e11b39-0af8-40bb-742a-912375a09743",
                "customer_name": "Charles Carmichael",
                "shipment_destination_country": "CA",
                "shipment_destination_postal_code": "H4R 2A4",
                "shipment_origin_country": "CA",
                "shipment_origin_postal_code": "H4R 2A4",
                "shipment_package_count": 3,
                "shipment_service": "SAMEDAY",
                "shipping_date": "2019-10-25",
            },
            "meta": {"reference": "shopifyid1234"},
            "tracking_number": "93e11b39-0af8-40bb-742a-912375a09743",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "boxknight",
            "carrier_name": "boxknight",
            "details": {"tracking_number": "93e11b39-0af8-40bb-742a-912375a09743"},
            "message": "Unauthorized",
        }
    ],
]


TrackingRequest = [{"order_id": "93e11b39-0af8-40bb-742a-912375a09743"}]

TrackingResponse = """{
  "id": "93e11b39-0af8-40bb-742a-912375a09743",
  "createdAt": "2019-10-25T22:56:06.000Z",
  "createdBy": "93e66b39-0uf8-40bb-742a-911235a09743",
  "merchantId": "13e11b39-0uf8-40bb-742a-913125a09743",
  "orderStatus": "GEOCODED",
  "scanningRequired": true,
  "validAddress": true,
  "labelUrl": "https://label12345.s3.amazonaws.com/BoxKnight-ShippingLabel-1234567.zpl",
  "pdfLabelUrl": "https://label12345.s3.amazonaws.com/BoxKnight-ShippingLabel-1234567.pdf",
  "recipient": {
    "name": "Charles Carmichael",
    "phone": "+15145573849",
    "notes": "Do not text, call instead.",
    "email": "charles.carmichael@boxknight.com"
  },
  "recipientAddress": {
    "number": 1234,
    "street": "Boul. Poirier",
    "city": "Montreal",
    "province": "Quebec",
    "country": "Canada",
    "postalCode": "H4R 2A4",
    "sublocality": "Communauté-Urbaine-de-Montréal",
    "location": {
      "lat": 45.4755722,
      "lng": -73.61911979999999
    }
  },
  "originAddress": {
    "number": 1234,
    "street": "Boul. Poirier",
    "city": "Montreal",
    "province": "Quebec",
    "country": "Canada",
    "postalCode": "H4R 2A4",
    "sublocality": "Communauté-Urbaine-de-Montréal",
    "location": {
      "lat": 45.4755722,
      "lng": -73.61911979999999
    }
  },
  "packageCount": 3,
  "signatureRequired": true,
  "service": "SAMEDAY",
  "notes": "The entrance is through the green fence on the left. If no answer, leave behind the black bin.",
  "refNumber": "shopifyid1234",
  "completeAfter": 1578439750000,
  "completeBefore": 1578439950000,
  "merchantDisplayName": "Metro Fleury No 2"
}
"""

ErrorResponse = """{
  "error": "Unauthorized"
}
"""
