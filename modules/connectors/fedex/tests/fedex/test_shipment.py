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

    def test_create_multi_piece_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.MultiPieceShipmentRequest)

        self.assertEqual(request.serialize(), MultiPieceShipmentRequest)

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
                f"{gateway.settings.server_url}/ship/v1/shipments",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/ship/v1/shipments/cancel",
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
    "options": {
        "currency": "USD",
        "shipment_date": "2024-02-15",
    },
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
    "options": {
        "currency": "USD",
        "paperless_trade": True,
        "shipment_date": "2024-02-17",
    },
}

ShipmentCancelPayload = {"shipment_identifier": "794953555571"}

ParsedShipmentResponse = [
    {
        "carrier_id": "fedex",
        "carrier_name": "fedex",
        "docs": {"label": ANY},
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=794953535000",
            "serviceCategory": "EXPRESS",
            "service_name": "fedex_standard_overnight",
            "trackingIdType": "FEDEX",
        },
        "shipment_identifier": "794953535000",
        "tracking_number": "794953535000",
    },
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
            "details": {},
            "message": "Recipient Postal-City Mismatch.",
        }
    ],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "fedex",
        "carrier_name": "fedex",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
            "details": {},
            "message": "Recipient Postal-City Mismatch.",
        }
    ],
]


ShipmentRequest = [
    {
        "accountNumber": {"value": "2349857"},
        "labelResponseOptions": "LABEL",
        "requestedShipment": {
            "customsClearanceDetail": {
                "commercialInvoice": {
                    "customerReferences": [
                        {
                            "customerReferenceType": "INVOICE_NUMBER",
                            "value": "123456789",
                        }
                    ],
                    "originatorName": "Input Your Information",
                    "termsOfSale": "DDU",
                },
                "commodities": [
                    {
                        "countryOfManufacture": "US",
                        "description": "test",
                        "harmonizedCode": "00339BB",
                        "numberOfPieces": 1,
                        "quantity": 1,
                        "quantityUnits": "PCS",
                        "weight": {"units": "LB", "value": 10.0},
                    }
                ],
                "dutiesPayment": {
                    "paymentType": "SENDER",
                    "payor": {
                        "responsibleParty": {
                            "address": {
                                "city": "MEMPHIS",
                                "countryCode": "US",
                                "postalCode": "38117",
                                "residential": False,
                                "stateOrProvinceCode": "TN",
                                "streetLines": [
                                    "Input Your Information",
                                    "Input Your Information",
                                ],
                            },
                            "contact": {
                                "companyName": "Input Your Information",
                                "emailAddress": "Input Your Information",
                                "personName": "Input Your Information",
                                "phoneNumber": "Input Your Information",
                            },
                        }
                    },
                },
                "isDocumentOnly": False,
            },
            "labelSpecification": {
                "imageType": "PDF",
                "labelFormatType": "COMMON2D",
                "labelOrder": "SHIPPING_LABEL_FIRST",
                "labelStockType": "STOCK_4X6",
            },
            "packagingType": "YOUR_PACKAGING",
            "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
            "preferredCurrency": "USD",
            "recipients": [
                {
                    "address": {
                        "city": "RICHMOND",
                        "countryCode": "CA",
                        "postalCode": "V7C4v7",
                        "residential": False,
                        "stateOrProvinceCode": "BC",
                        "streetLines": [
                            "Input Your Information",
                            "Input Your Information",
                        ],
                    },
                    "contact": {
                        "companyName": "Input Your Information",
                        "emailAddress": "Input Your Information",
                        "personName": "Input Your Information",
                        "phoneNumber": "Input Your Information",
                    },
                }
            ],
            "requestedPackageLineItems": [
                {
                    "dimensions": {
                        "height": 12.0,
                        "length": 12.0,
                        "units": "IN",
                        "width": 12.0,
                    },
                    "packageSpecialServices": {
                        "signatureOptionType": "SERVICE_DEFAULT",
                        "specialServiceTypes": ["SIGNATURE_OPTION"],
                    },
                    "sequenceNumber": 1,
                    "subPackagingType": "OTHER",
                    "weight": {"units": "LB", "value": 20.0},
                }
            ],
            "serviceType": "FEDEX_INTERNATIONAL_PRIORITY",
            "shipDatestamp": "2024-02-15",
            "shipper": {
                "address": {
                    "city": "MEMPHIS",
                    "countryCode": "US",
                    "postalCode": "38117",
                    "residential": False,
                    "stateOrProvinceCode": "TN",
                    "streetLines": ["Input Your Information", "Input Your Information"],
                },
                "contact": {
                    "companyName": "Input Your Information",
                    "emailAddress": "Input Your Information",
                    "personName": "Input Your Information",
                    "phoneNumber": "Input Your Information",
                },
            },
            "shippingChargesPayment": {
                "paymentType": "THIRD_PARTY",
                "payor": {"responsibleParty": {"accountNumber": "2349857"}},
            },
            "shippingDocumentSpecification": {
                "shippingDocumentTypes": ["COMMERCIAL_INVOICE"]
            },
            "totalPackageCount": 1,
            "totalWeight": 20.0,
        },
        "shipAction": "CONFIRM",
    }
]

MultiPieceShipmentRequest = [
    {
        "accountNumber": {"value": "2349857"},
        "labelResponseOptions": "LABEL",
        "requestedShipment": {
            "customsClearanceDetail": {
                "commercialInvoice": {
                    "customerReferences": [
                        {
                            "customerReferenceType": "INVOICE_NUMBER",
                            "value": "123456789",
                        }
                    ],
                    "originatorName": "Input " "Your " "Information",
                    "termsOfSale": "DDU",
                },
                "commodities": [
                    {
                        "countryOfManufacture": "US",
                        "description": "test",
                        "harmonizedCode": "00339BB",
                        "numberOfPieces": 1,
                        "quantity": 1,
                        "quantityUnits": "PCS",
                        "weight": {"units": "LB", "value": 10.0},
                    }
                ],
                "dutiesPayment": {
                    "paymentType": "SENDER",
                    "payor": {
                        "responsibleParty": {
                            "address": {
                                "city": "MEMPHIS",
                                "countryCode": "US",
                                "postalCode": "38117",
                                "residential": False,
                                "stateOrProvinceCode": "TN",
                                "streetLines": [
                                    "Input " "Your " "Information",
                                    "Input " "Your " "Information",
                                ],
                            },
                            "contact": {
                                "companyName": "Input " "Your " "Information",
                                "emailAddress": "Input " "Your " "Information",
                                "personName": "Input " "Your " "Information",
                                "phoneNumber": "Input " "Your " "Information",
                            },
                        }
                    },
                },
                "isDocumentOnly": False,
            },
            "labelSpecification": {
                "imageType": "PDF",
                "labelFormatType": "COMMON2D",
                "labelOrder": "SHIPPING_LABEL_FIRST",
                "labelStockType": "STOCK_4X6",
            },
            "packagingType": "YOUR_PACKAGING",
            "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
            "preferredCurrency": "USD",
            "recipients": [
                {
                    "address": {
                        "city": "RICHMOND",
                        "countryCode": "CA",
                        "postalCode": "V7C4v7",
                        "residential": False,
                        "stateOrProvinceCode": "BC",
                        "streetLines": [
                            "Input " "Your " "Information",
                            "Input " "Your " "Information",
                        ],
                    },
                    "contact": {
                        "companyName": "Input Your Information",
                        "emailAddress": "Input " "Your " "Information",
                        "personName": "Input Your Information",
                        "phoneNumber": "Input Your Information",
                    },
                }
            ],
            "requestedPackageLineItems": [
                {
                    "dimensions": {
                        "height": 12.0,
                        "length": 12.0,
                        "units": "IN",
                        "width": 12.0,
                    },
                    "packageSpecialServices": {
                        "signatureOptionType": "SERVICE_DEFAULT",
                        "specialServiceTypes": ["SIGNATURE_OPTION"],
                    },
                    "sequenceNumber": 1,
                    "subPackagingType": "OTHER",
                    "weight": {"units": "LB", "value": 1.0},
                }
            ],
            "serviceType": "FEDEX_INTERNATIONAL_PRIORITY",
            "shipDatestamp": "2024-02-17",
            "shipmentSpecialServices": {
                "etdDetail": {
                    "attributes": ["POST_SHIPMENT_UPLOAD_REQUESTED"],
                    "requestedDocumentTypes": ["COMMERCIAL_INVOICE"],
                },
                "specialServiceTypes": ["ELECTRONIC_TRADE_DOCUMENTS"],
            },
            "shipper": {
                "address": {
                    "city": "MEMPHIS",
                    "countryCode": "US",
                    "postalCode": "38117",
                    "residential": False,
                    "stateOrProvinceCode": "TN",
                    "streetLines": [
                        "Input Your Information",
                        "Input Your Information",
                    ],
                },
                "contact": {
                    "companyName": "Input Your Information",
                    "emailAddress": "Input Your Information",
                    "personName": "Input Your Information",
                    "phoneNumber": "Input Your Information",
                },
            },
            "shippingChargesPayment": {
                "paymentType": "THIRD_PARTY",
                "payor": {"responsibleParty": {"accountNumber": "2349857"}},
            },
            "totalPackageCount": 2,
            "totalWeight": 1.0,
        },
        "shipAction": "CONFIRM",
    },
    {
        "accountNumber": {"value": "2349857"},
        "labelResponseOptions": "LABEL",
        "requestedShipment": {
            "customsClearanceDetail": {
                "commercialInvoice": {
                    "customerReferences": [
                        {
                            "customerReferenceType": "INVOICE_NUMBER",
                            "value": "123456789",
                        }
                    ],
                    "originatorName": "Input " "Your " "Information",
                    "termsOfSale": "DDU",
                },
                "commodities": [
                    {
                        "countryOfManufacture": "US",
                        "description": "test",
                        "harmonizedCode": "00339BB",
                        "numberOfPieces": 1,
                        "quantity": 1,
                        "quantityUnits": "PCS",
                        "weight": {"units": "LB", "value": 10.0},
                    }
                ],
                "dutiesPayment": {
                    "paymentType": "SENDER",
                    "payor": {
                        "responsibleParty": {
                            "address": {
                                "city": "MEMPHIS",
                                "countryCode": "US",
                                "postalCode": "38117",
                                "residential": False,
                                "stateOrProvinceCode": "TN",
                                "streetLines": [
                                    "Input " "Your " "Information",
                                    "Input " "Your " "Information",
                                ],
                            },
                            "contact": {
                                "companyName": "Input " "Your " "Information",
                                "emailAddress": "Input " "Your " "Information",
                                "personName": "Input " "Your " "Information",
                                "phoneNumber": "Input " "Your " "Information",
                            },
                        }
                    },
                },
                "isDocumentOnly": False,
            },
            "labelSpecification": {
                "imageType": "PDF",
                "labelFormatType": "COMMON2D",
                "labelOrder": "SHIPPING_LABEL_FIRST",
                "labelStockType": "STOCK_4X6",
            },
            "masterTrackingId": {
                "trackingIdType": "[MASTER_ID_TYPE]",
                "trackingNumber": "[MASTER_TRACKING_ID]",
            },
            "packagingType": "YOUR_PACKAGING",
            "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
            "preferredCurrency": "USD",
            "recipients": [
                {
                    "address": {
                        "city": "RICHMOND",
                        "countryCode": "CA",
                        "postalCode": "V7C4v7",
                        "residential": False,
                        "stateOrProvinceCode": "BC",
                        "streetLines": [
                            "Input " "Your " "Information",
                            "Input " "Your " "Information",
                        ],
                    },
                    "contact": {
                        "companyName": "Input Your Information",
                        "emailAddress": "Input " "Your " "Information",
                        "personName": "Input Your Information",
                        "phoneNumber": "Input Your Information",
                    },
                }
            ],
            "requestedPackageLineItems": [
                {
                    "dimensions": {
                        "height": 11.0,
                        "length": 11.0,
                        "units": "IN",
                        "width": 11.0,
                    },
                    "packageSpecialServices": {
                        "signatureOptionType": "SERVICE_DEFAULT",
                        "specialServiceTypes": ["SIGNATURE_OPTION"],
                    },
                    "sequenceNumber": 2,
                    "subPackagingType": "OTHER",
                    "weight": {"units": "LB", "value": 2.0},
                }
            ],
            "serviceType": "FEDEX_INTERNATIONAL_PRIORITY",
            "shipDatestamp": "2024-02-17",
            "shipmentSpecialServices": {
                "etdDetail": {
                    "attributes": ["POST_SHIPMENT_UPLOAD_REQUESTED"],
                    "requestedDocumentTypes": ["COMMERCIAL_INVOICE"],
                },
                "specialServiceTypes": ["ELECTRONIC_TRADE_DOCUMENTS"],
            },
            "shipper": {
                "address": {
                    "city": "MEMPHIS",
                    "countryCode": "US",
                    "postalCode": "38117",
                    "residential": False,
                    "stateOrProvinceCode": "TN",
                    "streetLines": [
                        "Input Your Information",
                        "Input Your Information",
                    ],
                },
                "contact": {
                    "companyName": "Input Your Information",
                    "emailAddress": "Input Your Information",
                    "personName": "Input Your Information",
                    "phoneNumber": "Input Your Information",
                },
            },
            "shippingChargesPayment": {
                "paymentType": "THIRD_PARTY",
                "payor": {"responsibleParty": {"accountNumber": "2349857"}},
            },
            "totalPackageCount": 2,
            "totalWeight": 2.0,
        },
        "shipAction": "CONFIRM",
    },
]

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
            "contentType": "LABEL",
            "trackingNumber": "794953535000",
            "docType": "PDF",
            "encodedLabel": "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMyAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL091dGxpbmVzCi9Db3VudCAwCj4+CmVuZG9iagozIDAgb2JqCjw8Ci9UeXBlIC9QYWdlcwovQ291bnQgMwovS2lkcyBbMTggMCBSIDE5IDAgUiAyMCAwIFJdCj4+CmVuZG9iago0IDAgb2JqClsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXQplbmRvYmoKNSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iago2IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0hlbHZldGljYS1Cb2xkCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKNyAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EtT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjggMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhLUJvbGRPYmxpcXVlCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKOSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9Db3VyaWVyCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTAgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1Cb2xkCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTEgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1PYmxpcXVlCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTIgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1Cb2xkT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjEzIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLVJvbWFuCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTQgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvVGltZXMtQm9sZAovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjE1IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLUl0YWxpYwovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjE2IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLUJvbGRJdGFsaWMKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iagoxNyAwIG9iaiAKPDwKL0NyZWF0aW9uRGF0ZSAoRDoyMDAzKQovUHJvZHVjZXIgKEZlZEV4IFNlcnZpY2VzKQovVGl0bGUgKEZlZEV4IFNoaXBwaW5nIExhYmVsKQ0vQ3JlYXRvciAoRmVkRXggQ3VzdG9tZXIgQXV0b21hdGlvbikNL0F1dGhvciAoQ0xTIFZlcnNpb24gNTEyMDEzNSkKPj4KZW5kb2JqCjE4IDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMSAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjE5IDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMiAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjIwIDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMiAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjIxIDAgb2JqCjw8IC9MZW5ndGggMjYwNwovRmlsdGVyIFsvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGVdIAo+PgpzdHJlYW0KR2F0PS45bGpPSigjPHJOcnJGcTMsYiJRSVxAQjxYWyVnJUNWQl86XjhCWFJQUmw1NyZTVS9eRlBMZTJpaFpMTV1STl9gZSs7XjQnbCtEKGYKTWk3SDVjalozczUiOk0qYGVsL3BFUjlUXSRwKj1XKCw9ZVcudWdJbGR0Y1ckYlM5TUJpOz89aSJUTDRPMyVcdEU9J21eS3M1P1RsXVNzPjQKXClQPT0uaVUxSCR0NFkkaDxcYCw/NWFSLm1kRHJPQ0E1SzIxKCNILTFkOiZZQkhPO1lrMjZxUClYWnRROVJYNnFddC46J3EvMUo7Slw3RFMKTTglZ0VBJSgxYzEpZGk9XVVeXllQcWFGWUFGRWo7aHU5amM/TCdoUUlCRWZiLCFJLzBrRnJIXi9KZEEzXVw9RUlPTVswRixpbS9cbyEwLD8KUlM1SyhwM1ZbaF4zUjNkbC5gKm1bQHRaJF5MVlcxUUFlaGAqREVuZ3EhTHAqLExQW289TSpgVWoqYyk8b1o6R2E0LSVVJSNLKTw4Nix0SXMKcnIpWlttZXMzQltESyNQcVgybUZGU1tcYGBUbGphPiQ6XkdyaiooIXA/YmRGVz1eJS0nIWRSTzokLFNVTi1pRXNqaV9GXiMpT0NLW1BDUEMKLCRQUWZnMmpASE51KWc+XCooOVlTNDJEXEEvbXR0NjhaXnNNcmpwKlBiX3BNMyJUX1gkLyJRJUM9KU8mNydrXWYrYUEpLT09OVtjcF4kW1AKQkA+SykyKVw1JWQ8ayY6IV9NSyJbU24wJiM4SHVyIW8jWlEpTWQtSUs9L2U3M2VGUVo0OkVpdDdXcl9RbFwxP0RlRTEzNEM6LipDYFYjO0wKXlJfISo4ITFWODZSKDxrIm0lSFYoNWcvO1QrUi83X3RwWmloSj9OJWVSR2t0TjkxXSRrM0AtXUUnSVVHbm4lXDlFcEVBa104LC5tQzpoKjIKYj02dTFBPyEzXyVORzAwQXBxO0dYVCxCUTJlbSZFcShMXF42TWNqQGYoMCdoMXF0Ry5mbC40YjJsalBQWzldcE9iRC5rZCQnbzhLZismQj0KNnQzPlJaR1c9bmxjOCs1XChbcTYvVWgnTmtaU2tfPlFQazU2Vy9oODduJjIxPyFaaWBnUllwRmhebjZHRjgzQE5EZyFURiU5SFVJUDNbYDQKbilkaklcOXMiJmxVUVolV1QtISlkY11IUFlmTUQ1bCZWI3RAcz5oXUM0aVE0a1YjIzRxZC10S3FyKTghXydIIz1GZSE2U2k1Zmtycmc5WFQKNEVBXTE4LWZzJHBfN2tRRUBHQTU5Jy1dXFNSOSQ8TGtrY2JqY1xkUyIqMFktPVdZVW4zL0NaTTBtY2xjSFRqX3VWRExxRmc9WkFkVXFyIjUKJTUrO1s2M1g3Y3FlU2AjTDUoWzlWUDE3LWNFWjhBTFNAbFAlLl5aXFVEJyJucypRYFo1K0BzPSxcOCw6LFg5Oi47PXQ2MVNbcVhTQ0MvWkMKUyJePCpwLixDTktJZUgyVkNqWD80ISFUSS0qL0NrMms5UE5tMDVQal5pNkVlOUVGSDgpc11mXCxgdWkoWWxkVWJXX05gTC4+LmxNIjMlPGwKLEZPOV0hVUROXExFWV91YFpSOVAxaDZxcWhlWitAcSVUKnVoaDdObyVASWpbLj4tMHFnWCdbPFt0XmZPSyktYFQ+LEdRLlluYD1vVnI7ODcKWERfQ1dTUVpVMWtPQmFVME1vVklCLVgxQClSMlNkQmduTChlcm8hZGpiQVpGWi5xOE1dc2JwO2xSRjNeRF9lN1gzPmonTFRONFM3UXFSaFAKUF9sMCEmdSI+czlzKihfWVdlSV83bE1fNWkoOWRYQipxVjFTIldnKWRjOlBJNmkwPWMtdC5OYSEiR1lxIkdDJ09YUFQ9PCQxIiZpLlZiR1MKMk1lW1JGQSZLXW9yU1luZTwkXlAkXExFU2k4ZG4vJEVkSU8lUTZJP0Q4SVJII1xZTmNjWVEoK0VSaC4lRk1Yb1Q9dWxoaTtvaz5XbzA/SGsKQDEnK0NRKzEtRDJgZSY1TjlaK3JpPF42KGs2ZFY6XHVfMFE/UDZTRzp1WE5LNnJTZVJAbC9wLjJzUHIkWSZkJ2M3OEBpXCVCOllbJVpPRm4KXzAram1IbnEmN1U+U2JpWis1XWA+YzZbN2lkSURxZGxzRSFbWSt1bVZcIVVXSGpbYUlVKDxQanJEQ0UoJEpGc3JMSyFOISh1KkohS2xxXEMKYk1cUkg3cyQ/OltxYGVmWSM+VXM7RzlrLFNpXW88WFZFPSpTVkQyPEdDP0R0WG4sOTU1IjUuJWA6OXFTK2ZJKVhFaGJnc2kmWlFncjhpb2wKZ3U4b0QpV2FeI2xdbWtKcFJHbjJSKEFdPjhtSjlVOVA5YzxrVy9GYj4rWkdaLyopRilPUlUjOE5rTUU1JEw8dDZpdXNtTi5IajpSTUpzbEUKO15nI1ZZVD1nRUYwOmVwJDxYTFVGRjQxY1VObEw7alRtMDg7XmUqblMwIzpvbFA4RixBTmMza1ZjTk9qX0tvZTFmVlNFLUxfMClcTl9uYTMKS0YhOFMtLU0yaSldPVc9aiVRQWhvYTpOQkFQb0NpTzEoPj0uXyY0c1VXN3VsQElzWV4/MGRgVGA6WEpKbltVVjEhRmcqcEMwLEFmNj1GdD4KJlBDU2pDY0hWQmYtcytQMD1fW05VTHVwZGUuPSpMXWc9SlxRdCgxPypPcUE5LyVBPXRYJTBXLllRZ1tsYjhFb1dZN000PyViNGIuOnVYTUgKQDtRaUNbdCJJNT8vSVtcV1NmZ01gKUMuZWAwY2U1PXJYb2dGajtEa1RrPUVEKyxxX1ddV1QxcWMzVkJzZXJTUCNLajFILy0qNlJySnQqcEQKXio5NlA1V1JKWzNKRFVFJUUyXmklIT1zYlBSXXJeMThoP09VTm1jPWZIUSpIaGU0Myw9QSghdU0+NjxeYiVVYkdRQTU+LGpLKExNZ2AxM0cKZTw6RE0+Q0QhS2RGKEQpblgrRitoVkcwMy5uLEJsTzZZdSM9ZChbaktkRGstciswP09eOUxxVDpCSDBQMTUrblw5WUBdYlxobmdXa0stXF0KZ0dWOlBEOlBTai8jJGtnYUktL2xHU2w/QjU8YVMrNGVbdVYlSWw5US1tXCYhX2w9UTZtSyJccUonWEBjX3RYaiI2K1luckhiKmNyU2VRVz0KUkFwRiFwJShbJUosIVVOSDI3OENUMEUySFJwLF9OcWBdIiYyZltxRCVLUz5aX29eZjU7SWgxV24mUF5TMkVFLzI2b09RZCVuJWFSJ18xQiMKMTlEaSVpUEc/OystQj9QVHAnQmdvKU1YLiwrcUtocjdiUkNyVll0Nys4IVc3Py9OM1hGZUhmMElMM25PZURSPTIxXkI1WjhMTSM5ZzdbbzEKaHU+TGNtSmxTS1M4QX4+CmVuZHN0cmVhbQplbmRvYmoKMjIgMCBvYmoKPDwgL0xlbmd0aCAzMDY0Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0gCj4+CnN0cmVhbQpHYXQ9Lj1gWUxsKDROLzJzNT9yNVFeTGguZEQjKykhSU1vP2ZPTldURWJmIS1FJG82KUJGZzNEcFhlO3QoPDAhPzI2QTMqTD5eREBlKEtmMwozb1YiWFh1NjJoYGFmM1pQUjhSaVYkNzNTJF8rR0dnY09MUTVkWipxPGwtXWwoWSFIXUhbZUF1NWxSVVgtMDUqbCE8bilULitoNSheRVNnUApWKEpBSiJFUjVaPSQ/Pz9pYkVLcFJETkxhczg5cTUhLltaa0xrI0FsczRuWFdNMz1pZVBsLjVkPkptQmhdODdcbEBLbk5pMllVPyUuPjBvWApUaE4+bW1iOz8mI0lAXFA9a3AjST1lNVFJXF4oNk5IKnM3NFdxQUhAKmxGP1RgSUNUQEpiMmd0RSVpO2sjNEdxWnBpZiMnbztxWWgtSCZOTgooazNTOFplbSpyMEgwJDQ0dHVxRDBQLj5UNnQyYj0yWDFDQGBcOHAtSSIqc0wxdVtfMkJKSC9nXFtpOG9VOF9bJEM5RSs6SFddTUFTPUchRwpeZTZzRmY+a2c8SUAlXkBwLTJuaD9OR1c+aVdkQzVEVEsjMXMlYSNEMSQrKnNTbG05ZFZwQXFFPDFERGdnUTVKJVRfO2NeYVlaNTdbcjZoVwojK3RHIVA7cjkjSiJrOTJBW2FAZExRaVlibzorNEElaUIhYGcvcEJZTm5acGtOW0VxcTUmZzNvVzFWa1xuQFk1VUYmNm0+UkQvXFxeXWhIWAooKDVGQic/M1VBPT1fZWU+aTgzYTxVWyRBX1QyNF9aLFFZPyNmXWJPPkJpQz9tZko0aWhHRCtcI0FqOWBfX1YyVWNgJyhrRnU7SS9XRTRcJgolVmQiW2NIXWZVU3JVZmwwQGQ8LjsuTGJFPCxgN2UuZSklcCpFIk4pQk9SIWFPZTUjTVg3YzQtXWoiSE9SLGBQKEJkJlU5ajdQNF5DKmcqWQo0STZuIUhPNmE6M29tSUkhQCI+cllaOzkoRCk7WS1qYkc3MXFfZlBCRV0+IVhPM2NfaTdNZGJsYU1DbVM8XSknSFMvcj02SDkwMGcsRklURgo0KGRzPkhNMENeNnFGLD1xWy44KzJRZFpWYkcuOk9cWHJjcUNDO1NNI1ZYLk4tSl9kN0pEITpVKlNfV1k4ZnIsQSooSnVBT1M1bSM+PCItawpoJlNPZD07PERXTGsmO1JUKm82LzotdE9dZWQ6OlVMIV0hTDcpKXFGUSYjNThrXGNQdDxdYnBPNz9QcWhxIWs1WjFdRiprOD1WO1tGKklaNwomdEtRNitBQy5LMEYjXVpeIkprXCVsUSI/WUU6VDhLZColQk0qZV4/LUQmV11DRjIidWIhbjJwXmddRFdVTCYzaiU0Qjo4Y1FiNUhCOlUzbwo4OmQkVjY1NzNdQzg8WiVYYT1KXFVtL2xUUl1uVWk3UGFER1ZRUSg5LSY7Zz9LbENiN0EsRC1QVjhBQks9TiFdMT1KQTo7XTNmMj9PPTVXUAplND0vakxUVFFuKUEyTDohMSdSR2FfWFx0WGpnT0FSI0BFOzFgaTA2Tk11R1NFRltCTS5TTFBuLHIwSjQrNSIqTWEnLi4lOyVvODosUEdJcApMPipgRjlTQjtNOThgcTUvaUdSLFtvSm1HUixPTDw3IickJVcrMixsTWNqTSpOJHMzTEBtW1EpbyxXVF1CYmNVUTsjbHAnX3FSJkQmMicpOgpxKD4kUzEoZks3KGY6czRhSjFRSFtHYWFsOTo6YnNdYDlUOGsoTkQxYUpjT0g4PGIlVEJ1ODxqT2opLW0qJSxuVWQ0L1JyISVhNjsjRmFCOQo3UyMuSyxaVT40NmwrYFtPOWtjZGxTJnA+LTdtRCdkXjg6XyFFYmRTTVlKZ0QnVW1mXC02a28lPmFlLT5bSF9vOT1KQTolW2tXVGNOKyMrRQpcbTU8JWFKNC9tRTM6WS1uZUs5PSElYThRcUJncnJMTkFaOFEwXEslTkNXSG5MKXM6R2FEQFs/IkNQcWBUUzkhQFY4UnRFMGNRZyNURyJZMAo0dSFvQlBtZ2haW1JZJksnIidHWDAtbkg0OVhvc19YVS5ZTGB0NGpZYmFpaVBhczBhcEowamRVPG8jLCc5Qjs0YS8mZUc0PUdVT2E+UitZbgo0PVpRP0QqaERHQVQ1KnVpRyQuQUgkISkqVVRBRnAxUVJnSyElYThRW2NxZyw8KkU3Km1jUWcyVjhETEcsPz4yZmReNjloY2BRMFc6aF9XbAosPFNcJiwqMjxaVlpfSFlRJk5wMCFFYylQOVdLM05KPkppcjBSbkM5L0AxKWtYczgqRmRfbUgnPTpqRklLNihnZjBYNXBFX1BRTy49dURyYQovc1UvTktMQUghcW9WJ0hOQSo1ME0rajAxJSlFRi5tNnVvIjonIlRMJzVRLmY2RmFzaUUwI1I/IktmJnNBZ1YtJyElcTghajdjRmc6PiFkdApNTXRYXD5VZ0Q1XG0/b00jKCpfNmpcbC9HYU1fYm1gWVpMZzE5amxeMDgpdTBnKW8hYGJeVCEqJFh1ZSg+W20lU201JVhaLl8vUzJiMStBKwpsPUJpSl07PFhvNFAla0hcM3VtdDU2SmBMXzMpTionKF0kJVFbNmUrSHEqKmI3KE5VU1ohJjNhVikjI05TJDNHVmVVI2cwJCVBb2FmLj5BKAo2YiNPVCJEYCxzKHJFKylNMD5GREo0akk6bTVlWVVRY2MsWUZpIiwyUS0jWVQ6YEw7QTJgMHMjLTgoUypxTVxzPjtnODNSZVoiQnVJO1p0Wgo9YSdzViJEPiIyaTtiRSssOlZDP18jUSpROGMqbkIpWV1ANlgnMUldTStiNEhfQTFGRGNjKTtPPmZZaElKNG5CYG0xMWRmaSVcM08qWlA+awowcVM+Qmk4RDlgQ145Vk8uJHFwbEJuPFAsVUxbJT4iW20jM21VWCNjL0xER0ZwPHAxJ1teXEdVNCM+ZE1RL0VRJFYkKjBgcWQjRTdCY2wmOQorYCdAJklaY1MkXD1WaGFUQWZfL1prKCVUNWA9QU4hST0lcjo+PT1MQThqU2FPK1hlKUVQSiFRVm4yckhsV0pbVjUnck1gY21XaXIpZypzcApAP0xCX0AzOSkoV09xWU9VIlcpblpPNzAwbzAtRW1kVCFYJjw7QSpsRmx1QzliRGIuLm4/MVE0MFgiTlhsPzlGOlBoVURkLypELUJDMD50NQpHUiliJ1thZ2AjTygpJilOdFFyLDVPWVl0WS5USEFScWdKYipSXmkkUSw2dWNDL2lOS15LOztdIllBNSRiaWRPPVtUTGs8RU8hLS5oOyc7KwonWHQtXkhFbDpDTVleQiFWWXA6LT1iIzQ9U1gpVi5tJUtSW2dzUC5nSFoudWFwTiFVQkRgKE8xak91YDNZKEN0Tk1kZC49aVduN1dXazY1VwokYWA4KkJMMC1XMlZbNF1RU2w7OTpBI08wbi5AKk9qNkckbEdfImZRSVlnO0BbcUxvYycjJURWXmlmVSpbK0Q+M21VMEA7YjpQN11YMldAJQpYT0JmPiknbm9XYWI+KSdtJEciRzRkVilfIiZyWGNVcUE5PGA9ZzBUbWwwP08kWFlTTVE1K2thcFkwXmtlMCtMcj07PjE5WnMmZj1FMStDYwpiJDsuMVUmJ01LR2RrMWlUal1eRElKYEAhRWtaVWRFPDFaX0VvRHE9aTBMVkkjKDhHZl1vJWQ8VjZwMjgkY0BQO0QwbGw3XWVRYV4mOEFdJgpIY01ZODgpbUIhXDJmPCZgVDpfbEskMUxqP29IJDZfL0tnSC45cDFhJXRFPjRybUx1OW0lMi5cQV9eY0wwOixlMi5lKEUuaiFfI01bP2E4cApBZWlOa1xCc2VpcjpBPVlVVDQnRFBEK2JdWktfdG5GaydaWzU5YiwwOWwnJCVATEJHNztKXVE0ZW0/U1FiQWU+Ymw2YEc8bUxtJVtcLTIxOwpPTHFHbj9fMlVhT287aTZTPkQ4JCRDRSIwKGRXL1ZgaiFTQ29gJyJicVpDPzJbR2xSZyxMKl5kSFcwaGFxVlxOKX4+CmVuZHN0cmVhbQplbmRvYmoKMjMgMCBvYmoKPDwgL1R5cGUgL1hPYmplY3QKL1N1YnR5cGUgL0ltYWdlCi9XaWR0aCAxMTgKL0hlaWdodCA0OQovQ29sb3JTcGFjZSAvRGV2aWNlR3JheQovQml0c1BlckNvbXBvbmVudCA4Ci9MZW5ndGggNDYxCi9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiL2VKSV1SPyNYblhrVDZBPlhLbkRiV0IiTVpFYWpQcGQ0XScoXkBSbHQia0IiUzAkZiU/PW09NEM7Oy4kTihqUmNZUiVzZCZsOSRPdF4KKSY3PUwoNy1lcXFlQC4oL1NDOTg0LWZMWGVMWjVxY1o1bEFFQjU1PjNAMD1rIjtSaDJoQmNRTDMmSj81b1tjSDBiU0ZOXjw7O0A0MVNZOW0KYyJaST1ZbCNjNClgXyJZbG1OMyUuQS5sTlNgVmUvWTwlPy43KCgpLy5kQls7ayFKWyUnJURKXEk/K2E3OjVvTmtZXHFFUz4zPEk1YlptKEkKJWQ8QEIpOERidDNwS0djbGJRazEnaVpWczdOTTBcbyZSKnFVPmdIdS1GckNraDxrSEZHKlwkTT1fc1YvLSRcSkY6ZS8/PmZYQStDQ21wRGUKZFNQNkdjdSxcWCdBTD1hNUpDWzQ2Ry5ocDI9VTRlXiRlb1xRI2IqbTdDOCQtSkEoY1o/WWAnQzs2SnBIZVBsXCRIRUMhdV4qUWErNmdFTWsKW2ZFVipiLiM+cHI+LVdTZiM+aCZXP3Vra1RzaFlgPS9YLjY2QSo7YmlzL2RnQFFYWHNyOG07fj4KZW5kc3RyZWFtCmVuZG9iagoyNCAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDU0Ci9IZWlnaHQgNTQKL0NvbG9yU3BhY2UgL0RldmljZUdyYXkKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDc3Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiMEpkMFRkcSRqNG9GXlUsIkhUczlFSUU7MEFULF9FKkxaJW9AN0psNVY7SCdDcz1UcnFEYUguNEJmI2M0T1ZUOyhkI2Y8R0U5fj4KZW5kc3RyZWFtCmVuZG9iagoyNSAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDI3NwovSGVpZ2h0IDczCi9Db2xvclNwYWNlIC9EZXZpY2VHcmF5Ci9CaXRzUGVyQ29tcG9uZW50IDgKL0xlbmd0aCAxMzk0Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiL2NnUSE0LSRxJ2pqNUwjcFpHdTY9I0g/JWghJFonRWs9WCZuTU9vK0xPY1gvbXImKVZsP0ttSitFbkU5ISNrSSNwOTYyYy02LE11dUEKb0ZaSG08JnBIZ1NgJEAobS03LVVRKDckSV1fSl5ZU0E3bScpQiY5LVo7Oz1aNT03Xj5KZEhedFRxcWYqXz1JLWQqb0BVWjpjT1soIWFJTGEKYjByalFXUDslUFhjP3M8cFRbTzFiI0trUEVgdUVCV1xKUl47dVxrPjRSVjlmNGdoIjYzSnU2ZUgtQit1QzE8IjdpVVdbU1cqOllYalpjIygKQjdfQFpCWmM1T1w8cEQ8Q0RrTmVMYTE3O0o+TV5qMmovMWUrJV9sLTctSStaV1U0NCkvWDFzMCZXMEsiUElwOWZWPyYpSUMqWkNiNWtrZ1MKL1JgMGlGNkNibS4/RyZQJiZMRnNVKkZsWlVgbSpBKDxaWi9pb1lEWmFdL2phJ1I5Jjk5SUhLVF8uVTA4LzZlZ1NBZkI8NF9dQT8jO1wsJi0KIkQiZkBrJTVDTzZGZDhyXW8ldU1hOCdFcXEmTS5hOFxgJFRpciMvdCwvO1NWMFAiOjkkX2VuNFBpaVhFUW4hY1BeLyxUZjlkaEJkJ0kuZUEKUW9QISkmMj42IUUqKlgrVTtcbWBKYWVhRyUiY3BdMidaNV9dTUtEVUc2WVpVKDxUbzJCbXMjdDlZbG5uWG83IzMkJDAhbSluLFJQYGApcm8KN09gNT5LYjcrdCYyJFRST0M0YjVQXFgpYCs/PStmLXJtc10yQj0/bzJXWnVgVmBHbjdrYG4sdFVJYjtzckJxRUw3NjJdIyFTYGMoRGtTX0gKWCYrc1lyVFw7PU1MRD1cZCp1S2ZWWXRmKkUjS0A8bFRbO24vbjNNLyw+LSFZQmpoKm41Vjg0U0VaJ2FlUC1Hb14pSCdwI1cvNHJuRTQraTEKK0lCRlA1Uys0PThGOSU3Tyo6ZipuM0otYTc2MmIzYiFOV0hWKWhGK21iLC1VLUU5U05oST4sVSo8LkdtcC0pMiQvLztJOm4+W2I3cUljKDYKcElAI05UZSlHY0s3YFliUFRmZERhbiNLbVBdV145KDZqbGNMQlFlVzdxTCMjPDNlNW8rPC0pNGNsNFR1XFwoYFNiJm8qRUAnYytqam1aUCoKNE5nRkdFXiQmOi4mXyVQRkBONWQ1dSFgR1Y2bylVS0c3OCsmW1A6TGIlMnRRNC9DbF9OTltXI3A/XkxqNCRtVlZTZCZOMCwzPUA4J0xRKHQKTGBuZWAvWXM4aiwlbSVQOl9xMnItbWRjPVhYNSY+OiNZO24+LipHcGZtVyc8OE9fRWtsPSkkTi9HRCtRSFhyWD5HLCVpYUtzRlBDNjVfLE0KQD8yXic5Mk1JVz8kZ2s1aEQ+YGtuOzFPLSViazVuXVteOj5QX0YsaWIzM3ErW249OCFibkBBbGViMltVU2NoT0VrXVdpV189KCQxOjM4KTsKIklWbHFLNDFOK1BsNjxBOmk4Uyg0PSc1cChjV2RCQmQtZSNgMVdoOzs6QXQzQ3Q+YURLQklQaWNdKzMyXTtnXTRXWEVDM2drPFBMMnFnLHMKJG5FSDJqP14haFMrUztVTGR0U2pAYV9fYjtsQGprRlxvPUs1PCgxUSRzP3BjJGZzLi5abUE9dD47X0UpRzVjNzkocyokJFZCITA2WyEoLGUKLVUzTFJKbCQwWFxKT1loQjYtdSsoV28oVCMsVD0qLVVkPiU8V3FTXmVqKyUrZWRqXksiVnNIMi5wSCZXYT5sdUxOMDRPWUo0TkJoZz9DcSwKLi9zS19UPElEX1AkQCc0fj4KZW5kc3RyZWFtCmVuZG9iagoyNiAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDExOAovSGVpZ2h0IDQ5Ci9Db2xvclNwYWNlIC9EZXZpY2VHcmF5Ci9CaXRzUGVyQ29tcG9uZW50IDgKL0xlbmd0aCA0NjEKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIvZUpJXVI/I1huWGtUNkE+WEtuRGJXQiJNWkVhalBwZDRdJyheQFJsdCJrQiJTMCRmJT89bT00Qzs7LiROKGpSY1lSJXNkJmw5JE90XgopJjc9TCg3LWVxcWVALigvU0M5ODQtZkxYZUxaNXFjWjVsQUVCNTU+M0AwPWsiO1JoMmhCY1FMMyZKPzVvW2NIMGJTRk5ePDs7QDQxU1k5bQpjIlpJPVlsI2M0KWBfIllsbU4zJS5BLmxOU2BWZS9ZPCU/LjcoKCkvLmRCWztrIUpbJSclREpcST8rYTc6NW9Oa1lccUVTPjM8STViWm0oSQolZDxAQik4RGJ0M3BLR2NsYlFrMSdpWlZzN05NMFxvJlIqcVU+Z0h1LUZyQ2toPGtIRkcqXCRNPV9zVi8tJFxKRjplLz8+ZlhBK0NDbXBEZQpkU1A2R2N1LFxYJ0FMPWE1SkNbNDZHLmhwMj1VNGVeJGVvXFEjYiptN0M4JC1KQShjWj9ZYCdDOzZKcEhlUGxcJEhFQyF1XipRYSs2Z0VNawpbZkVWKmIuIz5wcj4tV1NmIz5oJlc/dWtrVHNoWWA9L1guNjZBKjtiaXMvZGdAUVhYc3I4bTt+PgplbmRzdHJlYW0KZW5kb2JqCjI3IDAgb2JqCjw8IC9UeXBlIC9YT2JqZWN0Ci9TdWJ0eXBlIC9JbWFnZQovV2lkdGggNTQKL0hlaWdodCA1NAovQ29sb3JTcGFjZSAvRGV2aWNlR3JheQovQml0c1BlckNvbXBvbmVudCA4Ci9MZW5ndGggNzcKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIwSmQwVGRxJGo0b0ZeVSwiSFRzOUVJRTswQVQsX0UqTFolb0A3Smw1VjtIJ0NzPVRycURhSC40QmYjYzRPVlQ7KGQjZjxHRTl+PgplbmRzdHJlYW0KZW5kb2JqCnhyZWYKMCAyOAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA1OCAwMDAwMCBuIAowMDAwMDAwMTA0IDAwMDAwIG4gCjAwMDAwMDAxNzYgMDAwMDAgbiAKMDAwMDAwMDIyOCAwMDAwMCBuIAowMDAwMDAwMzI2IDAwMDAwIG4gCjAwMDAwMDA0MjkgMDAwMDAgbiAKMDAwMDAwMDUzNSAwMDAwMCBuIAowMDAwMDAwNjQ1IDAwMDAwIG4gCjAwMDAwMDA3NDEgMDAwMDAgbiAKMDAwMDAwMDg0MyAwMDAwMCBuIAowMDAwMDAwOTQ4IDAwMDAwIG4gCjAwMDAwMDEwNTcgMDAwMDAgbiAKMDAwMDAwMTE1OCAwMDAwMCBuIAowMDAwMDAxMjU4IDAwMDAwIG4gCjAwMDAwMDEzNjAgMDAwMDAgbiAKMDAwMDAwMTQ2NiAwMDAwMCBuIAowMDAwMDAxNjM2IDAwMDAwIG4gCjAwMDAwMDIwNTMgMDAwMDAgbiAKMDAwMDAwMjQ3MCAwMDAwMCBuIAowMDAwMDAyODg3IDAwMDAwIG4gCjAwMDAwMDU1ODYgMDAwMDAgbiAKMDAwMDAwODc0MiAwMDAwMCBuIAowMDAwMDA5Mzg5IDAwMDAwIG4gCjAwMDAwMDk2NTAgMDAwMDAgbiAKMDAwMDAxMTIzMSAwMDAwMCBuIAowMDAwMDExODc4IDAwMDAwIG4gCnRyYWlsZXIKPDwKL0luZm8gMTcgMCBSCi9TaXplIDI4Ci9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgoxMjEzOQolJUVPRgo=",
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
                "contentType": "LABEL",
                "trackingNumber": "794953535000",
                "docType": "PDF",
                "alerts": [
                  {
                    "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
                    "alertType": "NOTE",
                    "message": "Recipient Postal-City Mismatch."
                  }
                ],
                "encodedLabel": "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMyAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL091dGxpbmVzCi9Db3VudCAwCj4+CmVuZG9iagozIDAgb2JqCjw8Ci9UeXBlIC9QYWdlcwovQ291bnQgMwovS2lkcyBbMTggMCBSIDE5IDAgUiAyMCAwIFJdCj4+CmVuZG9iago0IDAgb2JqClsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXQplbmRvYmoKNSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iago2IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0hlbHZldGljYS1Cb2xkCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKNyAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EtT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjggMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhLUJvbGRPYmxpcXVlCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKOSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9Db3VyaWVyCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTAgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1Cb2xkCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTEgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1PYmxpcXVlCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTIgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1Cb2xkT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjEzIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLVJvbWFuCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTQgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvVGltZXMtQm9sZAovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjE1IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLUl0YWxpYwovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjE2IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLUJvbGRJdGFsaWMKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iagoxNyAwIG9iaiAKPDwKL0NyZWF0aW9uRGF0ZSAoRDoyMDAzKQovUHJvZHVjZXIgKEZlZEV4IFNlcnZpY2VzKQovVGl0bGUgKEZlZEV4IFNoaXBwaW5nIExhYmVsKQ0vQ3JlYXRvciAoRmVkRXggQ3VzdG9tZXIgQXV0b21hdGlvbikNL0F1dGhvciAoQ0xTIFZlcnNpb24gNTEyMDEzNSkKPj4KZW5kb2JqCjE4IDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMSAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjE5IDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMiAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjIwIDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMiAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjIxIDAgb2JqCjw8IC9MZW5ndGggMjYwNwovRmlsdGVyIFsvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGVdIAo+PgpzdHJlYW0KR2F0PS45bGpPSigjPHJOcnJGcTMsYiJRSVxAQjxYWyVnJUNWQl86XjhCWFJQUmw1NyZTVS9eRlBMZTJpaFpMTV1STl9gZSs7XjQnbCtEKGYKTWk3SDVjalozczUiOk0qYGVsL3BFUjlUXSRwKj1XKCw9ZVcudWdJbGR0Y1ckYlM5TUJpOz89aSJUTDRPMyVcdEU9J21eS3M1P1RsXVNzPjQKXClQPT0uaVUxSCR0NFkkaDxcYCw/NWFSLm1kRHJPQ0E1SzIxKCNILTFkOiZZQkhPO1lrMjZxUClYWnRROVJYNnFddC46J3EvMUo7Slw3RFMKTTglZ0VBJSgxYzEpZGk9XVVeXllQcWFGWUFGRWo7aHU5amM/TCdoUUlCRWZiLCFJLzBrRnJIXi9KZEEzXVw9RUlPTVswRixpbS9cbyEwLD8KUlM1SyhwM1ZbaF4zUjNkbC5gKm1bQHRaJF5MVlcxUUFlaGAqREVuZ3EhTHAqLExQW289TSpgVWoqYyk8b1o6R2E0LSVVJSNLKTw4Nix0SXMKcnIpWlttZXMzQltESyNQcVgybUZGU1tcYGBUbGphPiQ6XkdyaiooIXA/YmRGVz1eJS0nIWRSTzokLFNVTi1pRXNqaV9GXiMpT0NLW1BDUEMKLCRQUWZnMmpASE51KWc+XCooOVlTNDJEXEEvbXR0NjhaXnNNcmpwKlBiX3BNMyJUX1gkLyJRJUM9KU8mNydrXWYrYUEpLT09OVtjcF4kW1AKQkA+SykyKVw1JWQ8ayY6IV9NSyJbU24wJiM4SHVyIW8jWlEpTWQtSUs9L2U3M2VGUVo0OkVpdDdXcl9RbFwxP0RlRTEzNEM6LipDYFYjO0wKXlJfISo4ITFWODZSKDxrIm0lSFYoNWcvO1QrUi83X3RwWmloSj9OJWVSR2t0TjkxXSRrM0AtXUUnSVVHbm4lXDlFcEVBa104LC5tQzpoKjIKYj02dTFBPyEzXyVORzAwQXBxO0dYVCxCUTJlbSZFcShMXF42TWNqQGYoMCdoMXF0Ry5mbC40YjJsalBQWzldcE9iRC5rZCQnbzhLZismQj0KNnQzPlJaR1c9bmxjOCs1XChbcTYvVWgnTmtaU2tfPlFQazU2Vy9oODduJjIxPyFaaWBnUllwRmhebjZHRjgzQE5EZyFURiU5SFVJUDNbYDQKbilkaklcOXMiJmxVUVolV1QtISlkY11IUFlmTUQ1bCZWI3RAcz5oXUM0aVE0a1YjIzRxZC10S3FyKTghXydIIz1GZSE2U2k1Zmtycmc5WFQKNEVBXTE4LWZzJHBfN2tRRUBHQTU5Jy1dXFNSOSQ8TGtrY2JqY1xkUyIqMFktPVdZVW4zL0NaTTBtY2xjSFRqX3VWRExxRmc9WkFkVXFyIjUKJTUrO1s2M1g3Y3FlU2AjTDUoWzlWUDE3LWNFWjhBTFNAbFAlLl5aXFVEJyJucypRYFo1K0BzPSxcOCw6LFg5Oi47PXQ2MVNbcVhTQ0MvWkMKUyJePCpwLixDTktJZUgyVkNqWD80ISFUSS0qL0NrMms5UE5tMDVQal5pNkVlOUVGSDgpc11mXCxgdWkoWWxkVWJXX05gTC4+LmxNIjMlPGwKLEZPOV0hVUROXExFWV91YFpSOVAxaDZxcWhlWitAcSVUKnVoaDdObyVASWpbLj4tMHFnWCdbPFt0XmZPSyktYFQ+LEdRLlluYD1vVnI7ODcKWERfQ1dTUVpVMWtPQmFVME1vVklCLVgxQClSMlNkQmduTChlcm8hZGpiQVpGWi5xOE1dc2JwO2xSRjNeRF9lN1gzPmonTFRONFM3UXFSaFAKUF9sMCEmdSI+czlzKihfWVdlSV83bE1fNWkoOWRYQipxVjFTIldnKWRjOlBJNmkwPWMtdC5OYSEiR1lxIkdDJ09YUFQ9PCQxIiZpLlZiR1MKMk1lW1JGQSZLXW9yU1luZTwkXlAkXExFU2k4ZG4vJEVkSU8lUTZJP0Q4SVJII1xZTmNjWVEoK0VSaC4lRk1Yb1Q9dWxoaTtvaz5XbzA/SGsKQDEnK0NRKzEtRDJgZSY1TjlaK3JpPF42KGs2ZFY6XHVfMFE/UDZTRzp1WE5LNnJTZVJAbC9wLjJzUHIkWSZkJ2M3OEBpXCVCOllbJVpPRm4KXzAram1IbnEmN1U+U2JpWis1XWA+YzZbN2lkSURxZGxzRSFbWSt1bVZcIVVXSGpbYUlVKDxQanJEQ0UoJEpGc3JMSyFOISh1KkohS2xxXEMKYk1cUkg3cyQ/OltxYGVmWSM+VXM7RzlrLFNpXW88WFZFPSpTVkQyPEdDP0R0WG4sOTU1IjUuJWA6OXFTK2ZJKVhFaGJnc2kmWlFncjhpb2wKZ3U4b0QpV2FeI2xdbWtKcFJHbjJSKEFdPjhtSjlVOVA5YzxrVy9GYj4rWkdaLyopRilPUlUjOE5rTUU1JEw8dDZpdXNtTi5IajpSTUpzbEUKO15nI1ZZVD1nRUYwOmVwJDxYTFVGRjQxY1VObEw7alRtMDg7XmUqblMwIzpvbFA4RixBTmMza1ZjTk9qX0tvZTFmVlNFLUxfMClcTl9uYTMKS0YhOFMtLU0yaSldPVc9aiVRQWhvYTpOQkFQb0NpTzEoPj0uXyY0c1VXN3VsQElzWV4/MGRgVGA6WEpKbltVVjEhRmcqcEMwLEFmNj1GdD4KJlBDU2pDY0hWQmYtcytQMD1fW05VTHVwZGUuPSpMXWc9SlxRdCgxPypPcUE5LyVBPXRYJTBXLllRZ1tsYjhFb1dZN000PyViNGIuOnVYTUgKQDtRaUNbdCJJNT8vSVtcV1NmZ01gKUMuZWAwY2U1PXJYb2dGajtEa1RrPUVEKyxxX1ddV1QxcWMzVkJzZXJTUCNLajFILy0qNlJySnQqcEQKXio5NlA1V1JKWzNKRFVFJUUyXmklIT1zYlBSXXJeMThoP09VTm1jPWZIUSpIaGU0Myw9QSghdU0+NjxeYiVVYkdRQTU+LGpLKExNZ2AxM0cKZTw6RE0+Q0QhS2RGKEQpblgrRitoVkcwMy5uLEJsTzZZdSM9ZChbaktkRGstciswP09eOUxxVDpCSDBQMTUrblw5WUBdYlxobmdXa0stXF0KZ0dWOlBEOlBTai8jJGtnYUktL2xHU2w/QjU8YVMrNGVbdVYlSWw5US1tXCYhX2w9UTZtSyJccUonWEBjX3RYaiI2K1luckhiKmNyU2VRVz0KUkFwRiFwJShbJUosIVVOSDI3OENUMEUySFJwLF9OcWBdIiYyZltxRCVLUz5aX29eZjU7SWgxV24mUF5TMkVFLzI2b09RZCVuJWFSJ18xQiMKMTlEaSVpUEc/OystQj9QVHAnQmdvKU1YLiwrcUtocjdiUkNyVll0Nys4IVc3Py9OM1hGZUhmMElMM25PZURSPTIxXkI1WjhMTSM5ZzdbbzEKaHU+TGNtSmxTS1M4QX4+CmVuZHN0cmVhbQplbmRvYmoKMjIgMCBvYmoKPDwgL0xlbmd0aCAzMDY0Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0gCj4+CnN0cmVhbQpHYXQ9Lj1gWUxsKDROLzJzNT9yNVFeTGguZEQjKykhSU1vP2ZPTldURWJmIS1FJG82KUJGZzNEcFhlO3QoPDAhPzI2QTMqTD5eREBlKEtmMwozb1YiWFh1NjJoYGFmM1pQUjhSaVYkNzNTJF8rR0dnY09MUTVkWipxPGwtXWwoWSFIXUhbZUF1NWxSVVgtMDUqbCE8bilULitoNSheRVNnUApWKEpBSiJFUjVaPSQ/Pz9pYkVLcFJETkxhczg5cTUhLltaa0xrI0FsczRuWFdNMz1pZVBsLjVkPkptQmhdODdcbEBLbk5pMllVPyUuPjBvWApUaE4+bW1iOz8mI0lAXFA9a3AjST1lNVFJXF4oNk5IKnM3NFdxQUhAKmxGP1RgSUNUQEpiMmd0RSVpO2sjNEdxWnBpZiMnbztxWWgtSCZOTgooazNTOFplbSpyMEgwJDQ0dHVxRDBQLj5UNnQyYj0yWDFDQGBcOHAtSSIqc0wxdVtfMkJKSC9nXFtpOG9VOF9bJEM5RSs6SFddTUFTPUchRwpeZTZzRmY+a2c8SUAlXkBwLTJuaD9OR1c+aVdkQzVEVEsjMXMlYSNEMSQrKnNTbG05ZFZwQXFFPDFERGdnUTVKJVRfO2NeYVlaNTdbcjZoVwojK3RHIVA7cjkjSiJrOTJBW2FAZExRaVlibzorNEElaUIhYGcvcEJZTm5acGtOW0VxcTUmZzNvVzFWa1xuQFk1VUYmNm0+UkQvXFxeXWhIWAooKDVGQic/M1VBPT1fZWU+aTgzYTxVWyRBX1QyNF9aLFFZPyNmXWJPPkJpQz9tZko0aWhHRCtcI0FqOWBfX1YyVWNgJyhrRnU7SS9XRTRcJgolVmQiW2NIXWZVU3JVZmwwQGQ8LjsuTGJFPCxgN2UuZSklcCpFIk4pQk9SIWFPZTUjTVg3YzQtXWoiSE9SLGBQKEJkJlU5ajdQNF5DKmcqWQo0STZuIUhPNmE6M29tSUkhQCI+cllaOzkoRCk7WS1qYkc3MXFfZlBCRV0+IVhPM2NfaTdNZGJsYU1DbVM8XSknSFMvcj02SDkwMGcsRklURgo0KGRzPkhNMENeNnFGLD1xWy44KzJRZFpWYkcuOk9cWHJjcUNDO1NNI1ZYLk4tSl9kN0pEITpVKlNfV1k4ZnIsQSooSnVBT1M1bSM+PCItawpoJlNPZD07PERXTGsmO1JUKm82LzotdE9dZWQ6OlVMIV0hTDcpKXFGUSYjNThrXGNQdDxdYnBPNz9QcWhxIWs1WjFdRiprOD1WO1tGKklaNwomdEtRNitBQy5LMEYjXVpeIkprXCVsUSI/WUU6VDhLZColQk0qZV4/LUQmV11DRjIidWIhbjJwXmddRFdVTCYzaiU0Qjo4Y1FiNUhCOlUzbwo4OmQkVjY1NzNdQzg8WiVYYT1KXFVtL2xUUl1uVWk3UGFER1ZRUSg5LSY7Zz9LbENiN0EsRC1QVjhBQks9TiFdMT1KQTo7XTNmMj9PPTVXUAplND0vakxUVFFuKUEyTDohMSdSR2FfWFx0WGpnT0FSI0BFOzFgaTA2Tk11R1NFRltCTS5TTFBuLHIwSjQrNSIqTWEnLi4lOyVvODosUEdJcApMPipgRjlTQjtNOThgcTUvaUdSLFtvSm1HUixPTDw3IickJVcrMixsTWNqTSpOJHMzTEBtW1EpbyxXVF1CYmNVUTsjbHAnX3FSJkQmMicpOgpxKD4kUzEoZks3KGY6czRhSjFRSFtHYWFsOTo6YnNdYDlUOGsoTkQxYUpjT0g4PGIlVEJ1ODxqT2opLW0qJSxuVWQ0L1JyISVhNjsjRmFCOQo3UyMuSyxaVT40NmwrYFtPOWtjZGxTJnA+LTdtRCdkXjg6XyFFYmRTTVlKZ0QnVW1mXC02a28lPmFlLT5bSF9vOT1KQTolW2tXVGNOKyMrRQpcbTU8JWFKNC9tRTM6WS1uZUs5PSElYThRcUJncnJMTkFaOFEwXEslTkNXSG5MKXM6R2FEQFs/IkNQcWBUUzkhQFY4UnRFMGNRZyNURyJZMAo0dSFvQlBtZ2haW1JZJksnIidHWDAtbkg0OVhvc19YVS5ZTGB0NGpZYmFpaVBhczBhcEowamRVPG8jLCc5Qjs0YS8mZUc0PUdVT2E+UitZbgo0PVpRP0QqaERHQVQ1KnVpRyQuQUgkISkqVVRBRnAxUVJnSyElYThRW2NxZyw8KkU3Km1jUWcyVjhETEcsPz4yZmReNjloY2BRMFc6aF9XbAosPFNcJiwqMjxaVlpfSFlRJk5wMCFFYylQOVdLM05KPkppcjBSbkM5L0AxKWtYczgqRmRfbUgnPTpqRklLNihnZjBYNXBFX1BRTy49dURyYQovc1UvTktMQUghcW9WJ0hOQSo1ME0rajAxJSlFRi5tNnVvIjonIlRMJzVRLmY2RmFzaUUwI1I/IktmJnNBZ1YtJyElcTghajdjRmc6PiFkdApNTXRYXD5VZ0Q1XG0/b00jKCpfNmpcbC9HYU1fYm1gWVpMZzE5amxeMDgpdTBnKW8hYGJeVCEqJFh1ZSg+W20lU201JVhaLl8vUzJiMStBKwpsPUJpSl07PFhvNFAla0hcM3VtdDU2SmBMXzMpTionKF0kJVFbNmUrSHEqKmI3KE5VU1ohJjNhVikjI05TJDNHVmVVI2cwJCVBb2FmLj5BKAo2YiNPVCJEYCxzKHJFKylNMD5GREo0akk6bTVlWVVRY2MsWUZpIiwyUS0jWVQ6YEw7QTJgMHMjLTgoUypxTVxzPjtnODNSZVoiQnVJO1p0Wgo9YSdzViJEPiIyaTtiRSssOlZDP18jUSpROGMqbkIpWV1ANlgnMUldTStiNEhfQTFGRGNjKTtPPmZZaElKNG5CYG0xMWRmaSVcM08qWlA+awowcVM+Qmk4RDlgQ145Vk8uJHFwbEJuPFAsVUxbJT4iW20jM21VWCNjL0xER0ZwPHAxJ1teXEdVNCM+ZE1RL0VRJFYkKjBgcWQjRTdCY2wmOQorYCdAJklaY1MkXD1WaGFUQWZfL1prKCVUNWA9QU4hST0lcjo+PT1MQThqU2FPK1hlKUVQSiFRVm4yckhsV0pbVjUnck1gY21XaXIpZypzcApAP0xCX0AzOSkoV09xWU9VIlcpblpPNzAwbzAtRW1kVCFYJjw7QSpsRmx1QzliRGIuLm4/MVE0MFgiTlhsPzlGOlBoVURkLypELUJDMD50NQpHUiliJ1thZ2AjTygpJilOdFFyLDVPWVl0WS5USEFScWdKYipSXmkkUSw2dWNDL2lOS15LOztdIllBNSRiaWRPPVtUTGs8RU8hLS5oOyc7KwonWHQtXkhFbDpDTVleQiFWWXA6LT1iIzQ9U1gpVi5tJUtSW2dzUC5nSFoudWFwTiFVQkRgKE8xak91YDNZKEN0Tk1kZC49aVduN1dXazY1VwokYWA4KkJMMC1XMlZbNF1RU2w7OTpBI08wbi5AKk9qNkckbEdfImZRSVlnO0BbcUxvYycjJURWXmlmVSpbK0Q+M21VMEA7YjpQN11YMldAJQpYT0JmPiknbm9XYWI+KSdtJEciRzRkVilfIiZyWGNVcUE5PGA9ZzBUbWwwP08kWFlTTVE1K2thcFkwXmtlMCtMcj07PjE5WnMmZj1FMStDYwpiJDsuMVUmJ01LR2RrMWlUal1eRElKYEAhRWtaVWRFPDFaX0VvRHE9aTBMVkkjKDhHZl1vJWQ8VjZwMjgkY0BQO0QwbGw3XWVRYV4mOEFdJgpIY01ZODgpbUIhXDJmPCZgVDpfbEskMUxqP29IJDZfL0tnSC45cDFhJXRFPjRybUx1OW0lMi5cQV9eY0wwOixlMi5lKEUuaiFfI01bP2E4cApBZWlOa1xCc2VpcjpBPVlVVDQnRFBEK2JdWktfdG5GaydaWzU5YiwwOWwnJCVATEJHNztKXVE0ZW0/U1FiQWU+Ymw2YEc8bUxtJVtcLTIxOwpPTHFHbj9fMlVhT287aTZTPkQ4JCRDRSIwKGRXL1ZgaiFTQ29gJyJicVpDPzJbR2xSZyxMKl5kSFcwaGFxVlxOKX4+CmVuZHN0cmVhbQplbmRvYmoKMjMgMCBvYmoKPDwgL1R5cGUgL1hPYmplY3QKL1N1YnR5cGUgL0ltYWdlCi9XaWR0aCAxMTgKL0hlaWdodCA0OQovQ29sb3JTcGFjZSAvRGV2aWNlR3JheQovQml0c1BlckNvbXBvbmVudCA4Ci9MZW5ndGggNDYxCi9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiL2VKSV1SPyNYblhrVDZBPlhLbkRiV0IiTVpFYWpQcGQ0XScoXkBSbHQia0IiUzAkZiU/PW09NEM7Oy4kTihqUmNZUiVzZCZsOSRPdF4KKSY3PUwoNy1lcXFlQC4oL1NDOTg0LWZMWGVMWjVxY1o1bEFFQjU1PjNAMD1rIjtSaDJoQmNRTDMmSj81b1tjSDBiU0ZOXjw7O0A0MVNZOW0KYyJaST1ZbCNjNClgXyJZbG1OMyUuQS5sTlNgVmUvWTwlPy43KCgpLy5kQls7ayFKWyUnJURKXEk/K2E3OjVvTmtZXHFFUz4zPEk1YlptKEkKJWQ8QEIpOERidDNwS0djbGJRazEnaVpWczdOTTBcbyZSKnFVPmdIdS1GckNraDxrSEZHKlwkTT1fc1YvLSRcSkY6ZS8/PmZYQStDQ21wRGUKZFNQNkdjdSxcWCdBTD1hNUpDWzQ2Ry5ocDI9VTRlXiRlb1xRI2IqbTdDOCQtSkEoY1o/WWAnQzs2SnBIZVBsXCRIRUMhdV4qUWErNmdFTWsKW2ZFVipiLiM+cHI+LVdTZiM+aCZXP3Vra1RzaFlgPS9YLjY2QSo7YmlzL2RnQFFYWHNyOG07fj4KZW5kc3RyZWFtCmVuZG9iagoyNCAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDU0Ci9IZWlnaHQgNTQKL0NvbG9yU3BhY2UgL0RldmljZUdyYXkKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDc3Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiMEpkMFRkcSRqNG9GXlUsIkhUczlFSUU7MEFULF9FKkxaJW9AN0psNVY7SCdDcz1UcnFEYUguNEJmI2M0T1ZUOyhkI2Y8R0U5fj4KZW5kc3RyZWFtCmVuZG9iagoyNSAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDI3NwovSGVpZ2h0IDczCi9Db2xvclNwYWNlIC9EZXZpY2VHcmF5Ci9CaXRzUGVyQ29tcG9uZW50IDgKL0xlbmd0aCAxMzk0Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiL2NnUSE0LSRxJ2pqNUwjcFpHdTY9I0g/JWghJFonRWs9WCZuTU9vK0xPY1gvbXImKVZsP0ttSitFbkU5ISNrSSNwOTYyYy02LE11dUEKb0ZaSG08JnBIZ1NgJEAobS03LVVRKDckSV1fSl5ZU0E3bScpQiY5LVo7Oz1aNT03Xj5KZEhedFRxcWYqXz1JLWQqb0BVWjpjT1soIWFJTGEKYjByalFXUDslUFhjP3M8cFRbTzFiI0trUEVgdUVCV1xKUl47dVxrPjRSVjlmNGdoIjYzSnU2ZUgtQit1QzE8IjdpVVdbU1cqOllYalpjIygKQjdfQFpCWmM1T1w8cEQ8Q0RrTmVMYTE3O0o+TV5qMmovMWUrJV9sLTctSStaV1U0NCkvWDFzMCZXMEsiUElwOWZWPyYpSUMqWkNiNWtrZ1MKL1JgMGlGNkNibS4/RyZQJiZMRnNVKkZsWlVgbSpBKDxaWi9pb1lEWmFdL2phJ1I5Jjk5SUhLVF8uVTA4LzZlZ1NBZkI8NF9dQT8jO1wsJi0KIkQiZkBrJTVDTzZGZDhyXW8ldU1hOCdFcXEmTS5hOFxgJFRpciMvdCwvO1NWMFAiOjkkX2VuNFBpaVhFUW4hY1BeLyxUZjlkaEJkJ0kuZUEKUW9QISkmMj42IUUqKlgrVTtcbWBKYWVhRyUiY3BdMidaNV9dTUtEVUc2WVpVKDxUbzJCbXMjdDlZbG5uWG83IzMkJDAhbSluLFJQYGApcm8KN09gNT5LYjcrdCYyJFRST0M0YjVQXFgpYCs/PStmLXJtc10yQj0/bzJXWnVgVmBHbjdrYG4sdFVJYjtzckJxRUw3NjJdIyFTYGMoRGtTX0gKWCYrc1lyVFw7PU1MRD1cZCp1S2ZWWXRmKkUjS0A8bFRbO24vbjNNLyw+LSFZQmpoKm41Vjg0U0VaJ2FlUC1Hb14pSCdwI1cvNHJuRTQraTEKK0lCRlA1Uys0PThGOSU3Tyo6ZipuM0otYTc2MmIzYiFOV0hWKWhGK21iLC1VLUU5U05oST4sVSo8LkdtcC0pMiQvLztJOm4+W2I3cUljKDYKcElAI05UZSlHY0s3YFliUFRmZERhbiNLbVBdV145KDZqbGNMQlFlVzdxTCMjPDNlNW8rPC0pNGNsNFR1XFwoYFNiJm8qRUAnYytqam1aUCoKNE5nRkdFXiQmOi4mXyVQRkBONWQ1dSFgR1Y2bylVS0c3OCsmW1A6TGIlMnRRNC9DbF9OTltXI3A/XkxqNCRtVlZTZCZOMCwzPUA4J0xRKHQKTGBuZWAvWXM4aiwlbSVQOl9xMnItbWRjPVhYNSY+OiNZO24+LipHcGZtVyc8OE9fRWtsPSkkTi9HRCtRSFhyWD5HLCVpYUtzRlBDNjVfLE0KQD8yXic5Mk1JVz8kZ2s1aEQ+YGtuOzFPLSViazVuXVteOj5QX0YsaWIzM3ErW249OCFibkBBbGViMltVU2NoT0VrXVdpV189KCQxOjM4KTsKIklWbHFLNDFOK1BsNjxBOmk4Uyg0PSc1cChjV2RCQmQtZSNgMVdoOzs6QXQzQ3Q+YURLQklQaWNdKzMyXTtnXTRXWEVDM2drPFBMMnFnLHMKJG5FSDJqP14haFMrUztVTGR0U2pAYV9fYjtsQGprRlxvPUs1PCgxUSRzP3BjJGZzLi5abUE9dD47X0UpRzVjNzkocyokJFZCITA2WyEoLGUKLVUzTFJKbCQwWFxKT1loQjYtdSsoV28oVCMsVD0qLVVkPiU8V3FTXmVqKyUrZWRqXksiVnNIMi5wSCZXYT5sdUxOMDRPWUo0TkJoZz9DcSwKLi9zS19UPElEX1AkQCc0fj4KZW5kc3RyZWFtCmVuZG9iagoyNiAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDExOAovSGVpZ2h0IDQ5Ci9Db2xvclNwYWNlIC9EZXZpY2VHcmF5Ci9CaXRzUGVyQ29tcG9uZW50IDgKL0xlbmd0aCA0NjEKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIvZUpJXVI/I1huWGtUNkE+WEtuRGJXQiJNWkVhalBwZDRdJyheQFJsdCJrQiJTMCRmJT89bT00Qzs7LiROKGpSY1lSJXNkJmw5JE90XgopJjc9TCg3LWVxcWVALigvU0M5ODQtZkxYZUxaNXFjWjVsQUVCNTU+M0AwPWsiO1JoMmhCY1FMMyZKPzVvW2NIMGJTRk5ePDs7QDQxU1k5bQpjIlpJPVlsI2M0KWBfIllsbU4zJS5BLmxOU2BWZS9ZPCU/LjcoKCkvLmRCWztrIUpbJSclREpcST8rYTc6NW9Oa1lccUVTPjM8STViWm0oSQolZDxAQik4RGJ0M3BLR2NsYlFrMSdpWlZzN05NMFxvJlIqcVU+Z0h1LUZyQ2toPGtIRkcqXCRNPV9zVi8tJFxKRjplLz8+ZlhBK0NDbXBEZQpkU1A2R2N1LFxYJ0FMPWE1SkNbNDZHLmhwMj1VNGVeJGVvXFEjYiptN0M4JC1KQShjWj9ZYCdDOzZKcEhlUGxcJEhFQyF1XipRYSs2Z0VNawpbZkVWKmIuIz5wcj4tV1NmIz5oJlc/dWtrVHNoWWA9L1guNjZBKjtiaXMvZGdAUVhYc3I4bTt+PgplbmRzdHJlYW0KZW5kb2JqCjI3IDAgb2JqCjw8IC9UeXBlIC9YT2JqZWN0Ci9TdWJ0eXBlIC9JbWFnZQovV2lkdGggNTQKL0hlaWdodCA1NAovQ29sb3JTcGFjZSAvRGV2aWNlR3JheQovQml0c1BlckNvbXBvbmVudCA4Ci9MZW5ndGggNzcKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIwSmQwVGRxJGo0b0ZeVSwiSFRzOUVJRTswQVQsX0UqTFolb0A3Smw1VjtIJ0NzPVRycURhSC40QmYjYzRPVlQ7KGQjZjxHRTl+PgplbmRzdHJlYW0KZW5kb2JqCnhyZWYKMCAyOAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA1OCAwMDAwMCBuIAowMDAwMDAwMTA0IDAwMDAwIG4gCjAwMDAwMDAxNzYgMDAwMDAgbiAKMDAwMDAwMDIyOCAwMDAwMCBuIAowMDAwMDAwMzI2IDAwMDAwIG4gCjAwMDAwMDA0MjkgMDAwMDAgbiAKMDAwMDAwMDUzNSAwMDAwMCBuIAowMDAwMDAwNjQ1IDAwMDAwIG4gCjAwMDAwMDA3NDEgMDAwMDAgbiAKMDAwMDAwMDg0MyAwMDAwMCBuIAowMDAwMDAwOTQ4IDAwMDAwIG4gCjAwMDAwMDEwNTcgMDAwMDAgbiAKMDAwMDAwMTE1OCAwMDAwMCBuIAowMDAwMDAxMjU4IDAwMDAwIG4gCjAwMDAwMDEzNjAgMDAwMDAgbiAKMDAwMDAwMTQ2NiAwMDAwMCBuIAowMDAwMDAxNjM2IDAwMDAwIG4gCjAwMDAwMDIwNTMgMDAwMDAgbiAKMDAwMDAwMjQ3MCAwMDAwMCBuIAowMDAwMDAyODg3IDAwMDAwIG4gCjAwMDAwMDU1ODYgMDAwMDAgbiAKMDAwMDAwODc0MiAwMDAwMCBuIAowMDAwMDA5Mzg5IDAwMDAwIG4gCjAwMDAwMDk2NTAgMDAwMDAgbiAKMDAwMDAxMTIzMSAwMDAwMCBuIAowMDAwMDExODc4IDAwMDAwIG4gCnRyYWlsZXIKPDwKL0luZm8gMTcgMCBSCi9TaXplIDI4Ci9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgoxMjEzOQolJUVPRgo=",
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
