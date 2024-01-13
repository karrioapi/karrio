import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestFedExShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )
        self.MultiPieceShipmentRequest = models.ShipmentRequest(
            **MultiPieceShipmentPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "person_name": "Input Your Information",
        "company_name": "Input Your Information",
        "phone_number": "Input Your Information",
        "email": "Input Your Information",
        "address_line1": "Input Your Information",
        "address_line2": "Input Your Information",
        "city": "MEMPHIS",
        "state_code": "TN",
        "postal_code": "38117",
        "country_code": "US",
    },
    "recipient": {
        "person_name": "Input Your Information",
        "company_name": "Input Your Information",
        "phone_number": "Input Your Information",
        "email": "Input Your Information",
        "address_line1": "Input Your Information",
        "address_line2": "Input Your Information",
        "city": "RICHMOND",
        "state_code": "BC",
        "postal_code": "V7C4v7",
        "country_code": "CA",
    },
    "parcels": [
        {
            "packaging_type": "your_packaging",
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "weight": 20.0,
            "length": 12,
            "width": 12,
            "height": 12,
        }
    ],
    "service": "fedex_international_priority",
    "options": {"currency": "USD"},
    "payment": {"paid_by": "third_party", "account_number": "2349857"},
    "customs": {
        "invoice": "123456789",
        "duty": {"paid_by": "sender", "declared_value": 100.0},
        "commodities": [{"weight": "10", "title": "test", "hs_code": "00339BB"}],
        "commercial_invoice": True,
    },
    "reference": "#Order 11111",
}

MultiPieceShipmentPayload = {
    **ShipmentPayload,
    "parcels": [
        {
            "packaging_type": "your_packaging",
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "weight": 1.0,
            "length": 12,
            "width": 12,
            "height": 12,
        },
        {
            "packaging_type": "your_packaging",
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "weight": 2.0,
            "length": 11,
            "width": 11,
            "height": 11,
        },
    ],
    "options": {"currency": "USD", "paperless_trade": True},
}

ShipmentCancelPayload = {"shipment_identifier": "794953555571"}

ParsedShipmentResponse = []

ParsedCancelShipmentResponse = []


ShipmentRequest = {
    "mergeLabelDocOption": "LABELS_AND_DOCS",
    "requestedShipment": {
        "shipDatestamp": "2019-10-14",
        "totalDeclaredValue": {"amount": 12.45, "currency": "USD"},
        "shipper": {
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
                "phoneExtension": "91",
                "phoneNumber": "XXXX567890",
                "companyName": "Fedex",
            },
            "tins": [
                {
                    "number": "XXX567",
                    "tinType": "FEDERAL",
                    "usage": "usage",
                    "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                    "expirationDate": "2000-01-23T04:56:07.000+00:00",
                }
            ],
        },
        "soldTo": {
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
                "phoneExtension": "91",
                "phoneNumber": "1234567890",
                "companyName": "Fedex",
            },
            "tins": [
                {
                    "number": "123567",
                    "tinType": "FEDERAL",
                    "usage": "usage",
                    "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                    "expirationDate": "2000-01-23T04:56:07.000+00:00",
                }
            ],
            "accountNumber": {"value": "Your account number"},
        },
        "recipients": [
            {
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
                    "phoneExtension": "000",
                    "phoneNumber": "XXXX345671",
                    "companyName": "FedEx",
                },
                "tins": [
                    {
                        "number": "123567",
                        "tinType": "FEDERAL",
                        "usage": "usage",
                        "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                        "expirationDate": "2000-01-23T04:56:07.000+00:00",
                    }
                ],
                "deliveryInstructions": "Delivery Instructions",
            }
        ],
        "recipientLocationNumber": "1234567",
        "pickupType": "USE_SCHEDULED_PICKUP",
        "serviceType": "PRIORITY_OVERNIGHT",
        "packagingType": "YOUR_PACKAGING",
        "totalWeight": 20.6,
        "origin": {
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
        "shippingChargesPayment": {
            "paymentType": "SENDER",
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
                        "phoneNumber": "XXXX567890",
                        "phoneExtension": "phone extension",
                        "companyName": "Fedex",
                        "faxNumber": "fax number",
                    },
                    "accountNumber": {"value": "Your account number"},
                }
            },
        },
        "shipmentSpecialServices": {
            "specialServiceTypes": [
                "THIRD_PARTY_CONSIGNEE",
                "PROTECTION_FROM_FREEZING",
            ],
            "etdDetail": {
                "attributes": ["POST_SHIPMENT_UPLOAD_REQUESTED"],
                "attachedDocuments": [
                    {
                        "documentType": "PRO_FORMA_INVOICE",
                        "documentReference": "DocumentReference",
                        "description": "PRO FORMA INVOICE",
                        "documentId": "090927d680038c61",
                    }
                ],
                "requestedDocumentTypes": [
                    "VICS_BILL_OF_LADING",
                    "GENERAL_AGENCY_AGREEMENT",
                ],
            },
            "returnShipmentDetail": {
                "returnEmailDetail": {
                    "merchantPhoneNumber": "19012635656",
                    "allowedSpecialService": ["SATURDAY_DELIVERY"],
                },
                "rma": {"reason": "Wrong Size or Color"},
                "returnAssociationDetail": {
                    "shipDatestamp": "2019-10-01",
                    "trackingNumber": "123456789",
                },
                "returnType": "PRINT_RETURN_LABEL",
            },
            "deliveryOnInvoiceAcceptanceDetail": {
                "recipient": {
                    "address": {
                        "streetLines": ["23, RUE JOSEPH-DE MA", "Suite 302"],
                        "city": "Beverly Hills",
                        "stateOrProvinceCode": "CA",
                        "postalCode": "90210",
                        "countryCode": "US",
                        "residential": False,
                    },
                    "contact": {
                        "personName": "John Taylor",
                        "emailAddress": "sample@company.com",
                        "phoneExtension": "000",
                        "phoneNumber": "1234567890",
                        "companyName": "Fedex",
                    },
                    "tins": [
                        {
                            "number": "123567",
                            "tinType": "FEDERAL",
                            "usage": "usage",
                            "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                            "expirationDate": "2000-01-23T04:56:07.000+00:00",
                        }
                    ],
                    "deliveryInstructions": "Delivery Instructions",
                }
            },
            "internationalTrafficInArmsRegulationsDetail": {
                "licenseOrExemptionNumber": "9871234"
            },
            "pendingShipmentDetail": {
                "pendingShipmentType": "EMAIL",
                "processingOptions": {"options": ["ALLOW_MODIFICATIONS"]},
                "recommendedDocumentSpecification": {
                    "types": "ANTIQUE_STATEMENT_EUROPEAN_UNION"
                },
                "emailLabelDetail": {
                    "recipients": [
                        {
                            "emailAddress": "neena@fedex.com",
                            "optionsRequested": {
                                "options": [
                                    "PRODUCE_PAPERLESS_SHIPPING_FORMAT",
                                    "SUPPRESS_ACCESS_EMAILS",
                                ]
                            },
                            "role": "SHIPMENT_COMPLETOR",
                            "locale": "en_US",
                        }
                    ],
                    "message": "your optional message",
                },
                "attachedDocuments": [
                    {
                        "documentType": "PRO_FORMA_INVOICE",
                        "documentReference": "DocumentReference",
                        "description": "PRO FORMA INVOICE",
                        "documentId": "090927d680038c61",
                    }
                ],
                "expirationTimeStamp": "2020-01-01",
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
                "codRecipient": {
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
                        "phoneExtension": "000",
                        "phoneNumber": "XXXX345671",
                        "companyName": "Fedex",
                    },
                    "accountNumber": {"value": "Your account number"},
                    "tins": [
                        {
                            "number": "123567",
                            "tinType": "FEDERAL",
                            "usage": "usage",
                            "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                            "expirationDate": "2000-01-23T04:56:07.000+00:00",
                        }
                    ],
                },
                "remitToName": "remitToName",
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
                "codCollectionAmount": {"amount": 12.45, "currency": "USD"},
                "returnReferenceIndicatorType": "INVOICE",
                "shipmentCodAmount": {"amount": 12.45, "currency": "USD"},
            },
            "shipmentDryIceDetail": {
                "totalWeight": {"units": "LB", "value": 10},
                "packageCount": 12,
            },
            "internationalControlledExportDetail": {
                "licenseOrPermitExpirationDate": "2019-12-03",
                "licenseOrPermitNumber": "11",
                "entryNumber": "125",
                "foreignTradeZoneCode": "US",
                "type": "WAREHOUSE_WITHDRAWAL",
            },
            "homeDeliveryPremiumDetail": {
                "phoneNumber": {
                    "areaCode": "901",
                    "localNumber": "3575012",
                    "extension": "200",
                    "personalIdentificationNumber": "98712345",
                },
                "deliveryDate": "2019-06-26",
                "homedeliveryPremiumType": "APPOINTMENT",
            },
        },
        "emailNotificationDetail": {
            "aggregationType": "PER_PACKAGE",
            "emailNotificationRecipients": [
                {
                    "name": "Joe Smith",
                    "emailNotificationRecipientType": "SHIPPER",
                    "emailAddress": "jsmith3@aol.com",
                    "notificationFormatType": "TEXT",
                    "notificationType": "EMAIL",
                    "locale": "en_US",
                    "notificationEventType": [
                        "ON_PICKUP_DRIVER_ARRIVED",
                        "ON_SHIPMENT",
                    ],
                }
            ],
            "personalMessage": "your personal message here",
        },
        "expressFreightDetail": {
            "bookingConfirmationNumber": "123456789812",
            "shippersLoadAndCount": 123,
            "packingListEnclosed": True,
        },
        "variableHandlingChargeDetail": {
            "rateType": "PREFERRED_CURRENCY",
            "percentValue": 12.45,
            "rateLevelType": "INDIVIDUAL_PACKAGE_RATE",
            "fixedValue": {"amount": 24.45, "currency": "USD"},
            "rateElementBasis": "NET_CHARGE_EXCLUDING_TAXES",
        },
        "customsClearanceDetail": {
            "regulatoryControls": "NOT_IN_FREE_CIRCULATION",
            "brokers": [
                {
                    "broker": {
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
                            "phoneExtension": 91,
                            "companyName": "Fedex",
                            "faxNumber": 1234567,
                        },
                        "accountNumber": {"value": "Your account number"},
                        "tins": [
                            {
                                "number": "number",
                                "tinType": "FEDERAL",
                                "usage": "usage",
                                "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                                "expirationDate": "2000-01-23T04:56:07.000+00:00",
                            }
                        ],
                        "deliveryInstructions": "deliveryInstructions",
                    },
                    "type": "IMPORT",
                }
            ],
            "commercialInvoice": {
                "originatorName": "originator Name",
                "comments": ["optional comments for the commercial invoice"],
                "customerReferences": [
                    {"customerReferenceType": "INVOICE_NUMBER", "value": "3686"}
                ],
                "taxesOrMiscellaneousCharge": {"amount": 12.45, "currency": "USD"},
                "taxesOrMiscellaneousChargeType": "COMMISSIONS",
                "freightCharge": {"amount": 12.45, "currency": "USD"},
                "packingCosts": {"amount": 12.45, "currency": "USD"},
                "handlingCosts": {"amount": 12.45, "currency": "USD"},
                "declarationStatement": "declarationStatement",
                "termsOfSale": "FCA",
                "specialInstructions": 'specialInstructions"',
                "shipmentPurpose": "REPAIR_AND_RETURN",
                "emailNotificationDetail": {
                    "emailAddress": "neena@fedex.com",
                    "type": "EMAILED",
                    "recipientType": "SHIPPER",
                },
            },
            "freightOnValue": "OWN_RISK",
            "dutiesPayment": {
                "payor": {
                    "responsibleParty": {
                        "address": {
                            "streetLines": ["10 FedEx Parkway", "Suite 302"],
                            "city": "Beverly Hills",
                            "stateOrProvinceCode": "CA",
                            "postalCode": "38127",
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
                        "accountNumber": {"value": "Your account number"},
                        "tins": [
                            {
                                "number": "number",
                                "tinType": "FEDERAL",
                                "usage": "usage",
                                "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                                "expirationDate": "2000-01-23T04:56:07.000+00:00",
                            },
                            {
                                "number": "number",
                                "tinType": "FEDERAL",
                                "usage": "usage",
                                "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                                "expirationDate": "2000-01-23T04:56:07.000+00:00",
                            },
                        ],
                    }
                },
                "billingDetails": {
                    "billingCode": "billingCode",
                    "billingType": "billingType",
                    "aliasId": "aliasId",
                    "accountNickname": "accountNickname",
                    "accountNumber": "Your account number",
                    "accountNumberCountryCode": "US",
                },
                "paymentType": "SENDER",
            },
            "commodities": [
                {
                    "unitPrice": {"amount": 12.45, "currency": "USD"},
                    "additionalMeasures": [{"quantity": 12.45, "units": "KG"}],
                    "numberOfPieces": 12,
                    "quantity": 125,
                    "quantityUnits": "Ea",
                    "customsValue": {"amount": "1556.25", "currency": "USD"},
                    "countryOfManufacture": "US",
                    "cIMarksAndNumbers": "87123",
                    "harmonizedCode": "0613",
                    "description": "description",
                    "name": "non-threaded rivets",
                    "weight": {"units": "KG", "value": 68},
                    "exportLicenseNumber": "26456",
                    "exportLicenseExpirationDate": "2023-06-10T10:51:32Z",
                    "partNumber": "167",
                    "purpose": "BUSINESS",
                    "usmcaDetail": {"originCriterion": "A"},
                }
            ],
            "isDocumentOnly": True,
            "recipientCustomsId": {"type": "PASSPORT", "value": "123"},
            "customsOption": {
                "description": "Description",
                "type": "COURTESY_RETURN_LABEL",
            },
            "importerOfRecord": {
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
                    "phoneExtension": "000",
                    "phoneNumber": "XXXX345671",
                    "companyName": "Fedex",
                },
                "accountNumber": {"value": "Your account number"},
                "tins": [
                    {
                        "number": "123567",
                        "tinType": "FEDERAL",
                        "usage": "usage",
                        "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                        "expirationDate": "2000-01-23T04:56:07.000+00:00",
                    }
                ],
            },
            "generatedDocumentLocale": "en_US",
            "exportDetail": {
                "destinationControlDetail": {
                    "endUser": "dest country user",
                    "statementTypes": "DEPARTMENT_OF_COMMERCE",
                    "destinationCountries": ["USA", "India"],
                },
                "b13AFilingOption": "NOT_REQUIRED",
                "exportComplianceStatement": "12345678901234567",
                "permitNumber": "12345",
            },
            "totalCustomsValue": {"amount": 12.45, "currency": "USD"},
            "partiesToTransactionAreRelated": True,
            "declarationStatementDetail": {
                "usmcaLowValueStatementDetail": {
                    "countryOfOriginLowValueDocumentRequested": True,
                    "customsRole": "EXPORTER",
                }
            },
            "insuranceCharge": {"amount": 12.45, "currency": "USD"},
        },
        "smartPostInfoDetail": {
            "ancillaryEndorsement": "RETURN_SERVICE",
            "hubId": "5015",
            "indicia": "PRESORTED_STANDARD",
            "specialServices": "USPS_DELIVERY_CONFIRMATION",
        },
        "blockInsightVisibility": true,
        "labelSpecification": {
            "labelFormatType": "COMMON2D",
            "labelOrder": "SHIPPING_LABEL_FIRST",
            "customerSpecifiedDetail": {
                "maskedData": ["CUSTOMS_VALUE", "TOTAL_WEIGHT"],
                "regulatoryLabels": [
                    {
                        "generationOptions": "CONTENT_ON_SHIPPING_LABEL_ONLY",
                        "type": "ALCOHOL_SHIPMENT_LABEL",
                    }
                ],
                "additionalLabels": [{"type": "CONSIGNEE", "count": 1}],
                "docTabContent": {
                    "docTabContentType": "BARCODED",
                    "zone001": {
                        "docTabZoneSpecifications": [
                            {
                                "zoneNumber": 0,
                                "header": "string",
                                "dataField": "string",
                                "literalValue": "string",
                                "justification": "RIGHT",
                            }
                        ]
                    },
                    "barcoded": {
                        "symbology": "UCC128",
                        "specification": {
                            "zoneNumber": 0,
                            "header": "string",
                            "dataField": "string",
                            "literalValue": "string",
                            "justification": "RIGHT",
                        },
                    },
                },
            },
            "printedLabelOrigin": {
                "address": {
                    "streetLines": ["10 FedEx Parkway", "Suite 302"],
                    "city": "Beverly Hills",
                    "stateOrProvinceCode": "CA",
                    "postalCode": "38127",
                    "countryCode": "US",
                    "residential": false,
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
            "labelStockType": "PAPER_85X11_TOP_HALF_LABEL",
            "labelRotation": "UPSIDE_DOWN",
            "imageType": "PDF",
            "labelPrintingOrientation": "TOP_EDGE_OF_TEXT_FIRST",
            "returnedDispositionDetail": true,
        },
        "shippingDocumentSpecification": {
            "generalAgencyAgreementDetail": {
                "documentFormat": {
                    "provideInstructions": true,
                    "optionsRequested": {
                        "options": [
                            "SUPPRESS_ADDITIONAL_LANGUAGES",
                            "SHIPPING_LABEL_LAST",
                        ]
                    },
                    "stockType": "PAPER_LETTER",
                    "dispositions": [
                        {
                            "eMailDetail": {
                                "eMailRecipients": [
                                    {
                                        "emailAddress": "email@fedex.com",
                                        "recipientType": "THIRD_PARTY",
                                    }
                                ],
                                "locale": "en_US",
                                "grouping": "NONE",
                            },
                            "dispositionType": "CONFIRMED",
                        }
                    ],
                    "locale": "en_US",
                    "docType": "PDF",
                }
            },
            "returnInstructionsDetail": {
                "customText": "This is additional text printed on Return instr",
                "documentFormat": {
                    "provideInstructions": true,
                    "optionsRequested": {
                        "options": [
                            "SUPPRESS_ADDITIONAL_LANGUAGES",
                            "SHIPPING_LABEL_LAST",
                        ]
                    },
                    "stockType": "PAPER_LETTER",
                    "dispositions": [
                        {
                            "eMailDetail": {
                                "eMailRecipients": [
                                    {
                                        "emailAddress": "email@fedex.com",
                                        "recipientType": "THIRD_PARTY",
                                    }
                                ],
                                "locale": "en_US",
                                "grouping": "NONE",
                            },
                            "dispositionType": "CONFIRMED",
                        }
                    ],
                    "locale": 'en_US"',
                    "docType": "PNG",
                },
            },
            "op900Detail": {
                "customerImageUsages": [
                    {
                        "id": "IMAGE_5",
                        "type": "SIGNATURE",
                        "providedImageType": "SIGNATURE",
                    }
                ],
                "signatureName": "Signature Name",
                "documentFormat": {
                    "provideInstructions": true,
                    "optionsRequested": {
                        "options": [
                            "SUPPRESS_ADDITIONAL_LANGUAGES",
                            "SHIPPING_LABEL_LAST",
                        ]
                    },
                    "stockType": "PAPER_LETTER",
                    "dispositions": [
                        {
                            "eMailDetail": {
                                "eMailRecipients": [
                                    {
                                        "emailAddress": "email@fedex.com",
                                        "recipientType": "THIRD_PARTY",
                                    }
                                ],
                                "locale": "en_US",
                                "grouping": "NONE",
                            },
                            "dispositionType": "CONFIRMED",
                        }
                    ],
                    "locale": "en_US",
                    "docType": "PDF",
                },
            },
            "usmcaCertificationOfOriginDetail": {
                "customerImageUsages": [
                    {
                        "id": "IMAGE_5",
                        "type": "SIGNATURE",
                        "providedImageType": "SIGNATURE",
                    }
                ],
                "documentFormat": {
                    "provideInstructions": true,
                    "optionsRequested": {
                        "options": [
                            "SUPPRESS_ADDITIONAL_LANGUAGES",
                            "SHIPPING_LABEL_LAST",
                        ]
                    },
                    "stockType": "PAPER_LETTER",
                    "dispositions": [
                        {
                            "eMailDetail": {
                                "eMailRecipients": [
                                    {
                                        "emailAddress": "email@fedex.com",
                                        "recipientType": "THIRD_PARTY",
                                    }
                                ],
                                "locale": "en_US",
                                "grouping": "NONE",
                            },
                            "dispositionType": "CONFIRMED",
                        }
                    ],
                    "locale": "en_US",
                    "docType": "PDF",
                },
                "certifierSpecification": "EXPORTER",
                "importerSpecification": "UNKNOWN",
                "producerSpecification": "SAME_AS_EXPORTER",
                "producer": {
                    "address": {
                        "streetLines": ["10 FedEx Parkway", "Suite 302"],
                        "city": "Beverly Hills",
                        "stateOrProvinceCode": "CA",
                        "postalCode": "90210",
                        "countryCode": "US",
                        "residential": false,
                    },
                    "contact": {
                        "personName": "John Taylor",
                        "emailAddress": "sample@company.com",
                        "phoneExtension": "000",
                        "phoneNumber": "XXXX345671",
                        "companyName": "Fedex",
                    },
                    "accountNumber": {"value": "Your account number"},
                    "tins": [
                        {
                            "number": "123567",
                            "tinType": "FEDERAL",
                            "usage": "usage",
                            "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                            "expirationDate": "2000-01-23T04:56:07.000+00:00",
                        }
                    ],
                },
                "blanketPeriod": {"begins": "22-01-2020", "ends": "2-01-2020"},
                "certifierJobTitle": "Manager",
            },
            "usmcaCommercialInvoiceCertificationOfOriginDetail": {
                "customerImageUsages": [
                    {
                        "id": "IMAGE_5",
                        "type": "SIGNATURE",
                        "providedImageType": "SIGNATURE",
                    }
                ],
                "documentFormat": {
                    "provideInstructions": true,
                    "optionsRequested": {
                        "options": [
                            "SUPPRESS_ADDITIONAL_LANGUAGES",
                            "SHIPPING_LABEL_LAST",
                        ]
                    },
                    "stockType": "PAPER_LETTER",
                    "dispositions": [
                        {
                            "eMailDetail": {
                                "eMailRecipients": [
                                    {
                                        "emailAddress": "email@fedex.com",
                                        "recipientType": "THIRD_PARTY",
                                    }
                                ],
                                "locale": "en_US",
                                "grouping": "NONE",
                            },
                            "dispositionType": "CONFIRMED",
                        }
                    ],
                    "locale": "en_US",
                    "docType": "PDF",
                },
                "certifierSpecification": "EXPORTER",
                "importerSpecification": "UNKNOWN",
                "producerSpecification": "SAME_AS_EXPORTER",
                "producer": {
                    "address": {
                        "streetLines": ["10 FedEx Parkway", "Suite 302"],
                        "city": "Beverly Hills",
                        "stateOrProvinceCode": "CA",
                        "postalCode": "90210",
                        "countryCode": "US",
                        "residential": false,
                    },
                    "contact": {
                        "personName": "John Taylor",
                        "emailAddress": "sample@company.com",
                        "phoneExtension": "000",
                        "phoneNumber": "XXXX345671",
                        "companyName": "Fedex",
                    },
                    "accountNumber": {"value": "Your account number"},
                    "tins": [
                        {
                            "number": "123567",
                            "tinType": "FEDERAL",
                            "usage": "usage",
                            "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                            "expirationDate": "2000-01-23T04:56:07.000+00:00",
                        }
                    ],
                },
                "certifierJobTitle": "Manager",
            },
            "shippingDocumentTypes": ["RETURN_INSTRUCTIONS"],
            "certificateOfOrigin": {
                "customerImageUsages": [
                    {
                        "id": "IMAGE_5",
                        "type": "SIGNATURE",
                        "providedImageType": "SIGNATURE",
                    }
                ],
                "documentFormat": {
                    "provideInstructions": true,
                    "optionsRequested": {
                        "options": [
                            "SUPPRESS_ADDITIONAL_LANGUAGES",
                            "SHIPPING_LABEL_LAST",
                        ]
                    },
                    "stockType": "PAPER_LETTER",
                    "dispositions": [
                        {
                            "eMailDetail": {
                                "eMailRecipients": [
                                    {
                                        "emailAddress": "email@fedex.com",
                                        "recipientType": "THIRD_PARTY",
                                    }
                                ],
                                "locale": "en_US",
                                "grouping": "NONE",
                            },
                            "dispositionType": "CONFIRMED",
                        }
                    ],
                    "locale": "en_US",
                    "docType": "PDF",
                },
            },
            "commercialInvoiceDetail": {
                "customerImageUsages": [
                    {
                        "id": "IMAGE_5",
                        "type": "SIGNATURE",
                        "providedImageType": "SIGNATURE",
                    }
                ],
                "documentFormat": {
                    "provideInstructions": true,
                    "optionsRequested": {
                        "options": [
                            "SUPPRESS_ADDITIONAL_LANGUAGES",
                            "SHIPPING_LABEL_LAST",
                        ]
                    },
                    "stockType": "PAPER_LETTER",
                    "dispositions": [
                        {
                            "eMailDetail": {
                                "eMailRecipients": [
                                    {
                                        "emailAddress": "email@fedex.com",
                                        "recipientType": "THIRD_PARTY",
                                    }
                                ],
                                "locale": "en_US",
                                "grouping": "NONE",
                            },
                            "dispositionType": "CONFIRMED",
                        }
                    ],
                    "locale": "en_US",
                    "docType": "PDF",
                },
            },
        },
        "rateRequestType": ["LIST", "PREFERRED"],
        "preferredCurrency": "USD",
        "totalPackageCount": 25,
        "masterTrackingId": {
            "formId": "0201",
            "trackingIdType": "EXPRESS",
            "uspsApplicationId": "92",
            "trackingNumber": "49092000070120032835",
        },
        "requestedPackageLineItems": [
            {
                "sequenceNumber": "1",
                "subPackagingType": "BUCKET",
                "customerReferences": [
                    {"customerReferenceType": "INVOICE_NUMBER", "value": "3686"}
                ],
                "declaredValue": {"amount": 12.45, "currency": "USD"},
                "weight": {"units": "KG", "value": 68},
                "dimensions": {"length": 100, "width": 50, "height": 30, "units": "CM"},
                "groupPackageCount": 2,
                "itemDescriptionForClearance": "description",
                "contentRecord": [
                    {
                        "itemNumber": "2876",
                        "receivedQuantity": 256,
                        "description": "Description",
                        "partNumber": "456",
                    }
                ],
                "itemDescription": "item description for the package",
                "variableHandlingChargeDetail": {
                    "rateType": "PREFERRED_CURRENCY",
                    "percentValue": 12.45,
                    "rateLevelType": "INDIVIDUAL_PACKAGE_RATE",
                    "fixedValue": {"amount": 24.45, "currency": "USD"},
                    "rateElementBasis": "NET_CHARGE_EXCLUDING_TAXES",
                },
                "packageSpecialServices": {
                    "specialServiceTypes": ["ALCOHOL", "NON_STANDARD_CONTAINER"],
                    "signatureOptionType": "ADULT",
                    "priorityAlertDetail": {
                        "enhancementTypes": ["PRIORITY_ALERT_PLUS"],
                        "content": ["string"],
                    },
                    "signatureOptionDetail": {"signatureReleaseNumber": "23456"},
                    "alcoholDetail": {
                        "alcoholRecipientType": "LICENSEE",
                        "shipperAgreementType": "Retailer",
                    },
                    "dangerousGoodsDetail": {
                        "cargoAircraftOnly": False,
                        "accessibility": "INACCESSIBLE",
                        "options": ["LIMITED_QUANTITIES_COMMODITIES", "ORM_D"],
                    },
                    "packageCODDetail": {
                        "codCollectionAmount": {"amount": 12.45, "currency": "USD"}
                    },
                    "pieceCountVerificationBoxCount": 0,
                    "batteryDetails": [
                        {
                            "batteryPackingType": "CONTAINED_IN_EQUIPMENT",
                            "batteryRegulatoryType": "IATA_SECTION_II",
                            "batteryMaterialType": "LITHIUM_METAL",
                        }
                    ],
                    "dryIceWeight": {"units": "KG", "value": 68},
                },
                "trackingNumber": "756477399",
            }
        ],
    },
    "labelResponseOptions": "LABEL",
    "accountNumber": {"value": "Your account number"},
    "shipAction": "CONFIRM",
    "processingOptionType": "ALLOW_ASYNCHRONOUS",
    "oneLabelAtATime": True,
}

ShipmentCancelRequest = {
    "accountNumber": {"value": "2349857"},
    "deletionControl": "DELETE_ALL_PACKAGES",
    "trackingNumber": "794953555571",
}

ShipmentResponse = """{
  "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "customerTransactionId": "AnyCo_order123456789",
  "output": {
    "transactionShipments": [
      {
        "serviceType": "STANDARD_OVERNIGHT",
        "shipDatestamp": "2010-03-04",
        "serviceCategory": "EXPRESS",
        "shipmentDocuments": [
          {
            "contentKey": "content key",
            "copiesToPrint": 10,
            "contentType": "COMMERCIAL_INVOICE",
            "trackingNumber": "794953535000",
            "docType": "PDF",
            "alerts": [
              {
                "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
                "alertType": "NOTE",
                "message": "Recipient Postal-City Mismatch."
              }
            ],
            "encodedLabel": "encoded label",
            "url": "https://wwwdev.idev.fedex.com/document/v2/document/retrieve/SH,794810209259_SHIPPING_P/isLabel=true&autoPrint=false"
          }
        ],
        "pieceResponses": [
          {
            "netChargeAmount": 21.45,
            "transactionDetails": [
              {
                "transactionDetails": "transactionDetails",
                "transactionId": "12345"
              }
            ],
            "packageDocuments": [
              {
                "contentKey": "content key",
                "copiesToPrint": 10,
                "contentType": "COMMERCIAL_INVOICE",
                "trackingNumber": "794953535000",
                "docType": "PDF",
                "alerts": [
                  {
                    "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
                    "alertType": "NOTE",
                    "message": "Recipient Postal-City Mismatch."
                  }
                ],
                "encodedLabel": "encoded label",
                "url": "https://wwwdev.idev.fedex.com/document/v2/document/retrieve/SH,794810209259_SHIPPING_P/isLabel=true&autoPrint=false"
              }
            ],
            "acceptanceTrackingNumber": "794953535000",
            "serviceCategory": "EXPRESS",
            "listCustomerTotalCharge": "listCustomerTotalCharge",
            "deliveryTimestamp": "2012-09-23",
            "trackingIdType": "FEDEX",
            "additionalChargesDiscount": 621.45,
            "netListRateAmount": 1.45,
            "baseRateAmount": 321.45,
            "packageSequenceNumber": 215,
            "netDiscountAmount": 121.45,
            "codcollectionAmount": 231.45,
            "masterTrackingNumber": "794953535000",
            "acceptanceType": "acceptanceType",
            "trackingNumber": "794953535000",
            "successful": true,
            "customerReferences": [
              {
                "customerReferenceType": "INVOICE_NUMBER",
                "value": "3686"
              }
            ]
          }
        ],
        "serviceName": "FedEx 2 Day Freight",
        "alerts": [
          {
            "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
            "alertType": "NOTE",
            "message": "Recipient Postal-City Mismatch."
          }
        ],
        "completedShipmentDetail": {
          "completedPackageDetails": [
            {
              "sequenceNumber": 256,
              "operationalDetail": {
                "astraHandlingText": "astraHandlingText",
                "barcodes": {
                  "binaryBarcodes": [
                    {
                      "type": "COMMON-2D",
                      "value": "string"
                    }
                  ],
                  "stringBarcodes": [
                    {
                      "type": "ADDRESS",
                      "value": "1010062512241535917900794953544894"
                    }
                  ]
                },
                "operationalInstructions": [
                  {
                    "number": 17,
                    "content": "content"
                  }
                ]
              },
              "signatureOption": "DIRECT",
              "trackingIds": [
                {
                  "formId": "0201",
                  "trackingIdType": "EXPRESS",
                  "uspsApplicationId": "92",
                  "trackingNumber": "49092000070120032835"
                }
              ],
              "groupNumber": 567,
              "oversizeClass": "OVERSIZE_1, OVERSIZE_2, OVERSIZE_3",
              "packageRating": {
                "effectiveNetDiscount": 0,
                "actualRateType": "PAYOR_ACCOUNT_PACKAGE",
                "packageRateDetails": [
                  {
                    "ratedWeightMethod": "DIM",
                    "totalFreightDiscounts": 44.55,
                    "totalTaxes": 3.45,
                    "minimumChargeType": "CUSTOMER",
                    "baseCharge": 45.67,
                    "totalRebates": 4.56,
                    "rateType": "PAYOR_RETAIL_PACKAGE",
                    "billingWeight": {
                      "units": "KG",
                      "value": 68
                    },
                    "netFreight": 4.89,
                    "surcharges": [
                      {
                        "amount": "string",
                        "surchargeType": "APPOINTMENT_DELIVERY",
                        "level": "PACKAGE, or SHIPMENT",
                        "description": "description"
                      }
                    ],
                    "totalSurcharges": 22.56,
                    "netFedExCharge": 12.56,
                    "netCharge": 121.56,
                    "currency": "USD"
                  }
                ]
              },
              "dryIceWeight": {
                "units": "KG",
                "value": 68
              },
              "hazardousPackageDetail": {
                "regulation": "IATA",
                "accessibility": "ACCESSIBLE",
                "labelType": "II_YELLOW",
                "containers": [
                  {
                    "qvalue": 2,
                    "hazardousCommodities": [
                      {
                        "quantity": {
                          "quantityType": "GROSS",
                          "amount": 24.56,
                          "units": "Kg"
                        },
                        "options": {
                          "quantity": {
                            "quantityType": "GROSS",
                            "amount": 24.56,
                            "units": "Kg"
                          },
                          "innerReceptacles": [
                            {
                              "quantity": {
                                "quantityType": "NET",
                                "amount": 34.56,
                                "units": "Kg"
                              }
                            }
                          ],
                          "options": {
                            "labelTextOption": "APPEND",
                            "customerSuppliedLabelText": "Customer Supplied Label Text."
                          },
                          "description": {
                            "sequenceNumber": 9812,
                            "processingOptions": [
                              "INCLUDE_SPECIAL_PROVISIONS"
                            ],
                            "subsidiaryClasses": [
                              "Subsidiary Classes"
                            ],
                            "labelText": "labelText",
                            "technicalName": "technicalName",
                            "packingDetails": {
                              "packingInstructions": "packing Instructions",
                              "cargoAircraftOnly": true
                            },
                            "authorization": "authorization",
                            "reportableQuantity": true,
                            "percentage": 12.45,
                            "id": "123",
                            "packingGroup": "I",
                            "properShippingName": "properShippingName",
                            "hazardClass": "hazard Class"
                          }
                        },
                        "description": {
                          "sequenceNumber": 876,
                          "packingInstructions": "packingInstructions",
                          "subsidiaryClasses": [
                            "Subsidiary Classes"
                          ],
                          "labelText": "labelText",
                          "tunnelRestrictionCode": "UN2919",
                          "specialProvisions": "specialProvisions",
                          "properShippingNameAndDescription": "properShippingNameAndDescription",
                          "technicalName": "technicalName",
                          "symbols": "symbols",
                          "authorization": "authorization",
                          "attributes": [
                            "attributes"
                          ],
                          "id": "1234",
                          "packingGroup": "packingGroup",
                          "properShippingName": "properShippingName",
                          "hazardClass": "hazardClass"
                        },
                        "netExplosiveDetail": {
                          "amount": 10,
                          "units": "units",
                          "type": "NET_EXPLOSIVE_WEIGHT"
                        },
                        "massPoints": 2
                      }
                    ]
                  }
                ],
                "cargoAircraftOnly": true,
                "referenceId": "123456",
                "radioactiveTransportIndex": 2.45
              }
            }
          ],
          "operationalDetail": {
            "originServiceArea": "A1",
            "serviceCode": "010",
            "airportId": "DFW",
            "postalCode": "38010",
            "scac": "scac",
            "deliveryDay": "TUE",
            "originLocationId": "678",
            "countryCode": "US",
            "astraDescription": "SMART POST",
            "originLocationNumber": 243,
            "deliveryDate": "2001-04-05",
            "deliveryEligibilities": [
              "deliveryEligibilities"
            ],
            "ineligibleForMoneyBackGuarantee": true,
            "maximumTransitTime": "SEVEN_DAYS",
            "destinationLocationStateOrProvinceCode": "GA",
            "astraPlannedServiceLevel": "TUE - 15 OCT 10:30A",
            "destinationLocationId": "DALA",
            "transitTime": "TWO_DAYS",
            "stateOrProvinceCode": "GA",
            "destinationLocationNumber": 876,
            "packagingCode": "03",
            "commitDate": "2019-10-15",
            "publishedDeliveryTime": "10:30A",
            "ursaSuffixCode": "Ga",
            "ursaPrefixCode": "XH",
            "destinationServiceArea": "A1",
            "commitDay": "TUE",
            "customTransitTime": "ONE_DAY"
          },
          "carrierCode": "FDXE",
          "completedHoldAtLocationDetail": {
            "holdingLocationType": "FEDEX_STAFFED",
            "holdingLocation": {
              "address": {
                "streetLines": [
                  "10 FedEx Parkway",
                  "Suite 302"
                ],
                "city": "Beverly Hills",
                "stateOrProvinceCode": "CA",
                "postalCode": "38127",
                "countryCode": "US",
                "residential": false
              },
              "contact": {
                "personName": "John Taylor",
                "tollFreePhoneNumber": "6127812",
                "emailAddress": "sample@company.com",
                "phoneNumber": "1234567890",
                "phoneExtension": "91",
                "faxNumber": "1234567890",
                "pagerNumber": "6127812",
                "companyName": "Fedex",
                "title": "title"
              }
            }
          },
          "completedEtdDetail": {
            "folderId": "0b0493e580dc1a1b",
            "type": "COMMERCIAL_INVOICE",
            "uploadDocumentReferenceDetails": [
              {
                "documentType": "PRO_FORMA_INVOICE",
                "documentReference": "DocumentReference",
                "description": "PRO FORMA INVOICE",
                "documentId": "090927d680038c61"
              }
            ]
          },
          "packagingDescription": "description",
          "masterTrackingId": {
            "formId": "0201",
            "trackingIdType": "EXPRESS",
            "uspsApplicationId": "92",
            "trackingNumber": "49092000070120032835"
          },
          "serviceDescription": {
            "serviceType": "FEDEX_1_DAY_FREIGHT",
            "code": "80",
            "names": [
              {
                "type": "long",
                "encoding": "UTF-8",
                "value": "F-2"
              }
            ],
            "operatingOrgCodes": [
              "FXE"
            ],
            "astraDescription": "2 DAY FRT",
            "description": "description",
            "serviceId": "EP1000000027",
            "serviceCategory": "freight"
          },
          "usDomestic": true,
          "hazardousShipmentDetail": {
            "hazardousSummaryDetail": {
              "smallQuantityExceptionPackageCount": 10
            },
            "adrLicense": {
              "licenseOrPermitDetail": {
                "number": "12345",
                "effectiveDate": "2019-08-09",
                "expirationDate": "2019-04-09"
              }
            },
            "dryIceDetail": {
              "totalWeight": {
                "units": "KG",
                "value": 68
              },
              "packageCount": 10,
              "processingOptions": {
                "options": [
                  "options"
                ]
              }
            }
          },
          "shipmentRating": {
            "actualRateType": "PAYOR_LIST_SHIPMENT",
            "shipmentRateDetails": [
              {
                "rateZone": "US001O",
                "ratedWeightMethod": "ACTUAL",
                "totalDutiesTaxesAndFees": 24.56,
                "pricingCode": "LTL_FREIGHT",
                "totalFreightDiscounts": 1.56,
                "totalTaxes": 3.45,
                "totalDutiesAndTaxes": 6.78,
                "totalAncillaryFeesAndTaxes": 5.67,
                "taxes": [
                  {
                    "amount": 10,
                    "level": "level",
                    "description": "description",
                    "type": "type"
                  }
                ],
                "totalRebates": 1.98,
                "fuelSurchargePercent": 4.56,
                "currencyExchangeRate": {
                  "rate": 25.6,
                  "fromCurrency": "Rupee",
                  "intoCurrency": "USD"
                },
                "totalNetFreight": 9.56,
                "totalNetFedExCharge": 88.56,
                "shipmentLegRateDetails": [
                  {
                    "rateZone": "rateZone",
                    "pricingCode": "pricingCode",
                    "taxes": [
                      {
                        "amount": 10,
                        "level": "level",
                        "description": "description",
                        "type": "type"
                      }
                    ],
                    "totalDimWeight": {
                      "units": "KG",
                      "value": 68
                    },
                    "totalRebates": 2,
                    "fuelSurchargePercent": 6,
                    "currencyExchangeRate": {
                      "rate": 25.6,
                      "fromCurrency": "Rupee",
                      "intoCurrency": "USD"
                    },
                    "dimDivisor": 6,
                    "rateType": "PAYOR_RETAIL_PACKAGE",
                    "legDestinationLocationId": "legDestinationLocationId",
                    "dimDivisorType": "dimDivisorType",
                    "totalBaseCharge": 6,
                    "ratedWeightMethod": "ratedWeightMethod",
                    "totalFreightDiscounts": 9,
                    "totalTaxes": 12.6,
                    "minimumChargeType": "minimumChargeType",
                    "totalDutiesAndTaxes": 17.78,
                    "totalNetFreight": 6,
                    "totalNetFedExCharge": 3.2,
                    "surcharges": [
                      {
                        "amount": "string",
                        "surchargeType": "APPOINTMENT_DELIVERY",
                        "level": "PACKAGE, or SHIPMENT",
                        "description": "description"
                      }
                    ],
                    "totalSurcharges": 5,
                    "totalBillingWeight": {
                      "units": "KG",
                      "value": 68
                    },
                    "freightDiscounts": [
                      {
                        "amount": 8.9,
                        "rateDiscountType": "COUPON",
                        "percent": 28.9,
                        "description": "description"
                      }
                    ],
                    "rateScale": "6702",
                    "totalNetCharge": 253,
                    "totalNetChargeWithDutiesAndTaxes": 25.67,
                    "currency": "USD"
                  }
                ],
                "dimDivisor": 0,
                "rateType": "RATED_ACCOUNT_SHIPMENT",
                "surcharges": [
                  {
                    "amount": "string",
                    "surchargeType": "APPOINTMENT_DELIVERY",
                    "level": "PACKAGE, or SHIPMENT",
                    "description": "description"
                  }
                ],
                "totalSurcharges": 9.88,
                "totalBillingWeight": {
                  "units": "KG",
                  "value": 68
                },
                "freightDiscounts": [
                  {
                    "amount": 8.9,
                    "rateDiscountType": "COUPON",
                    "percent": 28.9,
                    "description": "description"
                  }
                ],
                "rateScale": "00000",
                "totalNetCharge": 3.78,
                "totalBaseCharge": 234.56,
                "totalNetChargeWithDutiesAndTaxes": 222.56,
                "currency": "USD"
              }
            ]
          },
          "documentRequirements": {
            "requiredDocuments": [
              "COMMERCIAL_OR_PRO_FORMA_INVOICE",
              "AIR_WAYBILL"
            ],
            "prohibitedDocuments": [
              "CERTIFICATE_OF_ORIGIN"
            ],
            "generationDetails": [
              {
                "type": "COMMERCIAL_INVOICE",
                "minimumCopiesRequired": 3,
                "letterhead": "OPTIONAL",
                "electronicSignature": "OPTIONAL"
              }
            ]
          },
          "exportComplianceStatement": "12345678901234567",
          "accessDetail": {
            "accessorDetails": [
              {
                "password": "password",
                "role": "role",
                "emailLabelUrl": "emailLabelUrl",
                "userId": "userId"
              }
            ]
          }
        },
        "shipmentAdvisoryDetails": {
          "regulatoryAdvisory": {
            "prohibitions": [
              {
                "derivedHarmonizedCode": "01",
                "advisory": {
                  "code": "code",
                  "text": "Text",
                  "parameters": [
                    {
                      "id": "message ID",
                      "value": "Message value"
                    }
                  ],
                  "localizedText": "localizedText"
                },
                "commodityIndex": 12,
                "source": "source",
                "categories": [
                  "categories"
                ],
                "type": "type",
                "waiver": {
                  "advisories": [
                    {
                      "code": "code",
                      "text": "Text",
                      "parameters": [
                        {
                          "id": "message ID",
                          "value": "Message value"
                        }
                      ],
                      "localizedText": "localizedText"
                    }
                  ],
                  "description": "description",
                  "id": "id"
                },
                "status": "status"
              }
            ]
          }
        },
        "masterTrackingNumber": "794953535000"
      }
    ],
    "alerts": [
      {
        "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
        "alertType": "NOTE",
        "message": "Recipient Postal-City Mismatch."
      }
    ],
    "jobId": "abc123456"
  }
}
"""

ShipmentCancelResponse = """{
  "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "customerTransactionId": "AnyCo_order123456789",
  "output": {
    "cancelledShipment": true,
    "cancelledHistory": true,
    "successMessage": "Success",
    "alerts": [
      {
        "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
        "alertType": "NOTE",
        "message": "Recipient Postal-City Mismatch."
      }
    ]
  }
}
"""
