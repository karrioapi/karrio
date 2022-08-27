import unittest
from unittest.mock import patch, ANY
from tests.ups_freight.fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUPSFreightShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/ship/v1/freight/shipments/ground",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "ups_tforce_freight_ltl",
    "shipper": {
        "company_name": "Test US Shipper",
        "person_name": "Test Shipper",
        "postal_code": "21093",
        "country_code": "US",
        "state_code": "MD",
        "city": "TIMONIUM",
        "address_line1": "123 Lane",
        "residential": True,
    },
    "recipient": {
        "company_name": "Dilbert's Derbies",
        "person_name": "Test Shipper",
        "address_line1": "555 Main St",
        "postal_code": "40201",
        "city": "LOUISVILLE",
        "country_code": "US",
        "state_code": "KY",
    },
    "parcels": [
        {
            "height": 4,
            "length": 9,
            "width": 5,
            "weight": 150,
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "packaging_type": "pallet",
            "options": {"freight_class": "60"},
        }
    ],
    "options": {"ups_freight_call_before_delivery_indicator": True},
}

ParsedShipmentResponse = [
    {
        "carrier_id": "ups_freight",
        "carrier_name": "ups_freight",
        "docs": {"label": "R0lGODdhIAOwBPAAAA=="},
        "label_type": "PDF",
        "meta": {"pickup_confirmation_number": "WBU4760605"},
        "selected_rate": {
            "carrier_id": "ups_freight",
            "carrier_name": "ups_freight",
            "currency": "USD",
            "extra_charges": [
                {"amount": 1061.78, "currency": "USD", "name": "DSCNT"},
                {"amount": 70.0, "currency": "%", "name": "DSCNT_RATE"},
                {"amount": 116.49, "currency": "USD", "name": "2"},
                {"amount": 30.0, "currency": "USD", "name": "CA_BORDER"},
                {"amount": 7.5, "currency": "USD", "name": "HICST"},
                {"amount": 1516.83, "currency": "USD", "name": "LND_GROSS"},
                {"amount": 455.05, "currency": "USD", "name": "AFTR_DSCNT"},
            ],
            "meta": {"service_name": "ups_tforce_freight_ltl"},
            "service": "ups_tforce_freight_ltl",
            "total_charge": 609.04,
            "transit_days": 5,
        },
        "shipment_identifier": "071666884",
        "tracking_number": "071666884",
    },
    [
        {
            "carrier_id": "ups_freight",
            "carrier_name": "ups_freight",
            "code": "9369054",
            "message": "User is not registered for freight processing.",
        },
        {
            "carrier_id": "ups_freight",
            "carrier_name": "ups_freight",
            "code": "9369055",
            "message": "User is not eligible for contract rates.",
        },
    ],
]


ShipmentRequest = {
    "FreightShipRequest": {
        "Miscellaneous": {"ReleaseID": "07.12.2008", "WSVersion": "21.0.11"},
        "Shipment": {
            "Commodity": [
                {
                    "Dimensions": {
                        "Height": 4.0,
                        "Length": 9.0,
                        "UnitOfMeasurement": {"Code": "IN"},
                        "Width": 5.0,
                    },
                    "FreightClass": "60",
                    "NumberOfPieces": 0,
                    "PackagingType": {"Code": "Pallet"},
                    "Weight": {"UnitOfMeasurement": {"Code": "LBS"}, "Value": 150.0},
                }
            ],
            "Documents": {
                "Image": [
                    {
                        "Format": {"Code": "01"},
                        "LabelsPerPage": 1,
                        "PrintFormat": {"Code": "02"},
                        "PrintSize": {"Length": 4, "Width": 64},
                        "Type": {"Code": "30"},
                    }
                ]
            },
            "HandlingUnitOne": {"Quantity": 0, "Type": {"Code": "Pallet"}},
            "PaymentInformation": {
                "Payer": {
                    "Address": {
                        "AddressLine": "123 Lane",
                        "City": "TIMONIUM",
                        "CountryCode": "US",
                        "PostalCode": "21093",
                        "StateProvinceCode": "MD",
                    },
                    "AttentionName": "Test Shipper",
                    "Name": "Test US Shipper",
                    "ShipperNumber": "Your Account Number",
                },
                "ShipmentBillingOption": {"Code": "10"},
            },
            "Service": {"Code": "308"},
            "ShipFrom": {
                "Address": {
                    "AddressLine": "123 Lane",
                    "City": "TIMONIUM",
                    "CountryCode": "US",
                    "PostalCode": "21093",
                    "StateProvinceCode": "MD",
                },
                "AttentionName": "Test Shipper",
                "Name": "Test US Shipper",
                "Phone": {"Number": "000 000 0000"},
            },
            "ShipTo": {
                "Address": {
                    "AddressLine": "555 Main St",
                    "City": "LOUISVILLE",
                    "CountryCode": "US",
                    "PostalCode": "40201",
                    "StateProvinceCode": "KY",
                },
                "AttentionName": "Test Shipper",
                "Name": "Dilbert's Derbies",
                "Phone": {"Number": "0000"},
            },
            "ShipperNumber": "Your Account Number",
        },
    }
}

ShipmentResponse = """{
  "FreightShipResponse": {
    "Response": {
      "ResponseStatus": {
        "Code": "1",
        "Description": "Success"
      },
      "Alert": [
        {
          "Code": "9369054",
          "Description": "User is not registered for freight processing."
        },
        {
          "Code": "9369055",
          "Description": "User is not eligible for contract rates."
        }
      ],
      "TransactionReference": {
        "CustomerContext": "test",
        "TransactionIdentifier": "xwsspta21d57mXchCHhJST"
      }
    },
    "ShipmentResults": {
      "OriginServiceCenterCode": "SLO",
      "PickupRequestConfirmationNumber": "WBU4760605",
      "ShipmentNumber": "071666884",
      "BOLID": "44468128",
      "GuaranteedIndicator": "",
      "Rate": [
        {
          "Type": {
            "Code": "DSCNT",
            "Description": "DSCNT"
          },
          "Factor": {
            "Value": "1061.78",
            "UnitOfMeasurement": {
              "Code": "USD"
            }
          }
        },
        {
          "Type": {
            "Code": "DSCNT_RATE",
            "Description": "DSCNT_RATE"
          },
          "Factor": {
            "Value": "70.00",
            "UnitOfMeasurement": {
              "Code": "%"
            }
          }
        },
        {
          "Type": {
            "Code": "2",
            "Description": "2"
          },
          "Factor": {
            "Value": "116.49",
            "UnitOfMeasurement": {
              "Code": "USD"
            }
          }
        },
        {
          "Type": {
            "Code": "CA_BORDER",
            "Description": "CA_BORDER"
          },
          "Factor": {
            "Value": "30.00",
            "UnitOfMeasurement": {
              "Code": "USD"
            }
          }
        },
        {
          "Type": {
            "Code": "HICST",
            "Description": "HICST"
          },
          "Factor": {
            "Value": "7.50",
            "UnitOfMeasurement": {
              "Code": "USD"
            }
          }
        },
        {
          "Type": {
            "Code": "LND_GROSS",
            "Description": "LND_GROSS"
          },
          "Factor": {
            "Value": "1516.83",
            "UnitOfMeasurement": {
              "Code": "USD"
            }
          }
        },
        {
          "Type": {
            "Code": "AFTR_DSCNT",
            "Description": "AFTR_DSCNT"
          },
          "Factor": {
            "Value": "455.05",
            "UnitOfMeasurement": {
              "Code": "USD"
            }
          }
        }
      ],
      "TotalShipmentCharge": {
        "CurrencyCode": "USD",
        "MonetaryValue": "609.04"
      },
      "BillableShipmentWeight": {
        "UnitOfMeasurement": {
          "Code": "LBS"
        },
        "Value": "190"
      },
      "Service": {
        "Code": "308"
      },
      "Documents": {
        "Image": [
          {
            "Type": {
              "Code": "30",
              "Description": "string"
            },
            "GraphicImage": "R0lGODdhIAOwBPAAAA==",
            "Format": {
              "Code": "string",
              "Description": "string"
            }
          }
        ]
      },
      "TimeInTransit": {
        "DaysInTransit": "5"
      }
    }
  }
}
"""
