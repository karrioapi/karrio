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
                f"{gateway.settings.server_url}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {}

ParsedRateResponse = []


RateRequest = {
    "accountNumber": {"value": "Your account number"},
    "rateRequestControlParameters": {
        "returnTransitTimes": False,
        "servicesNeededOnRateFailure": True,
        "variableOptions": "FREIGHT_GUARANTEE",
        "rateSortOrder": "SERVICENAMETRADITIONAL",
    },
    "requestedShipment": {
        "shipper": {
            "address": {
                "streetLines": ["1550 Union Blvd", "Suite 302"],
                "city": "Beverly Hills",
                "stateOrProvinceCode": "TN",
                "postalCode": "65247",
                "countryCode": "US",
                "residential": False,
            }
        },
        "recipient": {
            "address": {
                "streetLines": ["1550 Union Blvd", "Suite 302"],
                "city": "Beverly Hills",
                "stateOrProvinceCode": "TN",
                "postalCode": "65247",
                "countryCode": "US",
                "residential": False,
            }
        },
        "serviceType": "STANDARD_OVERNIGHT",
        "emailNotificationDetail": {
            "recipients": [
                {
                    "emailAddress": "string",
                    "notificationEventType": ["ON_DELIVERY"],
                    "smsDetail": {
                        "phoneNumber": "string",
                        "phoneNumberCountryCode": "string",
                    },
                    "notificationFormatType": "HTML",
                    "emailNotificationRecipientType": "BROKER",
                    "notificationType": "EMAIL",
                    "locale": "string",
                }
            ],
            "personalMessage": "string",
            "PrintedReference": {
                "printedReferenceType": "BILL_OF_LADING",
                "value": "string",
            },
        },
        "preferredCurrency": "USD",
        "rateRequestType": ["ACCOUNT", "LIST"],
        "shipDateStamp": "2015-03-25T09:30:00",
        "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
        "requestedPackageLineItems": [
            {
                "subPackagingType": "BAG",
                "groupPackageCount": 1,
                "contentRecord": [
                    {
                        "itemNumber": "string",
                        "receivedQuantity": 0,
                        "description": "string",
                        "partNumber": "string",
                    }
                ],
                "declaredValue": {"amount": "100", "currency": "USD"},
                "weight": {"units": "LB", "value": 22},
                "dimensions": {"length": 10, "width": 8, "height": 2, "units": "IN"},
                "variableHandlingChargeDetail": {
                    "rateType": "ACCOUNT",
                    "percentValue": 0,
                    "rateLevelType": "BUNDLED_RATE",
                    "fixedValue": {"amount": "100", "currency": "USD"},
                    "rateElementBasis": "NET_CHARGE",
                },
                "packageSpecialServices": {
                    "specialServiceTypes": ["DANGEROUS_GOODS"],
                    "signatureOptionType": ["NO_SIGNATURE_REQUIRED"],
                    "alcoholDetail": {
                        "alcoholRecipientType": "LICENSEE",
                        "shipperAgreementType": "Retailer",
                    },
                    "dangerousGoodsDetail": {
                        "offeror": "Offeror Name",
                        "accessibility": "ACCESSIBLE",
                        "emergencyContactNumber": "3268545905",
                        "options": ["BATTERY"],
                        "containers": [
                            {
                                "offeror": "Offeror Name",
                                "hazardousCommodities": [
                                    {
                                        "quantity": {
                                            "quantityType": "GROSS",
                                            "amount": 0,
                                            "units": "LB",
                                        },
                                        "innerReceptacles": [
                                            {
                                                "quantity": {
                                                    "quantityType": "GROSS",
                                                    "amount": 0,
                                                    "units": "LB",
                                                }
                                            }
                                        ],
                                        "options": {
                                            "labelTextOption": "Override",
                                            "customerSuppliedLabelText": "LabelText",
                                        },
                                        "description": {
                                            "sequenceNumber": 0,
                                            "processingOptions": [
                                                "INCLUDE_SPECIAL_PROVISIONS"
                                            ],
                                            "subsidiaryClasses": "subsidiaryClass",
                                            "labelText": "labelText",
                                            "technicalName": "technicalName",
                                            "packingDetails": {
                                                "packingInstructions": "instruction",
                                                "cargoAircraftOnly": False,
                                            },
                                            "authorization": "Authorization Information",
                                            "reportableQuantity": False,
                                            "percentage": 10,
                                            "id": "ID",
                                            "packingGroup": "DEFAULT",
                                            "properShippingName": "ShippingName",
                                            "hazardClass": "hazardClass",
                                        },
                                    }
                                ],
                                "numberOfContainers": 10,
                                "containerType": "Copper Box",
                                "emergencyContactNumber": {
                                    "areaCode": "202",
                                    "extension": "3245",
                                    "countryCode": "US",
                                    "personalIdentificationNumber": "9545678",
                                    "localNumber": "23456",
                                },
                                "packaging": {"count": 20, "units": "Liter"},
                                "packingType": "ALL_PACKED_IN_ONE",
                                "radioactiveContainerClass": "EXCEPTED_PACKAGE",
                            }
                        ],
                        "packaging": {"count": 20, "units": "Liter"},
                    },
                    "packageCODDetail": {
                        "codCollectionAmount": {"amount": 12.45, "currency": "USD"},
                        "codCollectionType": "ANY",
                    },
                    "pieceCountVerificationBoxCount": 0,
                    "batteryDetails": [
                        {
                            "material": "LITHIUM_METAL",
                            "regulatorySubType": "IATA_SECTION_II",
                            "packing": "CONTAINED_IN_EQUIPMENT",
                        }
                    ],
                    "dryIceWeight": {"units": "LB", "value": 10},
                },
            }
        ],
        "documentShipment": False,
        "variableHandlingChargeDetail": {
            "rateType": "ACCOUNT",
            "percentValue": 0,
            "rateLevelType": "BUNDLED_RATE",
            "fixedValue": {"amount": "100", "currency": "USD"},
            "rateElementBasis": "NET_CHARGE",
        },
        "packagingType": "YOUR_PACKAGING",
        "totalPackageCount": 3,
        "totalWeight": 87.5,
        "shipmentSpecialServices": {
            "returnShipmentDetail": {"returnType": "PRINT_RETURN_LABEL"},
            "deliveryOnInvoiceAcceptanceDetail": {
                "recipient": {
                    "accountNumber": {"value": 123456789},
                    "address": {
                        "streetLines": ["10 FedEx Parkway", "Suite 30"],
                        "countryCode": "US",
                    },
                    "contact": {
                        "companyName": "FedEx",
                        "faxNumber": "9013577890",
                        "personName": "John Taylor",
                        "phoneNumber": "9013577890",
                    },
                }
            },
            "internationalTrafficInArmsRegulationsDetail": {
                "licenseOrExemptionNumber": "432345"
            },
            "pendingShipmentDetail": {
                "pendingShipmentType": "EMAIL",
                "processingOptions": {"options": ["ALLOW_MODIFICATIONS"]},
                "recommendedDocumentSpecification": {
                    "types": ["ANTIQUE_STATEMENT_EUROPEAN_UNION"]
                },
                "emailLabelDetail": {
                    "recipients": [
                        {
                            "emailAddress": "string",
                            "optionsRequested": {
                                "options": ["PRODUCE_PAPERLESS_SHIPPING_FORMAT"]
                            },
                            "role": "SHIPMENT_COMPLETOR",
                            "locale": {"country": "string", "language": "string"},
                        }
                    ],
                    "message": "string",
                },
                "documentReferences": [
                    {
                        "documentType": "CERTIFICATE_OF_ORIGIN",
                        "customerReference": "string",
                        "description": "ShippingDocumentSpecification",
                        "documentId": "98123",
                    }
                ],
                "expirationTimeStamp": "2012-12-31",
                "shipmentDryIceDetail": {
                    "totalWeight": {"units": "LB", "value": 10},
                    "packageCount": 12,
                },
            },
            "holdAtLocationDetail": {
                "locationId": "YBZA",
                "locationContactAndAddress": {
                    "address": {
                        "streetLines": ["10 FedEx Parkway", "Suite 302"],
                        "city": "Beverly Hills",
                        "stateOrProvinceCode": "CA",
                        "postalCode": "38127",
                        "countryCode": "US",
                        "residential": False,
                    },
                    "contact": {
                        "personName": "person name",
                        "emailAddress": "email address",
                        "phoneNumber": "phone number",
                        "phoneExtension": "phone extension",
                        "companyName": "company name",
                        "faxNumber": "fax number",
                    },
                },
                "locationType": "FEDEX_ONSITE",
            },
            "shipmentCODDetail": {
                "addTransportationChargesDetail": {
                    "rateType": "ACCOUNT",
                    "rateLevelType": "BUNDLED_RATE",
                    "chargeLevelType": "CURRENT_PACKAGE",
                    "chargeType": "COD_SURCHARGE",
                },
                "codRecipient": {"accountNumber": {"value": 123456789}},
                "remitToName": "FedEx",
                "codCollectionType": "ANY",
                "financialInstitutionContactAndAddress": {
                    "address": {
                        "streetLines": ["10 FedEx Parkway", "Suite 302"],
                        "city": "Beverly Hills",
                        "stateOrProvinceCode": "CA",
                        "postalCode": "38127",
                        "countryCode": "US",
                        "residential": False,
                    },
                    "contact": {
                        "personName": "person name",
                        "emailAddress": "email address",
                        "phoneNumber": "phone number",
                        "phoneExtension": "phone extension",
                        "companyName": "company name",
                        "faxNumber": "fax number",
                    },
                },
                "returnReferenceIndicatorType": "INVOICE",
            },
            "shipmentDryIceDetail": {
                "totalWeight": {"units": "LB", "value": 10},
                "packageCount": 12,
            },
            "internationalControlledExportDetail": {"type": "DEA_036"},
            "homeDeliveryPremiumDetail": {
                "phoneNumber": {
                    "areaCode": "areaCode",
                    "extension": "extension",
                    "countryCode": "countryCode",
                    "personalIdentificationNumber": "personalIdentificationNumber",
                    "localNumber": "localNumber",
                },
                "shipTimestamp": "2020-04-24",
                "homedeliveryPremiumType": "APPOINTMENT",
            },
            "specialServiceTypes": ["BROKER_SELECT_OPTION"],
        },
        "customsClearanceDetail": {
            "commercialInvoice": {"shipmentPurpose": "GIFT"},
            "freightOnValue": "CARRIER_RISK",
            "dutiesPayment": {
                "payor": {
                    "responsibleParty": {
                        "address": {
                            "streetLines": ["10 FedEx Parkway", "Suite 302"],
                            "city": "Beverly Hills",
                            "stateOrProvinceCode": "CA",
                            "postalCode": "90210",
                            "countryCode": "US",
                            "residential": False,
                        },
                        "contact": {
                            "personName": "John Taylor",
                            "emailAddress": "sample@company.com",
                            "phoneNumber": "1234567890",
                            "phoneExtension": "phone extension",
                            "companyName": "Fedex",
                            "faxNumber": "fax number",
                        },
                        "accountNumber": {"value": "123456789"},
                    }
                },
                "paymentType": "SENDER",
            },
            "commodities": [
                {
                    "description": "DOCUMENTS",
                    "weight": {"units": "LB", "value": 22},
                    "quantity": 1,
                    "customsValue": {"amount": "100", "currency": "USD"},
                    "unitPrice": {"amount": "100", "currency": "USD"},
                    "numberOfPieces": 1,
                    "countryOfManufacture": "US",
                    "quantityUnits": "PCS",
                    "name": "DOCUMENTS",
                    "harmonizedCode": "080211",
                    "partNumber": "P1",
                }
            ],
        },
        "groupShipment": True,
        "serviceTypeDetail": {
            "carrierCode": "FDXE",
            "description": "string",
            "serviceName": "string",
            "serviceCategory": "string",
        },
        "smartPostInfoDetail": {
            "ancillaryEndorsement": "ADDRESS_CORRECTION",
            "hubId": "5531",
            "indicia": "MEDIA_MAIL",
            "specialServices": "USPS_DELIVERY_CONFIRMATION",
        },
        "expressFreightDetail": {
            "bookingConfirmationNumber": "string",
            "shippersLoadAndCount": 0,
        },
        "groundShipment": false,
    },
    "carrierCodes": ["FDXE"],
}

RateResponse = """{
  "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "customerTransactionId": "AnyCo_order123456789",
  "output": {
    "rateReplyDetails": [
      {
        "serviceType": "INTERNATIONAL_FIRST",
        "serviceName": "FedEx International First",
        "packagingType": "YOUR_PACKAGING",
        "customerMessages": [
          {
            "code": "SERVICE.TYPE.INTERNATIONAL.MESSAGE",
            "message": "Rate does not include duties & taxes, clearance entry fees or other import fees.  The payor of duties/taxes/fees will be responsible for any applicable Clearance Entry Fees."
          },
          {
            "code": "EDT.DETAILS.MISSING",
            "message": "The harmonized code for the commodity at array index 1 is missing or invalid; estimated duties and taxes were not returned."
          }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 403.2,
            "totalNetCharge": 445.54,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 445.54,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 445.54,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA003O",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 42.34,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 42.34
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "CAD",
                "rate": 1
              },
              "totalBillingWeight": {
                "units": "LB",
                "valu": 22
              },
              "currency": "CAD"
            },
            "currency": "CAD"
          },
          {
            "rateType": "LIST",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 403.2,
            "totalNetCharge": 445.54,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 445.54,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 445.54,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA003O",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 42.34,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 42.34
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "CAD",
                "rate": 1
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "CAD"
            },
            "currency": "CAD"
          },
          {
            "rateType": "PREFERRED_INCENTIVE",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 308.71,
            "totalNetCharge": 341.13,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 341.13,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 341.13,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA003O",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 32.42,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 32.42
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "USD",
                "rate": 0.77
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "USD"
            },
            "currency": "USD"
          },
          {
            "rateType": "PREFERRED_CURRENCY",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 308.71,
            "totalNetCharge": 341.13,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 341.13,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 341.13,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA003O",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 32.42,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 32.42
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "USD",
                "rate": 0.77
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "USD"
            },
            "currency": "USD"
          }
        ],
        "anonymouslyAllowable": true,
        "operationalDetail": {
          "originLocationIds": "COSA",
          "commitDays": "",
          "serviceCode": "92",
          "airportId": "MEM",
          "scac": "",
          "originServiceAreas": "AM",
          "deliveryDay": "TUE",
          "originLocationNumbers": 1162,
          "destinationPostalCode": "38125",
          "commitDate": "2019-07-22T08:30:00",
          "astraDescription": "INTL1ST",
          "deliveryDate": "",
          "deliveryEligibilities": "",
          "ineligibleForMoneyBackGuarantee": false,
          "maximumTransitTime": "",
          "astraPlannedServiceLevel": "",
          "destinationLocationIds": "EHTA",
          "destinationLocationStateOrProvinceCodes": "CT",
          "transitTime": "THREE_DAYS",
          "packagingCode": "02",
          "destinationLocationNumbers": 892,
          "publishedDeliveryTime": "06:30:00",
          "countryCodes": "US",
          "stateOrProvinceCodes": "TX",
          "ursaPrefixCode": "82",
          "ursaSuffixCode": "EHTA",
          "destinationServiceAreas": "AA",
          "originPostalCodes": "75063",
          "customTransitTime": ""
        },
        "signatureOptionType": "SERVICE_DEFAULT",
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
            {
              "type": "short",
              "encoding": "utf-8",
              "value": "FO"
            },
            {
              "type": "short",
              "encoding": "ascii",
              "value": "FO"
            },
            {
              "type": "abbrv",
              "encoding": "ascii",
              "value": "FO"
            }
          ],
          "operatingOrgCodes": [
            "FXE"
          ],
          "serviceCategory": "parcel",
          "description": "International First",
          "astraDescription": "INTL1ST"
        },
        "commit": {
          "dateDetail": {
            "dayOfWeek": "THU",
            "dayCxsFormat": "2020-07-16T10:30:00"
          }
        }
      },
      {
        "serviceType": "INTERNATIONAL_PRIORITY",
        "serviceName": "FedEx International Priority",
        "packagingType": "YOUR_PACKAGING",
        "customerMessages": [
          {
            "code": "SERVICE.TYPE.INTERNATIONAL.MESSAGE",
            "message": "Rate does not include duties & taxes, clearance entry fees or other import fees.  The payor of duties/taxes/fees will be responsible for any applicable Clearance Entry Fees."
          },
          {
            "code": "EDT.DETAILS.MISSING",
            "message": "The harmonized code for the commodity at array index 1 is missing or invalid; estimated duties and taxes were not returned."
          }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 312.35,
            "totalNetCharge": 345.15,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 345.15,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 345.15,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA003O",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 32.8,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 32.8
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "CAD",
                "rate": 1
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "CAD"
            },
            "currency": "CAD"
          },
          {
            "rateType": "LIST",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 78.99,
            "totalNetCharge": 87.28,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 87.28,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 87.28,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA1520",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 8.29,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 8.29
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "CAD",
                "rate": 1
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "CAD"
            },
            "currency": "CAD"
          },
          {
            "rateType": "PREFERRED_INCENTIVE",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 60.48,
            "totalNetCharge": 66.83,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 66.83,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 66.83,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA1520",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 6.3,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 6.35
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "USD",
                "rate": 0.77
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "USD"
            },
            "currency": "USD"
          },
          {
            "rateType": "PREFERRED_CURRENCY",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 239.15,
            "totalNetCharge": 264.26,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 264.26,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 264.26,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA003O",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 25.11,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 25.11
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "USD",
                "rate": 0.77
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "USD"
            },
            "currency": "USD"
          }
        ],
        "anonymouslyAllowable": true,
        "operationalDetail": {
          "ineligibleForMoneyBackGuarantee": false,
          "astraDescription": "IP",
          "airportId": "MEM",
          "serviceCode": "01",
          "originLocationIds": "COSA",
          "commitDays": "",
          "scac": "",
          "originServiceAreas": "AM",
          "deliveryDay": "TUE",
          "originLocationNumbers": 1162,
          "destinationPostalCode": "38125",
          "commitDate": "2019-07-22T08:30:00",
          "deliveryDate": "",
          "deliveryEligibilities": "",
          "maximumTransitTime": "",
          "astraPlannedServiceLevel": "",
          "destinationLocationIds": "EHTA",
          "destinationLocationStateOrProvinceCodes": "CT",
          "transitTime": "THREE_DAYS",
          "packagingCode": "02",
          "destinationLocationNumbers": 892,
          "publishedDeliveryTime": "06:30:00",
          "countryCodes": "US",
          "stateOrProvinceCodes": "TX",
          "ursaPrefixCode": "82",
          "ursaSuffixCode": "EHTA",
          "destinationServiceAreas": "AA",
          "originPostalCodes": "75063",
          "customTransitTime": ""
        },
        "signatureOptionType": "SERVICE_DEFAULT",
        "serviceDescription": {
          "serviceId": "EP1000000001",
          "serviceType": "INTERNATIONAL_PRIORITY",
          "code": "01",
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
              "value": "FedEx International Priority®"
            },
            {
              "type": "medium",
              "encoding": "ascii",
              "value": "FedEx International Priority"
            },
            {
              "type": "short",
              "encoding": "utf-8",
              "value": "IP"
            },
            {
              "type": "short",
              "encoding": "ascii",
              "value": "IP"
            },
            {
              "type": "abbrv",
              "encoding": "ascii",
              "value": "IP"
            }
          ],
          "operatingOrgCodes": [
            "FXE"
          ],
          "serviceCategory": "parcel",
          "description": "International Priority",
          "astraDescription": "IP"
        },
        "commit": {
          "dateDetail": {
            "dayOfWeek": "FRI",
            "dayCxsFormat": "2020-07-16T10:30:00"
          }
        }
      },
      {
        "serviceType": "INTERNATIONAL_ECONOMY",
        "serviceName": "FedEx International Economy",
        "packagingType": "YOUR_PACKAGING",
        "customerMessages": [
          {
            "code": "SERVICE.TYPE.INTERNATIONAL.MESSAGE",
            "message": "Rate does not include duties & taxes, clearance entry fees or other import fees.  The payor of duties/taxes/fees will be responsible for any applicable Clearance Entry Fees."
          },
          {
            "code": "EDT.DETAILS.MISSING",
            "message": "The harmonized code for the commodity at array index 1 is missing or invalid; estimated duties and taxes were not returned."
          }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 189.65,
            "totalNetCharge": 209.56,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 209.56,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 209.56,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA003O",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 19.91,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 19.91
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "CAD",
                "rate": 1
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "CAD"
            },
            "currency": "CAD"
          },
          {
            "rateType": "LIST",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 48.56,
            "totalNetCharge": 53.66,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 53.66,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 53.66,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA1520",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 5.1,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 5.1
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "CAD",
                "rate": 1
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "CAD"
            },
            "currency": "CAD"
          },
          {
            "rateType": "PREFERRED_INCENTIVE",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 37.18,
            "totalNetCharge": 41.08,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 41.08,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 41.08,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA1520",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 3.9,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 3.9
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "USD",
                "rate": 0.77
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "USD"
            },
            "currency": "USD"
          },
          {
            "rateType": "PREFERRED_CURRENCY",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 145.21,
            "totalNetCharge": 160.45,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 160.45,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 160.45,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "CA003O",
              "dimDivisor": 0,
              "fuelSurchargePercent": 10.5,
              "totalSurcharges": 15.24,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "amount": 15.24
                }
              ],
              "pricingCode": "ACTUAL",
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "USD",
                "rate": 0.77
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "USD"
            },
            "currency": "USD"
          }
        ],
        "anonymouslyAllowable": true,
        "operationalDetail": {
          "ineligibleForMoneyBackGuarantee": false,
          "astraDescription": "IE",
          "airportId": "MEM",
          "serviceCode": "03",
          "originLocationIds": "COSA",
          "originServiceAreas": "AM",
          "deliveryDay": "TUE",
          "originLocationNumbers": 1162,
          "destinationPostalCode": "38125",
          "destinationLocationIds": "EHTA",
          "destinationLocationStateOrProvinceCodes": "CT",
          "transitTime": "THREE_DAYS",
          "packagingCode": "02",
          "destinationLocationNumbers": 892,
          "publishedDeliveryTime": "06:30:00",
          "countryCodes": "US",
          "stateOrProvinceCodes": "TX",
          "ursaPrefixCode": "82",
          "ursaSuffixCode": "EHTA",
          "destinationServiceAreas": "AA",
          "originPostalCodes": "75063"
        },
        "signatureOptionType": "SERVICE_DEFAULT",
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
            {
              "type": "short",
              "encoding": "utf-8",
              "value": "IE"
            },
            {
              "type": "short",
              "encoding": "ascii",
              "value": "IE"
            },
            {
              "type": "abbrv",
              "encoding": "ascii",
              "value": "IE"
            }
          ],
          "operatingOrgCodes": [
            "FXE"
          ],
          "serviceCategory": "parcel",
          "description": "International Two Day",
          "astraDescription": "IE"
        }
      },
      {
        "serviceType": "FEDEX_GROUND",
        "serviceName": "FedEx International Ground�",
        "packagingType": "YOUR_PACKAGING",
        "customerMessages": [
          {
            "code": "SERVICE.TYPE.INTERNATIONAL.MESSAGE",
            "message": "Rate does not include duties & taxes, clearance entry fees or other import fees.  The payor of duties/taxes/fees will be responsible for any applicable Clearance Entry Fees."
          },
          {
            "code": "EDT.DETAILS.MISSING",
            "message": "The harmonized code for the commodity at array index 1 is missing or invalid; estimated duties and taxes were not returned."
          }
        ],
        "ratedShipmentDetails": [
          {
            "rateType": "ACCOUNT",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 2.79,
            "totalBaseCharge": 49.85,
            "totalNetCharge": 53.59,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 53.59,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 53.59,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "52",
              "dimDivisor": 0,
              "fuelSurchargePercent": 7.5,
              "totalSurcharges": 3.74,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "PACKAGE",
                  "amount": 3.74
                }
              ],
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "CAD"
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 2.79,
                "packageRateDetail": {
                  "rateType": "PAYOR_ACCOUNT_PACKAGE",
                  "ratedWeightMethod": "ACTUAL",
                  "baseCharge": 49.85,
                  "netFreight": 49.85,
                  "totalSurcharges": 3.74,
                  "netFedExCharge": 53.59,
                  "totalTaxes": 0,
                  "netCharge": 53.59,
                  "totalRebates": 0,
                  "billingWeight": {
                    "units": "LB",
                    "value": 22
                  },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 3.74
                    }
                  ],
                  "currency": "CAD"
                }
              }
            ],
            "currency": "CAD"
          },
          {
            "rateType": "PREFERRED_INCENTIVE",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 40.16,
            "totalNetCharge": 43.17,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 43.17,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 43.17,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "52",
              "dimDivisor": 0,
              "fuelSurchargePercent": 7.5,
              "totalSurcharges": 3.01,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "PACKAGE",
                  "amount": 3.01
                }
              ],
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "USD",
                "rate": 0.77
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "USD"
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": {
                  "rateType": "PREFERRED_LIST_PACKAGE",
                  "ratedWeightMethod": "ACTUAL",
                  "baseCharge": 40.16,
                  "netFreight": 40.16,
                  "totalSurcharges": 3.01,
                  "netFedExCharge": 43.17,
                  "totalTaxes": 0,
                  "netCharge": 43.17,
                  "totalRebates": 0,
                  "billingWeight": {
                    "units": "LB",
                    "value": 22
                  },
                  "totalFreightDiscounts": 0,
                  "surcharges": [
                    {
                      "type": "FUEL",
                      "description": "Fuel Surcharge",
                      "level": "PACKAGE",
                      "amount": 3.01
                    }
                  ],
                  "currency": "USD"
                }
              }
            ]
          },
          {
            "rateType": "PREFERRED_CURRENCY",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 38.17,
            "totalNetCharge": 41.03,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 41.03,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 41.03,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "52",
              "dimDivisor": 0,
              "fuelSurchargePercent": 7.5,
              "totalSurcharges": 2.86,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "PACKAGE",
                  "amount": 2.86
                }
              ],
              "currencyExchangeRate": {
                "fromCurrency": "CAD",
                "intoCurrency": "USD",
                "rate": 0.77
              },
              "totalBillingWeight": {
                "units": "LB",
                "value": 22
              },
              "currency": "USD"
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": null,
                "rateType": "PREFERRED_ACCOUNT_PACKAGE",
                "ratedWeightMethod": "ACTUAL",
                "baseCharge": 38.17,
                "netFreight": 38.17,
                "totalSurcharges": 2.86,
                "netFedExCharge": 41.03,
                "totalTaxes": 0,
                "netCharge": 41.03,
                "totalRebates": 0,
                "billingWeight": {
                  "units": "LB",
                  "value": 22
                },
                "totalFreightDiscounts": 0,
                "surcharges": [
                  {
                    "type": "FUEL",
                    "description": "Fuel Surcharge",
                    "level": "PACKAGE",
                    "amount": 2.86
                  }
                ],
                "currency": "USD"
              }
            ],
            "currency": "USD"
          },
          {
            "rateType": "LIST",
            "ratedWeightMethod": "ACTUAL",
            "totalDiscounts": 0,
            "totalBaseCharge": 52.45,
            "totalNetCharge": 56.38,
            "totalVatCharge": 0,
            "totalNetFedExCharge": 56.38,
            "totalDutiesAndTaxes": 0,
            "totalNetChargeWithDutiesAndTaxes": 56.38,
            "totalDutiesTaxesAndFees": 0,
            "totalAncillaryFeesAndTaxes": 0,
            "shipmentRateDetail": {
              "rateZone": "52",
              "dimDivisor": 0,
              "fuelSurchargePercent": 7.5,
              "totalSurcharges": 3.93,
              "totalFreightDiscount": 0,
              "surCharges": [
                {
                  "type": "FUEL",
                  "description": "Fuel Surcharge",
                  "level": "PACKAGE",
                  "amount": 3.93
                }
              ],
              "totalBillingWeight\"": {
                "units": "LB",
                "value": 2
              },
              "currency": "CAD"
            },
            "ratedPackages": [
              {
                "groupNumber": 0,
                "effectiveNetDiscount": 0,
                "packageRateDetail": null,
                "rateType": "PAYOR_LIST_PACKAGE",
                "ratedWeightMethod": "ACTUAL",
                "baseCharge": 52.45,
                "netFreight": 52.45,
                "totalSurcharges": 3.93,
                "netFedExCharge": 56.38,
                "totalTaxes": 0,
                "netCharge": 56.38,
                "totalRebates": 0,
                "billingWeight": {
                  "units": "LB",
                  "value": 22
                },
                "totalFreightDiscounts": 0,
                "surcharges": [
                  {
                    "type": "FUEL",
                    "description": "Fuel Surcharge",
                    "level": "PACKAGE",
                    "amount": 3.93
                  }
                ],
                "currency": "CAD"
              }
            ],
            "currency": "CAD",
            "anonymouslyAllowable": true,
            "operationalDetail": {
              "ineligibleForMoneyBackGuarantee": false,
              "astraDescription": "FXG",
              "airportId": "MEM",
              "serviceCode": "92",
              "originLocationIds": "COSA",
              "commitDays": "",
              "scac": "",
              "originServiceAreas": "AM",
              "deliveryDay": "TUE",
              "originLocationNumbers": 1162,
              "destinationPostalCode": "38125",
              "commitDate": "2019-07-22T08:30:00",
              "deliveryDate": "",
              "deliveryEligibilities": "",
              "maximumTransitTime": "",
              "astraPlannedServiceLevel": "",
              "destinationLocationIds": "EHTA",
              "destinationLocationStateOrProvinceCodes": "CT",
              "transitTime": "THREE_DAYS",
              "packagingCode": "02",
              "destinationLocationNumbers": 892,
              "publishedDeliveryTime": "06:30:00",
              "countryCodes": "US",
              "stateOrProvinceCodes": "TX",
              "ursaPrefixCode": "82",
              "ursaSuffixCode": "EHTA",
              "destinationServiceAreas": "AA",
              "originPostalCodes": "75063",
              "customTransitTime": ""
            },
            "signatureOptionType": "SERVICE_DEFAULT",
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
                {
                  "type": "short",
                  "encoding": "utf-8",
                  "value": "IG"
                },
                {
                  "type": "short",
                  "encoding": "ascii",
                  "value": "IG"
                },
                {
                  "type": "abbrv",
                  "encoding": "ascii",
                  "value": "SG"
                }
              ],
              "operatingOrgCodes": [
                "FXG"
              ],
              "description": "FedEx Ground",
              "astraDescription": "FXG"
            }
          }
        ]
      }
    ],
    "quoteDate": "2019-09-06",
    "encoded": false,
    "alerts": [
      {
        "code": "MONEYBACKGUARANTEE.NOT.ELIGIBLE",
        "message": "We are unable to process this request. Please try again later or contact FedEx Customer Service.",
        "alertType": "NOTE"
      }
    ]
  }
}
"""
