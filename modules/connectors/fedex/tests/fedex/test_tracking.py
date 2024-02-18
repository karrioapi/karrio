import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestFedExTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/track/v1/trackingnumbers",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {"tracking_numbers": ["399368623212", "39936862321"]}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "delivered": False,
            "estimated_delivery": "2021-10-01",
            "events": [
                {
                    "code": "PU",
                    "date": "2018-02-02",
                    "description": "Package available for clearance",
                    "location": "SEATTLE, WA, 98101, US",
                    "time": "12:01",
                }
            ],
            "info": {
                "carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=123456789012",
                "package_weight": 22222.0,
                "package_weight_unit": "LB",
                "shipment_destination_country": "US",
                "shipment_origin_country": "US",
                "shipment_service": "FedEx Freight Economy.",
            },
            "status": "in_transit",
            "tracking_number": "123456789012",
        }
    ],
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "code": "TRACKING.TRACKINGNUMBER.EMPTY",
            "details": {"tracking_number": "128667043726"},
            "message": "Please provide tracking number.",
        },
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "code": "TRACKING.TRACKINGNUMBER.NOTFOUND",
            "details": {"tracking_number": "39936862321"},
            "message": "Tracking number cannot be found. Please correct the tracking "
            "number and try again.",
        },
    ],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "code": "TRACKING.TRACKINGNUMBER.EMPTY",
            "details": {},
            "message": "Please provide tracking number.",
        }
    ],
]


TrackingRequest = {
    "trackingInfo": [
        {"trackingNumberInfo": {"trackingNumber": "399368623212"}},
        {"trackingNumberInfo": {"trackingNumber": "39936862321"}},
    ],
    "includeDetailedScans": True,
}


TrackingResponse = """{
  "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "customerTransactionId": "AnyCo_order123456789",
  "output": {
    "completeTrackResults": [
      {
        "trackingNumber": "123456789012",
        "trackResults": [
          {
            "trackingNumberInfo": {
              "trackingNumber": "128667043726",
              "carrierCode": "FDXE",
              "trackingNumberUniqueId": "245822~123456789012~FDEG"
            },
            "additionalTrackingInfo": {
              "hasAssociatedShipments": false,
              "nickname": "shipment nickname",
              "packageIdentifiers": [
                {
                  "type": "SHIPPER_REFERENCE",
                  "value": "ASJFGVAS",
                  "trackingNumberUniqueId": "245822~123456789012~FDEG"
                }
              ],
              "shipmentNotes": "shipment notes"
            },
            "distanceToDestination": {
              "units": "KM",
              "value": 685.7
            },
            "consolidationDetail": [
              {
                "timeStamp": "2020-10-13T03:54:44-06:00",
                "consolidationID": "47936927",
                "reasonDetail": {
                  "description": "Wrong color",
                  "type": "REJECTED"
                },
                "packageCount": 25,
                "eventType": "PACKAGE_ADDED_TO_CONSOLIDATION"
              }
            ],
            "meterNumber": "8468376",
            "returnDetail": {
              "authorizationName": "Sammy Smith",
              "reasonDetail": [
                {
                  "description": "Wrong color",
                  "type": "REJECTED"
                }
              ]
            },
            "serviceDetail": {
              "description": "FedEx Freight Economy.",
              "shortDescription": "FL",
              "type": "FEDEX_FREIGHT_ECONOMY"
            },
            "destinationLocation": {
              "locationId": "SEA",
              "locationContactAndAddress": {
                "contact": {
                  "personName": "John Taylor",
                  "phoneNumber": "1234567890",
                  "companyName": "Fedex"
                },
                "address": {
                  "addressClassification": "BUSINESS",
                  "residential": false,
                  "streetLines": [
                    "1043 North Easy Street",
                    "Suite 999"
                  ],
                  "city": "SEATTLE",
                  "urbanizationCode": "RAFAEL",
                  "stateOrProvinceCode": "WA",
                  "postalCode": "98101",
                  "countryCode": "US",
                  "countryName": "United States"
                }
              },
              "locationType": "PICKUP_LOCATION"
            },
            "latestStatusDetail": {
              "scanLocation": {
                "addressClassification": "BUSINESS",
                "residential": false,
                "streetLines": [
                  "1043 North Easy Street",
                  "Suite 999"
                ],
                "city": "SEATTLE",
                "urbanizationCode": "RAFAEL",
                "stateOrProvinceCode": "WA",
                "postalCode": "98101",
                "countryCode": "US",
                "countryName": "United States"
              },
              "code": "PU",
              "derivedCode": "PU",
              "ancillaryDetails": [
                {
                  "reason": "15",
                  "reasonDescription": "Customer not available or business closed",
                  "action": "Contact us at <http://www.fedex.com/us/customersupport/call/index.html> to discuss possible delivery or pickup alternatives.",
                  "actionDescription": "Customer not Available or Business Closed"
                }
              ],
              "statusByLocale": "Picked up",
              "description": "Picked up",
              "delayDetail": {
                "type": "WEATHER",
                "subType": "SNOW",
                "status": "DELAYED"
              }
            },
            "serviceCommitMessage": {
              "message": "No scheduled delivery date available at this time.",
              "type": "ESTIMATED_DELIVERY_DATE_UNAVAILABLE"
            },
            "informationNotes": [
              {
                "code": "CLEARANCE_ENTRY_FEE_APPLIES",
                "description": "this is an informational message"
              }
            ],
            "error": {
              "code": "TRACKING.TRACKINGNUMBER.EMPTY",
              "parameterList": [
                {
                  "value": "value",
                  "key": "key"
                }
              ],
              "message": "Please provide tracking number."
            },
            "specialHandlings": [
              {
                "description": "Deliver Weekday",
                "type": "DELIVER_WEEKDAY",
                "paymentType": "OTHER"
              }
            ],
            "availableImages": [
              {
                "size": "LARGE",
                "type": "BILL_OF_LADING"
              }
            ],
            "deliveryDetails": {
              "receivedByName": "Reciever",
              "destinationServiceArea": "EDDUNAVAILABLE",
              "destinationServiceAreaDescription": "Appointment required",
              "locationDescription": "Receptionist/Front Desk",
              "actualDeliveryAddress": {
                "addressClassification": "BUSINESS",
                "residential": false,
                "streetLines": [
                  "1043 North Easy Street",
                  "Suite 999"
                ],
                "city": "SEATTLE",
                "urbanizationCode": "RAFAEL",
                "stateOrProvinceCode": "WA",
                "postalCode": "98101",
                "countryCode": "US",
                "countryName": "United States"
              },
              "deliveryToday": false,
              "locationType": "FEDEX_EXPRESS_STATION",
              "signedByName": "Reciever",
              "officeOrderDeliveryMethod": "Courier",
              "deliveryAttempts": "0",
              "deliveryOptionEligibilityDetails": [
                {
                  "option": "INDIRECT_SIGNATURE_RELEASE",
                  "eligibility": "INELIGIBLE"
                }
              ]
            },
            "scanEvents": [
              {
                "date": "2018-02-02T12:01:00-07:00",
                "derivedStatus": "Picked Up",
                "scanLocation": {
                  "addressClassification": "BUSINESS",
                  "residential": false,
                  "streetLines": [
                    "1043 North Easy Street",
                    "Suite 999"
                  ],
                  "city": "SEATTLE",
                  "urbanizationCode": "RAFAEL",
                  "stateOrProvinceCode": "WA",
                  "postalCode": "98101",
                  "countryCode": "US",
                  "countryName": "United States"
                },
                "locationId": "SEA",
                "locationType": "PICKUP_LOCATION",
                "exceptionDescription": "Package available for clearance",
                "eventDescription": "Picked Up",
                "eventType": "PU",
                "derivedStatusCode": "PU",
                "exceptionCode": "A25",
                "delayDetail": {
                  "type": "WEATHER",
                  "subType": "SNOW",
                  "status": "DELAYED"
                }
              }
            ],
            "dateAndTimes": [
              {
                "dateTime": "2007-09-27T00:00:00",
                "type": "ACTUAL_DELIVERY"
              }
            ],
            "packageDetails": {
              "physicalPackagingType": "BARREL",
              "sequenceNumber": "45",
              "undeliveredCount": "7",
              "packagingDescription": {
                "description": "FedEx Pak",
                "type": "FEDEX_PAK"
              },
              "count": "1",
              "weightAndDimensions": {
                "weight": [
                  {
                    "unit": "LB",
                    "value": "22222.0"
                  }
                ],
                "dimensions": [
                  {
                    "length": 100,
                    "width": 50,
                    "height": 30,
                    "units": "CM"
                  }
                ]
              },
              "packageContent": [
                "wire hangers",
                "buttons"
              ],
              "contentPieceCount": "100",
              "declaredValue": {
                "currency": "USD",
                "value": 56.8
              }
            },
            "goodsClassificationCode": "goodsClassificationCode",
            "holdAtLocation": {
              "locationId": "SEA",
              "locationContactAndAddress": {
                "contact": {
                  "personName": "John Taylor",
                  "phoneNumber": "1234567890",
                  "companyName": "Fedex"
                },
                "address": {
                  "addressClassification": "BUSINESS",
                  "residential": false,
                  "streetLines": [
                    "1043 North Easy Street",
                    "Suite 999"
                  ],
                  "city": "SEATTLE",
                  "urbanizationCode": "RAFAEL",
                  "stateOrProvinceCode": "WA",
                  "postalCode": "98101",
                  "countryCode": "US",
                  "countryName": "United States"
                }
              },
              "locationType": "PICKUP_LOCATION"
            },
            "customDeliveryOptions": [
              {
                "requestedAppointmentDetail": {
                  "date": "2019-05-07",
                  "window": [
                    {
                      "description": "Description field",
                      "window": {
                        "begins": "2021-10-01T08:00:00",
                        "ends": "2021-10-15T00:00:00-06:00"
                      },
                      "type": "ESTIMATED_DELIVERY"
                    }
                  ]
                },
                "description": "Redirect the package to the hold location.",
                "type": "REDIRECT_TO_HOLD_AT_LOCATION",
                "status": "HELD"
              }
            ],
            "estimatedDeliveryTimeWindow": {
              "description": "Description field",
              "window": {
                "begins": "2021-10-01T08:00:00",
                "ends": "2021-10-15T00:00:00-06:00"
              },
              "type": "ESTIMATED_DELIVERY"
            },
            "pieceCounts": [
              {
                "count": "35",
                "description": "picec count description",
                "type": "ORIGIN"
              }
            ],
            "originLocation": {
              "locationId": "SEA",
              "locationContactAndAddress": {
                "contact": {
                  "personName": "John Taylor",
                  "phoneNumber": "1234567890",
                  "companyName": "Fedex"
                },
                "address": {
                  "addressClassification": "BUSINESS",
                  "residential": false,
                  "streetLines": [
                    "1043 North Easy Street",
                    "Suite 999"
                  ],
                  "city": "SEATTLE",
                  "urbanizationCode": "RAFAEL",
                  "stateOrProvinceCode": "WA",
                  "postalCode": "98101",
                  "countryCode": "US",
                  "countryName": "United States"
                }
              },
              "locationType": "PICKUP_LOCATION"
            },
            "recipientInformation": {
              "contact": {
                "personName": "John Taylor",
                "phoneNumber": "1234567890",
                "companyName": "Fedex"
              },
              "address": {
                "addressClassification": "BUSINESS",
                "residential": false,
                "streetLines": [
                  "1043 North Easy Street",
                  "Suite 999"
                ],
                "city": "SEATTLE",
                "urbanizationCode": "RAFAEL",
                "stateOrProvinceCode": "WA",
                "postalCode": "98101",
                "countryCode": "US",
                "countryName": "United States"
              }
            },
            "standardTransitTimeWindow": {
              "description": "Description field",
              "window": {
                "begins": "2021-10-01T08:00:00",
                "ends": "2021-10-15T00:00:00-06:00"
              },
              "type": "ESTIMATED_DELIVERY"
            },
            "shipmentDetails": {
              "contents": [
                {
                  "itemNumber": "RZ5678",
                  "receivedQuantity": "13",
                  "description": "pulyurethane rope",
                  "partNumber": "RK1345"
                }
              ],
              "beforePossessionStatus": false,
              "weight": [
                {
                  "unit": "LB",
                  "value": "22222.0"
                }
              ],
              "contentPieceCount": "3333",
              "splitShipments": [
                {
                  "pieceCount": "10",
                  "statusDescription": "status",
                  "timestamp": "2019-05-07T08:00:07",
                  "statusCode": "statuscode"
                }
              ]
            },
            "reasonDetail": {
              "description": "Wrong color",
              "type": "REJECTED"
            },
            "availableNotifications": [
              "ON_DELIVERY",
              "ON_EXCEPTION"
            ],
            "shipperInformation": {
              "contact": {
                "personName": "John Taylor",
                "phoneNumber": "1234567890",
                "companyName": "Fedex"
              },
              "address": {
                "addressClassification": "BUSINESS",
                "residential": false,
                "streetLines": [
                  "1043 North Easy Street",
                  "Suite 999"
                ],
                "city": "SEATTLE",
                "urbanizationCode": "RAFAEL",
                "stateOrProvinceCode": "WA",
                "postalCode": "98101",
                "countryCode": "US",
                "countryName": "United States"
              }
            },
            "lastUpdatedDestinationAddress": {
              "addressClassification": "BUSINESS",
              "residential": false,
              "streetLines": [
                "1043 North Easy Street",
                "Suite 999"
              ],
              "city": "SEATTLE",
              "urbanizationCode": "RAFAEL",
              "stateOrProvinceCode": "WA",
              "postalCode": "98101",
              "countryCode": "US",
              "countryName": "United States"
            }
          }
        ]
      },
      {
        "trackingNumber": "39936862321",
        "trackResults": [
          {
            "trackingNumberInfo": {
              "trackingNumber": "39936862321",
              "trackingNumberUniqueId": "",
              "carrierCode": ""
            },
            "error": {
              "code": "TRACKING.TRACKINGNUMBER.NOTFOUND",
              "message": "Tracking number cannot be found. Please correct the tracking number and try again."
            }
          }
        ]
      }
    ],
    "alerts": "TRACKING.DATA.NOTFOUND -  Tracking data unavailable"
  }
}
"""

ErrorResponse = """{
  "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "customerTransactionId": "AnyCo_order123456789",
  "errors": [
    {
      "code": "TRACKING.TRACKINGNUMBER.EMPTY",
      "message": "Please provide tracking number."
    }
  ]
}
"""
