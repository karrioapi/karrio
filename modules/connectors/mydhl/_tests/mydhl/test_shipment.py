import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLExpressShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
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
    "service": "carrier_service",
    "options": {
        "signature_required": True,
    },
    "reference": "#Order 11111",
}


ParsedShipmentResponse = []


ShipmentRequest = {
    "plannedShippingDateAndTime": "2022-10-19T19:19:40 GMT+00:00",
    "pickup": {"isRequested": False},
    "productCode": "P",
    "localProductCode": "P",
    "getRateEstimates": False,
    "accounts": [{"typeCode": "shipper", "number": "123456789"}],
    "valueAddedServices": [{"serviceCode": "II", "value": 10, "currency": "USD"}],
    "outputImageProperties": {
        "printerDPI": 300,
        "encodingFormat": "pdf",
        "imageOptions": [
            {
                "typeCode": "invoice",
                "templateName": "COMMERCIAL_INVOICE_P_10",
                "isRequested": True,
                "invoiceType": "commercial",
                "languageCode": "eng",
                "languageCountryCode": "US",
            },
            {
                "typeCode": "waybillDoc",
                "templateName": "ARCH_8x4",
                "isRequested": True,
                "hideAccountNumber": False,
                "numberOfCopies": 1,
            },
            {
                "typeCode": "label",
                "templateName": "ECOM26_84_001",
                "renderDHLLogo": True,
                "fitLabelsToA4": False,
            },
        ],
        "splitTransportAndWaybillDocLabels": True,
        "allDocumentsInOneImage": False,
        "splitDocumentsByPages": False,
        "splitInvoiceAndReceipt": True,
        "receiptAndLabelsInOneImage": False,
    },
    "customerDetails": {
        "shipperDetails": {
            "postalAddress": {
                "postalCode": "526238",
                "cityName": "Zhaoqing",
                "countryCode": "CN",
                "addressLine1": "4FENQU, 2HAOKU, WEIPINHUI WULIU YUAN，DAWANG",
                "addressLine2": "GAOXIN QU, BEIJIANG DADAO, SIHUI,",
                "addressLine3": "ZHAOQING, GUANDONG",
                "countyName": "SIHUI",
                "countryName": "CHINA, PEOPLES REPUBLIC",
            },
            "contactInformation": {
                "email": "shipper_create_shipmentapi@dhltestmail.com",
                "phone": "18211309039",
                "mobilePhone": "18211309039",
                "companyName": "Cider BookStore",
                "fullName": "LiuWeiMing",
            },
            "registrationNumbers": [
                {"typeCode": "SDT", "number": "CN123456789", "issuerCountryCode": "CN"}
            ],
            "bankDetails": [
                {
                    "name": "Bank of China",
                    "settlementLocalCurrency": "RMB",
                    "settlementForeignCurrency": "USD",
                }
            ],
            "typeCode": "business",
        },
        "receiverDetails": {
            "postalAddress": {
                "cityName": "Graford",
                "countryCode": "US",
                "postalCode": "76449",
                "addressLine1": "116 Marine Dr",
                "countryName": "UNITED STATES OF AMERICA",
            },
            "contactInformation": {
                "email": "recipient_create_shipmentapi@dhltestmail.com",
                "phone": "9402825665",
                "mobilePhone": "9402825666",
                "companyName": "Baylee Marshall",
                "fullName": "Baylee Marshall",
            },
            "registrationNumbers": [
                {"typeCode": "SSN", "number": "US123456789", "issuerCountryCode": "US"}
            ],
            "bankDetails": [
                {
                    "name": "Bank of America",
                    "settlementLocalCurrency": "USD",
                    "settlementForeignCurrency": "USD",
                }
            ],
            "typeCode": "business",
        },
    },
    "content": {
        "packages": [
            {
                "typeCode": "2BP",
                "weight": 0.5,
                "dimensions": {"length": 1, "width": 1, "height": 1},
                "customerReferences": [{"value": "3654673", "typeCode": "CU"}],
                "description": "Piece content description",
                "labelDescription": "bespoke label description",
            }
        ],
        "isCustomsDeclarable": True,
        "declaredValue": 120,
        "declaredValueCurrency": "USD",
        "exportDeclaration": {
            "lineItems": [
                {
                    "number": 1,
                    "description": "Harry Steward biography first edition",
                    "price": 15,
                    "quantity": {"value": 4, "unitOfMeasurement": "GM"},
                    "commodityCodes": [
                        {"typeCode": "outbound", "value": "84713000"},
                        {"typeCode": "inbound", "value": "5109101110"},
                    ],
                    "exportReasonType": "permanent",
                    "manufacturerCountry": "US",
                    "exportControlClassificationNumber": "US123456789",
                    "weight": {"netValue": 0.1, "grossValue": 0.7},
                    "isTaxesPaid": True,
                    "additionalInformation": ["450pages"],
                    "customerReferences": [{"typeCode": "AFE", "value": "1299210"}],
                    "customsDocuments": [
                        {"typeCode": "COO", "value": "MyDHLAPI - LN#1-CUSDOC-001"}
                    ],
                },
                {
                    "number": 2,
                    "description": "Andromeda Chapter 394 - Revenge of Brook",
                    "price": 15,
                    "quantity": {"value": 4, "unitOfMeasurement": "GM"},
                    "commodityCodes": [
                        {"typeCode": "outbound", "value": "6109100011"},
                        {"typeCode": "inbound", "value": "5109101111"},
                    ],
                    "exportReasonType": "permanent",
                    "manufacturerCountry": "US",
                    "exportControlClassificationNumber": "US123456789",
                    "weight": {"netValue": 0.1, "grossValue": 0.7},
                    "isTaxesPaid": True,
                    "additionalInformation": ["36pages"],
                    "customerReferences": [{"typeCode": "AFE", "value": "1299211"}],
                    "customsDocuments": [
                        {"typeCode": "COO", "value": "MyDHLAPI - LN#1-CUSDOC-001"}
                    ],
                },
            ],
            "invoice": {
                "number": "2667168671",
                "date": "2022-10-22",
                "instructions": ["Handle with care"],
                "totalNetWeight": 0.4,
                "totalGrossWeight": 0.5,
                "customerReferences": [
                    {"typeCode": "UCN", "value": "UCN-783974937"},
                    {"typeCode": "CN", "value": "CUN-76498376498"},
                    {"typeCode": "RMA", "value": "MyDHLAPI-TESTREF-001"},
                ],
                "termsOfPayment": "100 days",
                "indicativeCustomsValues": {
                    "importCustomsDutyValue": 150.57,
                    "importTaxesValue": 49.43,
                },
            },
            "remarks": [{"value": "Right side up only"}],
            "additionalCharges": [
                {"value": 10, "caption": "fee", "typeCode": "freight"},
                {"value": 20, "caption": "freight charges", "typeCode": "other"},
                {"value": 10, "caption": "ins charges", "typeCode": "insurance"},
                {"value": 7, "caption": "rev charges", "typeCode": "reverse_charge"},
            ],
            "destinationPortName": "New York Port",
            "placeOfIncoterm": "ShenZhen Port",
            "payerVATNumber": "12345ED",
            "recipientReference": "01291344",
            "exporter": {"id": "121233", "code": "S"},
            "packageMarks": "Fragile glass bottle",
            "declarationNotes": [{"value": "up to three declaration notes"}],
            "exportReference": "export reference",
            "exportReason": "export reason",
            "exportReasonType": "permanent",
            "licenses": [{"typeCode": "export", "value": "123127233"}],
            "shipmentType": "personal",
            "customsDocuments": [{"typeCode": "INV", "value": "MyDHLAPI - CUSDOC-001"}],
        },
        "description": "Shipment",
        "USFilingTypeValue": "12345",
        "incoterm": "DAP",
        "unitOfMeasurement": "metric",
    },
    "shipmentNotification": [
        {
            "typeCode": "email",
            "receiverId": "shipmentnotification@mydhlapisample.com",
            "languageCode": "eng",
            "languageCountryCode": "UK",
            "bespokeMessage": "message to be included in the notification",
        }
    ],
    "getTransliteratedResponse": False,
    "estimatedDeliveryDate": {"isRequested": True, "typeCode": "QDDC"},
    "getAdditionalInformation": [{"typeCode": "pickupDetails", "isRequested": True}],
}


ShipmentResponse = """{
  "shipmentTrackingNumber": "5374534616",
  "trackingUrl": "https://expressapi.dhl.com/mydhlapi/shipments/5374534616/tracking",
  "packages": [
    {
      "referenceNumber": 1,
      "trackingNumber": "JD014600004617230711",
      "trackingUrl": "https://expressapi.dhl.com/mydhlapi/shipments/5374534616/tracking?pieceTrackingNumber=JD014600004617230711"
    },
    {
      "referenceNumber": 2,
      "trackingNumber": "JD014600004617230712",
      "trackingUrl": "https://expressapi.dhl.com/mydhlapi/shipments/5374534616/tracking?pieceTrackingNumber=JD014600004617230712"
    },
    {
      "referenceNumber": 3,
      "trackingNumber": "JD014600004617230713",
      "trackingUrl": "https://expressapi.dhl.com/mydhlapi/shipments/5374534616/tracking?pieceTrackingNumber=JD014600004617230713"
    }
  ],
  "documents": [
    {
      "imageFormat": "PDF",
      "content": "JVBERi0xLjQKJeLjz9MKNCAwIG9iago8PC9GaWx0ZXIvRmxhdGVEZWNv",
      "typeCode": "label",
      "packageReferenceNumber": 1
    },
    {
      "imageFormat": "PDF",
      "content": "JVBERi0xLjQKJeLjz9MKNCAwIG9iago8PC9GaWx0ZXdGVEZWNvZGUvTGVuZ",
      "typeCode": "label",
      "packageReferenceNumber": 2
    },
    {
      "imageFormat": "PDF",
      "content": "JVBERi0xLjQKJeLjz9MKNCAwIG9iago8PC9GaWx0ZXGVEZWNvZGUvACgQCtwYL",
      "typeCode": "label",
      "packageReferenceNumber": 3
    },
    {
      "imageFormat": "PDF",
      "content": "JVBERi0xLjQKJeLjz9MNvZGUvACgo8PC9GaWx0ZXGVEZWNvZGUvACgQCtwYL",
      "typeCode": "waybillDoc"
    },
    {
      "imageFormat": "PDF",
      "content": "JVBERi0xLjQKJeLjz9MKNiAwIG9i8PC9GaWx0ZXIvRmxhdGVEZWNvZGUvTG",
      "typeCode": "invoice"
    }
  ],
  "shipmentDetails": [
    {
      "pickupDetails": {
        "localCutoffDateAndTime": "2022-12-12T19:00:00",
        "gmtCutoffTime": "21:00:00",
        "cutoffTimeOffset": "PT2H",
        "pickupEarliest": "09:30:00",
        "pickupLatest": "21:00:00",
        "totalTransitDays": "3",
        "pickupAdditionalDays": "0",
        "deliveryAdditionalDays": "0",
        "pickupDayOfWeek": "1",
        "deliveryDayOfWeek": "4"
      }
    }
  ],
  "estimatedDeliveryDate": {
    "estimatedDeliveryDate": "2022-12-15T23:59:00Z",
    "estimatedDeliveryType": "QDDC"
  }
}
"""
