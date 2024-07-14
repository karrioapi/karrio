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
                lib.to_query_unquote(mock.call_args[1]["url"]),
                lib.to_query_unquote(
                    f"{gateway.settings.server_url}/api/v2/track/events?includePublished=True&pageable=%7B%0A++++%22page%22%3A+0%2C%0A++++%22size%22%3A+25%2C%0A++++%22sort%22%3A+%5B%5D%0A%7D&trackingNumbers=1ZA82D672031801317&trackingNumbers=1Z6559X42067174856"
                ),
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
    "tracking_numbers": ["1ZA82D672031801317", "1Z6559X42067174856"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "delivered": True,
            "estimated_delivery": "2024-07-16",
            "events": [
                {
                    "code": "string",
                    "date": "2024-07-16",
                    "description": "string",
                    "location": "string",
                    "time": "10:20",
                }
            ],
            "tracking_number": "string",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "eshipper",
            "carrier_name": "eshipper",
            "code": "string",
            "details": {
                "fieldErrors": [
                    {"field": "string", "message": "string", "objectName": "string"}
                ],
                "thirdPartyMessage": "string",
                "type": "Success",
            },
            "message": "string",
        }
    ],
]


TrackingRequest = {
    "includePublished": True,
    "pageable": '{\n    "page": 0,\n    "size": 25,\n    "sort": []\n}',
    "trackingNumbers": ["1ZA82D672031801317", "1Z6559X42067174856"],
}

TrackingResponse = """[
  {
    "eventTime": "string",
    "shipDate": "string",
    "carrierName": "string",
    "carrierService": "string",
    "trackingUrl": "string",
    "trackingNumber": "string",
    "referenceCodes": [
      "string"
    ],
    "expectedDeliveryDate": "2024-07-16 10:20:44",
    "currentStatus": "string",
    "shipmentStatus": {
      "labelGenerated": true,
      "reachedAtWarehouse": true,
      "inTransit": true,
      "delivered": true,
      "exception": true
    },
    "orderId": "string",
    "eventId": "string",
    "event": [
      {
        "dateTime": "string",
        "description": "string",
        "location": "string",
        "proofOfDelivery": "string",
        "postalCode": "string",
        "additionalInformation": "string",
        "originalEvent": {
          "name": "string",
          "identifier": "string",
          "eventDate": "2024-07-16 10:20:44",
          "eventLocation": "string",
          "data": {
            "empty": true,
            "additionalProp1": {},
            "additionalProp2": {},
            "additionalProp3": {}
          }
        }
      }
    ]
  }
]
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
