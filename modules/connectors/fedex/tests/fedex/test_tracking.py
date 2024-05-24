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

    def test_parse_duplicate_tracking_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = DuplicateTrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedDuplicateTrackingResponse
            )


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

ParsedDuplicateTrackingResponse = [
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "delivered": True,
            "events": [
                {
                    "code": "DL",
                    "date": "2024-04-26",
                    "description": "Delivered",
                    "time": "09:26",
                },
                {
                    "code": "OD",
                    "date": "2024-04-26",
                    "description": "On FedEx vehicle for delivery",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "08:52",
                },
                {
                    "code": "AO",
                    "date": "2024-04-25",
                    "description": "Shipment arriving On-Time",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "14:29",
                },
                {
                    "code": "PU",
                    "date": "2024-04-25",
                    "description": "Picked up",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "14:25",
                },
                {
                    "code": "AF",
                    "date": "2024-04-25",
                    "description": "Tendered at FedEx Facility",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "13:26",
                },
                {
                    "code": "DE",
                    "date": "2024-04-25",
                    "description": "FedEx redirected your package to a nearby FedEx "
                    "location",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "11:28",
                },
                {
                    "code": "DE",
                    "date": "2024-04-25",
                    "description": "Customer not available or business closed",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "11:26",
                },
                {
                    "code": "OD",
                    "date": "2024-04-25",
                    "description": "On FedEx vehicle for delivery",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "08:55",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=776094337676",
                "package_weight": 1.0,
                "package_weight_unit": "LB",
                "shipment_origin_country": "US",
                "shipment_service": "FedEx Priority Overnight",
            },
            "status": "delivered",
            "tracking_number": "776094337676",
        }
    ],
    [],
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

DuplicateTrackingResponse = """{
  "transactionId": "9ca3d632-0af5-436e-b184-4a99f88598d4",
  "customerTransactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "output": {
    "completeTrackResults": [
      {
        "trackingNumber": "776094337676",
        "trackResults": [
          {
            "trackingNumberInfo": {
              "trackingNumber": "776094337676",
              "trackingNumberUniqueId": "2460425000~776094337676~FX",
              "carrierCode": "FDXE"
            },
            "additionalTrackingInfo": {
              "nickname": "",
              "hasAssociatedShipments": false
            },
            "shipperInformation": {
              "contact": {},
              "address": {
                "city": "Orange",
                "stateOrProvinceCode": "CA",
                "countryCode": "US",
                "residential": false,
                "countryName": "United States"
              }
            },
            "recipientInformation": {
              "contact": {},
              "address": {
                "city": "FRESNO",
                "stateOrProvinceCode": "CA",
                "countryCode": "US",
                "residential": false,
                "countryName": "United States"
              }
            },
            "latestStatusDetail": {
              "code": "FD",
              "derivedCode": "RL",
              "statusByLocale": "Running Late",
              "description": "At FedEx destination facility",
              "scanLocation": {
                "city": "CLOVIS",
                "stateOrProvinceCode": "CA",
                "countryCode": "US",
                "residential": false,
                "countryName": "United States"
              },
              "delayDetail": {
                "status": "DELAYED"
              }
            },
            "dateAndTimes": [
              {
                "type": "ACTUAL_PICKUP",
                "dateTime": "2024-04-24T16:05:00-07:00"
              },
              {
                "type": "SHIP",
                "dateTime": "2024-04-24T00:00:00-06:00"
              },
              {
                "type": "ACTUAL_TENDER",
                "dateTime": "2024-04-24T16:05:00-07:00"
              }
            ],
            "availableImages": [],
            "specialHandlings": [
              {
                "type": "HOLD_AT_LOCATION",
                "description": "Hold at Location",
                "paymentType": "OTHER"
              },
              {
                "type": "RESIDENTIAL_DELIVERY",
                "description": "Residential Delivery",
                "paymentType": "OTHER"
              },
              {
                "type": "ADULT_SIGNATURE_REQUIRED",
                "description": "Adult Signature Required",
                "paymentType": "OTHER"
              }
            ],
            "packageDetails": {
              "packagingDescription": {
                "type": "YOUR_PACKAGING",
                "description": "Your Packaging"
              },
              "sequenceNumber": "1",
              "count": "1",
              "weightAndDimensions": {
                "weight": [
                  {
                    "value": "1.0",
                    "unit": "LB"
                  },
                  {
                    "value": "0.45",
                    "unit": "KG"
                  }
                ],
                "dimensions": [
                  {
                    "length": 7,
                    "width": 6,
                    "height": 6,
                    "units": "IN"
                  },
                  {
                    "length": 17,
                    "width": 15,
                    "height": 15,
                    "units": "CM"
                  }
                ]
              },
              "packageContent": []
            },
            "shipmentDetails": {
              "possessionStatus": true,
              "weight": [
                {
                  "value": "1.0",
                  "unit": "LB"
                },
                {
                  "value": "0.45",
                  "unit": "KG"
                }
              ]
            },
            "scanEvents": [
              {
                "date": "2024-04-26T07:50:00-07:00",
                "eventType": "AR",
                "eventDescription": "At local FedEx facility",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93612",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "FATA",
                "locationType": "DESTINATION_FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-04-25T13:26:00-07:00",
                "eventType": "HP",
                "eventDescription": "Ready for recipient pickup",
                "exceptionCode": "",
                "exceptionDescription": "Package available for pickup at: 2420 N BLACKSTONE AVE ",
                "scanLocation": {
                  "streetLines": ["2420 N BLACKSTONE AVE "],
                  "city": "FRESNO",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93703",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "BWY81",
                "locationType": "DESTINATION_FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-04-25T11:29:00-07:00",
                "eventType": "DY",
                "eventDescription": "Delay",
                "exceptionCode": "A52",
                "exceptionDescription": "Package delayed",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93612",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "FATA",
                "locationType": "DESTINATION_FEDEX_FACILITY",
                "derivedStatusCode": "DY",
                "derivedStatus": "Delay",
                "delayDetail": {
                  "type": "GENERAL"
                }
              },
              {
                "date": "2024-04-25T08:12:00-07:00",
                "eventType": "AR",
                "eventDescription": "At local FedEx facility",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93612",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "FATA",
                "locationType": "DESTINATION_FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-04-25T02:15:00-07:00",
                "eventType": "DP",
                "eventDescription": "Departed FedEx hub",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "OAKLAND",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "94621",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "OAKH",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-04-24T22:39:00-07:00",
                "eventType": "AR",
                "eventDescription": "Arrived at FedEx hub",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "OAKLAND",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "94621",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "OAKH",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-04-24T18:56:00-07:00",
                "eventType": "DP",
                "eventDescription": "Left FedEx origin facility",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "COSTA MESA",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "92626",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "APVA",
                "locationType": "ORIGIN_FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-04-24T16:43:00-07:00",
                "eventType": "AO",
                "eventDescription": "Shipment arriving On-Time",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "COSTA MESA",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "92626",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "APVA",
                "locationType": "PICKUP_LOCATION",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-04-24T16:05:00-07:00",
                "eventType": "PU",
                "eventDescription": "Picked up",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "COSTA MESA",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "92626",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "APVA",
                "locationType": "PICKUP_LOCATION",
                "derivedStatusCode": "PU",
                "derivedStatus": "Picked up"
              },
              {
                "date": "2024-04-24T15:30:57-05:00",
                "eventType": "OC",
                "eventDescription": "Shipment information sent to FedEx",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "residential": false
                },
                "locationType": "CUSTOMER",
                "derivedStatusCode": "IN",
                "derivedStatus": "Label created"
              }
            ],
            "availableNotifications": [
              "ON_DELIVERY",
              "ON_EXCEPTION",
              "ON_ESTIMATED_DELIVERY"
            ],
            "deliveryDetails": {
              "deliveryAttempts": "0",
              "deliveryOptionEligibilityDetails": [
                {
                  "option": "INDIRECT_SIGNATURE_RELEASE",
                  "eligibility": "POSSIBLY_ELIGIBLE"
                },
                {
                  "option": "REDIRECT_TO_HOLD_AT_LOCATION",
                  "eligibility": "POSSIBLY_ELIGIBLE"
                },
                {
                  "option": "REROUTE",
                  "eligibility": "POSSIBLY_ELIGIBLE"
                },
                {
                  "option": "RESCHEDULE",
                  "eligibility": "POSSIBLY_ELIGIBLE"
                },
                {
                  "option": "RETURN_TO_SHIPPER",
                  "eligibility": "POSSIBLY_ELIGIBLE"
                },
                {
                  "option": "DISPUTE_DELIVERY",
                  "eligibility": "POSSIBLY_ELIGIBLE"
                },
                {
                  "option": "SUPPLEMENT_ADDRESS",
                  "eligibility": "POSSIBLY_ELIGIBLE"
                }
              ],
              "destinationServiceArea": "HELDPACKAGENOTAVAILABLEFORRECIPIENTPICKUP"
            },
            "originLocation": {
              "locationContactAndAddress": {
                "address": {
                  "city": "COSTA MESA",
                  "stateOrProvinceCode": "CA",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                }
              },
              "locationId": "APVA"
            },
            "destinationLocation": {
              "locationContactAndAddress": {
                "address": {
                  "city": "FRESNO",
                  "stateOrProvinceCode": "CA",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                }
              },
              "locationType": ""
            },
            "lastUpdatedDestinationAddress": {
              "city": "FRESNO",
              "stateOrProvinceCode": "CA",
              "countryCode": "US",
              "residential": false,
              "countryName": "United States"
            },
            "serviceCommitMessage": {
              "message": "Package is not yet available for pickup.",
              "type": "HELD_PACKAGE_NOT_AVAILABLE_FOR_RECIPIENT_PICKUP"
            },
            "serviceDetail": {
              "type": "PRIORITY_OVERNIGHT",
              "description": "FedEx Priority Overnight",
              "shortDescription": "P-1"
            },
            "standardTransitTimeWindow": {
              "window": {
                "ends": "2024-04-25T10:30:00-07:00"
              }
            },
            "estimatedDeliveryTimeWindow": {
              "window": {}
            },
            "goodsClassificationCode": "",
            "returnDetail": {}
          },
          {
            "trackingNumberInfo": {
              "trackingNumber": "776094337676",
              "trackingNumberUniqueId": "2460426000~776094337676~FX",
              "carrierCode": "FDXE"
            },
            "additionalTrackingInfo": {
              "nickname": "",
              "packageIdentifiers": [
                {
                  "type": "TRACKING_NUMBER_OR_DOORTAG",
                  "values": ["DT106798246430"],
                  "trackingNumberUniqueId": "",
                  "carrierCode": ""
                }
              ],
              "hasAssociatedShipments": false
            },
            "shipperInformation": {
              "address": {
                "residential": false
              }
            },
            "recipientInformation": {
              "address": {
                "residential": false
              }
            },
            "latestStatusDetail": {
              "code": "DL",
              "derivedCode": "DL",
              "statusByLocale": "Delivered",
              "description": "Delivered",
              "scanLocation": {
                "residential": false
              }
            },
            "dateAndTimes": [
              {
                "type": "ACTUAL_DELIVERY",
                "dateTime": "2024-04-26T09:26:00-07:00"
              },
              {
                "type": "ACTUAL_PICKUP",
                "dateTime": "2024-04-25T08:55:00-07:00"
              },
              {
                "type": "SHIP",
                "dateTime": "2024-04-25T00:00:00-06:00"
              },
              {
                "type": "ACTUAL_TENDER",
                "dateTime": "2024-04-25T08:55:00-07:00"
              }
            ],
            "availableImages": [
              {
                "type": "SIGNATURE_PROOF_OF_DELIVERY"
              }
            ],
            "specialHandlings": [
              {
                "type": "DELIVER_WEEKDAY",
                "description": "Deliver Weekday",
                "paymentType": "OTHER"
              },
              {
                "type": "RESIDENTIAL_DELIVERY",
                "description": "Residential Delivery",
                "paymentType": "OTHER"
              },
              {
                "type": "ADULT_SIGNATURE_REQUIRED",
                "description": "Adult Signature Required",
                "paymentType": "OTHER"
              }
            ],
            "packageDetails": {
              "packagingDescription": {
                "type": "YOUR_PACKAGING",
                "description": "Your Packaging"
              },
              "count": "1",
              "weightAndDimensions": {
                "weight": [
                  {
                    "value": "1.0",
                    "unit": "LB"
                  },
                  {
                    "value": "0.45",
                    "unit": "KG"
                  }
                ]
              },
              "packageContent": []
            },
            "shipmentDetails": {
              "possessionStatus": true,
              "weight": [
                {
                  "value": "1.0",
                  "unit": "LB"
                },
                {
                  "value": "0.45",
                  "unit": "KG"
                }
              ]
            },
            "scanEvents": [
              {
                "date": "2024-04-26T09:26:00-07:00",
                "eventType": "DL",
                "eventDescription": "Delivered",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "residential": false
                },
                "locationId": "FATA",
                "locationType": "DELIVERY_LOCATION",
                "derivedStatusCode": "DL",
                "derivedStatus": "Delivered"
              },
              {
                "date": "2024-04-26T08:52:00-07:00",
                "eventType": "OD",
                "eventDescription": "On FedEx vehicle for delivery",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93612",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "FATA",
                "locationType": "VEHICLE",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-04-25T14:29:00-07:00",
                "eventType": "AO",
                "eventDescription": "Shipment arriving On-Time",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93612",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "FATA",
                "locationType": "PICKUP_LOCATION",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-04-25T14:25:00-07:00",
                "eventType": "PU",
                "eventDescription": "Picked up",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93612",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "FATA",
                "locationType": "PICKUP_LOCATION",
                "derivedStatusCode": "PU",
                "derivedStatus": "Picked up"
              },
              {
                "date": "2024-04-25T13:26:00-07:00",
                "eventType": "AF",
                "eventDescription": "At local FedEx facility",
                "exceptionCode": "A3",
                "exceptionDescription": "Tendered at FedEx Facility",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93612",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "FATA",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-04-25T11:28:00-07:00",
                "eventType": "DE",
                "eventDescription": "Delivery exception",
                "exceptionCode": "A47",
                "exceptionDescription": "FedEx redirected your package to a nearby FedEx location",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93612",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "FATA",
                "locationType": "DESTINATION_FEDEX_FACILITY",
                "derivedStatusCode": "DE",
                "derivedStatus": "Delivery exception"
              },
              {
                "date": "2024-04-25T11:26:00-07:00",
                "eventType": "DE",
                "eventDescription": "Delivery exception",
                "exceptionCode": "08",
                "exceptionDescription": "Customer not available or business closed",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93612",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "FATA",
                "locationType": "DELIVERY_LOCATION",
                "derivedStatusCode": "DE",
                "derivedStatus": "Delivery exception"
              },
              {
                "date": "2024-04-25T08:55:00-07:00",
                "eventType": "OD",
                "eventDescription": "On FedEx vehicle for delivery",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [""],
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "postalCode": "93612",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "FATA",
                "locationType": "VEHICLE",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              }
            ],
            "availableNotifications": ["ON_DELIVERY"],
            "deliveryDetails": {
              "actualDeliveryAddress": {
                "residential": false
              },
              "locationType": "RESIDENCE",
              "locationDescription": "Residence",
              "deliveryAttempts": "0",
              "receivedByName": "D.HERRERA",
              "deliveryOptionEligibilityDetails": [
                {
                  "option": "INDIRECT_SIGNATURE_RELEASE",
                  "eligibility": "INELIGIBLE"
                },
                {
                  "option": "REDIRECT_TO_HOLD_AT_LOCATION",
                  "eligibility": "INELIGIBLE"
                },
                {
                  "option": "REROUTE",
                  "eligibility": "INELIGIBLE"
                },
                {
                  "option": "RESCHEDULE",
                  "eligibility": "INELIGIBLE"
                },
                {
                  "option": "RETURN_TO_SHIPPER",
                  "eligibility": "INELIGIBLE"
                },
                {
                  "option": "DISPUTE_DELIVERY",
                  "eligibility": "INELIGIBLE"
                },
                {
                  "option": "SUPPLEMENT_ADDRESS",
                  "eligibility": "INELIGIBLE"
                }
              ]
            },
            "originLocation": {
              "locationContactAndAddress": {
                "address": {
                  "city": "CLOVIS",
                  "stateOrProvinceCode": "CA",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                }
              },
              "locationId": "FATA"
            },
            "destinationLocation": {
              "locationContactAndAddress": {
                "address": {
                  "residential": false
                }
              },
              "locationType": ""
            },
            "lastUpdatedDestinationAddress": {
              "city": "FRESNO",
              "stateOrProvinceCode": "CA",
              "countryCode": "US",
              "residential": false,
              "countryName": "United States"
            },
            "serviceDetail": {
              "type": "PRIORITY_OVERNIGHT",
              "description": "FedEx Priority Overnight",
              "shortDescription": "P-1"
            },
            "standardTransitTimeWindow": {
              "window": {
                "ends": "2024-04-26T00:00:00-06:00"
              }
            },
            "estimatedDeliveryTimeWindow": {
              "window": {}
            },
            "customDeliveryOptions": [
              {
                "type": "EVENING",
                "status": "REQUESTED"
              }
            ],
            "goodsClassificationCode": "",
            "returnDetail": {}
          }
        ]
      }
    ]
  }
}
"""
