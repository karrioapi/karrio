import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLExpressTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["1234567890"],
}

ParsedTrackingResponse = []

ParsedErrorResponse = []


TrackingRequest = {}

TrackingResponse = """{
  "shipments": [
    {
      "shipmentTrackingNumber": "1234567890",
      "status": "Success",
      "shipmentTimestamp": "2020-05-14T18:00:31",
      "productCode": "N",
      "description": "Shipment Description",
      "shipperDetails": {
        "name": "",
        "postalAddress": {
          "cityName": "",
          "countyName": "",
          "postalCode": "",
          "provinceCode": "",
          "countryCode": "CZ"
        },
        "serviceArea": [
          {
            "code": "ABC",
            "description": "Alpha Beta Area",
            "outboundSortCode": "string"
          }
        ]
      },
      "receiverDetails": {
        "name": "",
        "postalAddress": {
          "cityName": "",
          "countyName": "",
          "postalCode": "",
          "provinceCode": "",
          "countryCode": "SK"
        },
        "serviceArea": [
          {
            "code": "BSA",
            "description": "BSA Area",
            "facilityCode": "facil area",
            "inboundSortCode": "string"
          }
        ]
      },
      "totalWeight": 10,
      "unitOfMeasurements": "metric",
      "shipperReferences": [
        {
          "value": "Customer reference",
          "typeCode": "CU"
        }
      ],
      "events": [
        {
          "date": "2020-06-10",
          "time": "13:06:00",
          "GMTOffset": "+09:00",
          "typeCode": "PU",
          "description": "Shipment picked up",
          "serviceArea": [
            {
              "code": "BNE",
              "description": "Brisbane-AU"
            }
          ],
          "signedBy": ""
        }
      ],
      "numberOfPieces": 1,
      "pieces": [
        {
          "number": 1,
          "typeCode": "string",
          "shipmentTrackingNumber": "string",
          "trackingNumber": "string",
          "description": "string",
          "weight": 22.5,
          "dimensionalWeight": 22.5,
          "actualWeight": 22.5,
          "dimensions": {
            "length": 15,
            "width": 15,
            "height": 40
          },
          "actualDimensions": {
            "length": 15,
            "width": 15,
            "height": 40
          },
          "unitOfMeasurements": "string",
          "shipperReferences": [
            {
              "value": "Customer reference",
              "typeCode": "CU"
            }
          ],
          "events": [
            {
              "date": "string",
              "GMTOffset": "+09:00",
              "time": "string",
              "typeCode": "string",
              "description": "string",
              "serviceArea": [
                {
                  "code": "string",
                  "description": "string"
                }
              ],
              "signedBy": ""
            }
          ]
        }
      ],
      "estimatedDeliveryDate": "2020-06-12",
      "childrenShipmentIdentificationNumbers": [
        "1234567890"
      ],
      "controlledAccessDataCodes": [
        "SHPR_CTY"
      ]
    }
  ]
}
"""

ErrorResponse = """{
  "instance": "/expressapi/tracking?shipmentReference=ShipReferenceRCS03&trackingView=shipment-details-only&levelOfDetail=shipment",
  "detail": "Missing mandatory parameters: shipperAccountNumber",
  "title": "Missing parameters",
  "message": "Bad request",
  "status": "400"
}
"""
