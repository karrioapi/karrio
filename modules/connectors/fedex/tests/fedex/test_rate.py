import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestFedExRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rate/v1/rates/quotes",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_intl_rate_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = IntlRateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), IntlParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA", "state_code": "QC"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "parcels": [
        {
            "id": "1",
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 4.0,
            "items": [
                {"weight": "10", "title": "test", "hs_code": "00339BB"},
            ],
        },
    ],
    "options": {
        "currency": "USD",
        "fedex_one_rate": True,
        "shipment_date": "2024-02-15",
        "fedex_smart_post_hub_id": "1000",
        "fedex_smart_post_allowed_indicia": "PARCEL_SELECT",
    },
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 39.98, "currency": "CAD", "name": "Base Charge"},
                {"amount": 0.0, "currency": "CAD", "name": "Discounts"},
                {"amount": 6.88, "currency": "CAD", "name": "HST"},
                {"amount": 5.9, "currency": "CAD", "name": "Fuel Surcharge"},
            ],
            "meta": {"service_name": "fedex_express_saver"},
            "service": "fedex_express_saver",
            "total_charge": 52.76,
        }
    ],
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "code": "SHIPMENT.CHARGES.NOTE",
            "details": {},
            "message": "Shipment level charges have been added to first package.",
        }
    ],
]

IntlParsedRateResponse = [
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "currency": "USD",
            "extra_charges": [
                {"amount": 887.88, "currency": "USD", "name": "Base Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Discounts"},
                {"amount": 45.44, "currency": "USD", "name": "Fuel Surcharge"},
                {"amount": 14.7, "currency": "USD", "name": "Demand Surcharge"},
                {
                    "amount": 6.15,
                    "currency": "USD",
                    "name": "Residential delivery surcharge",
                },
            ],
            "meta": {"service_name": "fedex_international_economy"},
            "service": "fedex_international_economy",
            "total_charge": 954.17,
        },
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "currency": "USD",
            "extra_charges": [
                {"amount": 1253.91, "currency": "USD", "name": "Base Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Discounts"},
                {"amount": 63.74, "currency": "USD", "name": "Fuel Surcharge"},
                {"amount": 14.7, "currency": "USD", "name": "Demand Surcharge"},
                {
                    "amount": 6.15,
                    "currency": "USD",
                    "name": "Residential delivery surcharge",
                },
            ],
            "meta": {"service_name": "fedex_international_first"},
            "service": "fedex_international_first",
            "total_charge": 1338.5,
        },
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "currency": "USD",
            "estimated_delivery": "2024-07-25",
            "extra_charges": [
                {"amount": 344.1, "currency": "USD", "name": "Base Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Discounts"},
                {"amount": 27.24, "currency": "USD", "name": "Fuel Surcharge"},
                {
                    "amount": 19.68,
                    "currency": "USD",
                    "name": "Residential delivery surcharge",
                },
            ],
            "meta": {"service_name": "fedex_ground", "transit_time": "FOUR_DAYS"},
            "service": "fedex_ground",
            "total_charge": 408.45,
            "transit_days": 115,
        },
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "currency": "USD",
            "extra_charges": [
                {"amount": 1195.11, "currency": "USD", "name": "Base Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Discounts"},
                {"amount": 60.8, "currency": "USD", "name": "Fuel Surcharge"},
                {
                    "amount": 6.15,
                    "currency": "USD",
                    "name": "Residential delivery surcharge",
                },
                {"amount": 14.7, "currency": "USD", "name": "Demand Surcharge"},
            ],
            "meta": {"service_name": "fedex_international_priority_express"},
            "service": "fedex_international_priority_express",
            "total_charge": 1276.76,
        },
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "currency": "USD",
            "extra_charges": [
                {"amount": 887.88, "currency": "USD", "name": "Base Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Discounts"},
                {"amount": 44.39, "currency": "USD", "name": "Fuel Surcharge"},
                {
                    "amount": 0.0,
                    "currency": "USD",
                    "name": "Residential delivery surcharge",
                },
            ],
            "meta": {"service_name": "fedex_international_connect_plus"},
            "service": "fedex_international_connect_plus",
            "total_charge": 932.27,
        },
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "currency": "USD",
            "extra_charges": [
                {"amount": 1139.25, "currency": "USD", "name": "Base Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Discounts"},
                {"amount": 84.11, "currency": "USD", "name": "Fuel Surcharge"},
                {"amount": 546.1, "currency": "USD", "name": "Demand Surcharge"},
                {
                    "amount": 6.15,
                    "currency": "USD",
                    "name": "Residential delivery surcharge",
                },
            ],
            "meta": {"service_name": "fedex_international_priority"},
            "service": "fedex_international_priority",
            "total_charge": 1775.61,
        },
    ],
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "code": "MONEYBACKGUARANTEE.NOT.ELIGIBLE",
            "details": {},
            "message": "We are unable to process this request. Please try again later or contact FedEx Customer Service.",
        },
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "code": "SHIPMENT.CHARGES.NOTE",
            "details": {},
            "message": "Shipment level charges have been added to first package.",
        },
    ],
]


RateRequest = {
    "accountNumber": {"value": "2349857"},
    "rateRequestControlParameters": {
        "rateSortOrder": "COMMITASCENDING",
        "returnTransitTimes": True,
        "servicesNeededOnRateFailure": True,
        "variableOptions": "SMART_POST_HUB_ID,SMART_POST_ALLOWED_INDICIA",
    },
    "requestedShipment": {
        "customsClearanceDetail": {
            "commodities": [
                {
                    "name": "test",
                    "description": "test",
                    "harmonizedCode": "00339BB",
                    "numberOfPieces": 1,
                    "quantity": 1,
                    "quantityUnits": "PCS",
                    "weight": {"units": "LB", "value": 10.0},
                    "customsValue": {"amount": 1.0, "currency": "USD"},
                }
            ],
            "dutiesPayment": {
                "paymentType": "SENDER",
                "payor": {"responsibleParty": {"accountNumber": {"value": "2349857"}}},
            },
        },
        "documentShipment": False,
        "packagingType": "YOUR_PACKAGING",
        "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
        "preferredCurrency": "USD",
        "rateRequestType": ["LIST", "ACCOUNT", "PREFERRED"],
        "recipient": {
            "address": {"city": "Lome", "countryCode": "TG", "residential": False}
        },
        "requestedPackageLineItems": [
            {
                "dimensions": {
                    "height": 3.0,
                    "length": 10.0,
                    "units": "IN",
                    "width": 3.0,
                },
                "groupPackageCount": 1,
                "subPackagingType": "OTHER",
                "weight": {"units": "LB", "value": 4.0},
            }
        ],
        "shipDateStamp": "2024-02-15",
        "shipmentSpecialServices": {"specialServiceTypes": ["FEDEX_ONE_RATE"]},
        "shipper": {
            "address": {
                "countryCode": "CA",
                "postalCode": "H3N1S4",
                "residential": False,
                "stateOrProvinceCode": "PQ",
            }
        },
        "smartPostInfoDetail": {"hubId": "1000", "indicia": "PARCEL_SELECT"},
        "totalWeight": 4.0,
    },
}

RateResponse = """{
  "transactionId": "4cbf8c73-61eb-4538-a65a-4830fef5d265",
  "output": {
    "alerts": [
      {
        "code": "SHIPMENT.CHARGES.NOTE",
        "message": "Shipment level charges have been added to first package.",
        "alertType": "NOTE",
        "parameterList": []
      }
    ],
    "rateReplyDetails": [
      {
        "serviceType": "FEDEX_EXPRESS_SAVER",
        "serviceName": "FedEx Economy",
        "packagingType": "YOUR_PACKAGING",
        "commit": {
          "label": "Delivery date unavailable",
          "commitMessageDetails": "Delivery date and time estimates are not available for this shipment.",
          "derivedOriginDetail": {
            "countryCode": "CA",
            "stateOrProvinceCode": "NB",
            "postalCode": "E1C4Z8",
            "serviceArea": "A2",
            "locationId": "YMOA ",
            "locationNumber": 0
          },
          "derivedDestinationDetail": {
            "countryCode": "CA",
            "stateOrProvinceCode": "NB",
            "postalCode": "E1C4Z8",
            "serviceArea": "A2",
            "locationId": "YMOA ",
            "locationNumber": 0,
            "airportId": "YQM"
          },
          "saturdayDelivery": false
        },
        "customerMessages": [
          { "code": "SC04", "message": "SC04" },
          { "code": "E", "message": "E" },
          { "code": "Commit505", "message": "Commit505" }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 29.2,
            "totalNetCharge": 38.54,
            "totalNetFedExCharge": 33.51,
            "shipmentRateDetail": {
              "rateZone": "2",
              "dimDivisor": 139,
              "fuelSurchargePercent": 14.75,
              "totalSurcharges": 4.31,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 4.31
                }
              ],
              "taxes": [
                { "type": "HST", "description": "Canada HST", "amount": 5.03 }
              ],
              "pricingCode": "",
              "totalBillingWeight": { "units": "KG", "value": 3.4 },
              "dimDivisorType": "COUNTRY",
              "currency": "USD",
              "rateScale": "CA0001F2_20_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 8 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_SHIPMENT",
                  "ratedWeightMethod": "ACTUAL",
                  "baseCharge": 29.2,
                  "netFreight": 29.2,
                  "totalSurcharges": 4.31,
                  "netFedExCharge": 33.51,
                  "totalTaxes": 5.03,
                  "netCharge": 38.54,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 3.4 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 4.31
                    }
                  ],
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          },
          {
            "rateType": "PREFERRED_CURRENCY",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 39.98,
            "totalNetCharge": 52.76,
            "totalNetFedExCharge": 45.88,
            "shipmentRateDetail": {
              "rateZone": "2",
              "dimDivisor": 139,
              "fuelSurchargePercent": 14.75,
              "totalSurcharges": 5.9,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 5.9
                }
              ],
              "taxes": [
                { "type": "HST", "description": "Canada HST", "amount": 6.88 }
              ],
              "pricingCode": "",
              "totalBillingWeight": { "units": "KG", "value": 3.4 },
              "dimDivisorType": "COUNTRY",
              "currency": "CAD",
              "rateScale": "CA0001F2_20_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 8 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_ACCOUNT_SHIPMENT",
                  "ratedWeightMethod": "ACTUAL",
                  "baseCharge": 39.98,
                  "netFreight": 39.98,
                  "totalSurcharges": 5.9,
                  "netFedExCharge": 45.88,
                  "totalTaxes": 6.88,
                  "netCharge": 52.76,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 3.4 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "amount": 5.9
                    }
                  ],
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "CAD"
          }
        ],
        "operationalDetail": {
          "originLocationIds": ["YMOA "],
          "originLocationNumbers": [0],
          "originServiceAreas": ["A2"],
          "destinationLocationIds": ["YMOA "],
          "destinationLocationNumbers": [0],
          "destinationServiceAreas": ["A2"],
          "destinationLocationStateOrProvinceCodes": ["NB"],
          "ineligibleForMoneyBackGuarantee": false,
          "astraDescription": "XS",
          "originPostalCodes": ["E1C4Z8"],
          "stateOrProvinceCodes": ["NB"],
          "countryCodes": ["CA"],
          "airportId": "YQM",
          "serviceCode": "20",
          "destinationPostalCode": "E1C4Z8"
        },
        "signatureOptionType": "SERVICE_DEFAULT",
        "serviceDescription": {
          "serviceId": "EP1000000013",
          "serviceType": "FEDEX_EXPRESS_SAVER",
          "code": "20",
          "names": [
            { "type": "long", "encoding": "utf-8", "value": "FedEx Economy" },
            { "type": "long", "encoding": "ascii", "value": "FedEx Economy" },
            { "type": "medium", "encoding": "utf-8", "value": "FedEx Economy" },
            { "type": "medium", "encoding": "ascii", "value": "FedEx Economy" },
            { "type": "short", "encoding": "utf-8", "value": "XS" },
            { "type": "short", "encoding": "ascii", "value": "XS" },
            { "type": "abbrv", "encoding": "ascii", "value": "XS" }
          ],
          "serviceCategory": "parcel",
          "description": "FedEx Economy",
          "astraDescription": "XS"
        },
        "deliveryStation": "YMOA "
      }
    ],
    "quoteDate": "2024-07-18",
    "encoded": false
  }
}
"""

IntlRateResponse = """{
  "transactionId": "d497f5d8-4420-43ba-b72f-f1820ffb5904",
  "output": {
    "alerts": [
      {
        "code": "MONEYBACKGUARANTEE.NOT.ELIGIBLE",
        "message": "We are unable to process this request. Please try again later or contact FedEx Customer Service.",
        "alertType": "NOTE"
      },
      {
        "code": "SHIPMENT.CHARGES.NOTE",
        "message": "Shipment level charges have been added to first package.",
        "alertType": "NOTE",
        "parameterList": []
      }
    ],
    "rateReplyDetails": [
      {
        "serviceType": "INTERNATIONAL_ECONOMY",
        "serviceName": "FedEx International Economy®",
        "packagingType": "YOUR_PACKAGING",
        "commit": {
          "label": "Delivery date unavailable",
          "commitMessageDetails": "Delivery date and time estimates are not available for this shipment.",
          "commodityName": "Blue Jean Coat",
          "deliveryMessages": [" 0:00 A.M. IF NO CUSTOMS DELAY"],
          "derivedOriginDetail": {
            "countryCode": "CA",
            "stateOrProvinceCode": "BC",
            "postalCode": "V6M2V9",
            "serviceArea": "A2",
            "locationId": "YVRA ",
            "locationNumber": 0
          },
          "derivedDestinationDetail": {
            "countryCode": "US",
            "stateOrProvinceCode": "NV",
            "postalCode": "89109",
            "serviceArea": "A1",
            "locationId": "FLXA ",
            "locationNumber": 0,
            "airportId": "LAS"
          },
          "saturdayDelivery": false
        },
        "customerMessages": [
          {
            "code": "SERVICE.TYPE.INTERNATIONAL.MESSAGE",
            "message": "Rate does not include duties & taxes, clearance entry fees or other import fees.  The payor of duties/taxes/fees will be responsible for any applicable Clearance Entry Fees."
          },
          {
            "code": "DIM.APPLIED.NOTE",
            "message": "Dimensional Weight of your package(s) was used to calculate your rate."
          },
          { "code": "COMMODITY.NOT.FOUND", "message": "Commodity not found." }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 887.88,
            "totalNetCharge": 954.17,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 954.17,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 954.17,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "US001D",
              "dimDivisor": 139,
              "fuelSurchargePercent": 5,
              "totalSurcharges": 66.29,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 45.44
                },
                {
                  "type": "DEMAND",
                  "description": "Demand Surcharge",
                  "level": "SHIPMENT",
                  "amount": 14.7
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "SHIPMENT",
                  "amount": 6.15
                }
              ],
              "pricingCode": "",
              "currencyExchangeRate": {
                "fromCurrency": "USD",
                "intoCurrency": "USD",
                "rate": 1
              },
              "totalBillingWeight": { "units": "KG", "value": 66.6 },
              "dimDivisorType": "COUNTRY",
              "totalDimWeight": { "units": "KG", "value": 66.6 },
              "currency": "USD",
              "rateScale": "US001DFA_03_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 147 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_SHIPMENT",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 887.88,
                  "netFreight": 887.88,
                  "totalSurcharges": 66.29,
                  "netFedExCharge": 954.17,
                  "totalTaxes": 0,
                  "netCharge": 954.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 66.6 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 45.44
                    },
                    {
                      "type": "DEMAND",
                      "description": "Demand Surcharge",
                      "level": "SHIPMENT",
                      "amount": 14.7
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "SHIPMENT",
                      "amount": 6.15
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 66.6 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          },
          {
            "rateType": "LIST",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 887.88,
            "totalNetCharge": 954.17,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 954.17,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 954.17,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "US001D",
              "dimDivisor": 139,
              "fuelSurchargePercent": 5,
              "totalSurcharges": 66.29,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 45.44
                },
                {
                  "type": "DEMAND",
                  "description": "Demand Surcharge",
                  "level": "SHIPMENT",
                  "amount": 14.7
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "SHIPMENT",
                  "amount": 6.15
                }
              ],
              "pricingCode": "",
              "currencyExchangeRate": {
                "fromCurrency": "USD",
                "intoCurrency": "USD",
                "rate": 1
              },
              "totalBillingWeight": { "units": "KG", "value": 66.6 },
              "dimDivisorType": "COUNTRY",
              "totalDimWeight": { "units": "KG", "value": 66.6 },
              "currency": "USD",
              "rateScale": "US001DFA_03_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 147 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_SHIPMENT",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 887.88,
                  "netFreight": 887.88,
                  "totalSurcharges": 66.29,
                  "netFedExCharge": 954.17,
                  "totalTaxes": 0,
                  "netCharge": 954.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 66.6 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 45.44
                    },
                    {
                      "type": "DEMAND",
                      "description": "Demand Surcharge",
                      "level": "SHIPMENT",
                      "amount": 14.7
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "SHIPMENT",
                      "amount": 6.15
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 66.6 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          }
        ],
        "operationalDetail": {
          "originLocationIds": ["YVRA "],
          "originLocationNumbers": [0],
          "originServiceAreas": ["A2"],
          "destinationLocationIds": ["FLXA "],
          "destinationLocationNumbers": [0],
          "destinationServiceAreas": ["A1"],
          "destinationLocationStateOrProvinceCodes": ["NV"],
          "ineligibleForMoneyBackGuarantee": false,
          "astraDescription": "IE",
          "originPostalCodes": ["V6M2V9"],
          "stateOrProvinceCodes": ["BC"],
          "countryCodes": ["CA"],
          "airportId": "LAS",
          "serviceCode": "03",
          "destinationPostalCode": "89109"
        },
        "signatureOptionType": "NO_SIGNATURE_REQUIRED",
        "serviceDescription": {
          "serviceId": "EP1000000004",
          "serviceType": "INTERNATIONAL_ECONOMY",
          "code": "03",
          "names": [
            {
              "type": "long",
              "encoding": "utf-8",
              "value": "FedEx International Economy®"
            },
            {
              "type": "long",
              "encoding": "ascii",
              "value": "FedEx International Economy"
            },
            {
              "type": "medium",
              "encoding": "utf-8",
              "value": "FedEx International Economy®"
            },
            {
              "type": "medium",
              "encoding": "ascii",
              "value": "FedEx International Economy"
            },
            { "type": "short", "encoding": "utf-8", "value": "IE" },
            { "type": "short", "encoding": "ascii", "value": "IE" },
            { "type": "abbrv", "encoding": "ascii", "value": "IE" }
          ],
          "serviceCategory": "parcel",
          "description": "International Two Day",
          "astraDescription": "IE"
        },
        "deliveryStation": "FLXA "
      },
      {
        "serviceType": "INTERNATIONAL_FIRST",
        "serviceName": "FedEx International First®",
        "packagingType": "YOUR_PACKAGING",
        "commit": {
          "label": "Delivery date unavailable",
          "commitMessageDetails": "Delivery date and time estimates are not available for this shipment.",
          "commodityName": "Blue Jean Coat",
          "deliveryMessages": [" 0:00 A.M. IF NO CUSTOMS DELAY"],
          "derivedOriginDetail": {
            "countryCode": "CA",
            "stateOrProvinceCode": "BC",
            "postalCode": "V6M2V9",
            "serviceArea": "A2",
            "locationId": "YVRA ",
            "locationNumber": 0
          },
          "derivedDestinationDetail": {
            "countryCode": "US",
            "stateOrProvinceCode": "NV",
            "postalCode": "89109",
            "serviceArea": "A1",
            "locationId": "FLXA ",
            "locationNumber": 0,
            "airportId": "LAS"
          },
          "saturdayDelivery": false
        },
        "customerMessages": [
          {
            "code": "SERVICE.TYPE.INTERNATIONAL.MESSAGE",
            "message": "Rate does not include duties & taxes, clearance entry fees or other import fees.  The payor of duties/taxes/fees will be responsible for any applicable Clearance Entry Fees."
          },
          {
            "code": "DIM.APPLIED.NOTE",
            "message": "Dimensional Weight of your package(s) was used to calculate your rate."
          },
          { "code": "COMMODITY.NOT.FOUND", "message": "Commodity not found." }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 1253.91,
            "totalNetCharge": 1338.5,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 1338.5,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 1338.5,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "US001D",
              "dimDivisor": 139,
              "fuelSurchargePercent": 5,
              "totalSurcharges": 84.59,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 63.74
                },
                {
                  "type": "DEMAND",
                  "description": "Demand Surcharge",
                  "level": "SHIPMENT",
                  "amount": 14.7
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "SHIPMENT",
                  "amount": 6.15
                }
              ],
              "pricingCode": "",
              "currencyExchangeRate": {
                "fromCurrency": "USD",
                "intoCurrency": "USD",
                "rate": 1
              },
              "totalBillingWeight": { "units": "KG", "value": 66.6 },
              "dimDivisorType": "COUNTRY",
              "totalDimWeight": { "units": "KG", "value": 66.6 },
              "currency": "USD",
              "rateScale": "US001DFA_06_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 147 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_SHIPMENT",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 1253.91,
                  "netFreight": 1253.91,
                  "totalSurcharges": 84.59,
                  "netFedExCharge": 1338.5,
                  "totalTaxes": 0,
                  "netCharge": 1338.5,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 66.6 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 63.74
                    },
                    {
                      "type": "DEMAND",
                      "description": "Demand Surcharge",
                      "level": "SHIPMENT",
                      "amount": 14.7
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "SHIPMENT",
                      "amount": 6.15
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 66.6 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          },
          {
            "rateType": "LIST",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 1253.91,
            "totalNetCharge": 1338.5,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 1338.5,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 1338.5,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "US001D",
              "dimDivisor": 139,
              "fuelSurchargePercent": 5,
              "totalSurcharges": 84.59,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 63.74
                },
                {
                  "type": "DEMAND",
                  "description": "Demand Surcharge",
                  "level": "SHIPMENT",
                  "amount": 14.7
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "SHIPMENT",
                  "amount": 6.15
                }
              ],
              "pricingCode": "",
              "currencyExchangeRate": {
                "fromCurrency": "USD",
                "intoCurrency": "USD",
                "rate": 1
              },
              "totalBillingWeight": { "units": "KG", "value": 66.6 },
              "dimDivisorType": "COUNTRY",
              "totalDimWeight": { "units": "KG", "value": 66.6 },
              "currency": "USD",
              "rateScale": "US001DFA_06_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 147 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_SHIPMENT",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 1253.91,
                  "netFreight": 1253.91,
                  "totalSurcharges": 84.59,
                  "netFedExCharge": 1338.5,
                  "totalTaxes": 0,
                  "netCharge": 1338.5,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 66.6 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 63.74
                    },
                    {
                      "type": "DEMAND",
                      "description": "Demand Surcharge",
                      "level": "SHIPMENT",
                      "amount": 14.7
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "SHIPMENT",
                      "amount": 6.15
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 66.6 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          }
        ],
        "operationalDetail": {
          "originLocationIds": ["YVRA "],
          "originLocationNumbers": [0],
          "originServiceAreas": ["A2"],
          "destinationLocationIds": ["FLXA "],
          "destinationLocationNumbers": [0],
          "destinationServiceAreas": ["A1"],
          "destinationLocationStateOrProvinceCodes": ["NV"],
          "ineligibleForMoneyBackGuarantee": false,
          "astraDescription": "INTL1ST",
          "originPostalCodes": ["V6M2V9"],
          "stateOrProvinceCodes": ["BC"],
          "countryCodes": ["CA"],
          "airportId": "LAS",
          "serviceCode": "06",
          "destinationPostalCode": "89109"
        },
        "signatureOptionType": "NO_SIGNATURE_REQUIRED",
        "serviceDescription": {
          "serviceId": "EP1000000007",
          "serviceType": "INTERNATIONAL_FIRST",
          "code": "06",
          "names": [
            {
              "type": "long",
              "encoding": "utf-8",
              "value": "FedEx International First®"
            },
            {
              "type": "long",
              "encoding": "ascii",
              "value": "FedEx International First"
            },
            {
              "type": "medium",
              "encoding": "utf-8",
              "value": "FedEx International First®"
            },
            {
              "type": "medium",
              "encoding": "ascii",
              "value": "FedEx International First"
            },
            { "type": "short", "encoding": "utf-8", "value": "FO" },
            { "type": "short", "encoding": "ascii", "value": "FO" },
            { "type": "abbrv", "encoding": "ascii", "value": "FO" }
          ],
          "serviceCategory": "parcel",
          "description": "International First",
          "astraDescription": "INTL1ST"
        },
        "deliveryStation": "FLXA "
      },
      {
        "serviceType": "FEDEX_GROUND",
        "serviceName": "FedEx International Ground®",
        "packagingType": "YOUR_PACKAGING",
        "commit": {
          "dateDetail": {
            "dayOfWeek": "Thu",
            "dayFormat": "2024-07-25T23:59:00"
          },
          "transitDays": {
            "minimumTransitTime": "FOUR_DAYS",
            "description": "4 Business Days"
          },
          "derivedOriginDetail": {
            "countryCode": "CA",
            "stateOrProvinceCode": "BC",
            "postalCode": "V6M2V9",
            "locationNumber": 6259
          },
          "derivedDestinationDetail": {
            "countryCode": "US",
            "stateOrProvinceCode": "NV",
            "postalCode": "89109",
            "locationNumber": 891,
            "airportId": "LAS"
          },
          "saturdayDelivery": false
        },
        "customerMessages": [
          {
            "code": "TRANSIT.CEFIMPORT.FEE",
            "message": "The payor of duties/taxes/fees will be responsible for any applicable Clearance Entry Fees and other import fees."
          },
          {
            "code": "DIM.APPLIED.NOTE",
            "message": "Dimensional Weight of your package(s) was used to calculate your rate."
          },
          { "code": "2036", "message": "End of Day" }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 471.3,
            "totalNetCharge": 535.68,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 535.68,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 559.55,
            "ancillaryFeesAndTaxes": [
              {
                "type": "CLEARANCE_ENTRY_FEE",
                "description": "Clearance Entry Fee",
                "amount": 23.87
              }
            ],
            "totalDutiesTaxesAndFees": 23.87,
            "totalAncillaryFeesAndTaxes": 23.87,
            "shipmentRateDetail": {
              "rateZone": "52",
              "dimDivisor": 139,
              "fuelSurchargePercent": 7.5,
              "totalSurcharges": 64.38,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "PACKAGE",
                  "amount": 37.38
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "PACKAGE",
                  "amount": 27
                }
              ],
              "totalBillingWeight": { "units": "LB", "value": 162 },
              "totalDimWeight": { "units": "LB", "value": 162 },
              "currency": "CAD"
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "CAD"
          },
          {
            "rateType": "PREFERRED_INCENTIVE",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 344.1,
            "totalNetCharge": 391.02,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 391.02,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 408.45,
            "ancillaryFeesAndTaxes": [
              {
                "type": "CLEARANCE_ENTRY_FEE",
                "description": "Clearance Entry Fee",
                "amount": 17.43
              }
            ],
            "totalDutiesTaxesAndFees": 17.43,
            "totalAncillaryFeesAndTaxes": 17.43,
            "shipmentRateDetail": {
              "rateZone": "52",
              "dimDivisor": 139,
              "fuelSurchargePercent": 7.5,
              "totalSurcharges": 46.92,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "PACKAGE",
                  "amount": 27.24
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "PACKAGE",
                  "amount": 19.68
                }
              ],
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "USD",
                "rate": 0.73
              },
              "totalBillingWeight": { "units": "LB", "value": 162 },
              "totalDimWeight": { "units": "LB", "value": 162 },
              "currency": "USD"
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          },
          {
            "rateType": "PREFERRED_CURRENCY",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 344.1,
            "totalNetCharge": 391.02,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 391.02,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 408.45,
            "ancillaryFeesAndTaxes": [
              {
                "type": "CLEARANCE_ENTRY_FEE",
                "description": "Clearance Entry Fee",
                "amount": 17.43
              }
            ],
            "totalDutiesTaxesAndFees": 17.43,
            "totalAncillaryFeesAndTaxes": 17.43,
            "shipmentRateDetail": {
              "rateZone": "52",
              "dimDivisor": 139,
              "fuelSurchargePercent": 7.5,
              "totalSurcharges": 46.92,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "PACKAGE",
                  "amount": 27.24
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "PACKAGE",
                  "amount": 19.68
                }
              ],
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "USD",
                "rate": 0.73
              },
              "totalBillingWeight": { "units": "LB", "value": 162 },
              "totalDimWeight": { "units": "LB", "value": 162 },
              "currency": "USD"
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 57.35,
                  "netFreight": 57.35,
                  "totalSurcharges": 7.82,
                  "netFedExCharge": 65.17,
                  "totalTaxes": 0,
                  "netCharge": 65.17,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 4.54
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 3.28
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          },
          {
            "rateType": "LIST",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 471.3,
            "totalNetCharge": 535.68,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 535.68,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 559.55,
            "ancillaryFeesAndTaxes": [
              {
                "type": "CLEARANCE_ENTRY_FEE",
                "description": "Clearance Entry Fee",
                "amount": 23.87
              }
            ],
            "totalDutiesTaxesAndFees": 23.87,
            "totalAncillaryFeesAndTaxes": 23.87,
            "shipmentRateDetail": {
              "rateZone": "52",
              "dimDivisor": 139,
              "fuelSurchargePercent": 7.5,
              "totalSurcharges": 64.38,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "PACKAGE",
                  "amount": 37.38
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "PACKAGE",
                  "amount": 27
                }
              ],
              "totalBillingWeight": { "units": "LB", "value": 162 },
              "totalDimWeight": { "units": "LB", "value": 162 },
              "currency": "CAD"
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              },
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_PACKAGE",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 78.55,
                  "netFreight": 78.55,
                  "totalSurcharges": 10.73,
                  "netFedExCharge": 89.28,
                  "totalTaxes": 0,
                  "netCharge": 89.28,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 12.25 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 6.23
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "PACKAGE",
                      "amount": 4.5
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 12.25 },
                  "currency": "CAD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "CAD"
          }
        ],
        "operationalDetail": {
          "originLocationNumbers": [6259],
          "destinationLocationNumbers": [891],
          "destinationLocationStateOrProvinceCodes": ["NV"],
          "deliveryDate": "2024-07-25T23:59:00",
          "deliveryDay": "THU",
          "commitDate": "2024-07-25T23:59:00",
          "commitDays": ["THU"],
          "transitTime": "FOUR_DAYS",
          "ineligibleForMoneyBackGuarantee": true,
          "astraDescription": "FXG",
          "originPostalCodes": ["V6M2V9"],
          "stateOrProvinceCodes": ["BC"],
          "countryCodes": ["CA"],
          "airportId": "LAS",
          "serviceCode": "92",
          "destinationPostalCode": "89109"
        },
        "signatureOptionType": "NO_SIGNATURE_REQUIRED",
        "serviceDescription": {
          "serviceId": "EP1000000135",
          "serviceType": "FEDEX_GROUND",
          "code": "92",
          "names": [
            {
              "type": "long",
              "encoding": "utf-8",
              "value": "FedEx International Ground®"
            },
            {
              "type": "long",
              "encoding": "ascii",
              "value": "FedEx International Ground"
            },
            {
              "type": "medium",
              "encoding": "utf-8",
              "value": "International Ground®"
            },
            {
              "type": "medium",
              "encoding": "ascii",
              "value": "International Ground"
            },
            { "type": "short", "encoding": "utf-8", "value": "IG" },
            { "type": "short", "encoding": "ascii", "value": "IG" },
            { "type": "abbrv", "encoding": "ascii", "value": "SG" }
          ],
          "description": "FedEx Ground",
          "astraDescription": "FXG"
        }
      },
      {
        "serviceType": "FEDEX_INTERNATIONAL_PRIORITY_EXPRESS",
        "serviceName": "FedEx International Priority® Express",
        "packagingType": "YOUR_PACKAGING",
        "commit": {
          "label": "Delivery date unavailable",
          "commitMessageDetails": "Delivery date and time estimates are not available for this shipment.",
          "commodityName": "Blue Jean Coat",
          "deliveryMessages": [" 0:00 A.M. IF NO CUSTOMS DELAY"],
          "derivedOriginDetail": {
            "countryCode": "CA",
            "stateOrProvinceCode": "BC",
            "postalCode": "V6M2V9",
            "serviceArea": "A2",
            "locationId": "YVRA ",
            "locationNumber": 0
          },
          "derivedDestinationDetail": {
            "countryCode": "US",
            "stateOrProvinceCode": "NV",
            "postalCode": "89109",
            "serviceArea": "A1",
            "locationId": "FLXA ",
            "locationNumber": 0,
            "airportId": "LAS"
          },
          "saturdayDelivery": false
        },
        "customerMessages": [
          {
            "code": "SERVICE.TYPE.INTERNATIONAL.MESSAGE",
            "message": "Rate does not include duties & taxes, clearance entry fees or other import fees.  The payor of duties/taxes/fees will be responsible for any applicable Clearance Entry Fees."
          },
          {
            "code": "DIM.APPLIED.NOTE",
            "message": "Dimensional Weight of your package(s) was used to calculate your rate."
          },
          { "code": "COMMODITY.NOT.FOUND", "message": "Commodity not found." }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 1195.11,
            "totalNetCharge": 1276.76,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 1276.76,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 1276.76,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "A",
              "dimDivisor": 139,
              "fuelSurchargePercent": 5,
              "totalSurcharges": 81.65,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 60.8
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "SHIPMENT",
                  "amount": 6.15
                },
                {
                  "type": "DEMAND",
                  "description": "Demand Surcharge",
                  "level": "SHIPMENT",
                  "amount": 14.7
                }
              ],
              "pricingCode": "",
              "currencyExchangeRate": {
                "fromCurrency": "USD",
                "intoCurrency": "USD",
                "rate": 1
              },
              "totalBillingWeight": { "units": "KG", "value": 66.6 },
              "dimDivisorType": "COUNTRY",
              "totalDimWeight": { "units": "KG", "value": 66.6 },
              "currency": "USD",
              "rateScale": "US001DFA_2A_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 147 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_SHIPMENT",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 1195.11,
                  "netFreight": 1195.11,
                  "totalSurcharges": 81.65,
                  "netFedExCharge": 1276.76,
                  "totalTaxes": 0,
                  "netCharge": 1276.76,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 66.6 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 60.8
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "SHIPMENT",
                      "amount": 6.15
                    },
                    {
                      "type": "DEMAND",
                      "description": "Demand Surcharge",
                      "level": "SHIPMENT",
                      "amount": 14.7
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 66.6 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          },
          {
            "rateType": "LIST",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 1195.11,
            "totalNetCharge": 1276.76,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 1276.76,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 1276.76,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "A",
              "dimDivisor": 139,
              "fuelSurchargePercent": 5,
              "totalSurcharges": 81.65,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 60.8
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "SHIPMENT",
                  "amount": 6.15
                },
                {
                  "type": "DEMAND",
                  "description": "Demand Surcharge",
                  "level": "SHIPMENT",
                  "amount": 14.7
                }
              ],
              "pricingCode": "",
              "currencyExchangeRate": {
                "fromCurrency": "USD",
                "intoCurrency": "USD",
                "rate": 1
              },
              "totalBillingWeight": { "units": "KG", "value": 66.6 },
              "dimDivisorType": "COUNTRY",
              "totalDimWeight": { "units": "KG", "value": 66.6 },
              "currency": "USD",
              "rateScale": "US001DFA_2A_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 147 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_SHIPMENT",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 1195.11,
                  "netFreight": 1195.11,
                  "totalSurcharges": 81.65,
                  "netFedExCharge": 1276.76,
                  "totalTaxes": 0,
                  "netCharge": 1276.76,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 66.6 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 60.8
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "SHIPMENT",
                      "amount": 6.15
                    },
                    {
                      "type": "DEMAND",
                      "description": "Demand Surcharge",
                      "level": "SHIPMENT",
                      "amount": 14.7
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 66.6 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          }
        ],
        "operationalDetail": {
          "originLocationIds": ["YVRA "],
          "originLocationNumbers": [0],
          "originServiceAreas": ["A2"],
          "destinationLocationIds": ["FLXA "],
          "destinationLocationNumbers": [0],
          "destinationServiceAreas": ["A1"],
          "destinationLocationStateOrProvinceCodes": ["NV"],
          "ineligibleForMoneyBackGuarantee": false,
          "astraDescription": "IPE",
          "originPostalCodes": ["V6M2V9"],
          "stateOrProvinceCodes": ["BC"],
          "countryCodes": ["CA"],
          "airportId": "LAS",
          "serviceCode": "2A",
          "destinationPostalCode": "89109"
        },
        "signatureOptionType": "NO_SIGNATURE_REQUIRED",
        "serviceDescription": {
          "serviceId": "EP1000000299",
          "serviceType": "FEDEX_INTERNATIONAL_PRIORITY_EXPRESS",
          "code": "2A",
          "names": [
            {
              "type": "long",
              "encoding": "utf-8",
              "value": "FedEx International Priority® Express"
            },
            {
              "type": "long",
              "encoding": "ascii",
              "value": "FedEx International Priority Express"
            },
            {
              "type": "medium",
              "encoding": "utf-8",
              "value": "FedEx Intl Priority Express"
            },
            {
              "type": "medium",
              "encoding": "ascii",
              "value": "FedEx Intl Priority Express"
            },
            { "type": "short", "encoding": "utf-8", "value": "IPM" },
            { "type": "short", "encoding": "ascii", "value": "IPM" },
            { "type": "abbrv", "encoding": "ascii", "value": "LO" }
          ],
          "serviceCategory": "parcel",
          "description": "International Priority Express (IP EXP)",
          "astraDescription": "IPE"
        },
        "deliveryStation": "FLXA "
      },
      {
        "serviceType": "FEDEX_INTERNATIONAL_CONNECT_PLUS",
        "serviceName": "FedEx International Connect Plus",
        "packagingType": "YOUR_PACKAGING",
        "commit": {
          "label": "Delivery date unavailable",
          "commitMessageDetails": "Delivery date and time estimates are not available for this shipment.",
          "commodityName": "Blue Jean Coat",
          "deliveryMessages": [" 0:00 A.M. IF NO CUSTOMS DELAY"],
          "derivedOriginDetail": {
            "countryCode": "CA",
            "stateOrProvinceCode": "BC",
            "postalCode": "V6M2V9",
            "serviceArea": "A2",
            "locationId": "YVRA ",
            "locationNumber": 0
          },
          "derivedDestinationDetail": {
            "countryCode": "US",
            "stateOrProvinceCode": "NV",
            "postalCode": "89109",
            "serviceArea": "A1",
            "locationId": "FLXA ",
            "locationNumber": 0,
            "airportId": "LAS"
          },
          "saturdayDelivery": false
        },
        "customerMessages": [
          {
            "code": "SERVICE.TYPE.INTERNATIONAL.MESSAGE",
            "message": "Rate does not include duties & taxes, clearance entry fees or other import fees.  The payor of duties/taxes/fees will be responsible for any applicable Clearance Entry Fees."
          },
          {
            "code": "DIM.APPLIED.NOTE",
            "message": "Dimensional Weight of your package(s) was used to calculate your rate."
          },
          { "code": "COMMODITY.NOT.FOUND", "message": "Commodity not found." }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 887.88,
            "totalNetCharge": 932.27,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 932.27,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 932.27,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "A",
              "dimDivisor": 139,
              "fuelSurchargePercent": 5,
              "totalSurcharges": 44.39,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 44.39
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "SHIPMENT",
                  "amount": 0
                }
              ],
              "pricingCode": "",
              "currencyExchangeRate": {
                "fromCurrency": "USD",
                "intoCurrency": "USD",
                "rate": 1
              },
              "totalBillingWeight": { "units": "KG", "value": 66.6 },
              "dimDivisorType": "COUNTRY",
              "totalDimWeight": { "units": "KG", "value": 66.6 },
              "currency": "USD",
              "rateScale": "USALLFA_EC_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 147 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_SHIPMENT",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 887.88,
                  "netFreight": 887.88,
                  "totalSurcharges": 44.39,
                  "netFedExCharge": 932.27,
                  "totalTaxes": 0,
                  "netCharge": 932.27,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 66.6 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 44.39
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "SHIPMENT",
                      "amount": 0
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 66.6 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          },
          {
            "rateType": "LIST",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 887.88,
            "totalNetCharge": 932.27,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 932.27,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 932.27,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "A",
              "dimDivisor": 139,
              "fuelSurchargePercent": 5,
              "totalSurcharges": 44.39,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 44.39
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "SHIPMENT",
                  "amount": 0
                }
              ],
              "pricingCode": "",
              "currencyExchangeRate": {
                "fromCurrency": "USD",
                "intoCurrency": "USD",
                "rate": 1
              },
              "totalBillingWeight": { "units": "KG", "value": 66.6 },
              "dimDivisorType": "COUNTRY",
              "totalDimWeight": { "units": "KG", "value": 66.6 },
              "currency": "USD",
              "rateScale": "USALLFA_EC_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 147 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_SHIPMENT",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 887.88,
                  "netFreight": 887.88,
                  "totalSurcharges": 44.39,
                  "netFedExCharge": 932.27,
                  "totalTaxes": 0,
                  "netCharge": 932.27,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 66.6 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 44.39
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "SHIPMENT",
                      "amount": 0
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 66.6 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          }
        ],
        "operationalDetail": {
          "originLocationIds": ["YVRA "],
          "originLocationNumbers": [0],
          "originServiceAreas": ["A2"],
          "destinationLocationIds": ["FLXA "],
          "destinationLocationNumbers": [0],
          "destinationServiceAreas": ["A1"],
          "destinationLocationStateOrProvinceCodes": ["NV"],
          "ineligibleForMoneyBackGuarantee": false,
          "astraDescription": "ICP",
          "originPostalCodes": ["V6M2V9"],
          "stateOrProvinceCodes": ["BC"],
          "countryCodes": ["CA"],
          "airportId": "LAS",
          "serviceCode": "EC",
          "destinationPostalCode": "89109"
        },
        "signatureOptionType": "NO_SIGNATURE_REQUIRED",
        "serviceDescription": {
          "serviceId": "EP1000000305",
          "serviceType": "FEDEX_INTERNATIONAL_CONNECT_PLUS",
          "code": "EC",
          "names": [
            {
              "type": "long",
              "encoding": "utf-8",
              "value": "FedEx International Connect Plus"
            },
            {
              "type": "long",
              "encoding": "ascii",
              "value": "FedEx International Connect Plus"
            },
            {
              "type": "medium",
              "encoding": "utf-8",
              "value": "FedEx Intl Connect Plus"
            },
            {
              "type": "medium",
              "encoding": "ascii",
              "value": "FedEx Intl Connect Plus"
            },
            { "type": "short", "encoding": "utf-8", "value": "ICP" },
            { "type": "short", "encoding": "ascii", "value": "ICP" },
            { "type": "abbrv", "encoding": "ascii", "value": "MN" }
          ],
          "serviceCategory": "parcel",
          "description": "International Connect Plus",
          "astraDescription": "ICP"
        },
        "deliveryStation": "FLXA "
      },
      {
        "serviceType": "FEDEX_INTERNATIONAL_PRIORITY",
        "serviceName": "FedEx International Priority®",
        "packagingType": "YOUR_PACKAGING",
        "commit": {
          "label": "Delivery date unavailable",
          "commitMessageDetails": "Delivery date and time estimates are not available for this shipment.",
          "commodityName": "Blue Jean Coat",
          "deliveryMessages": [" 0:00 A.M. IF NO CUSTOMS DELAY"],
          "derivedOriginDetail": {
            "countryCode": "CA",
            "stateOrProvinceCode": "BC",
            "postalCode": "V6M2V9",
            "serviceArea": "A2",
            "locationId": "YVRA ",
            "locationNumber": 0
          },
          "derivedDestinationDetail": {
            "countryCode": "US",
            "stateOrProvinceCode": "NV",
            "postalCode": "89109",
            "serviceArea": "A1",
            "locationId": "FLXA ",
            "locationNumber": 0,
            "airportId": "LAS"
          },
          "saturdayDelivery": false
        },
        "customerMessages": [
          {
            "code": "SERVICE.TYPE.INTERNATIONAL.MESSAGE",
            "message": "Rate does not include duties & taxes, clearance entry fees or other import fees.  The payor of duties/taxes/fees will be responsible for any applicable Clearance Entry Fees."
          },
          {
            "code": "DIM.APPLIED.NOTE",
            "message": "Dimensional Weight of your package(s) was used to calculate your rate."
          },
          { "code": "COMMODITY.NOT.FOUND", "message": "Commodity not found." }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 1139.25,
            "totalNetCharge": 1775.61,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 1775.61,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 1775.61,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "A",
              "dimDivisor": 139,
              "fuelSurchargePercent": 5,
              "totalSurcharges": 636.36,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 84.11
                },
                {
                  "type": "DEMAND",
                  "description": "Demand Surcharge",
                  "level": "SHIPMENT",
                  "amount": 546.1
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "SHIPMENT",
                  "amount": 6.15
                }
              ],
              "pricingCode": "",
              "currencyExchangeRate": {
                "fromCurrency": "USD",
                "intoCurrency": "USD",
                "rate": 1
              },
              "totalBillingWeight": { "units": "KG", "value": 66.6 },
              "dimDivisorType": "COUNTRY",
              "totalDimWeight": { "units": "KG", "value": 66.6 },
              "currency": "USD",
              "rateScale": "US001DFA_2P_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 147 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_SHIPMENT",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 1139.25,
                  "netFreight": 1139.25,
                  "totalSurcharges": 636.36,
                  "netFedExCharge": 1775.61,
                  "totalTaxes": 0,
                  "netCharge": 1775.61,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 66.6 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 84.11
                    },
                    {
                      "type": "DEMAND",
                      "description": "Demand Surcharge",
                      "level": "SHIPMENT",
                      "amount": 546.1
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "SHIPMENT",
                      "amount": 6.15
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 66.6 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          },
          {
            "rateType": "LIST",
            "ratedWeightMethod": "DIM",
            "totalDiscounts": 0,
            "totalBaseCharge": 1139.25,
            "totalNetCharge": 1775.61,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 1775.61,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 1775.61,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "A",
              "dimDivisor": 139,
              "fuelSurchargePercent": 5,
              "totalSurcharges": 636.36,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "SHIPMENT",
                  "amount": 84.11
                },
                {
                  "type": "DEMAND",
                  "description": "Demand Surcharge",
                  "level": "SHIPMENT",
                  "amount": 546.1
                },
                {
                  "type": "RESIDENTIAL_DELIVERY",
                  "description": "Residential delivery surcharge",
                  "level": "SHIPMENT",
                  "amount": 6.15
                }
              ],
              "pricingCode": "",
              "currencyExchangeRate": {
                "fromCurrency": "USD",
                "intoCurrency": "USD",
                "rate": 1
              },
              "totalBillingWeight": { "units": "KG", "value": 66.6 },
              "dimDivisorType": "COUNTRY",
              "totalDimWeight": { "units": "KG", "value": 66.6 },
              "currency": "USD",
              "rateScale": "US001DFA_2P_YOUR_PACKAGING",
              "totalRateScaleWeight": { "units": "LB", "value": 147 }
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PAYOR_LIST_SHIPMENT",
                  "ratedWeightMethod": "DIM",
                  "baseCharge": 1139.25,
                  "netFreight": 1139.25,
                  "totalSurcharges": 636.36,
                  "netFedExCharge": 1775.61,
                  "totalTaxes": 0,
                  "netCharge": 1775.61,
                  "totalRebates": 0,
                  "billingWeight": { "units": "KG", "value": 66.6 },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "SHIPMENT",
                      "amount": 84.11
                    },
                    {
                      "type": "DEMAND",
                      "description": "Demand Surcharge",
                      "level": "SHIPMENT",
                      "amount": 546.1
                    },
                    {
                      "type": "RESIDENTIAL_DELIVERY",
                      "description": "Residential delivery surcharge",
                      "level": "SHIPMENT",
                      "amount": 6.15
                    }
                  ],
                  "dimWeight": { "units": "KG", "value": 66.6 },
                  "currency": "USD"
                },
                "sequenceNumber": 1
              }
            ],
            "currency": "USD"
          }
        ],
        "operationalDetail": {
          "originLocationIds": ["YVRA "],
          "originLocationNumbers": [0],
          "originServiceAreas": ["A2"],
          "destinationLocationIds": ["FLXA "],
          "destinationLocationNumbers": [0],
          "destinationServiceAreas": ["A1"],
          "destinationLocationStateOrProvinceCodes": ["NV"],
          "ineligibleForMoneyBackGuarantee": false,
          "astraDescription": "IP EOD",
          "originPostalCodes": ["V6M2V9"],
          "stateOrProvinceCodes": ["BC"],
          "countryCodes": ["CA"],
          "airportId": "LAS",
          "serviceCode": "2P",
          "destinationPostalCode": "89109"
        },
        "signatureOptionType": "NO_SIGNATURE_REQUIRED",
        "serviceDescription": {
          "serviceId": "EP1000000300",
          "serviceType": "FEDEX_INTERNATIONAL_PRIORITY",
          "code": "2P",
          "names": [
            {
              "type": "long",
              "encoding": "utf-8",
              "value": "FedEx International Priority®"
            },
            {
              "type": "long",
              "encoding": "ascii",
              "value": "FedEx International Priority"
            },
            {
              "type": "medium",
              "encoding": "utf-8",
              "value": "FedEx International Priority"
            },
            {
              "type": "medium",
              "encoding": "ascii",
              "value": "FedEx International Priority"
            },
            { "type": "short", "encoding": "utf-8", "value": "IPED" },
            { "type": "short", "encoding": "ascii", "value": "IPED" },
            { "type": "abbrv", "encoding": "ascii", "value": "OA" }
          ],
          "serviceCategory": "parcel",
          "description": "International Priority EOD (IP EOD)",
          "astraDescription": "IP EOD"
        },
        "deliveryStation": "FLXA "
      }
    ],
    "quoteDate": "2024-07-19",
    "encoded": false
  }
}
"""
