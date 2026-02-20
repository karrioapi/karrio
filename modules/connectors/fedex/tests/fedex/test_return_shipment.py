import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestFedExReturnShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ReturnShipmentRequest = models.ShipmentRequest(
            **ReturnShipmentPayload
        )

    def test_create_return_shipment_request(self):
        request = gateway.mapper.create_return_shipment_request(
            self.ReturnShipmentRequest
        )
        serialized = request.serialize()

        # Verify the return shipment detail is set
        return_detail = (
            serialized.get("requestedShipment", {})
            .get("shipmentSpecialServices", {})
            .get("returnShipmentDetail")
        )
        print(return_detail)
        self.assertIsNotNone(return_detail)
        self.assertEqual(return_detail["returnType"], "PRINT_RETURN_LABEL")

    def test_create_return_shipment(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseJSON
            karrio.Shipment.create(self.ReturnShipmentRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(
                url, f"{gateway.settings.server_url}/ship/v1/shipments"
            )

    def test_parse_return_shipment_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseJSON
            parsed_response = (
                karrio.Shipment.create(self.ReturnShipmentRequest)
                .from_(gateway)
                .parse()
            )

            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedReturnShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ReturnShipmentPayload = {
    "shipper": {
        "person_name": "Customer Name",
        "company_name": "Customer Inc",
        "phone_number": "+1 123 456 7890",
        "address_line1": "123 Customer St",
        "city": "MEMPHIS",
        "state_code": "TN",
        "postal_code": "38117",
        "country_code": "US",
    },
    "recipient": {
        "person_name": "Warehouse Manager",
        "company_name": "Return Center Inc",
        "phone_number": "000-000-0000",
        "address_line1": "456 Warehouse Ave",
        "city": "RICHMOND",
        "state_code": "BC",
        "postal_code": "V7C4V7",
        "country_code": "CA",
    },
    "parcels": [
        {
            "packaging_type": "your_packaging",
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "weight": 10.0,
            "length": 12,
            "width": 12,
            "height": 12,
        }
    ],
    "service": "fedex_standard_overnight",
    "is_return": True,
    "options": {
        "currency": "USD",
        "shipment_date": "2024-02-15",
    },
    "payment": {"paid_by": "sender", "account_number": "2349857"},
    "reference": "#Return 12345",
}

ParsedReturnShipmentResponse = [
    {
        "carrier_id": "fedex",
        "carrier_name": "fedex",
        "docs": {"label": ANY},
        "label_type": "PDF",
        "return_shipment": {
            "tracking_number": "794953535000",
            "shipment_identifier": "794953535000",
            "tracking_url": "https://www.fedex.com/fedextrack/?trknbr=794953535000",
            "service": "fedex_return_shipment",
        },
        "meta": {
            "carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=794953535000",
            "serviceCategory": "EXPRESS",
            "service_name": "fedex_standard_overnight",
            "trackingIdType": "FEDEX",
            "fedex_carrier_code": "FDXE",
        },
        "shipment_identifier": "794953535000",
        "tracking_number": "794953535000",
    },
    [],
]

ShipmentResponseJSON = """{
    "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
    "customerTransactionId": "AnyCo_order123456789",
    "output": {
        "transactionShipments": [
            {
                "serviceType": "STANDARD_OVERNIGHT",
                "shipDatestamp": "2019-10-14",
                "serviceName": "FedEx Standard Overnight",
                "alerts": [
                    {
                        "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
                        "alertType": "NOTE",
                        "message": "Recipient Postal-City Mismatch."
                    }
                ],
                "completedShipmentDetail": {
                    "usDomestic": false,
                    "carrierCode": "FDXE",
                    "masterTrackingId": {
                        "trackingIdType": "FEDEX",
                        "formId": "",
                        "trackingNumber": "794953535000"
                    },
                    "serviceDescription": {
                        "serviceId": "EP1000000135",
                        "serviceType": "STANDARD_OVERNIGHT",
                        "code": "06",
                        "names": [
                            {
                                "type": "long",
                                "encoding": "utf-8",
                                "value": "FedEx Standard Overnight\u00ae"
                            },
                            {
                                "type": "long",
                                "encoding": "ascii",
                                "value": "FedEx Standard Overnight"
                            },
                            {
                                "type": "medium",
                                "encoding": "utf-8",
                                "value": "FedEx Standard Overnight\u00ae"
                            },
                            {
                                "type": "medium",
                                "encoding": "ascii",
                                "value": "FedEx Standard Overnight"
                            },
                            {
                                "type": "short",
                                "encoding": "utf-8",
                                "value": "SO"
                            },
                            {
                                "type": "short",
                                "encoding": "ascii",
                                "value": "SO"
                            },
                            {
                                "type": "abbrv",
                                "encoding": "ascii",
                                "value": "SO"
                            }
                        ],
                        "operatingOrgCodes": ["FXE"],
                        "serviceCategory": "EXPRESS",
                        "description": "Standard Overnight",
                        "astraDescription": "SO"
                    },
                    "operationalDetail": {
                        "originLocationIds": ["XTNA "],
                        "commitDates": ["2019-10-15"],
                        "commitDays": "TUE",
                        "deliveryDay": "TUE",
                        "ineligibleForMoneyBackGuarantee": false,
                        "deliveryEligibilities": ["SATURDAY_DELIVERY"],
                        "astraDescription": "SO",
                        "originServiceAreas": ["A1"],
                        "destinationServiceAreas": ["A1"],
                        "originLocationNumbers": [0],
                        "destinationLocationNumbers": [0],
                        "transitTime": "ONE_DAY",
                        "publishedDeliveryTime": "2019-10-15T15:00:00",
                        "scac": ""
                    }
                },
                "masterTrackingNumber": "794953535000",
                "pieceResponses": [
                    {
                        "netChargeAmount": 120.0,
                        "transactionDetails": [
                            {
                                "transactionDetails": "",
                                "transactionId": "624deea6-b709-470c-8c39-4b5511281492"
                            }
                        ],
                        "packageDocuments": [
                            {
                                "url": "https://api.fedex.com/document/v2/document",
                                "contentType": "LABEL",
                                "copiesToPrint": 1,
                                "docType": "PDF",
                                "encodedLabel": "JVBERi0xLjQKMSAwIG9iajw8L1R5cGUvQ2F0YWxvZy9QYWdlcyAyIDAgUj4+ZW5kb2JqCjIgMCBvYmo8PC9UeXBlL1BhZ2VzL0tpZHNbMyAwIFJdL0NvdW50IDE+PmVuZG9iagozIDAgb2JqPDwvVHlwZS9QYWdlL01lZGlhQm94WzAgMCA2MTIgNzkyXS9QYXJlbnQgMiAwIFI+PmVuZG9iagp4cmVmCjAgNAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA1MiAwMDAwMCBuIAowMDAwMDAwMTAxIDAwMDAwIG4gCnRyYWlsZXI8PC9TaXplIDQvUm9vdCAxIDAgUj4+CnN0YXJ0eHJlZgoxNjQKJSVFT0Y="
                            }
                        ],
                        "acceptanceTrackingNumber": "794953535000",
                        "serviceDescription": {
                            "serviceId": "EP1000000135",
                            "serviceType": "STANDARD_OVERNIGHT",
                            "code": "06",
                            "names": [
                                {
                                    "type": "long",
                                    "encoding": "utf-8",
                                    "value": "FedEx Standard Overnight\u00ae"
                                }
                            ],
                            "operatingOrgCodes": ["FXE"],
                            "serviceCategory": "EXPRESS",
                            "description": "Standard Overnight",
                            "astraDescription": "SO"
                        },
                        "serviceCategory": "EXPRESS",
                        "trackingIdType": "FEDEX",
                        "additionalChargesDiscount": 0.0,
                        "netListRateAmount": 0.0,
                        "netDiscountAmount": 0.0,
                        "netRateAmount": 0.0,
                        "masterTrackingNumber": "794953535000",
                        "trackingNumber": "794953535000",
                        "baseRateAmount": 0.0
                    }
                ]
            }
        ]
    }
}"""
