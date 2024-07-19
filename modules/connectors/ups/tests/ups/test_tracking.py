import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio.core.models import TrackingRequest
from .fixture import gateway
import karrio


class TestUPSTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TrackingRequestPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequestPayload)

    @patch("karrio.mappers.ups.proxy.lib.request", return_value="<a></a>")
    def test_get_tracking(self, http_mock):
        karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}/api/track/v1/details/{self.TrackingRequest.tracking_numbers[0]}?locale=en_US&returnSignature=true",
        )

    def test_tracking_auth_error_parsing(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = AuthError
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertEqual(DP.to_dict(parsed_response), ParsedAuthError)

    def test_tracking_response_parsing(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(DP.to_dict(parsed_response), ParsedTrackingResponse)

    def test_invalid_tracking_number_response_parsing(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = InvalidTrackingNumberResponseJSON
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                DP.to_dict(parsed_response),
                ParsedInvalidTrackingNumberResponse,
            )

    def test_tracking_number_not_found_response_parsing(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = TrackingNumberNotFoundResponseJSON
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                DP.to_dict(parsed_response),
                ParsedTrackingNumberNotFound,
            )


if __name__ == "__main__":
    unittest.main()


TrackingRequestPayload = ["1ZA82D672031716786"]

ParsedAuthError = [
    [],
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "code": "250003",
            "message": "Invalid Access License number",
        }
    ],
]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "delivered": False,
            "images": {
                "delivery_image": "encoding Base64",
                "signature_image": "encoding Base64",
            },
            "events": [
                {
                    "code": "SR",
                    "date": "2021-02-10",
                    "description": "Your package was released by the customs agency.",
                    "location": "Wayne, NJ, 07470, US",
                    "time": "07:13 AM",
                }
            ],
            "info": {
                "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=string/trackdetails",
                "package_weight": "string",
                "package_weight_unit": "string",
                "shipment_service": "UPS Ground",
                "signed_by": "163000",
            },
            "status": "on_hold",
            "tracking_number": "string",
        }
    ],
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "code": "string",
            "message": "string",
        }
    ],
]

ParsedTrackingNumberNotFound = [
    [],
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "code": "TW0001",
            "message": "Tracking Information Not Found",
        }
    ],
]

ParsedInvalidTrackingNumberResponse = [
    [],
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "code": "TV1002",
            "message": "Invalid inquiry number",
        }
    ],
]


AuthError = """{
  "response": {
    "errors": [
      {
        "code": "250003",
        "message": "Invalid Access License number"
      }
    ]
  }
}
"""

TrackingResponseJSON = """{
  "trackResponse": {
    "shipment": [
      {
        "inquiryNumber": "1Z023E2X0214323462",
        "package": [
          {
            "accessPointInformation": {
              "pickupByDate": "string"
            },
            "activity": [
              {
                "date": "20210210",
                "location": {
                  "address": {
                    "addressLine1": "100 Main St",
                    "addressLine2": "Warehouse",
                    "addressLine3": "Building 1",
                    "city": "Wayne",
                    "country": "US",
                    "countryCode": "US",
                    "postalCode": "07470",
                    "stateProvince": "NJ"
                  },
                  "slic": "8566"
                },
                "status": {
                  "code": "SR",
                  "description": "Your package was released by the customs agency.",
                  "simplifiedTextDescription": "Delivered",
                  "statusCode": "003",
                  "type": "X"
                },
                "time": "071356"
              }
            ],
            "additionalAttributes": [
              "SENSOR_EVENT"
            ],
            "additionalServices": [
              "ADULT_SIGNATURE_REQUIRED",
              "SIGNATURE_REQUIRED",
              "ADDITIONAL_HANDLING",
              "CARBON_NEUTRAL",
              "UPS_PREMIER_SILVER",
              "UPS_PREMIER_GOLD",
              "UPS_PREMIER_PLATINUM"
            ],
            "alternateTrackingNumber": [
              {
                "number": "92419900000033499522966220",
                "type": "USPS_PIC"
              }
            ],
            "currentStatus": {
              "code": "SR",
              "description": "Your package was released by the customs agency.",
              "simplifiedTextDescription": "Delivered",
              "statusCode": "003",
              "type": "X"
            },
            "deliveryDate": [
              {
                "date": "string",
                "type": "string"
              }
            ],
            "deliveryInformation": {
              "location": "DEL",
              "receivedBy": "163000",
              "signature": {
                "image": "encoding Base64"
              },
              "deliveryPhoto": {
                "isNonPostalCodeCountry": false,
                "photo": "encoding Base64",
                "photoCaptureInd": "string",
                "photoDispositionCode": "string"
              }
            },
            "deliveryTime": {
              "endTime": "string",
              "startTime": "string",
              "type": "string"
            },
            "milestones": [
              {
                "category": "string",
                "code": "string",
                "current": true,
                "description": "string",
                "linkedActivity": "string",
                "state": "string",
                "subMilestone": {
                  "category": "string"
                }
              }
            ],
            "packageAddress": [
              {
                "address": {
                  "addressLine1": "100 Main St",
                  "addressLine2": "Warehouse",
                  "addressLine3": "Building 1",
                  "city": "Wayne",
                  "country": "US",
                  "countryCode": "US",
                  "postalCode": "07470",
                  "stateProvince": "NJ"
                },
                "attentionName": "string",
                "name": "Sears",
                "type": "ORIGIN/DESTINATION"
              }
            ],
            "packageCount": 2,
            "paymentInformation": [
              {
                "amount": "243.5",
                "currency": "EUR",
                "id": "3S35571M1L381K5O0P316L0M1R2E6H14",
                "paid": false,
                "paymentMethod": "C0, C1, ... C9",
                "type": "ICOD/COD"
              }
            ],
            "referenceNumber": [
              {
                "number": "ShipRef123",
                "type": "SHIPMENT"
              }
            ],
            "service": {
              "code": "518",
              "description": "UPS Ground"
            },
            "statusCode": "string",
            "statusDescription": "string",
            "suppressionIndicators": "DETAIL",
            "trackingNumber": "string",
            "weight": {
              "unitOfMeasurement": "string",
              "weight": "string"
            }
          }
        ],
        "userRelation": "MYCHOICE_HOME",
        "warnings": [
          {
            "code": "string",
            "message": "string"
          }
        ]
      }
    ]
  }
}
"""

InvalidTrackingNumberResponseJSON = """{
  "response": {
    "errors": [
      {
        "code": "TV1002",
        "message": "Invalid inquiry number"
      }
    ]
  }
}
"""

TrackingNumberNotFoundResponseJSON = """{
    "trackResponse": {
        "shipment": [
            {
                "warnings": [
                    {"code": "TW0001", "message": "Tracking Information Not Found"}
                ]
            }
        ]
    }
}"""
