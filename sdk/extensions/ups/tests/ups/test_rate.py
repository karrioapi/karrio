import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from .fixture import gateway
import karrio


class TestUPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_req_data)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(request.serialize(), RateRequestData)

    def test_create_rate_with_package_preset_request(self):
        request = gateway.mapper.create_rate_request(
            RateRequest(**rate_req_with_package_preset_data)
        )
        self.assertEqual(request.serialize(), RateRequestWithPackagePresetData)

    @patch("karrio.mappers.ups.proxy.lib.request", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        karrio.Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}/api/rating/v2205/Shop?additionalinfo=timeintransit",
        )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = RateResponseJSON
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


rate_req_data = {
    "shipper": {
        "postal_code": "V6M2V9",
        "city": "Vancouver",
        "country_code": "CA",
        "state_code": "BC",
        "residential": True,
        "address_line1": "5840 Oak St",
    },
    "recipient": {
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "country_code": "CA",
        "state_code": "NB",
        "residential": False,
        "address_line1": "125 Church St",
    },
    "parcels": [
        {
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 0.5,
            "weight_unit": "KG",
            "packaging_type": "ups_large_express_box",
            "description": "TV",
        }
    ],
    "reference": "Your Customer Context",
    "services": ["ups_standard"],
    "options": {
        "shipment_date": "2023-02-27",
        "negotiated_rates_indicator": True,
    },
}

rate_req_with_package_preset_data = {
    "shipper": {
        "company_name": "Shipper Name",
        "postal_code": "H3N1S4",
        "country_code": "CA",
        "city": "Montreal",
        "address_line1": "Address Line",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "address_line1": "Address Line",
        "postal_code": "89109",
        "city": "Las Vegas",
        "country_code": "US",
        "state_code": "StateProvinceCode",
    },
    "parcels": [
        {
            "package_preset": "ups_express_pak",
            "description": "TV",
            "weight": 4.0,
        }
    ],
    "reference": "Your Customer Context",
    "services": ["ups_standard"],
    "options": {
        "shipment_date": "2023-02-27",
        "negotiated_rates_indicator": True,
    },
}


ParsedRateResponse = [
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 137.87, "currency": "CAD", "name": "Base charge"},
                {"amount": 0.0, "currency": "CAD", "name": "14"},
                {"amount": 21.52, "currency": "CAD", "name": "375"},
                {"amount": 20.68, "currency": "CAD", "name": "HST"},
            ],
            "meta": {"service_name": "ups_express_early_ca"},
            "service": "ups_express_early_ca",
            "total_charge": 158.55,
            "transit_days": 2,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 85.26, "currency": "CAD", "name": "Base charge"},
                {"amount": 0.0, "currency": "CAD", "name": "01"},
                {"amount": 13.31, "currency": "CAD", "name": "375"},
                {"amount": 12.79, "currency": "CAD", "name": "HST"},
            ],
            "meta": {"service_name": "ups_express_ca"},
            "service": "ups_express_ca",
            "total_charge": 98.05,
            "transit_days": 2,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 84.02, "currency": "CAD", "name": "Base charge"},
                {"amount": 0.0, "currency": "CAD", "name": "13"},
                {"amount": 13.12, "currency": "CAD", "name": "375"},
                {"amount": 12.6, "currency": "CAD", "name": "HST"},
            ],
            "meta": {"service_name": "ups_express_saver_ca"},
            "service": "ups_express_saver_ca",
            "total_charge": 96.62,
            "transit_days": 2,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 79.51, "currency": "CAD", "name": "Base charge"},
                {"amount": 0.0, "currency": "CAD", "name": "02"},
                {"amount": 12.41, "currency": "CAD", "name": "375"},
                {"amount": 11.93, "currency": "CAD", "name": "HST"},
            ],
            "meta": {"service_name": "ups_expedited_ca"},
            "service": "ups_expedited_ca",
            "total_charge": 91.44,
            "transit_days": 3,
        },
    ],
    [],
]


RateRequestData = {
    "RateRequest": {
        "Request": {
            "RequestOption": "Shoptimeintransit",
            "SubVersion": "2205",
            "TransactionReference": {"CustomerContext": "Your Customer Context"},
        },
        "Shipment": {
            "DeliveryTimeInformation": {
                "PackageBillType": "03",
                "Pickup": {"Date": "20230227"},
            },
            "InvoiceLineTotal": {"CurrencyCode": "USD", "MonetaryValue": "1.0"},
            "Package": [
                {
                    "Dimensions": {
                        "Height": "3.0",
                        "Length": "10.0",
                        "UnitOfMeasurement": {"Code": "CM", "Description": "Dimension"},
                        "Width": "3.0",
                    },
                    "PackageWeight": {
                        "UnitOfMeasurement": {"Code": "KGS", "Description": "Weight"},
                        "Weight": "0.5",
                    },
                    "PackagingType": {"Code": "2c", "Description": "Packaging Type"},
                }
            ],
            "PaymentDetails": {
                "ShipmentCharge": {
                    "BillShipper": {"AccountNumber": "Your Account Number"},
                    "Type": "01",
                }
            },
            "RatingMethodRequestedIndicator": "Y",
            "Service": {"Code": "11", "Description": "Weight"},
            "ShipFrom": {
                "Address": {
                    "AddressLine": "5840 Oak St",
                    "City": "Vancouver",
                    "CountryCode": "CA",
                    "PostalCode": "V6M2V9",
                    "StateProvinceCode": "BC",
                }
            },
            "ShipTo": {
                "Address": {
                    "AddressLine": "125 Church St",
                    "City": "Moncton",
                    "CountryCode": "CA",
                    "PostalCode": "E1C4Z8",
                    "StateProvinceCode": "NB",
                }
            },
            "ShipmentRatingOptions": {"NegotiatedRatesIndicator": "Y"},
            "ShipmentTotalWeight": {
                "UnitOfMeasurement": {"Code": "KGS", "Description": "Dimension"},
                "Weight": "0.5",
            },
            "Shipper": {
                "Address": {
                    "AddressLine": "5840 Oak St",
                    "City": "Vancouver",
                    "CountryCode": "CA",
                    "PostalCode": "V6M2V9",
                    "StateProvinceCode": "BC",
                },
                "ShipperNumber": "Your Account Number",
            },
            "TaxInformationIndicator": "Y",
        },
    }
}

RateRequestWithPackagePresetData = {
    "RateRequest": {
        "Request": {
            "RequestOption": "Shoptimeintransit",
            "SubVersion": "2205",
            "TransactionReference": {"CustomerContext": "Your Customer Context"},
        },
        "Shipment": {
            "DeliveryTimeInformation": {
                "PackageBillType": "03",
                "Pickup": {"Date": "20230227"},
            },
            "InvoiceLineTotal": {"CurrencyCode": "USD", "MonetaryValue": "1.0"},
            "Package": [
                {
                    "Dimensions": {
                        "Height": "11.75",
                        "Length": "1.5",
                        "UnitOfMeasurement": {"Code": "IN", "Description": "Dimension"},
                        "Width": "16.0",
                    },
                    "PackageWeight": {
                        "UnitOfMeasurement": {"Code": "LBS", "Description": "Weight"},
                        "Weight": "4.0",
                    },
                    "PackagingType": {"Code": "02", "Description": "Packaging Type"},
                }
            ],
            "PaymentDetails": {
                "ShipmentCharge": {
                    "BillShipper": {"AccountNumber": "Your Account Number"},
                    "Type": "01",
                }
            },
            "RatingMethodRequestedIndicator": "Y",
            "Service": {"Code": "11", "Description": "Weight"},
            "ShipFrom": {
                "Address": {
                    "AddressLine": "Address Line",
                    "City": "Montreal",
                    "CountryCode": "CA",
                    "PostalCode": "H3N1S4",
                },
                "AttentionName": "Shipper Name",
            },
            "ShipTo": {
                "Address": {
                    "AddressLine": "Address Line",
                    "City": "Las Vegas",
                    "CountryCode": "US",
                    "PostalCode": "89109",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Ship To Name",
            },
            "ShipmentRatingOptions": {"NegotiatedRatesIndicator": "Y"},
            "ShipmentTotalWeight": {
                "UnitOfMeasurement": {"Code": "LBS", "Description": "Dimension"},
                "Weight": "4.0",
            },
            "Shipper": {
                "Address": {
                    "AddressLine": "Address Line",
                    "City": "Montreal",
                    "CountryCode": "CA",
                    "PostalCode": "H3N1S4",
                },
                "AttentionName": "Shipper Name",
                "ShipperNumber": "Your Account Number",
            },
            "TaxInformationIndicator": "Y",
        },
    }
}

RateResponseJSON = """{
  "RateResponse": {
    "Response": {
      "ResponseStatus": {
        "Code": "1",
        "Description": "Success"
      },
      "Alert": [
        {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        {
          "Code": "120900",
          "Description": "User Id and Shipper Number combination is not qualified to receive negotiated rates"
        }
      ],
      "TransactionReference": {
        "CustomerContext": "testing",
        "TransactionIdentifier": "iewssoat2634G4WGGx4hfZ"
      }
    },
    "RatedShipment": [
      {
        "Disclaimer": {
          "Code": "01",
          "Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": {
          "Code": "14",
          "Description": ""
        },
        "RatedShipmentAlert": [
          {
            "Code": "120900",
            "Description": "User Id and Shipper Number combination is not qualified to receive negotiated rates."
          },
          {
            "Code": "110971",
            "Description": "Your invoice may vary from the displayed reference rates"
          }
        ],
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": {
            "Code": "KGS",
            "Description": "Kilograms"
          },
          "Weight": "0.5"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "137.87"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "116.35"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "CAD",
          "MonetaryValue": "21.52"
        },
        "TaxCharges": {
          "Type": "HST",
          "MonetaryValue": "20.68"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "137.87"
        },
        "TotalChargesWithTaxes": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "158.55"
        },
        "GuaranteedDelivery": {
          "BusinessDaysInTransit": "1",
          "DeliveryByTime": "9:00 A.M."
        },
        "RatedPackage": {
          "Weight": "0.5"
        },
        "TimeInTransit": {
          "PickupDate": "20230605",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": {
              "Description": "UPS Express Early"
            },
            "EstimatedArrival": {
              "Arrival": {
                "Date": "20230607",
                "Time": "090000"
              },
              "BusinessDaysInTransit": "2",
              "Pickup": {
                "Date": "20230605",
                "Time": "150000"
              },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "140000",
              "TotalTransitDays": "2"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": {
          "Code": "01",
          "Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": {
          "Code": "01",
          "Description": ""
        },
        "RatedShipmentAlert": [
          {
            "Code": "120900",
            "Description": "User Id and Shipper Number combination is not qualified to receive negotiated rates."
          },
          {
            "Code": "110971",
            "Description": "Your invoice may vary from the displayed reference rates"
          }
        ],
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": {
            "Code": "KGS",
            "Description": "Kilograms"
          },
          "Weight": "0.5"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "85.26"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "71.95"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "CAD",
          "MonetaryValue": "13.31"
        },
        "TaxCharges": {
          "Type": "HST",
          "MonetaryValue": "12.79"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "85.26"
        },
        "TotalChargesWithTaxes": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "98.05"
        },
        "GuaranteedDelivery": {
          "BusinessDaysInTransit": "1"
        },
        "RatedPackage": {
          "Weight": "0.5"
        },
        "TimeInTransit": {
          "PickupDate": "20230605",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": {
              "Description": "UPS Express"
            },
            "EstimatedArrival": {
              "Arrival": {
                "Date": "20230607",
                "Time": "103000"
              },
              "BusinessDaysInTransit": "2",
              "Pickup": {
                "Date": "20230605",
                "Time": "150000"
              },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "140000",
              "TotalTransitDays": "2"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": {
          "Code": "01",
          "Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": {
          "Code": "13",
          "Description": ""
        },
        "RatedShipmentAlert": [
          {
            "Code": "120900",
            "Description": "User Id and Shipper Number combination is not qualified to receive negotiated rates."
          },
          {
            "Code": "110971",
            "Description": "Your invoice may vary from the displayed reference rates"
          }
        ],
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": {
            "Code": "KGS",
            "Description": "Kilograms"
          },
          "Weight": "0.5"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "84.02"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "70.90"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "CAD",
          "MonetaryValue": "13.12"
        },
        "TaxCharges": {
          "Type": "HST",
          "MonetaryValue": "12.60"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "84.02"
        },
        "TotalChargesWithTaxes": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "96.62"
        },
        "GuaranteedDelivery": {
          "BusinessDaysInTransit": "1",
          "DeliveryByTime": "3:00 P.M."
        },
        "RatedPackage": {
          "Weight": "0.5"
        },
        "TimeInTransit": {
          "PickupDate": "20230605",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": {
              "Description": "UPS Express Saver"
            },
            "EstimatedArrival": {
              "Arrival": {
                "Date": "20230607",
                "Time": "150000"
              },
              "BusinessDaysInTransit": "2",
              "Pickup": {
                "Date": "20230605",
                "Time": "150000"
              },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "140000",
              "TotalTransitDays": "2"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": {
          "Code": "01",
          "Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": {
          "Code": "02",
          "Description": ""
        },
        "RatedShipmentAlert": [
          {
            "Code": "120900",
            "Description": "User Id and Shipper Number combination is not qualified to receive negotiated rates."
          },
          {
            "Code": "110971",
            "Description": "Your invoice may vary from the displayed reference rates"
          }
        ],
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": {
            "Code": "KGS",
            "Description": "Kilograms"
          },
          "Weight": "0.5"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "79.51"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "67.10"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "CAD",
          "MonetaryValue": "12.41"
        },
        "TaxCharges": {
          "Type": "HST",
          "MonetaryValue": "11.93"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "79.51"
        },
        "TotalChargesWithTaxes": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "91.44"
        },
        "RatedPackage": {
          "Weight": "0.5"
        },
        "TimeInTransit": {
          "PickupDate": "20230605",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": {
              "Description": "UPS Expedited"
            },
            "EstimatedArrival": {
              "Arrival": {
                "Date": "20230608",
                "Time": "233000"
              },
              "BusinessDaysInTransit": "3",
              "Pickup": {
                "Date": "20230605",
                "Time": "150000"
              },
              "DayOfWeek": "THU",
              "CustomerCenterCutoff": "140000",
              "TotalTransitDays": "3"
            },
            "SaturdayDelivery": "0"
          }
        }
      }
    ]
  }
}
"""
