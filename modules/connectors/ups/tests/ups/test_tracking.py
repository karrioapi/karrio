import unittest
import uuid
from unittest.mock import patch

import karrio.sdk as karrio
from karrio.core.models import TrackingRequest
from karrio.core.utils import DP

from .fixture import gateway


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
        headers = http_mock.call_args[1]["headers"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}/api/track/v1/details/{self.TrackingRequest.tracking_numbers[0]}?locale=en_US&returnSignature=true",
        )
        self.assertEqual(headers["transactionSrc"], "karrio-prod")
        self.assertTrue(headers["transId"])
        uuid.UUID(headers["transId"])

    def test_tracking_auth_error_parsing(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = AuthError
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertEqual(DP.to_dict(parsed_response), ParsedAuthError)

    def test_tracking_response_parsing(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertListEqual(DP.to_dict(parsed_response), ParsedTrackingResponse)

    def test_invalid_tracking_number_response_parsing(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = InvalidTrackingNumberResponseJSON
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertListEqual(
                DP.to_dict(parsed_response),
                ParsedInvalidTrackingNumberResponse,
            )

    def test_tracking_number_not_found_response_parsing(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = TrackingNumberNotFoundResponseJSON
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertListEqual(
                DP.to_dict(parsed_response),
                ParsedTrackingNumberNotFound,
            )

    def test_tracking_pickup_response_parsing(self):
        """Regression: PU activity with type='I' must resolve to 'picked_up', not 'in_transit'.

        Fails on unpatched (type-first) code where find('I').name -> 'in_transit'.
        Passes after the code-first fix where find('PU').name -> 'picked_up'.
        Grounded in the UPS coarse status.type taxonomy documented in units.py (~L740):
        I=in-progress is the bucket for all active scans including pickup (PU), so
        type-first resolution wrongly yields in_transit — this test guards the code-first fix.
        """
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = PickupTrackingResponseJSON
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertListEqual(DP.to_dict(parsed_response), ParsedPickupTrackingResponse)

    def test_tracking_label_created_response_parsing(self):
        """Regression for #786: a label-created (MP) activity with type='I' must resolve to
        'pending', not 'in_transit' — the exact pre-pickup scenario reported in the bug.

        Fails on unpatched (type-first) code where find('I').name -> 'in_transit'.
        Passes after the code-first fix where find('MP').name -> 'pending'.
        MP ("Shipper created a label, UPS has not received the package yet") is the manifest
        code in units.py's pending bucket (~L743); UPS carries it under the coarse type='I'
        in-progress bucket, so only code-first resolution keeps it out of in_transit.
        """
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = LabelCreatedTrackingResponseJSON
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertListEqual(DP.to_dict(parsed_response), ParsedLabelCreatedTrackingResponse)


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
            "level": "error",
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
                    "status": "on_hold",
                    "time": "07:13 AM",
                    "timestamp": "2021-02-10T07:13:00.000Z",
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
            "level": "warning",
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
            "level": "warning",
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
            "level": "error",
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

# Pickup event fixture: code="PU", type="I" (in-progress coarse bucket).
# Under type-first code this resolves to in_transit; under the code-first fix it resolves to
# picked_up. Grounded in the UPS coarse status.type taxonomy in units.py (~L740):
# I=in-progress covers all active scans including pickup; PU is the specific pickup code.
PickupTrackingResponseJSON = """{
  "trackResponse": {
    "shipment": [
      {
        "inquiryNumber": "1Z999AA10123456784",
        "package": [
          {
            "activity": [
              {
                "date": "20240315",
                "location": {
                  "address": {
                    "city": "Frankfurt",
                    "country": "DE",
                    "countryCode": "DE",
                    "postalCode": "60314",
                    "stateProvince": ""
                  }
                },
                "status": {
                  "code": "PU",
                  "description": "Package picked up.",
                  "type": "I"
                },
                "time": "092500"
              }
            ],
            "deliveryDate": [],
            "packageAddress": [],
            "service": {
              "code": "065",
              "description": "UPS Express Saver"
            },
            "trackingNumber": "1Z999AA10123456784",
            "weight": {
              "unitOfMeasurement": "KGS",
              "weight": "2.5"
            }
          }
        ],
        "warnings": []
      }
    ]
  }
}"""

ParsedPickupTrackingResponse = [
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "delivered": False,
            "events": [
                {
                    "code": "PU",
                    "date": "2024-03-15",
                    "description": "Package picked up.",
                    "location": "Frankfurt, 60314, DE",
                    "status": "picked_up",
                    "time": "09:25 AM",
                    "timestamp": "2024-03-15T09:25:00.000Z",
                }
            ],
            "images": {},
            "info": {
                "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1Z999AA10123456784/trackdetails",
                "package_weight": "2.5",
                "package_weight_unit": "KGS",
                "shipment_service": "UPS Express Saver",
            },
            "status": "picked_up",
            "tracking_number": "1Z999AA10123456784",
        }
    ],
    [],
]

# Label-created (pre-pickup) fixture: code="MP", type="I" (in-progress coarse bucket).
# Under type-first code this resolves to in_transit; under the code-first fix it resolves to
# pending. This is the exact #786 scenario — a shipment showing in_transit before pickup.
# MP is in units.py's pending bucket (~L743): "Shipper created a label, UPS has not received
# the package yet"; UPS carries the coarse type="I" alongside it.
LabelCreatedTrackingResponseJSON = """{
  "trackResponse": {
    "shipment": [
      {
        "inquiryNumber": "1Z999AA10123456784",
        "package": [
          {
            "activity": [
              {
                "date": "20240315",
                "location": {
                  "address": {
                    "city": "Frankfurt",
                    "country": "DE",
                    "countryCode": "DE",
                    "postalCode": "60314",
                    "stateProvince": ""
                  }
                },
                "status": {
                  "code": "MP",
                  "description": "Shipper created a label, UPS has not received the package yet.",
                  "type": "I"
                },
                "time": "074600"
              }
            ],
            "deliveryDate": [],
            "packageAddress": [],
            "service": {
              "code": "065",
              "description": "UPS Express Saver"
            },
            "trackingNumber": "1Z999AA10123456784",
            "weight": {
              "unitOfMeasurement": "KGS",
              "weight": "2.5"
            }
          }
        ],
        "warnings": []
      }
    ]
  }
}"""

ParsedLabelCreatedTrackingResponse = [
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "delivered": False,
            "events": [
                {
                    "code": "MP",
                    "date": "2024-03-15",
                    "description": "Shipper created a label, UPS has not received the package yet.",
                    "location": "Frankfurt, 60314, DE",
                    "status": "pending",
                    "time": "07:46 AM",
                    "timestamp": "2024-03-15T07:46:00.000Z",
                }
            ],
            "images": {},
            "info": {
                "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1Z999AA10123456784/trackdetails",
                "package_weight": "2.5",
                "package_weight_unit": "KGS",
                "shipment_service": "UPS Express Saver",
            },
            "status": "pending",
            "tracking_number": "1Z999AA10123456784",
        }
    ],
    [],
]
