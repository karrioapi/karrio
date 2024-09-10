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
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock1:
            mock1.return_value = TrackingResponse
            response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            with patch("karrio.providers.fedex.utils.lib.request") as mock2:
                mock2.return_value = ProofOfDeliveryResponse
                parsed_response = response.parse()

                self.assertListEqual(
                    lib.to_dict(parsed_response), ParsedTrackingResponse
                )

    def test_parse_error_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)

    def test_parse_duplicate_tracking_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock1:
            mock1.return_value = DuplicateTrackingResponse
            response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            with patch("karrio.providers.fedex.utils.lib.request") as mock2:
                mock2.return_value = ProofOfDeliveryResponse
                parsed_response = response.parse()

                self.assertListEqual(
                    lib.to_dict(parsed_response), ParsedDuplicateTrackingResponse
                )

    def test_parse_inconsistent_datetime_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock1:
            mock1.return_value = InconsistentDateTimeResponse
            response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            with patch("karrio.providers.fedex.utils.lib.request") as mock2:
                mock2.return_value = ProofOfDeliveryResponse
                parsed_response = response.parse()

                self.assertListEqual(
                    lib.to_dict(parsed_response), ParsedInconsistentDateTimeResponse
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
                    "time": "12:01 PM",
                }
            ],
            "info": {
                "carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=123456789012",
                "package_weight": 22222.0,
                "package_weight_unit": "LB",
                "shipment_destination_postal_code": "98101",
                "shipment_destination_country": "US",
                "shipment_origin_postal_code": "98101",
                "shipment_origin_country": "US",
                "shipment_service": "FedEx Freight Economy.",
                "signed_by": "Reciever",
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
                    "time": "09:26 AM",
                },
                {
                    "code": "OD",
                    "date": "2024-04-26",
                    "description": "On FedEx vehicle for delivery",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "08:52 AM",
                },
                {
                    "code": "AO",
                    "date": "2024-04-25",
                    "description": "Shipment arriving On-Time",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "14:29 PM",
                },
                {
                    "code": "PU",
                    "date": "2024-04-25",
                    "description": "Picked up",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "14:25 PM",
                },
                {
                    "code": "AF",
                    "date": "2024-04-25",
                    "description": "Tendered at FedEx Facility",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "13:26 PM",
                },
                {
                    "code": "DE",
                    "date": "2024-04-25",
                    "description": "FedEx redirected your package to a nearby FedEx location",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "11:28 AM",
                },
                {
                    "code": "DE",
                    "date": "2024-04-25",
                    "description": "Customer not available or business closed",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "11:26 AM",
                },
                {
                    "code": "OD",
                    "date": "2024-04-25",
                    "description": "On FedEx vehicle for delivery",
                    "location": "CLOVIS, CA, 93612, US",
                    "time": "08:55 AM",
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

ParsedInconsistentDateTimeResponse = [
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "delivered": True,
            "events": [
                {
                    "code": "DL",
                    "date": "2024-08-20",
                    "description": "Delivered",
                    "location": "Blue Point, NY, 11715, US",
                    "time": "12:41 PM",
                },
                {
                    "code": "OD",
                    "date": "2024-08-20",
                    "description": "On FedEx vehicle for delivery",
                    "location": "HOLBROOK, NY, 11741, US",
                    "time": "06:47 AM",
                },
                {
                    "code": "AR",
                    "date": "2024-08-20",
                    "description": "At local FedEx facility",
                    "location": "HOLBROOK, NY, 11741, US",
                    "time": "06:38 AM",
                },
                {
                    "code": "DP",
                    "date": "2024-08-20",
                    "description": "Departed FedEx location",
                    "location": "KEASBEY, NJ, 08832, US",
                    "time": "01:29 AM",
                },
                {
                    "code": "AR",
                    "date": "2024-08-19",
                    "description": "Arrived at FedEx location",
                    "location": "KEASBEY, NJ, 08832, US",
                    "time": "14:31 PM",
                },
                {
                    "code": "IT",
                    "date": "2024-08-19",
                    "description": "On the way",
                    "location": "WOODBRIDGE TWP, NJ, 08832, US",
                    "time": "09:13 AM",
                },
                {
                    "code": "IT",
                    "date": "2024-08-18",
                    "description": "On the way",
                    "location": "WOODBRIDGE TWP, NJ, 08832, US",
                    "time": "16:03 PM",
                },
                {
                    "code": "IT",
                    "date": "2024-08-18",
                    "description": "On the way",
                    "location": "WOODBRIDGE TWP, NJ, 08832, US",
                    "time": "03:39 AM",
                },
                {
                    "code": "DP",
                    "date": "2024-08-17",
                    "description": "Departed FedEx location",
                    "location": "GROVE CITY, OH, 43123, US",
                    "time": "08:52 AM",
                },
                {
                    "code": "AR",
                    "date": "2024-08-16",
                    "description": "Arrived at FedEx location",
                    "location": "GROVE CITY, OH, 43123, US",
                    "time": "19:39 PM",
                },
                {
                    "code": "DP",
                    "date": "2024-08-16",
                    "description": "Departed FedEx location",
                    "location": "CEDAR RAPIDS, IA, 52404, US",
                    "time": "07:35 AM",
                },
                {
                    "code": "AR",
                    "date": "2024-08-16",
                    "description": "Arrived at FedEx location",
                    "location": "CEDAR RAPIDS, IA, 52404, US",
                    "time": "04:34 AM",
                },
                {
                    "code": "DP",
                    "date": "2024-08-15",
                    "description": "Left FedEx origin facility",
                    "location": "MANKATO, MN, 56001, US",
                    "time": "19:29 PM",
                },
                {
                    "code": "AE",
                    "date": "2024-08-15",
                    "description": "Shipment arriving early",
                    "location": "MANKATO, MN, 56001, US",
                    "time": "18:40 PM",
                },
                {
                    "code": "AR",
                    "date": "2024-08-15",
                    "description": "Arrived at FedEx location",
                    "location": "MANKATO, MN, 56001, US",
                    "time": "18:35 PM",
                },
                {
                    "code": "OC",
                    "date": "2024-08-15",
                    "description": "Shipment information sent to FedEx",
                    "location": "56003, US",
                    "time": "10:36 AM",
                },
                {
                    "code": "PU",
                    "date": "2024-08-15",
                    "description": "Picked up",
                    "location": "MANKATO, MN, 56001, US",
                    "time": "00:00 AM",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=738488882438",
                "shipment_origin_country": "US",
                "shipment_service": "FedEx Ground",
            },
            "status": "delivered",
            "tracking_number": "738488882438",
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

ProofOfDeliveryResponse = """{
  "transactionId": "APIF_SV_TRKC_TxID6d2984b6-9218-4be2-a422-b6b28c9266",
  "output": {
    "alerts": [
      {
        "code": "VIRTUAL.RESPONSE",
        "message": "This is a Virtual Response."
      }
    ],
    "localization": {
      "localeCode": "US",
      "languageCode": "en"
    },
    "documentType": "SIGNATURE_PROOF_OF_DELIVERY",
    "documentFormat": "PDF",
    "documents": [
      "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"
    ]
  }
}
"""

InconsistentDateTimeResponse = """{
  "transactionId": "ccfcfe7f-b79a-425d-b368-8063f064a046",
  "output": {
    "completeTrackResults": [
      {
        "trackingNumber": "738488882438",
        "trackResults": [
          {
            "trackingNumberInfo": {
              "trackingNumber": "738488882438",
              "trackingNumberUniqueId": "12028~738488882438~FDEG",
              "carrierCode": "FDXG"
            },
            "additionalTrackingInfo": {
              "nickname": "",
              "packageIdentifiers": [
                {
                  "type": "CUSTOMER_REFERENCE",
                  "values": [
                    "G177832"
                  ],
                  "trackingNumberUniqueId": "",
                  "carrierCode": ""
                }
              ],
              "hasAssociatedShipments": false
            },
            "shipperInformation": {
              "contact": {},
              "address": {
                "city": "NORTH MANKATO",
                "stateOrProvinceCode": "MN",
                "countryCode": "US",
                "residential": false,
                "countryName": "United States"
              }
            },
            "recipientInformation": {
              "contact": {},
              "address": {
                "city": "Blue Point",
                "stateOrProvinceCode": "NY",
                "countryCode": "US",
                "residential": false,
                "countryName": "United States"
              }
            },
            "latestStatusDetail": {
              "code": "DL",
              "derivedCode": "DL",
              "statusByLocale": "Delivered",
              "description": "Delivered",
              "scanLocation": {
                "city": "Blue Point",
                "stateOrProvinceCode": "NY",
                "countryCode": "US",
                "residential": false,
                "countryName": "United States"
              }
            },
            "dateAndTimes": [
              {
                "type": "ACTUAL_DELIVERY",
                "dateTime": "2024-08-20T12:41:57-04:00"
              },
              {
                "type": "ACTUAL_PICKUP",
                "dateTime": "2024-08-15T00:00:00-06:00"
              },
              {
                "type": "SHIP",
                "dateTime": "2024-08-15T00:00:00-06:00"
              },
              {
                "type": "ACTUAL_TENDER",
                "dateTime": "2024-08-15T00:00:00-06:00"
              },
              {
                "type": "ANTICIPATED_TENDER",
                "dateTime": "2024-08-15T00:00:00-06:00"
              }
            ],
            "availableImages": [
              {
                "type": "SIGNATURE_PROOF_OF_DELIVERY"
              }
            ],
            "packageDetails": {
              "packagingDescription": {
                "type": "YOUR_PACKAGING",
                "description": "Package"
              },
              "physicalPackagingType": "PACKAGE",
              "sequenceNumber": "1",
              "count": "1",
              "weightAndDimensions": {
                "weight": [
                  {
                    "value": "28.8",
                    "unit": "LB"
                  },
                  {
                    "value": "13.06",
                    "unit": "KG"
                  }
                ],
                "dimensions": [
                  {
                    "length": 15,
                    "width": 12,
                    "height": 11,
                    "units": "IN"
                  },
                  {
                    "length": 38,
                    "width": 30,
                    "height": 27,
                    "units": "CM"
                  }
                ]
              },
              "packageContent": []
            },
            "shipmentDetails": {
              "possessionStatus": true
            },
            "scanEvents": [
              {
                "date": "2024-08-20T12:41:57-04:00",
                "eventType": "DL",
                "eventDescription": "Delivered",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "Blue Point",
                  "stateOrProvinceCode": "NY",
                  "postalCode": "11715",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationType": "DELIVERY_LOCATION",
                "derivedStatusCode": "DL",
                "derivedStatus": "Delivered"
              },
              {
                "date": "2024-08-20T06:47:00-04:00",
                "eventType": "OD",
                "eventDescription": "On FedEx vehicle for delivery",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "HOLBROOK",
                  "stateOrProvinceCode": "NY",
                  "postalCode": "11741",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0117",
                "locationType": "VEHICLE",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-20T06:38:00-04:00",
                "eventType": "AR",
                "eventDescription": "At local FedEx facility",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "HOLBROOK",
                  "stateOrProvinceCode": "NY",
                  "postalCode": "11741",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0117",
                "locationType": "DESTINATION_FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-20T01:29:05-04:00",
                "eventType": "DP",
                "eventDescription": "Departed FedEx location",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "KEASBEY",
                  "stateOrProvinceCode": "NJ",
                  "postalCode": "08832",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0089",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-19T14:31:00-04:00",
                "eventType": "AR",
                "eventDescription": "Arrived at FedEx location",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "KEASBEY",
                  "stateOrProvinceCode": "NJ",
                  "postalCode": "08832",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0089",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-19T09:13:51-04:00",
                "eventType": "IT",
                "eventDescription": "On the way",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "WOODBRIDGE TWP",
                  "stateOrProvinceCode": "NJ",
                  "postalCode": "08832",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationType": "VEHICLE",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-18T16:03:54-04:00",
                "eventType": "IT",
                "eventDescription": "On the way",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "WOODBRIDGE TWP",
                  "stateOrProvinceCode": "NJ",
                  "postalCode": "08832",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationType": "VEHICLE",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-18T03:39:18-04:00",
                "eventType": "IT",
                "eventDescription": "On the way",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "WOODBRIDGE TWP",
                  "stateOrProvinceCode": "NJ",
                  "postalCode": "08832",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationType": "VEHICLE",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-17T08:52:11-04:00",
                "eventType": "DP",
                "eventDescription": "Departed FedEx location",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "GROVE CITY",
                  "stateOrProvinceCode": "OH",
                  "postalCode": "43123",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0432",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-16T19:39:00-04:00",
                "eventType": "AR",
                "eventDescription": "Arrived at FedEx location",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "GROVE CITY",
                  "stateOrProvinceCode": "OH",
                  "postalCode": "43123",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0432",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-16T07:35:16-05:00",
                "eventType": "DP",
                "eventDescription": "Departed FedEx location",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "CEDAR RAPIDS",
                  "stateOrProvinceCode": "IA",
                  "postalCode": "52404",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0522",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-16T04:34:00-05:00",
                "eventType": "AR",
                "eventDescription": "Arrived at FedEx location",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "CEDAR RAPIDS",
                  "stateOrProvinceCode": "IA",
                  "postalCode": "52404",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0522",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-15T19:29:25-05:00",
                "eventType": "DP",
                "eventDescription": "Left FedEx origin facility",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "MANKATO",
                  "stateOrProvinceCode": "MN",
                  "postalCode": "56001",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0560",
                "locationType": "ORIGIN_FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-15T18:40:27-05:00",
                "eventType": "AE",
                "eventDescription": "Shipment arriving early",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "MANKATO",
                  "stateOrProvinceCode": "MN",
                  "postalCode": "56001",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0560",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-15T18:35:00-05:00",
                "eventType": "AR",
                "eventDescription": "Arrived at FedEx location",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "MANKATO",
                  "stateOrProvinceCode": "MN",
                  "postalCode": "56001",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0560",
                "locationType": "FEDEX_FACILITY",
                "derivedStatusCode": "IT",
                "derivedStatus": "In transit"
              },
              {
                "date": "2024-08-15T10:36:00-05:00",
                "eventType": "OC",
                "eventDescription": "Shipment information sent to FedEx",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "postalCode": "56003",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationType": "CUSTOMER",
                "derivedStatusCode": "IN",
                "derivedStatus": "Label created"
              },
              {
                "date": "2024-08-15T00:00:00",
                "eventType": "PU",
                "eventDescription": "Picked up",
                "exceptionCode": "",
                "exceptionDescription": "",
                "scanLocation": {
                  "streetLines": [
                    ""
                  ],
                  "city": "MANKATO",
                  "stateOrProvinceCode": "MN",
                  "postalCode": "56001",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                },
                "locationId": "0560",
                "locationType": "PICKUP_LOCATION",
                "derivedStatusCode": "PU",
                "derivedStatus": "Picked up"
              }
            ],
            "availableNotifications": [
              "ON_DELIVERY"
            ],
            "deliveryDetails": {
              "actualDeliveryAddress": {
                "city": "Blue Point",
                "stateOrProvinceCode": "NY",
                "countryCode": "US",
                "residential": false,
                "countryName": "United States"
              },
              "deliveryAttempts": "0",
              "receivedByName": "CREILLY",
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
                  "eligibility": "POSSIBLY_ELIGIBLE"
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
                  "city": "MANKATO",
                  "stateOrProvinceCode": "MN",
                  "countryCode": "US",
                  "residential": false,
                  "countryName": "United States"
                }
              }
            },
            "lastUpdatedDestinationAddress": {
              "city": "BLUE POINT",
              "stateOrProvinceCode": "NY",
              "countryCode": "US",
              "residential": false,
              "countryName": "United States"
            },
            "serviceDetail": {
              "type": "FEDEX_GROUND",
              "description": "FedEx Ground",
              "shortDescription": "FG"
            },
            "standardTransitTimeWindow": {
              "window": {
                "ends": "2024-08-21T00:00:00-06:00"
              }
            },
            "estimatedDeliveryTimeWindow": {
              "window": {}
            },
            "goodsClassificationCode": "",
            "returnDetail": {}
          }
        ]
      }
    ]
  }
}
"""
