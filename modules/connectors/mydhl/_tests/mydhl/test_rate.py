import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLExpressRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "person_name": "TEST USER",
        "state_code": "WA",
        "email": "test@gmail.com",
        "phone_number": "(07) 3114 1499",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "k1k 4t3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "parcels": [
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "options": {},
    "reference": "REF-001",
}

ParsedRateResponse = []


RateRequest = {
    "customerDetails": {
        "shipperDetails": {
            "postalCode": "048582",
            "cityName": "SINGAPORE",
            "addressLine1": "Blk 6 Lock Rd",
            "addressLine2": "02-10 Gillman Barracks",
            "addressLine3": "Barrack Street",
            "countryCode": "SG",
        },
        "receiverDetails": {
            "postalCode": "75001",
            "cityName": "PARIS",
            "addressLine1": "9",
            "addressLine2": "Rue Simart",
            "countryCode": "FR",
        },
    },
    "accounts": [{"typeCode": "shipper", "number": "123456789"}],
    "productsAndServices": [{"productCode": "P", "localProductCode": "P"}],
    "payerCountryCode": "SG",
    "plannedShippingDateAndTime": "2022-11-20T13:00:00GMT+00:00",
    "unitOfMeasurement": "metric",
    "isCustomsDeclarable": True,
    "monetaryAmount": [{"typeCode": "declaredValue", "value": 100, "currency": "SGD"}],
    "estimatedDeliveryDate": {"isRequested": True, "typeCode": "QDDC"},
    "getAdditionalInformation": [
        {"typeCode": "allValueAddedServices", "isRequested": True}
    ],
    "returnStandardProductsOnly": False,
    "nextBusinessDay": True,
    "productTypeCode": "all",
    "packages": [
        {
            "typeCode": "3BX",
            "weight": 1,
            "dimensions": {"length": 10, "width": 20, "height": 30},
        }
    ],
}

RateResponse = """{
  "products": [
    {
      "productName": "EXPRESS WORLDWIDE NONDOC",
      "productCode": "P",
      "localProductCode": "P",
      "localProductCountryCode": "SG",
      "networkTypeCode": "TD",
      "isCustomerAgreement": false,
      "weight": {
        "volumetric": 1.2,
        "provided": 1.5,
        "unitOfMeasurement": "metric"
      },
      "totalPrice": [
        {
          "currencyType": "BILLC",
          "priceCurrency": "GBP",
          "price": 157.95
        },
        {
          "currencyType": "PULCL",
          "priceCurrency": "GBP",
          "price": 157.95
        },
        {
          "currencyType": "BASEC",
          "priceCurrency": "EUR",
          "price": 182.84
        }
      ],
      "totalPriceBreakdown": [
        {
          "currencyType": "BILLC",
          "priceCurrency": "GBP",
          "priceBreakdown": [
            {
              "typeCode": "STTXA",
              "price": 0
            },
            {
              "typeCode": "SPRQT",
              "price": 130
            }
          ]
        },
        {
          "currencyType": "PULCL",
          "priceCurrency": "GBP",
          "priceBreakdown": [
            {
              "typeCode": "STTXA",
              "price": 0
            },
            {
              "typeCode": "SPRQT",
              "price": 130
            }
          ]
        },
        {
          "currencyType": "BASEC",
          "priceCurrency": "EUR",
          "priceBreakdown": [
            {
              "typeCode": "STTXA",
              "price": 0
            },
            {
              "typeCode": "SPRQT",
              "price": 150.49
            }
          ]
        }
      ],
      "detailedPriceBreakdown": [
        {
          "currencyType": "BILLC",
          "priceCurrency": "GBP",
          "breakdown": [
            {
              "name": "EXPRESS WORLDWIDE",
              "price": 130,
              "priceBreakdown": [
                {
                  "priceType": "TAX",
                  "typeCode": "All Bu",
                  "price": 0,
                  "rate": 0,
                  "basePrice": 130
                }
              ]
            },
            {
              "name": "EMERGENCY SITUATION",
              "serviceCode": "CR",
              "localServiceCode": "CR",
              "serviceTypeCode": "SCH",
              "price": 0.27,
              "isCustomerAgreement": false,
              "isMarketedService": true,
              "priceBreakdown": [
                {
                  "priceType": "TAX",
                  "typeCode": "All Bu",
                  "price": 0,
                  "rate": 0,
                  "basePrice": 0.27
                }
              ]
            },
            {
              "name": "FUEL SURCHARGE",
              "serviceCode": "FF",
              "localServiceCode": "FF",
              "serviceTypeCode": "SCH",
              "price": 27.68,
              "isCustomerAgreement": false,
              "isMarketedService": false,
              "priceBreakdown": [
                {
                  "priceType": "TAX",
                  "typeCode": "All Bu",
                  "price": 0,
                  "rate": 0,
                  "basePrice": 27.68
                }
              ]
            },
            {
              "name": "IMPORT BILLING ACCOUNT",
              "serviceCode": "30",
              "localServiceCode": "30",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "SATURDAY DELIVERY",
              "serviceCode": "AA",
              "localServiceCode": "AA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "DIPLOMATIC MAIL",
              "serviceCode": "CG",
              "localServiceCode": "CG",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "DUTY TAX PAID",
              "serviceCode": "DD",
              "localServiceCode": "DD",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "RECEIVER PAID",
              "serviceCode": "DE",
              "localServiceCode": "DE",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "IMPORT BILLING",
              "serviceCode": "DT",
              "localServiceCode": "DT",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "DUTY TAX IMPORTER",
              "serviceCode": "DU",
              "localServiceCode": "DU",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "GOGREEN CLIMATE NEUTRAL",
              "serviceCode": "EE",
              "localServiceCode": "EE",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "GO GREEN PLUS- CARBON REDUCED",
              "serviceCode": "FE",
              "localServiceCode": "FE",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "PACKAGING",
              "serviceCode": "GG",
              "localServiceCode": "GG",
              "typeCode": "PACKAGING ITEM",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "DRY ICE UN1845",
              "serviceCode": "HC",
              "localServiceCode": "HC",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "LITHIUM ION PI966 SECTION II",
              "serviceCode": "HD",
              "localServiceCode": "HD",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "DANGEROUS GOODS",
              "serviceCode": "HE",
              "localServiceCode": "HE",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "EXCEPTED QUANTITIES",
              "serviceCode": "HH",
              "localServiceCode": "HH",
              "typeCode": "EXCEPTED QUANTITY",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "CONSUMER COMMODITIES",
              "serviceCode": "HK",
              "localServiceCode": "HK",
              "typeCode": "CONSUMER GOODS ID8000",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "LITHIUM METAL",
              "serviceCode": "HM",
              "localServiceCode": "HM",
              "typeCode": "LITHIUM METAL PI969 SECTION II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "ACTIVE DATA LOGGER",
              "serviceCode": "HT",
              "localServiceCode": "HT",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "NOT RESTRICTED DANGEROUS GOODS",
              "serviceCode": "HU",
              "localServiceCode": "HU",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "LITHIUM ION PI967-SECTION II",
              "serviceCode": "HV",
              "localServiceCode": "HV",
              "typeCode": "LITHIUM ION PI967 SECTION II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "LITHIUM METAL PI970-SECTION II",
              "serviceCode": "HW",
              "localServiceCode": "HW",
              "typeCode": "LITHIUM METAL PI970 SECTION II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "MAGNETIZED MATERIAL",
              "serviceCode": "HX",
              "localServiceCode": "HX",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "SHIPMENT INSURANCE",
              "serviceCode": "II",
              "localServiceCode": "II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "VERBAL NOTIFICATION",
              "serviceCode": "JA",
              "localServiceCode": "JA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "VERBAL NOTIFICATION",
              "serviceCode": "JD",
              "localServiceCode": "JD",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "COURIER TIME WINDOW",
              "serviceCode": "JY",
              "localServiceCode": "JY",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COLD STORAGE",
              "serviceCode": "LG",
              "localServiceCode": "LG",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "SANCTIONS ROUTING",
              "serviceCode": "LU",
              "localServiceCode": "LU",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "HOLD FOR COLLECTION",
              "serviceCode": "LX",
              "localServiceCode": "LX",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "ADDRESS CORRECTION",
              "serviceCode": "MA",
              "localServiceCode": "MA",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "NEUTRAL DELIVERY",
              "serviceCode": "NN",
              "localServiceCode": "NN",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "REMOTE AREA DELIVERY",
              "serviceCode": "OO",
              "localServiceCode": "OO",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "SHIPMENT PREPARATION",
              "serviceCode": "PA",
              "localServiceCode": "PA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "DATA ENTRY",
              "serviceCode": "PD",
              "localServiceCode": "PD",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "RETURN TO SELLER",
              "serviceCode": "PH",
              "localServiceCode": "PH",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "AUTOMATED DIGITAL IMAGING",
              "serviceCode": "PJ",
              "localServiceCode": "PJ",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "PLT IMAGES PENDING",
              "serviceCode": "PK",
              "localServiceCode": "PK",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "OPTICAL CHARACTER RECOGNITION",
              "serviceCode": "PL",
              "localServiceCode": "PL",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COMMERCIAL INVOICE DATA MERGE",
              "serviceCode": "PM",
              "localServiceCode": "PM",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COMAT",
              "serviceCode": "PO",
              "localServiceCode": "PO",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "NEUTRAL DESCRIPTION LABEL",
              "serviceCode": "PP",
              "localServiceCode": "PP",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "PERSONALLY IDENTIFIABLE DATA",
              "serviceCode": "PQ",
              "localServiceCode": "PQ",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "RETURN TO ORIGIN",
              "serviceCode": "PR",
              "localServiceCode": "PR",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 03",
              "serviceCode": "PT",
              "localServiceCode": "PT",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 06",
              "serviceCode": "PU",
              "localServiceCode": "PU",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 12",
              "serviceCode": "PV",
              "localServiceCode": "PV",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 24",
              "serviceCode": "PW",
              "localServiceCode": "PW",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "LABEL FREE",
              "serviceCode": "PZ",
              "localServiceCode": "PZ",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "DEDICATED PICKUP",
              "serviceCode": "QA",
              "localServiceCode": "QA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DIRECT SIGNATURE",
              "serviceCode": "SF",
              "localServiceCode": "SF",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "SIGNATURE RELEASE",
              "serviceCode": "SX",
              "localServiceCode": "SX",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "VERIFIED DELIVERY",
              "serviceCode": "TF",
              "localServiceCode": "TF",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "RESIDENTIAL DELIVERY",
              "serviceCode": "TK",
              "localServiceCode": "TK",
              "typeCode": "RESIDENTIAL ADDRESS",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "SCHEDULED DELIVERY",
              "serviceCode": "TT",
              "localServiceCode": "TT",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COLLECT FROM SERVICE POINT",
              "serviceCode": "TV",
              "localServiceCode": "TV",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "NON-ROUTINE ENTRY",
              "serviceCode": "WB",
              "localServiceCode": "WB",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "CLEARANCE AUTHORIZATION",
              "serviceCode": "WD",
              "localServiceCode": "WD",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "MULTILINE ENTRY",
              "serviceCode": "WE",
              "localServiceCode": "WE",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "CLEARANCE DATA MODIFICATION",
              "serviceCode": "WF",
              "localServiceCode": "WF",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "BROKER NOTIFICATION",
              "serviceCode": "WG",
              "localServiceCode": "WG",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "PHYSICAL INTERVENTION",
              "serviceCode": "WH",
              "localServiceCode": "WH",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "OTHER GOVERNMENT AGENCY",
              "serviceCode": "WI",
              "localServiceCode": "WI",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "OBTAINING PERMITS & LICENCES",
              "serviceCode": "WJ",
              "localServiceCode": "WJ",
              "typeCode": "PERMITS & LICENSES",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "BONDED STORAGE",
              "serviceCode": "WK",
              "localServiceCode": "WK",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "BONDED TRANSIT",
              "serviceCode": "WL",
              "localServiceCode": "WL",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "TEMPORARY IMPORT/EXPORT",
              "serviceCode": "WM",
              "localServiceCode": "WM",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "EXPORT DECLARATION",
              "serviceCode": "WO",
              "localServiceCode": "WO",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "POST CLEARANCE MODIFICATION",
              "serviceCode": "WS",
              "localServiceCode": "WS",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "SALE IN TRANSIT",
              "serviceCode": "WT",
              "localServiceCode": "WT",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "PAPERLESS TRADE",
              "serviceCode": "WY",
              "localServiceCode": "WY",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "IMPORT EXPORT TAXES",
              "serviceCode": "XB",
              "localServiceCode": "XB",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "MERCHANDISE PROCESS",
              "serviceCode": "XE",
              "localServiceCode": "XE",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "TRADE ZONE PROCESS",
              "serviceCode": "XJ",
              "localServiceCode": "XJ",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "REGULATORY CHARGES",
              "serviceCode": "XK",
              "localServiceCode": "XK",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "IMPORT EXPORT DUTIES",
              "serviceCode": "XX",
              "localServiceCode": "XX",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "NON STACKABLE PALLET",
              "serviceCode": "YC",
              "localServiceCode": "YC",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            }
          ]
        },
        {
          "currencyType": "PULCL",
          "priceCurrency": "GBP",
          "breakdown": [
            {
              "name": "EXPRESS WORLDWIDE",
              "price": 130,
              "priceBreakdown": [
                {
                  "priceType": "TAX",
                  "typeCode": "All Bu",
                  "price": 0,
                  "rate": 0,
                  "basePrice": 130
                }
              ]
            },
            {
              "name": "EMERGENCY SITUATION",
              "serviceCode": "CR",
              "localServiceCode": "CR",
              "serviceTypeCode": "SCH",
              "price": 0.27,
              "isCustomerAgreement": false,
              "isMarketedService": true,
              "priceBreakdown": [
                {
                  "priceType": "TAX",
                  "typeCode": "All Bu",
                  "price": 0,
                  "rate": 0,
                  "basePrice": 0.27
                }
              ]
            },
            {
              "name": "FUEL SURCHARGE",
              "serviceCode": "FF",
              "localServiceCode": "FF",
              "serviceTypeCode": "SCH",
              "price": 27.68,
              "isCustomerAgreement": false,
              "isMarketedService": false,
              "priceBreakdown": [
                {
                  "priceType": "TAX",
                  "typeCode": "All Bu",
                  "price": 0,
                  "rate": 0,
                  "basePrice": 27.68
                }
              ]
            },
            {
              "name": "IMPORT BILLING ACCOUNT",
              "serviceCode": "30",
              "localServiceCode": "30",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "SATURDAY DELIVERY",
              "serviceCode": "AA",
              "localServiceCode": "AA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "DIPLOMATIC MAIL",
              "serviceCode": "CG",
              "localServiceCode": "CG",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "DUTY TAX PAID",
              "serviceCode": "DD",
              "localServiceCode": "DD",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "RECEIVER PAID",
              "serviceCode": "DE",
              "localServiceCode": "DE",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "IMPORT BILLING",
              "serviceCode": "DT",
              "localServiceCode": "DT",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "DUTY TAX IMPORTER",
              "serviceCode": "DU",
              "localServiceCode": "DU",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "GOGREEN CLIMATE NEUTRAL",
              "serviceCode": "EE",
              "localServiceCode": "EE",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "GO GREEN PLUS- CARBON REDUCED",
              "serviceCode": "FE",
              "localServiceCode": "FE",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "PACKAGING",
              "serviceCode": "GG",
              "localServiceCode": "GG",
              "typeCode": "PACKAGING ITEM",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "DRY ICE UN1845",
              "serviceCode": "HC",
              "localServiceCode": "HC",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "LITHIUM ION PI966 SECTION II",
              "serviceCode": "HD",
              "localServiceCode": "HD",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "DANGEROUS GOODS",
              "serviceCode": "HE",
              "localServiceCode": "HE",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "EXCEPTED QUANTITIES",
              "serviceCode": "HH",
              "localServiceCode": "HH",
              "typeCode": "EXCEPTED QUANTITY",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "CONSUMER COMMODITIES",
              "serviceCode": "HK",
              "localServiceCode": "HK",
              "typeCode": "CONSUMER GOODS ID8000",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "LITHIUM METAL",
              "serviceCode": "HM",
              "localServiceCode": "HM",
              "typeCode": "LITHIUM METAL PI969 SECTION II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "ACTIVE DATA LOGGER",
              "serviceCode": "HT",
              "localServiceCode": "HT",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "NOT RESTRICTED DANGEROUS GOODS",
              "serviceCode": "HU",
              "localServiceCode": "HU",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "LITHIUM ION PI967-SECTION II",
              "serviceCode": "HV",
              "localServiceCode": "HV",
              "typeCode": "LITHIUM ION PI967 SECTION II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "LITHIUM METAL PI970-SECTION II",
              "serviceCode": "HW",
              "localServiceCode": "HW",
              "typeCode": "LITHIUM METAL PI970 SECTION II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "MAGNETIZED MATERIAL",
              "serviceCode": "HX",
              "localServiceCode": "HX",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "SHIPMENT INSURANCE",
              "serviceCode": "II",
              "localServiceCode": "II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "VERBAL NOTIFICATION",
              "serviceCode": "JA",
              "localServiceCode": "JA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "VERBAL NOTIFICATION",
              "serviceCode": "JD",
              "localServiceCode": "JD",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "COURIER TIME WINDOW",
              "serviceCode": "JY",
              "localServiceCode": "JY",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COLD STORAGE",
              "serviceCode": "LG",
              "localServiceCode": "LG",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "SANCTIONS ROUTING",
              "serviceCode": "LU",
              "localServiceCode": "LU",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "HOLD FOR COLLECTION",
              "serviceCode": "LX",
              "localServiceCode": "LX",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "ADDRESS CORRECTION",
              "serviceCode": "MA",
              "localServiceCode": "MA",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "NEUTRAL DELIVERY",
              "serviceCode": "NN",
              "localServiceCode": "NN",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "REMOTE AREA DELIVERY",
              "serviceCode": "OO",
              "localServiceCode": "OO",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "SHIPMENT PREPARATION",
              "serviceCode": "PA",
              "localServiceCode": "PA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "DATA ENTRY",
              "serviceCode": "PD",
              "localServiceCode": "PD",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "RETURN TO SELLER",
              "serviceCode": "PH",
              "localServiceCode": "PH",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "AUTOMATED DIGITAL IMAGING",
              "serviceCode": "PJ",
              "localServiceCode": "PJ",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "PLT IMAGES PENDING",
              "serviceCode": "PK",
              "localServiceCode": "PK",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "OPTICAL CHARACTER RECOGNITION",
              "serviceCode": "PL",
              "localServiceCode": "PL",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COMMERCIAL INVOICE DATA MERGE",
              "serviceCode": "PM",
              "localServiceCode": "PM",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COMAT",
              "serviceCode": "PO",
              "localServiceCode": "PO",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "NEUTRAL DESCRIPTION LABEL",
              "serviceCode": "PP",
              "localServiceCode": "PP",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "PERSONALLY IDENTIFIABLE DATA",
              "serviceCode": "PQ",
              "localServiceCode": "PQ",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "RETURN TO ORIGIN",
              "serviceCode": "PR",
              "localServiceCode": "PR",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 03",
              "serviceCode": "PT",
              "localServiceCode": "PT",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 06",
              "serviceCode": "PU",
              "localServiceCode": "PU",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 12",
              "serviceCode": "PV",
              "localServiceCode": "PV",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 24",
              "serviceCode": "PW",
              "localServiceCode": "PW",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "LABEL FREE",
              "serviceCode": "PZ",
              "localServiceCode": "PZ",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "DEDICATED PICKUP",
              "serviceCode": "QA",
              "localServiceCode": "QA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DIRECT SIGNATURE",
              "serviceCode": "SF",
              "localServiceCode": "SF",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "SIGNATURE RELEASE",
              "serviceCode": "SX",
              "localServiceCode": "SX",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "VERIFIED DELIVERY",
              "serviceCode": "TF",
              "localServiceCode": "TF",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "RESIDENTIAL DELIVERY",
              "serviceCode": "TK",
              "localServiceCode": "TK",
              "typeCode": "RESIDENTIAL ADDRESS",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "SCHEDULED DELIVERY",
              "serviceCode": "TT",
              "localServiceCode": "TT",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COLLECT FROM SERVICE POINT",
              "serviceCode": "TV",
              "localServiceCode": "TV",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "NON-ROUTINE ENTRY",
              "serviceCode": "WB",
              "localServiceCode": "WB",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "CLEARANCE AUTHORIZATION",
              "serviceCode": "WD",
              "localServiceCode": "WD",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "MULTILINE ENTRY",
              "serviceCode": "WE",
              "localServiceCode": "WE",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "CLEARANCE DATA MODIFICATION",
              "serviceCode": "WF",
              "localServiceCode": "WF",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "BROKER NOTIFICATION",
              "serviceCode": "WG",
              "localServiceCode": "WG",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "PHYSICAL INTERVENTION",
              "serviceCode": "WH",
              "localServiceCode": "WH",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "OTHER GOVERNMENT AGENCY",
              "serviceCode": "WI",
              "localServiceCode": "WI",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "OBTAINING PERMITS & LICENCES",
              "serviceCode": "WJ",
              "localServiceCode": "WJ",
              "typeCode": "PERMITS & LICENSES",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "BONDED STORAGE",
              "serviceCode": "WK",
              "localServiceCode": "WK",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "BONDED TRANSIT",
              "serviceCode": "WL",
              "localServiceCode": "WL",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "TEMPORARY IMPORT/EXPORT",
              "serviceCode": "WM",
              "localServiceCode": "WM",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "EXPORT DECLARATION",
              "serviceCode": "WO",
              "localServiceCode": "WO",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "POST CLEARANCE MODIFICATION",
              "serviceCode": "WS",
              "localServiceCode": "WS",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "SALE IN TRANSIT",
              "serviceCode": "WT",
              "localServiceCode": "WT",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "PAPERLESS TRADE",
              "serviceCode": "WY",
              "localServiceCode": "WY",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "IMPORT EXPORT TAXES",
              "serviceCode": "XB",
              "localServiceCode": "XB",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "MERCHANDISE PROCESS",
              "serviceCode": "XE",
              "localServiceCode": "XE",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "TRADE ZONE PROCESS",
              "serviceCode": "XJ",
              "localServiceCode": "XJ",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "REGULATORY CHARGES",
              "serviceCode": "XK",
              "localServiceCode": "XK",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "IMPORT EXPORT DUTIES",
              "serviceCode": "XX",
              "localServiceCode": "XX",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "NON STACKABLE PALLET",
              "serviceCode": "YC",
              "localServiceCode": "YC",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            }
          ]
        },
        {
          "currencyType": "BASEC",
          "priceCurrency": "EUR",
          "breakdown": [
            {
              "name": "EXPRESS WORLDWIDE",
              "price": 150.49,
              "priceBreakdown": [
                {
                  "priceType": "TAX",
                  "typeCode": "All Bu",
                  "price": 0,
                  "rate": 0,
                  "basePrice": 150.49
                }
              ]
            },
            {
              "name": "EMERGENCY SITUATION",
              "serviceCode": "CR",
              "localServiceCode": "CR",
              "serviceTypeCode": "SCH",
              "price": 0.31,
              "isCustomerAgreement": false,
              "isMarketedService": true,
              "priceBreakdown": [
                {
                  "priceType": "TAX",
                  "typeCode": "All Bu",
                  "price": 0,
                  "rate": 0,
                  "basePrice": 0.31
                }
              ]
            },
            {
              "name": "FUEL SURCHARGE",
              "serviceCode": "FF",
              "localServiceCode": "FF",
              "serviceTypeCode": "SCH",
              "price": 32.04,
              "isCustomerAgreement": false,
              "isMarketedService": false,
              "priceBreakdown": [
                {
                  "priceType": "TAX",
                  "typeCode": "All Bu",
                  "price": 0,
                  "rate": 0,
                  "basePrice": 32.04
                }
              ]
            },
            {
              "name": "IMPORT BILLING ACCOUNT",
              "serviceCode": "30",
              "localServiceCode": "30",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "SATURDAY DELIVERY",
              "serviceCode": "AA",
              "localServiceCode": "AA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "DIPLOMATIC MAIL",
              "serviceCode": "CG",
              "localServiceCode": "CG",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "DUTY TAX PAID",
              "serviceCode": "DD",
              "localServiceCode": "DD",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "RECEIVER PAID",
              "serviceCode": "DE",
              "localServiceCode": "DE",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "IMPORT BILLING",
              "serviceCode": "DT",
              "localServiceCode": "DT",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "DUTY TAX IMPORTER",
              "serviceCode": "DU",
              "localServiceCode": "DU",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "GOGREEN CLIMATE NEUTRAL",
              "serviceCode": "EE",
              "localServiceCode": "EE",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "GO GREEN PLUS- CARBON REDUCED",
              "serviceCode": "FE",
              "localServiceCode": "FE",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "PACKAGING",
              "serviceCode": "GG",
              "localServiceCode": "GG",
              "typeCode": "PACKAGING ITEM",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "DRY ICE UN1845",
              "serviceCode": "HC",
              "localServiceCode": "HC",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "LITHIUM ION PI966 SECTION II",
              "serviceCode": "HD",
              "localServiceCode": "HD",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "DANGEROUS GOODS",
              "serviceCode": "HE",
              "localServiceCode": "HE",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "EXCEPTED QUANTITIES",
              "serviceCode": "HH",
              "localServiceCode": "HH",
              "typeCode": "EXCEPTED QUANTITY",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "CONSUMER COMMODITIES",
              "serviceCode": "HK",
              "localServiceCode": "HK",
              "typeCode": "CONSUMER GOODS ID8000",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "LITHIUM METAL",
              "serviceCode": "HM",
              "localServiceCode": "HM",
              "typeCode": "LITHIUM METAL PI969 SECTION II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "ACTIVE DATA LOGGER",
              "serviceCode": "HT",
              "localServiceCode": "HT",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "NOT RESTRICTED DANGEROUS GOODS",
              "serviceCode": "HU",
              "localServiceCode": "HU",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "LITHIUM ION PI967-SECTION II",
              "serviceCode": "HV",
              "localServiceCode": "HV",
              "typeCode": "LITHIUM ION PI967 SECTION II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "LITHIUM METAL PI970-SECTION II",
              "serviceCode": "HW",
              "localServiceCode": "HW",
              "typeCode": "LITHIUM METAL PI970 SECTION II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "MAGNETIZED MATERIAL",
              "serviceCode": "HX",
              "localServiceCode": "HX",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "SHIPMENT INSURANCE",
              "serviceCode": "II",
              "localServiceCode": "II",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "VERBAL NOTIFICATION",
              "serviceCode": "JA",
              "localServiceCode": "JA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "VERBAL NOTIFICATION",
              "serviceCode": "JD",
              "localServiceCode": "JD",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "COURIER TIME WINDOW",
              "serviceCode": "JY",
              "localServiceCode": "JY",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COLD STORAGE",
              "serviceCode": "LG",
              "localServiceCode": "LG",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "SANCTIONS ROUTING",
              "serviceCode": "LU",
              "localServiceCode": "LU",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "HOLD FOR COLLECTION",
              "serviceCode": "LX",
              "localServiceCode": "LX",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "ADDRESS CORRECTION",
              "serviceCode": "MA",
              "localServiceCode": "MA",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "NEUTRAL DELIVERY",
              "serviceCode": "NN",
              "localServiceCode": "NN",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "REMOTE AREA DELIVERY",
              "serviceCode": "OO",
              "localServiceCode": "OO",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "SHIPMENT PREPARATION",
              "serviceCode": "PA",
              "localServiceCode": "PA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "DATA ENTRY",
              "serviceCode": "PD",
              "localServiceCode": "PD",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "RETURN TO SELLER",
              "serviceCode": "PH",
              "localServiceCode": "PH",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "AUTOMATED DIGITAL IMAGING",
              "serviceCode": "PJ",
              "localServiceCode": "PJ",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "PLT IMAGES PENDING",
              "serviceCode": "PK",
              "localServiceCode": "PK",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "OPTICAL CHARACTER RECOGNITION",
              "serviceCode": "PL",
              "localServiceCode": "PL",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COMMERCIAL INVOICE DATA MERGE",
              "serviceCode": "PM",
              "localServiceCode": "PM",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COMAT",
              "serviceCode": "PO",
              "localServiceCode": "PO",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "NEUTRAL DESCRIPTION LABEL",
              "serviceCode": "PP",
              "localServiceCode": "PP",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "PERSONALLY IDENTIFIABLE DATA",
              "serviceCode": "PQ",
              "localServiceCode": "PQ",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "RETURN TO ORIGIN",
              "serviceCode": "PR",
              "localServiceCode": "PR",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 03",
              "serviceCode": "PT",
              "localServiceCode": "PT",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 06",
              "serviceCode": "PU",
              "localServiceCode": "PU",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 12",
              "serviceCode": "PV",
              "localServiceCode": "PV",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DATA STAGING 24",
              "serviceCode": "PW",
              "localServiceCode": "PW",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "LABEL FREE",
              "serviceCode": "PZ",
              "localServiceCode": "PZ",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "DEDICATED PICKUP",
              "serviceCode": "QA",
              "localServiceCode": "QA",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "DIRECT SIGNATURE",
              "serviceCode": "SF",
              "localServiceCode": "SF",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "SIGNATURE RELEASE",
              "serviceCode": "SX",
              "localServiceCode": "SX",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "VERIFIED DELIVERY",
              "serviceCode": "TF",
              "localServiceCode": "TF",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "RESIDENTIAL DELIVERY",
              "serviceCode": "TK",
              "localServiceCode": "TK",
              "typeCode": "RESIDENTIAL ADDRESS",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "SCHEDULED DELIVERY",
              "serviceCode": "TT",
              "localServiceCode": "TT",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "COLLECT FROM SERVICE POINT",
              "serviceCode": "TV",
              "localServiceCode": "TV",
              "serviceTypeCode": "TEC",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "NON-ROUTINE ENTRY",
              "serviceCode": "WB",
              "localServiceCode": "WB",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "CLEARANCE AUTHORIZATION",
              "serviceCode": "WD",
              "localServiceCode": "WD",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "MULTILINE ENTRY",
              "serviceCode": "WE",
              "localServiceCode": "WE",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "CLEARANCE DATA MODIFICATION",
              "serviceCode": "WF",
              "localServiceCode": "WF",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "BROKER NOTIFICATION",
              "serviceCode": "WG",
              "localServiceCode": "WG",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "PHYSICAL INTERVENTION",
              "serviceCode": "WH",
              "localServiceCode": "WH",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "OTHER GOVERNMENT AGENCY",
              "serviceCode": "WI",
              "localServiceCode": "WI",
              "serviceTypeCode": "CDZ",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "OBTAINING PERMITS & LICENCES",
              "serviceCode": "WJ",
              "localServiceCode": "WJ",
              "typeCode": "PERMITS & LICENSES",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "BONDED STORAGE",
              "serviceCode": "WK",
              "localServiceCode": "WK",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "BONDED TRANSIT",
              "serviceCode": "WL",
              "localServiceCode": "WL",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "TEMPORARY IMPORT/EXPORT",
              "serviceCode": "WM",
              "localServiceCode": "WM",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": true
            },
            {
              "name": "EXPORT DECLARATION",
              "serviceCode": "WO",
              "localServiceCode": "WO",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "POST CLEARANCE MODIFICATION",
              "serviceCode": "WS",
              "localServiceCode": "WS",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "SALE IN TRANSIT",
              "serviceCode": "WT",
              "localServiceCode": "WT",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "PAPERLESS TRADE",
              "serviceCode": "WY",
              "localServiceCode": "WY",
              "serviceTypeCode": "XCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "IMPORT EXPORT TAXES",
              "serviceCode": "XB",
              "localServiceCode": "XB",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "MERCHANDISE PROCESS",
              "serviceCode": "XE",
              "localServiceCode": "XE",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": true,
              "isMarketedService": false
            },
            {
              "name": "TRADE ZONE PROCESS",
              "serviceCode": "XJ",
              "localServiceCode": "XJ",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": true
            },
            {
              "name": "REGULATORY CHARGES",
              "serviceCode": "XK",
              "localServiceCode": "XK",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "IMPORT EXPORT DUTIES",
              "serviceCode": "XX",
              "localServiceCode": "XX",
              "serviceTypeCode": "FIS",
              "isCustomerAgreement": false,
              "isMarketedService": false
            },
            {
              "name": "NON STACKABLE PALLET",
              "serviceCode": "YC",
              "localServiceCode": "YC",
              "serviceTypeCode": "SCH",
              "isCustomerAgreement": false,
              "isMarketedService": false
            }
          ]
        }
      ],
      "pickupCapabilities": {
        "nextBusinessDay": true,
        "localCutoffDateAndTime": "2022-11-21T19:00:00",
        "GMTCutoffTime": "21:00:00",
        "pickupEarliest": "09:30:00",
        "pickupLatest": "21:00:00",
        "originServiceAreaCode": "SIN",
        "originFacilityAreaCode": "ESC",
        "pickupAdditionalDays": 0,
        "pickupDayOfWeek": 1
      },
      "deliveryCapabilities": {
        "deliveryTypeCode": "QDDC",
        "estimatedDeliveryDateAndTime": "2022-11-24T23:59:00",
        "destinationServiceAreaCode": "CDG",
        "destinationFacilityAreaCode": "GVL",
        "deliveryAdditionalDays": 0,
        "deliveryDayOfWeek": 4,
        "totalTransitDays": 3
      },
      "pricingDate": "2022-12-21"
    }
  ],
  "exchangeRates": [
    {
      "currentExchangeRate": 1.157608,
      "currency": "GBP",
      "baseCurrency": "EUR"
    }
  ]
}
"""
