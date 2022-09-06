import unittest
from unittest.mock import patch
from tests.ups_freight.fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUPSFreightRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/ship/v1/freight/shipments/ground",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
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

ParsedRateResponse = [
    [
        {
            "carrier_id": "ups_freight",
            "carrier_name": "ups_freight",
            "currency": "USD",
            "extra_charges": [
                {"amount": 117.24, "currency": "USD", "name": "fuel_surcharge"},
                {"amount": 457.98, "currency": "USD", "name": "gross_charges"},
                {"amount": 457.98, "currency": "USD", "name": "amount_after_discount"},
            ],
            "meta": {"service_name": "ups_tforce_freight_ltl"},
            "service": "ups_tforce_freight_ltl",
            "total_charge": 575.22,
            "transit_days": 2,
        }
    ],
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
        {
            "carrier_id": "ups_freight",
            "carrier_name": "ups_freight",
            "code": "9369080",
            "message": "Time in Transit (for FRS/GFP) information not available at this time.",
        },
    ],
]


RateRequest = {
    "FreightRateRequest": {
        "AlternateRateOptions": {"Code": "3"},
        "Commodity": [
            {
                "Dimensions": {
                    "Height": 4.0,
                    "Length": 9.0,
                    "UnitOfMeasurement": {"Code": "IN"},
                    "Width": 5.0,
                },
                "FreightClass": "50",
                "NumberOfPieces": 0,
                "PackagingType": {"Code": "Pallet"},
                "Weight": {"UnitOfMeasurement": {"Code": "LBS"}, "Value": 150.0},
            }
        ],
        "PaymentInformation": {
            "Payer": {
                "Address": {
                    "AddressLine": "123 Lane",
                    "City": "TIMONIUM",
                    "CountryCode": "US",
                    "PostalCode": "21093",
                    "ResidentialAddressIndicator": "true",
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
                "ResidentialAddressIndicator": "true",
                "StateProvinceCode": "MD",
            },
            "Name": "Test US Shipper",
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
        },
        "ShipmentServiceOptions": {
            "DeliveryOptions": {"CallBeforeDeliveryIndicator": "true"}
        },
    }
}


RateResponse = """{
  "FreightRateResponse": {
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
        },
        {
          "Code": "9369080",
          "Description": "Time in Transit (for FRS/GFP) information not available at this time."
        }
      ],
      "TransactionReference": {
        "CustomerContext": "test",
        "TransactionIdentifier": "xwsspta21dg7HtJj4gW7tR"
      }
    },
    "Rate": [
      {
        "Type": {
          "Code": "2",
          "Description": "2"
        },
        "Factor": {
          "Value": "117.24",
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
          "Value": "457.98",
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
          "Value": "457.98",
          "UnitOfMeasurement": {
            "Code": "USD"
          }
        }
      }
    ],
    "Commodity": {
      "Description": "FRS-Freight",
      "Weight": {
        "Value": "150",
        "UnitOfMeasurement": {
          "Code": "LBS"
        }
      },
      "AdjustedWeight": {
        "Value": "150",
        "UnitOfMeasurement": {
          "Code": "LBS"
        }
      }
    },
    "TotalShipmentCharge": {
      "CurrencyCode": "USD",
      "MonetaryValue": "575.22"
    },
    "BillableShipmentWeight": {
      "Value": "150",
      "UnitOfMeasurement": {
        "Code": "LBS"
      }
    },
    "DimensionalWeight": {
      "Value": "0",
      "UnitOfMeasurement": {
        "Code": "LBS"
      }
    },
    "Service": {
      "Code": "308"
    },
    "GuaranteedIndicator": "",
    "MinimumChargeAppliedIndicator": "",
    "AlternateRatesResponse": {
      "AlternateRateType": {
        "Code": "1",
        "Description": "FRS Rate"
      },
      "Rate": [
        {
          "Type": {
            "Code": "FRS_TOTAL_ACCS_SUR_CHARGE_COMBO",
            "Description": "FRS_TOTAL_ACCS_SUR_CHARGE_COMBO"
          },
          "Factor": {
            "Value": "137.60"
          }
        },
        {
          "Type": {
            "Code": "FRS_SHIPMENT_LEVEL_GROSS",
            "Description": "FRS_SHIPMENT_LEVEL_GROSS"
          },
          "Factor": {
            "Value": "457.98"
          }
        },
        {
          "Type": {
            "Code": "FRS_SHIPMENT_LEVEL_DISCOUNT_AMOUNT",
            "Description": "FRS_SHIPMENT_LEVEL_DISCOUNT_AMOUNT"
          },
          "Factor": {
            "Value": "366.38"
          }
        },
        {
          "Type": {
            "Code": "FRS_SHIPMENT_LEVEL_DISCOUNT_RATE",
            "Description": "FRS_SHIPMENT_LEVEL_DISCOUNT_RATE"
          },
          "Factor": {
            "Value": "80.00",
            "UnitOfMeasurement": {
              "Code": "%"
            }
          }
        },
        {
          "Type": {
            "Code": "FRS_SHIPMENT_LEVEL_NET_CHARGE",
            "Description": "FRS_SHIPMENT_LEVEL_NET_CHARGE"
          },
          "Factor": {
            "Value": "91.60"
          }
        },
        {
          "Type": {
            "Code": "FRS_PACKAGELEVEL_ACCESSORIAL_TOTAL",
            "Description": "FRS_PACKAGELEVEL_ACCESSORIAL_TOTAL"
          },
          "Factor": {
            "Value": "46.00"
          }
        },
        {
          "Type": {
            "Code": "FRS_ADDITIONAL_HANDLING",
            "Description": "FRS_ADDITIONAL_HANDLING"
          },
          "Factor": {
            "Value": "46.00"
          }
        }
      ],
      "BillableShipmentWeight": {
        "Value": "151",
        "UnitOfMeasurement": {
          "Code": "LBS"
        }
      }
    },
    "RatingSchedule": {
      "Code": "02",
      "Description": "Published Rates"
    },
    "TimeInTransit": {
      "DaysInTransit": "2"
    }
  }
}
"""
