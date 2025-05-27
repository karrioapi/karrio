import unittest
from unittest.mock import patch
import karrio.lib as lib
import karrio.core.models as models
from .fixture import gateway
import karrio.sdk as karrio


class TestUPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(request.serialize(), RateRequestData)

    def test_create_rate_with_package_preset_request(self):
        request = gateway.mapper.create_rate_request(
            models.RateRequest(**RateWithPresetPayload)
        )
        self.assertEqual(request.serialize(), RateRequestWithPackagePresetData)

    @patch("karrio.mappers.ups.proxy.lib.request", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        karrio.Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}/api/rating/v2409/Shop?additionalinfo=timeintransit",
        )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = RateResponseJSON
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_fr_rate_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = FRRateResponseJSON
            RateRequest = models.RateRequest(
                **{
                    **RatePayload,
                    **{"shipper": {**RatePayload["shipper"], "country_code": "FR"}},
                }
            )
            parsed_response = karrio.Rating.fetch(RateRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed_response), ParsedFRRateResponse)

    def test_parse_rate_response_with_total_charges(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = RateResponseWithTotalChargesJSON
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedRateResponseWithTotalCharges
            )

    def test_parse_rate_response_with_missing_amount(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = RateResponseWithMissingAmountJSON
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedRateResponseWithMissingAmount
            )


if __name__ == "__main__":
    unittest.main()


RatePayload = {
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
        "ups_available_services_option": "3",
        "ups_delivery_confirmation": "1",
    },
}

RateWithPresetPayload = {
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
                {"amount": 251.11, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 6.65, "currency": "CAD", "name": "14"},
                {"amount": 16.38, "currency": "CAD", "name": "GST"},
                {"amount": 16.38, "currency": "CAD", "name": "GST"},
            ],
            "meta": {"rate_zone": "708", "service_name": "ups_express_early_ca"},
            "service": "ups_express_early_ca",
            "total_charge": 344.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 220.13, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 6.65, "currency": "CAD", "name": "01"},
                {"amount": 14.45, "currency": "CAD", "name": "GST"},
                {"amount": 14.45, "currency": "CAD", "name": "GST"},
            ],
            "meta": {"rate_zone": "408", "service_name": "ups_express_ca"},
            "service": "ups_express_ca",
            "total_charge": 303.48,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 195.33, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 6.65, "currency": "CAD", "name": "13"},
                {"amount": 12.91, "currency": "CAD", "name": "GST"},
                {"amount": 12.91, "currency": "CAD", "name": "GST"},
            ],
            "meta": {"rate_zone": "508", "service_name": "ups_express_saver_ca"},
            "service": "ups_express_saver_ca",
            "total_charge": 271.07,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 184.88, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 6.65, "currency": "CAD", "name": "02"},
                {"amount": 12.26, "currency": "CAD", "name": "GST"},
                {"amount": 12.26, "currency": "CAD", "name": "GST"},
            ],
            "meta": {"rate_zone": "308", "service_name": "ups_expedited_ca"},
            "service": "ups_expedited_ca",
            "total_charge": 257.41,
            "transit_days": 2,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 92.96, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 6.65, "currency": "CAD", "name": "11"},
                {"amount": 6.33, "currency": "CAD", "name": "GST"},
                {"amount": 6.33, "currency": "CAD", "name": "GST"},
            ],
            "meta": {"rate_zone": "208", "service_name": "ups_standard_ca"},
            "service": "ups_standard_ca",
            "total_charge": 132.84,
            "transit_days": 6,
        },
    ],
    [],
]

ParsedFRRateResponse = [
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "EUR",
            "extra_charges": [
                {"amount": 12.37, "currency": "EUR", "name": "BASE CHARGE"},
                {"amount": 2.74, "currency": "EUR", "name": "FUEL SURCHARGE"},
                {"amount": 3.02, "currency": "EUR", "name": "TVA"},
            ],
            "meta": {"service_name": "ups_express_eu"},
            "service": "ups_express_eu",
            "total_charge": 18.13,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "EUR",
            "extra_charges": [
                {"amount": 10.21, "currency": "EUR", "name": "BASE CHARGE"},
                {"amount": 2.26, "currency": "EUR", "name": "FUEL SURCHARGE"},
                {"amount": 2.49, "currency": "EUR", "name": "TVA"},
            ],
            "meta": {"service_name": "ups_worldwide_saver_eu"},
            "service": "ups_worldwide_saver_eu",
            "total_charge": 14.96,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "EUR",
            "extra_charges": [
                {"amount": 8.22, "currency": "EUR", "name": "BASE CHARGE"},
                {"amount": 1.16, "currency": "EUR", "name": "FUEL SURCHARGE"},
                {"amount": 1.87, "currency": "EUR", "name": "TVA"},
            ],
            "meta": {"service_name": "ups_standard_eu"},
            "service": "ups_standard_eu",
            "total_charge": 11.25,
            "transit_days": 1,
        },
    ],
    [],
]

ParsedRateResponseWithTotalCharges = [
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 54.4, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 11.83, "currency": "CAD", "name": "FUEL SURCHARGE"},
            ],
            "meta": {"service_name": "ups_express_early_ca"},
            "service": "ups_express_early_ca",
            "total_charge": 66.23,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 25.75, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 5.6, "currency": "CAD", "name": "FUEL SURCHARGE"},
            ],
            "meta": {"service_name": "ups_worldwide_express_ca"},
            "service": "ups_worldwide_express_ca",
            "total_charge": 31.35,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 14.28, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 3.11, "currency": "CAD", "name": "FUEL SURCHARGE"},
            ],
            "meta": {"service_name": "ups_express_saver_intl_ca"},
            "service": "ups_express_saver_intl_ca",
            "total_charge": 17.39,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 12.38, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 2.69, "currency": "CAD", "name": "FUEL SURCHARGE"},
            ],
            "meta": {"service_name": "ups_worldwide_expedited_ca"},
            "service": "ups_worldwide_expedited_ca",
            "total_charge": 15.07,
            "transit_days": 2,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 18.6, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 4.05, "currency": "CAD", "name": "FUEL SURCHARGE"},
            ],
            "meta": {"service_name": "ups_3_day_select_ca_us"},
            "service": "ups_3_day_select_ca_us",
            "total_charge": 22.65,
            "transit_days": 3,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 11.3, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 1.69, "currency": "CAD", "name": "FUEL SURCHARGE"},
                {"amount": 0.55, "currency": "CAD", "name": "434"},
            ],
            "meta": {"service_name": "ups_standard_ca"},
            "service": "ups_standard_ca",
            "total_charge": 13.54,
            "transit_days": 3,
        },
    ],
    [],
]

ParsedRateResponseWithMissingAmount = [
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 54.4, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 26.25, "currency": "CAD", "name": "14"},
                {"amount": 17.74, "currency": "CAD", "name": "FUEL SURCHARGE"},
                {"amount": 26.25, "currency": "CAD", "name": "SATURDAY DELIVERY"},
            ],
            "meta": {"service_name": "ups_express_early_ca"},
            "service": "ups_express_early_ca",
            "total_charge": 98.39,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 25.75, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 26.25, "currency": "CAD", "name": "07"},
                {"amount": 11.44, "currency": "CAD", "name": "FUEL SURCHARGE"},
                {"amount": 26.25, "currency": "CAD", "name": "SATURDAY DELIVERY"},
            ],
            "meta": {"service_name": "ups_worldwide_express_ca"},
            "service": "ups_worldwide_express_ca",
            "total_charge": 63.44,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 54.4, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 11.97, "currency": "CAD", "name": "FUEL SURCHARGE"},
            ],
            "meta": {"service_name": "ups_express_early_ca"},
            "service": "ups_express_early_ca",
            "total_charge": 66.37,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 25.75, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 5.67, "currency": "CAD", "name": "FUEL SURCHARGE"},
            ],
            "meta": {"service_name": "ups_worldwide_express_ca"},
            "service": "ups_worldwide_express_ca",
            "total_charge": 31.42,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 14.28, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 3.14, "currency": "CAD", "name": "FUEL SURCHARGE"},
            ],
            "meta": {"service_name": "ups_express_saver_intl_ca"},
            "service": "ups_express_saver_intl_ca",
            "total_charge": 17.42,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 12.38, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 2.72, "currency": "CAD", "name": "FUEL SURCHARGE"},
            ],
            "meta": {"service_name": "ups_worldwide_expedited_ca"},
            "service": "ups_worldwide_expedited_ca",
            "total_charge": 15.1,
            "transit_days": 1,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 18.6, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 4.09, "currency": "CAD", "name": "FUEL SURCHARGE"},
            ],
            "meta": {"service_name": "ups_3_day_select_ca_us"},
            "service": "ups_3_day_select_ca_us",
            "total_charge": 22.69,
            "transit_days": 2,
        },
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 11.3, "currency": "CAD", "name": "BASE CHARGE"},
                {"amount": 1.69, "currency": "CAD", "name": "FUEL SURCHARGE"},
                {"amount": 0.55, "currency": "CAD", "name": "434"},
            ],
            "meta": {"service_name": "ups_standard_ca"},
            "service": "ups_standard_ca",
            "total_charge": 13.54,
            "transit_days": 3,
        },
    ],
    [],
]


RateRequestData = {
    "RateRequest": {
        "Request": {
            "RequestOption": "Shoptimeintransit",
            "SubVersion": "2409",
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
                    "PackageServiceOptions": {
                        "DeliveryConfirmation": {"DCISType": "1"}
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
            "ShipmentServiceOptions": {"AvailableServicesOption": "3"},
        },
    }
}

RateRequestWithPackagePresetData = {
    "RateRequest": {
        "Request": {
            "RequestOption": "Shoptimeintransit",
            "SubVersion": "2409",
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
        }
      ],
      "TransactionReference": {
        "CustomerContext": "testing",
        "TransactionIdentifier": "ciewssoas5s6fsYNx17dFY"
      }
    },
    "RatedShipment": [
      {
        "Disclaimer": [
          {
            "Code": "01",
            "Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": {
          "Code": "14",
          "Description": ""
        },
        "Zone": "708",
        "RatedShipmentAlert": [
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
          "Weight": "13.6"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "324.27"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "253.65"
        },
        "ItemizedCharges": [
          {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "65.12"
          },
          {
            "Code": "434",
            "CurrencyCode": "CAD",
            "MonetaryValue": "0.70",
            "SubType": "Surge_Fee_Residential"
          },
          {
            "Code": "270",
            "CurrencyCode": "CAD",
            "MonetaryValue": "4.80"
          }
        ],
        "TaxCharges": [
          {
            "Type": "GST",
            "MonetaryValue": "16.55"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "6.65"
        },
        "TotalCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "330.92"
        },
        "TotalChargesWithTaxes": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "347.47"
        },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "251.11"
          },
          "TaxCharges": [
            {
              "Type": "GST",
              "MonetaryValue": "16.38"
            },
            {
              "Type": "GST",
              "MonetaryValue": "16.38"
            }
          ],
          "TotalCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "321.03"
          },
          "TotalChargesWithTaxes": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "344.00"
          }
        },
        "GuaranteedDelivery": {
          "BusinessDaysInTransit": "1",
          "DeliveryByTime": "9:00 A.M."
        },
        "RatedPackage": [
          {
            "ItemizedCharges": [
              {
                "Code": "120",
                "CurrencyCode": "CAD",
                "MonetaryValue": "6.65",
                "SubType": "Signature and Date Required"
              }
            ],
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ItemizedCharges": [
                {
                  "Code": "120",
                  "CurrencyCode": "CAD",
                  "MonetaryValue": "0.00",
                  "SubType": "Signature and Date Required"
                }
              ]
            },
            "Weight": "3.2"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20250526",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": {
              "Description": "UPS Express Early"
            },
            "EstimatedArrival": {
              "Arrival": {
                "Date": "20250527",
                "Time": "103000"
              },
              "BusinessDaysInTransit": "1",
              "Pickup": {
                "Date": "20250526",
                "Time": "180000"
              },
              "DayOfWeek": "TUE",
              "CustomerCenterCutoff": "170000",
              "TotalTransitDays": "1"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": [
          {
            "Code": "01",
            "Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": {
          "Code": "01",
          "Description": ""
        },
        "Zone": "408",
        "RatedShipmentAlert": [
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
          "Weight": "13.6"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "285.30"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "222.35"
        },
        "ItemizedCharges": [
          {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "57.45"
          },
          {
            "Code": "434",
            "CurrencyCode": "CAD",
            "MonetaryValue": "0.70",
            "SubType": "Surge_Fee_Residential"
          },
          {
            "Code": "270",
            "CurrencyCode": "CAD",
            "MonetaryValue": "4.80"
          }
        ],
        "TaxCharges": [
          {
            "Type": "GST",
            "MonetaryValue": "14.60"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "6.65"
        },
        "TotalCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "291.95"
        },
        "TotalChargesWithTaxes": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "306.55"
        },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "220.13"
          },
          "TaxCharges": [
            {
              "Type": "GST",
              "MonetaryValue": "14.45"
            },
            {
              "Type": "GST",
              "MonetaryValue": "14.45"
            }
          ],
          "TotalCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "282.45"
          },
          "TotalChargesWithTaxes": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "303.48"
          }
        },
        "GuaranteedDelivery": {
          "BusinessDaysInTransit": "1",
          "DeliveryByTime": "10:30 A.M."
        },
        "RatedPackage": [
          {
            "ItemizedCharges": [
              {
                "Code": "120",
                "CurrencyCode": "CAD",
                "MonetaryValue": "6.65",
                "SubType": "Signature and Date Required"
              }
            ],
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ItemizedCharges": [
                {
                  "Code": "120",
                  "CurrencyCode": "CAD",
                  "MonetaryValue": "0.00",
                  "SubType": "Signature and Date Required"
                }
              ]
            },
            "Weight": "3.2"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20250526",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": {
              "Description": "UPS Express"
            },
            "EstimatedArrival": {
              "Arrival": {
                "Date": "20250527",
                "Time": "120000"
              },
              "BusinessDaysInTransit": "1",
              "Pickup": {
                "Date": "20250526",
                "Time": "180000"
              },
              "DayOfWeek": "TUE",
              "CustomerCenterCutoff": "170000",
              "TotalTransitDays": "1"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": [
          {
            "Code": "01",
            "Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": {
          "Code": "13",
          "Description": ""
        },
        "Zone": "508",
        "RatedShipmentAlert": [
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
          "Weight": "13.6"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "254.12"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "197.30"
        },
        "ItemizedCharges": [
          {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "51.32"
          },
          {
            "Code": "434",
            "CurrencyCode": "CAD",
            "MonetaryValue": "0.70",
            "SubType": "Surge_Fee_Residential"
          },
          {
            "Code": "270",
            "CurrencyCode": "CAD",
            "MonetaryValue": "4.80"
          }
        ],
        "TaxCharges": [
          {
            "Type": "GST",
            "MonetaryValue": "13.04"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "6.65"
        },
        "TotalCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "260.77"
        },
        "TotalChargesWithTaxes": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "273.81"
        },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "195.33"
          },
          "TaxCharges": [
            {
              "Type": "GST",
              "MonetaryValue": "12.91"
            },
            {
              "Type": "GST",
              "MonetaryValue": "12.91"
            }
          ],
          "TotalCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "251.58"
          },
          "TotalChargesWithTaxes": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "271.07"
          }
        },
        "GuaranteedDelivery": {
          "BusinessDaysInTransit": "1"
        },
        "RatedPackage": [
          {
            "ItemizedCharges": [
              {
                "Code": "120",
                "CurrencyCode": "CAD",
                "MonetaryValue": "6.65",
                "SubType": "Signature and Date Required"
              }
            ],
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ItemizedCharges": [
                {
                  "Code": "120",
                  "CurrencyCode": "CAD",
                  "MonetaryValue": "0.00",
                  "SubType": "Signature and Date Required"
                }
              ]
            },
            "Weight": "3.2"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20250526",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": {
              "Description": "UPS Express Saver"
            },
            "EstimatedArrival": {
              "Arrival": {
                "Date": "20250527",
                "Time": "233000"
              },
              "BusinessDaysInTransit": "1",
              "Pickup": {
                "Date": "20250526",
                "Time": "180000"
              },
              "DayOfWeek": "TUE",
              "CustomerCenterCutoff": "170000",
              "TotalTransitDays": "1"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": [
          {
            "Code": "01",
            "Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": {
          "Code": "02",
          "Description": ""
        },
        "Zone": "308",
        "RatedShipmentAlert": [
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
          "Weight": "13.6"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "240.98"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "186.75"
        },
        "ItemizedCharges": [
          {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "48.73"
          },
          {
            "Code": "434",
            "CurrencyCode": "CAD",
            "MonetaryValue": "0.70",
            "SubType": "Surge_Fee_Residential"
          },
          {
            "Code": "270",
            "CurrencyCode": "CAD",
            "MonetaryValue": "4.80"
          }
        ],
        "TaxCharges": [
          {
            "Type": "GST",
            "MonetaryValue": "12.38"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "6.65"
        },
        "TotalCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "247.63"
        },
        "TotalChargesWithTaxes": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "260.01"
        },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "184.88"
          },
          "TaxCharges": [
            {
              "Type": "GST",
              "MonetaryValue": "12.26"
            },
            {
              "Type": "GST",
              "MonetaryValue": "12.26"
            }
          ],
          "TotalCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "238.57"
          },
          "TotalChargesWithTaxes": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "257.41"
          }
        },
        "RatedPackage": [
          {
            "ItemizedCharges": [
              {
                "Code": "120",
                "CurrencyCode": "CAD",
                "MonetaryValue": "6.65",
                "SubType": "Signature and Date Required"
              }
            ],
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ItemizedCharges": [
                {
                  "Code": "120",
                  "CurrencyCode": "CAD",
                  "MonetaryValue": "0.00",
                  "SubType": "Signature and Date Required"
                }
              ]
            },
            "Weight": "3.2"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20250526",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": {
              "Description": "UPS Expedited"
            },
            "EstimatedArrival": {
              "Arrival": {
                "Date": "20250528",
                "Time": "233000"
              },
              "BusinessDaysInTransit": "2",
              "Pickup": {
                "Date": "20250526",
                "Time": "180000"
              },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "170000",
              "TotalTransitDays": "2"
            },
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": [
          {
            "Code": "01",
            "Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": {
          "Code": "11",
          "Description": ""
        },
        "Zone": "208",
        "RatedShipmentAlert": [
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
          "Weight": "11.3"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "121.14"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "93.90"
        },
        "ItemizedCharges": [
          {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "21.74"
          },
          {
            "Code": "434",
            "CurrencyCode": "CAD",
            "MonetaryValue": "0.70",
            "SubType": "Surge_Fee_Residential"
          },
          {
            "Code": "270",
            "CurrencyCode": "CAD",
            "MonetaryValue": "4.80"
          }
        ],
        "TaxCharges": [
          {
            "Type": "GST",
            "MonetaryValue": "6.39"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "6.65"
        },
        "TotalCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "127.79"
        },
        "TotalChargesWithTaxes": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "134.18"
        },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "92.96"
          },
          "TaxCharges": [
            {
              "Type": "GST",
              "MonetaryValue": "6.33"
            },
            {
              "Type": "GST",
              "MonetaryValue": "6.33"
            }
          ],
          "TotalCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "119.93"
          },
          "TotalChargesWithTaxes": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "132.84"
          }
        },
        "RatedPackage": [
          {
            "ItemizedCharges": [
              {
                "Code": "120",
                "CurrencyCode": "CAD",
                "MonetaryValue": "6.65",
                "SubType": "Signature and Date Required"
              }
            ],
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ItemizedCharges": [
                {
                  "Code": "120",
                  "CurrencyCode": "CAD",
                  "MonetaryValue": "0.00",
                  "SubType": "Signature and Date Required"
                }
              ]
            },
            "Weight": "3.2"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20250526",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": {
              "Description": "UPS Standard"
            },
            "EstimatedArrival": {
              "Arrival": {
                "Date": "20250604",
                "Time": "233000"
              },
              "BusinessDaysInTransit": "6",
              "Pickup": {
                "Date": "20250527",
                "Time": "180000"
              },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "170000",
              "RestDays": "2",
              "TotalTransitDays": "8"
            },
            "SaturdayDelivery": "0",
            "SundayDelivery": "0"
          }
        }
      }
    ]
  }
}
"""

FRRateResponseJSON = """{
  "RateResponse": {
    "Response": {
      "ResponseStatus": { "Code": "1", "Description": "Success" },
      "Alert": {
        "Code": "110971",
        "Description": "Your invoice may vary from the displayed reference rates"
      },
      "TransactionReference": {
        "CustomerContext": "x-trans-src",
        "TransactionIdentifier": "wssoa2t278w6TLJX3HT1t0"
      }
    },
    "RatedShipment": [
      {
        "Disclaimer": {
          "Code": "01",
          "Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": { "Code": "07", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "KGS", "Description": "Kilograms" },
          "Weight": "3.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "EUR",
          "MonetaryValue": "68.05"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "EUR",
          "MonetaryValue": "52.55"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "EUR",
          "MonetaryValue": "15.50"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "EUR",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "EUR", "MonetaryValue": "68.05" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "EUR",
            "MonetaryValue": "12.37"
          },
          "ItemizedCharges": {
            "Code": "375",
            "CurrencyCode": "EUR",
            "MonetaryValue": "2.74"
          },
          "TaxCharges": { "Type": "TVA", "MonetaryValue": "3.02" },
          "TotalCharge": { "CurrencyCode": "EUR", "MonetaryValue": "15.11" },
          "TotalChargesWithTaxes": {
            "CurrencyCode": "EUR",
            "MonetaryValue": "18.13"
          }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "EUR",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "EUR",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "EUR",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "EUR", "MonetaryValue": "0.00" }
          },
          "Weight": "3.0"
        },
        "TimeInTransit": {
          "PickupDate": "20240827",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS Express" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20240828", "Time": "120000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20240827", "Time": "180000" },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "160000",
              "TotalTransitDays": "1"
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
        "Service": { "Code": "65", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "KGS", "Description": "Kilograms" },
          "Weight": "3.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "EUR",
          "MonetaryValue": "58.21"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "EUR",
          "MonetaryValue": "44.95"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "EUR",
          "MonetaryValue": "13.26"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "EUR",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "EUR", "MonetaryValue": "58.21" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "EUR",
            "MonetaryValue": "10.21"
          },
          "ItemizedCharges": {
            "Code": "375",
            "CurrencyCode": "EUR",
            "MonetaryValue": "2.26"
          },
          "TaxCharges": { "Type": "TVA", "MonetaryValue": "2.49" },
          "TotalCharge": { "CurrencyCode": "EUR", "MonetaryValue": "12.47" },
          "TotalChargesWithTaxes": {
            "CurrencyCode": "EUR",
            "MonetaryValue": "14.96"
          }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "EUR",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "EUR",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "EUR",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "EUR", "MonetaryValue": "0.00" }
          },
          "Weight": "3.0"
        },
        "TimeInTransit": {
          "PickupDate": "20240827",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS Express Saver" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20240828", "Time": "233000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20240827", "Time": "180000" },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "160000",
              "TotalTransitDays": "1"
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
        "Service": { "Code": "11", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "KGS", "Description": "Kilograms" },
          "Weight": "3.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "EUR",
          "MonetaryValue": "36.40"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "EUR",
          "MonetaryValue": "30.65"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "EUR",
          "MonetaryValue": "5.75"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "EUR",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "EUR", "MonetaryValue": "36.40" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "EUR",
            "MonetaryValue": "8.22"
          },
          "ItemizedCharges": {
            "Code": "375",
            "CurrencyCode": "EUR",
            "MonetaryValue": "1.16"
          },
          "TaxCharges": { "Type": "TVA", "MonetaryValue": "1.87" },
          "TotalCharge": { "CurrencyCode": "EUR", "MonetaryValue": "9.38" },
          "TotalChargesWithTaxes": {
            "CurrencyCode": "EUR",
            "MonetaryValue": "11.25"
          }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "EUR",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "EUR",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "EUR",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "EUR", "MonetaryValue": "0.00" }
          },
          "Weight": "3.0"
        },
        "TimeInTransit": {
          "PickupDate": "20240827",
          "PackageBillType": "03",
          "AutoDutyCode": "02",
          "Disclaimer": "Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS Standard" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20240828", "Time": "233000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20240827", "Time": "180000" },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "160000",
              "TotalTransitDays": "1"
            },
            "SaturdayDelivery": "0"
          }
        }
      }
    ]
  }
}
"""

RateResponseWithTotalChargesJSON = """{
  "RateResponse": {
    "Response": {
      "ResponseStatus": { "Code": "1", "Description": "Success" },
      "Alert": [
        {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        {
          "Code": "110920",
          "Description": "Ship To Address Classification is changed from Residential to Commercial"
        }
      ],
      "TransactionReference": {
        "CustomerContext": "x-trans-src",
        "TransactionIdentifier": "xwssoat18b18k7YtWDNp5m"
      }
    },
    "RatedShipment": [
      {
        "Disclaimer": [
          {
            "Code": "02",
            "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": { "Code": "14", "Description": "" },
        "RatedShipmentAlert": [
          {
            "Code": "110971",
            "Description": "Your invoice may vary from the displayed reference rates"
          },
          {
            "Code": "110920",
            "Description": "Ship To Address Classification is changed from Residential to Commercial"
          }
        ],
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "275.95"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "226.65"
        },
        "ItemizedCharges": [
          {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "49.30"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "275.95" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "54.40"
          },
          "ItemizedCharges": [
            {
              "Code": "375",
              "CurrencyCode": "CAD",
              "MonetaryValue": "11.83"
            }
          ],
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "66.23" }
        },
        "RatedPackage": [
          {
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              }
            },
            "Weight": "1.5"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20241001",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": [
            "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance."
          ],
          "ServiceSummary": {
            "Service": { "Description": "UPS Express Early" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241002", "Time": "083000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20241001", "Time": "163000" },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "153000",
              "TotalTransitDays": "1"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": [
          {
            "Code": "02",
            "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": { "Code": "07", "Description": "" },
        "RatedShipmentAlert": [
          {
            "Code": "110971",
            "Description": "Your invoice may vary from the displayed reference rates"
          },
          {
            "Code": "110920",
            "Description": "Ship To Address Classification is changed from Residential to Commercial"
          }
        ],
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "130.64"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "107.30"
        },
        "ItemizedCharges": [
          {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "23.34"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "130.64" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "25.75"
          },
          "ItemizedCharges": [
            {
              "Code": "375",
              "CurrencyCode": "CAD",
              "MonetaryValue": "5.60"
            }
          ],
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "31.35" }
        },
        "RatedPackage": [
          {
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              }
            },
            "Weight": "1.5"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20241001",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": [
            "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance."
          ],
          "ServiceSummary": {
            "Service": { "Description": "UPS Worldwide Express" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241002", "Time": "120000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20241001", "Time": "163000" },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "153000",
              "TotalTransitDays": "1"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": [
          {
            "Code": "02",
            "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": { "Code": "65", "Description": "" },
        "RatedShipmentAlert": [
          {
            "Code": "110971",
            "Description": "Your invoice may vary from the displayed reference rates"
          },
          {
            "Code": "110920",
            "Description": "Ship To Address Classification is changed from Residential to Commercial"
          }
        ],
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "124.19"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "102.00"
        },
        "ItemizedCharges": [
          {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "22.19"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "124.19" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "14.28"
          },
          "ItemizedCharges": [
            {
              "Code": "375",
              "CurrencyCode": "CAD",
              "MonetaryValue": "3.11"
            }
          ],
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "17.39" }
        },
        "RatedPackage": [
          {
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              }
            },
            "Weight": "1.5"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20241001",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": [
            "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance."
          ],
          "ServiceSummary": {
            "Service": { "Description": "UPS Express Saver" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241002", "Time": "233000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20241001", "Time": "163000" },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "153000",
              "TotalTransitDays": "1"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": [
          {
            "Code": "02",
            "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": { "Code": "08", "Description": "" },
        "RatedShipmentAlert": [
          {
            "Code": "110971",
            "Description": "Your invoice may vary from the displayed reference rates"
          },
          {
            "Code": "110920",
            "Description": "Ship To Address Classification is changed from Residential to Commercial"
          }
        ],
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "107.63"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "88.40"
        },
        "ItemizedCharges": [
          {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "19.23"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "107.63" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "12.38"
          },
          "ItemizedCharges": [
            {
              "Code": "375",
              "CurrencyCode": "CAD",
              "MonetaryValue": "2.69"
            }
          ],
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "15.07" }
        },
        "RatedPackage": [
          {
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              }
            },
            "Weight": "1.5"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20241001",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": [
            "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance."
          ],
          "ServiceSummary": {
            "Service": { "Description": "UPS Worldwide Expedited" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241003", "Time": "233000" },
              "BusinessDaysInTransit": "2",
              "Pickup": { "Date": "20241001", "Time": "163000" },
              "DayOfWeek": "THU",
              "CustomerCenterCutoff": "153000",
              "TotalTransitDays": "2"
            },
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": [
          {
            "Code": "02",
            "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": { "Code": "12", "Description": "" },
        "RatedShipmentAlert": [
          {
            "Code": "110971",
            "Description": "Your invoice may vary from the displayed reference rates"
          },
          {
            "Code": "110920",
            "Description": "Ship To Address Classification is changed from Residential to Commercial"
          }
        ],
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "94.36"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "77.50"
        },
        "ItemizedCharges": [
          {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "16.86"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "94.36" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "18.60"
          },
          "ItemizedCharges": [
            {
              "Code": "375",
              "CurrencyCode": "CAD",
              "MonetaryValue": "4.05"
            }
          ],
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "22.65" }
        },
        "RatedPackage": [
          {
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              }
            },
            "Weight": "1.5"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20241001",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": [
            "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance."
          ],
          "ServiceSummary": {
            "Service": { "Description": "UPS 3 Day Select" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241004", "Time": "233000" },
              "BusinessDaysInTransit": "3",
              "Pickup": { "Date": "20241001", "Time": "163000" },
              "DayOfWeek": "FRI",
              "CustomerCenterCutoff": "153000",
              "TotalTransitDays": "3"
            },
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": [
          {
            "Code": "02",
            "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
          }
        ],
        "Service": { "Code": "11", "Description": "" },
        "RatedShipmentAlert": [
          {
            "Code": "110971",
            "Description": "Your invoice may vary from the displayed reference rates"
          },
          {
            "Code": "110920",
            "Description": "Ship To Address Classification is changed from Residential to Commercial"
          }
        ],
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "40.96"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "35.30"
        },
        "ItemizedCharges": [
          { "Code": "375", "CurrencyCode": "CAD", "MonetaryValue": "5.11" },
          {
            "Code": "434",
            "CurrencyCode": "CAD",
            "MonetaryValue": "0.55",
            "SubType": "Surge_Fee_Commercial"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "40.96" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "11.30"
          },
          "ItemizedCharges": [
            { "Code": "375", "CurrencyCode": "CAD", "MonetaryValue": "1.69" },
            {
              "Code": "434",
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.55",
              "SubType": "Surge_Fee_Commercial"
            }
          ],
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "13.54" }
        },
        "RatedPackage": [
          {
            "NegotiatedCharges": {
              "BaseServiceCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TransportationCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "ServiceOptionsCharges": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              },
              "TotalCharge": {
                "CurrencyCode": "CAD",
                "MonetaryValue": "0.00"
              }
            },
            "Weight": "1.5"
          }
        ],
        "TimeInTransit": {
          "PickupDate": "20241001",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": [
            "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance."
          ],
          "ServiceSummary": {
            "Service": { "Description": "UPS Standard" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241004", "Time": "233000" },
              "BusinessDaysInTransit": "3",
              "Pickup": { "Date": "20241001", "Time": "163000" },
              "DayOfWeek": "FRI",
              "CustomerCenterCutoff": "153000",
              "TotalTransitDays": "3"
            },
            "SaturdayDelivery": "0",
            "SundayDelivery": "0"
          }
        }
      }
    ]
  }
}
"""

RateResponseWithMissingAmountJSON = """{
  "RateResponse": {
    "Response": {
      "ResponseStatus": { "Code": "1", "Description": "Success" },
      "Alert": {
        "Code": "110971",
        "Description": "Your invoice may vary from the displayed reference rates"
      },
      "TransactionReference": {
        "CustomerContext": "x-trans-src",
        "TransactionIdentifier": "wssoa3t47bc4xJyzfqptwQ"
      }
    },
    "RatedShipment": [
      {
        "Disclaimer": {
          "Code": "02",
          "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": { "Code": "14", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "282.29"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "226.65"
        },
        "ItemizedCharges": [
          { "Code": "375", "CurrencyCode": "CAD", "MonetaryValue": "55.64" },
          { "Code": "300", "CurrencyCode": "CAD", "MonetaryValue": "26.25" }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "26.25"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "308.54" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "54.40"
          },
          "ItemizedCharges": [
            { "Code": "375", "CurrencyCode": "CAD", "MonetaryValue": "17.74" },
            { "Code": "300", "CurrencyCode": "CAD", "MonetaryValue": "26.25" }
          ],
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "98.39" }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "0.00" }
          },
          "Weight": "2.0"
        },
        "TimeInTransit": {
          "PickupDate": "20241011",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS Worldwide Express Plus" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241012", "Time": "093000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20241011", "Time": "163000" },
              "DayOfWeek": "SAT",
              "CustomerCenterCutoff": "153000",
              "HolidayCount": "1",
              "RestDays": "2",
              "TotalTransitDays": "3"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "1",
            "SaturdayDeliveryDisclaimer": "Saturday Delivery is available for an additional charge."
          }
        }
      },
      {
        "Disclaimer": {
          "Code": "02",
          "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": { "Code": "07", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "136.68"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "107.30"
        },
        "ItemizedCharges": [
          { "Code": "375", "CurrencyCode": "CAD", "MonetaryValue": "29.38" },
          { "Code": "300", "CurrencyCode": "CAD", "MonetaryValue": "26.25" }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "26.25"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "162.93" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "25.75"
          },
          "ItemizedCharges": [
            { "Code": "375", "CurrencyCode": "CAD", "MonetaryValue": "11.44" },
            { "Code": "300", "CurrencyCode": "CAD", "MonetaryValue": "26.25" }
          ],
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "63.44" }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "0.00" }
          },
          "Weight": "2.0"
        },
        "TimeInTransit": {
          "PickupDate": "20241011",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS Worldwide Express" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241012", "Time": "120000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20241011", "Time": "163000" },
              "DayOfWeek": "SAT",
              "CustomerCenterCutoff": "153000",
              "HolidayCount": "1",
              "RestDays": "2",
              "TotalTransitDays": "3"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "1",
            "SaturdayDeliveryDisclaimer": "Saturday Delivery is available for an additional charge."
          }
        }
      },
      {
        "Disclaimer": {
          "Code": "02",
          "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": { "Code": "14", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "276.51"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "226.65"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "CAD",
          "MonetaryValue": "49.86"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "276.51" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "54.40"
          },
          "ItemizedCharges": {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "11.97"
          },
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "66.37" }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "0.00" }
          },
          "Weight": "2.0"
        },
        "TimeInTransit": {
          "PickupDate": "20241011",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS Express Early" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241014", "Time": "083000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20241011", "Time": "163000" },
              "DayOfWeek": "MON",
              "CustomerCenterCutoff": "153000",
              "HolidayCount": "1",
              "RestDays": "2",
              "TotalTransitDays": "3"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0",
            "SundayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": {
          "Code": "02",
          "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": { "Code": "07", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "130.91"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "107.30"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "CAD",
          "MonetaryValue": "23.61"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "130.91" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "25.75"
          },
          "ItemizedCharges": {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "5.67"
          },
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "31.42" }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "0.00" }
          },
          "Weight": "2.0"
        },
        "TimeInTransit": {
          "PickupDate": "20241011",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS Worldwide Express" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241014", "Time": "103000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20241011", "Time": "163000" },
              "DayOfWeek": "MON",
              "CustomerCenterCutoff": "153000",
              "HolidayCount": "1",
              "RestDays": "2",
              "TotalTransitDays": "3"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0",
            "SundayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": {
          "Code": "02",
          "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": { "Code": "65", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "124.44"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "102.00"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "CAD",
          "MonetaryValue": "22.44"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "124.44" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "14.28"
          },
          "ItemizedCharges": {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "3.14"
          },
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "17.42" }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "0.00" }
          },
          "Weight": "2.0"
        },
        "TimeInTransit": {
          "PickupDate": "20241011",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS Express Saver" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241014", "Time": "233000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20241011", "Time": "163000" },
              "DayOfWeek": "MON",
              "CustomerCenterCutoff": "153000",
              "HolidayCount": "1",
              "RestDays": "2",
              "TotalTransitDays": "3"
            },
            "GuaranteedIndicator": "",
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": {
          "Code": "02",
          "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": { "Code": "08", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "107.85"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "88.40"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "CAD",
          "MonetaryValue": "19.45"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "107.85" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "12.38"
          },
          "ItemizedCharges": {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "2.72"
          },
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "15.10" }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "0.00" }
          },
          "Weight": "2.0"
        },
        "TimeInTransit": {
          "PickupDate": "20241011",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS Worldwide Expedited" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241015", "Time": "233000" },
              "BusinessDaysInTransit": "1",
              "Pickup": { "Date": "20241011", "Time": "163000" },
              "DayOfWeek": "TUE",
              "CustomerCenterCutoff": "153000",
              "HolidayCount": "1",
              "RestDays": "2",
              "TotalTransitDays": "4"
            },
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": {
          "Code": "02",
          "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": { "Code": "12", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "94.55"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "77.50"
        },
        "ItemizedCharges": {
          "Code": "375",
          "CurrencyCode": "CAD",
          "MonetaryValue": "17.05"
        },
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "94.55" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "18.60"
          },
          "ItemizedCharges": {
            "Code": "375",
            "CurrencyCode": "CAD",
            "MonetaryValue": "4.09"
          },
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "22.69" }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "0.00" }
          },
          "Weight": "2.0"
        },
        "TimeInTransit": {
          "PickupDate": "20241011",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS 3 Day Select" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241016", "Time": "233000" },
              "BusinessDaysInTransit": "2",
              "Pickup": { "Date": "20241011", "Time": "163000" },
              "DayOfWeek": "WED",
              "CustomerCenterCutoff": "153000",
              "HolidayCount": "1",
              "RestDays": "2",
              "TotalTransitDays": "5"
            },
            "SaturdayDelivery": "0"
          }
        }
      },
      {
        "Disclaimer": {
          "Code": "02",
          "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
        },
        "Service": { "Code": "11", "Description": "" },
        "RatedShipmentAlert": {
          "Code": "110971",
          "Description": "Your invoice may vary from the displayed reference rates"
        },
        "RatingMethod": "01",
        "BillableWeightCalculationMethod": "02",
        "BillingWeight": {
          "UnitOfMeasurement": { "Code": "LBS", "Description": "Pounds" },
          "Weight": "2.0"
        },
        "TransportationCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "40.96"
        },
        "BaseServiceCharge": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "35.30"
        },
        "ItemizedCharges": [
          { "Code": "375", "CurrencyCode": "CAD", "MonetaryValue": "5.11" },
          {
            "Code": "434",
            "CurrencyCode": "CAD",
            "MonetaryValue": "0.55",
            "SubType": "Surge_Fee_Commercial"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "CAD",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": { "CurrencyCode": "CAD", "MonetaryValue": "40.96" },
        "NegotiatedRateCharges": {
          "BaseServiceCharge": {
            "CurrencyCode": "CAD",
            "MonetaryValue": "11.30"
          },
          "ItemizedCharges": [
            { "Code": "375", "CurrencyCode": "CAD", "MonetaryValue": "1.69" },
            {
              "Code": "434",
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.55",
              "SubType": "Surge_Fee_Commercial"
            }
          ],
          "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "13.54" }
        },
        "RatedPackage": {
          "NegotiatedCharges": {
            "BaseServiceCharge": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TransportationCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "ServiceOptionsCharges": {
              "CurrencyCode": "CAD",
              "MonetaryValue": "0.00"
            },
            "TotalCharge": { "CurrencyCode": "CAD", "MonetaryValue": "0.00" }
          },
          "Weight": "2.0"
        },
        "TimeInTransit": {
          "PickupDate": "20241011",
          "PackageBillType": "03",
          "AutoDutyCode": "09",
          "Disclaimer": "All services are guaranteed if shipment is paid for in full by a payee in Canada or the United States. Services listed as guaranteed are backed by a money-back guarantee for transportation charges only. See Terms and Conditions in the Service Guide for details. Certain commodities and high value shipments may require additional transit time for customs clearance.",
          "ServiceSummary": {
            "Service": { "Description": "UPS Standard" },
            "EstimatedArrival": {
              "Arrival": { "Date": "20241017", "Time": "233000" },
              "BusinessDaysInTransit": "3",
              "Pickup": { "Date": "20241011", "Time": "163000" },
              "DayOfWeek": "THU",
              "CustomerCenterCutoff": "153000",
              "HolidayCount": "1",
              "RestDays": "2",
              "TotalTransitDays": "6"
            },
            "SaturdayDelivery": "0"
          }
        }
      }
    ]
  }
}
"""
