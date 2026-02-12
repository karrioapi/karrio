import unittest
import logging
from unittest.mock import patch, ANY
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from .fixture import gateway
import karrio.sdk as karrio


class TestUPSShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**PackageShipmentData)
        self.ShipmentCancelRequest = ShipmentCancelRequest(**ShipmentCancelRequestData)

    def test_create_package_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(request.serialize(), ShipmentRequestJSON)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(
            request.serialize(),
            {"shipmentidentificationnumber": "1ZWA82900191640782"},
        )

    def test_create_package_shipment_with_package_preset_request(self):
        request = gateway.mapper.create_shipment_request(
            ShipmentRequest(**PackageShipmentWithPackagePresetData)
        )
        self.assertEqual(request.serialize(), ShipmentRequestWithPresetJSON)

    def test_create_return_shipment_request(self):
        request = gateway.mapper.create_shipment_request(
            ShipmentRequest(**ReturnShipmentData)
        )
        print(request.serialize())
        self.assertEqual(request.serialize(), ReturnShipmentRequestJSON)

    def test_create_international_shipment_request(self):
        request = gateway.mapper.create_shipment_request(
            ShipmentRequest(**InternationalShipmentData)
        )
        self.assertEqual(request.serialize(), InternationalShipmentRequestJSON)

    @patch("karrio.mappers.ups.proxy.lib.request", return_value="{}")
    def test_create_shipment(self, http_mock):
        karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/api/shipments/v2409/ship")

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseJSON
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_shipment_response_with_invoice(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseWithInvoice
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedShipmentResponseWithInvoice
            )

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponseJSON
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedShipmentCancelResponse
            )


if __name__ == "__main__":
    unittest.main()


# International shipment test data
InternationalShipmentData = {
    "shipper": {
        "company_name": "US Exporter Corp",
        "person_name": "John Exporter",
        "federal_tax_id": "123456789",
        "phone_number": "555-987-6543",
        "email": "exporter@usexporter.com",
        "address_line1": "123 Export Street",
        "city": "New York",
        "state_code": "NY",
        "postal_code": "10001",
        "country_code": "US",
        "residential": False,
    },
    "recipient": {
        "company_name": "International Buyer Corp",
        "person_name": "John Buyer",
        "phone_number": "555-123-4567",
        "email": "buyer@internationalbuyer.com",
        "address_line1": "123 International Street",
        "city": "Toronto",
        "state_code": "ON",
        "postal_code": "M5V 3A8",
        "country_code": "CA",
        "residential": False,
    },
    "parcels": [
        {
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "packaging_type": "ups_customer_supplied_package",
            "description": "Electronics Components",
            "length": 10,
            "width": 8,
            "height": 4,
            "weight": 2.5,
        }
    ],
    "service": "ups_worldwide_express",
    "options": {
        "email_notification_to": "buyer@internationalbuyer.com",
        "signature_confirmation": True,
    },
    "payment": {"paid_by": "sender"},
    "reference": "INT-2024-001",
    "customs": {
        "commodities": [
            {
                "title": "Electronics Components",
                "description": "Electronic circuit components",
                "quantity": 1,
                "hs_code": "8541.40.20.00",
                "value_amount": 150.00,
                "value_currency": "USD",
                "weight": 2.5,
                "weight_unit": "LB",
                "origin_country": "US",
            }
        ],
        "content_type": "merchandise",
        "content_description": "Electronic components for industrial use",
        "incoterm": "DAP",
        "invoice": "INV-2024-001",
        "invoice_date": "2024-01-15",
        "duty": {
            "paid_by": "sender",
            "currency": "USD",
            "declared_value": 150.00,
        },
    },
}

InternationalShipmentRequestJSON = {
    "ShipmentRequest": {
        "LabelSpecification": {
            "LabelImageFormat": {"Code": "PNG", "Description": "lable format"},
            "LabelStockSize": {"Height": "6", "Width": "4"},
        },
        "Request": {
            "RequestOption": "validate",
            "SubVersion": "v2409",
            "TransactionReference": {"CustomerContext": "INT-2024-001"},
        },
        "Shipment": {
            "Description": "Electronics Components",
            "InvoiceLineTotal": {"CurrencyCode": "USD", "MonetaryValue": "1.0"},
            "NumOfPiecesInShipment": "0",
            "Package": [
                {
                    "Description": "Electronics Components",
                    "Dimensions": {
                        "Height": "4.0",
                        "Length": "10.0",
                        "UnitOfMeasurement": {"Code": "IN", "Description": "Dimension"},
                        "Width": "8.0",
                    },
                    "PackageWeight": {
                        "UnitOfMeasurement": {"Code": "LBS", "Description": "Weight"},
                        "Weight": "2.5",
                    },
                    "Packaging": {"Code": "02", "Description": "Packaging Type"},
                }
            ],
            "PaymentInformation": {
                "ShipmentCharge": [
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "01",
                    },
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "02",
                    },
                ]
            },
            "RatingMethodRequestedIndicator": "Y",
            "ReferenceNumber": {"Value": "INT-2024-001"},
            "Service": {"Code": "07", "Description": "ups_express"},
            "ShipFrom": {
                "Address": {
                    "AddressLine": ["123 Export Street"],
                    "City": "New York",
                    "CountryCode": "US",
                    "PostalCode": "10001",
                    "StateProvinceCode": "NY",
                },
                "AttentionName": "John Exporter",
                "CompanyDisplayableName": "US Exporter Corp",
                "EMailAddress": "exporter@usexporter.com",
                "Name": "US Exporter Corp",
                "Phone": {"Number": "555-987-6543"},
                "TaxIdentificationNumber": "123456789",
            },
            "ShipTo": {
                "Address": {
                    "AddressLine": ["123 International Street"],
                    "City": "Toronto",
                    "CountryCode": "CA",
                    "PostalCode": "M5V 3A8",
                    "StateProvinceCode": "ON",
                },
                "AttentionName": "John Buyer",
                "CompanyDisplayableName": "International Buyer Corp",
                "EMailAddress": "buyer@internationalbuyer.com",
                "Name": "International Buyer Corp",
                "Phone": {"Number": "555-123-4567"},
            },
            "ShipmentDate": ANY,
            "ShipmentRatingOptions": {"NegotiatedRatesIndicator": "Y"},
            "ShipmentServiceOptions": {
                "DeliveryConfirmation": {"DCISType": "1"},
                "InternationalForms": {
                    "Contacts": {
                        "SoldTo": {
                            "Address": {
                                "AddressLine": ["123 International Street"],
                                "City": "Toronto",
                                "CountryCode": "CA",
                                "PostalCode": "M5V 3A8",
                                "StateProvinceCode": "ON",
                            },
                            "AttentionName": "John Buyer",
                            "EMailAddress": "buyer@internationalbuyer.com",
                            "Name": "International Buyer Corp",
                            "Phone": {"Number": "555-123-4567"},
                        }
                    },
                    "CurrencyCode": "USD",
                    "DeclarationStatement": "I hereby certify that the information on this invoice is true and correct and the contents and value of this shipment is as stated above.",
                    "FormType": "01",
                    "InvoiceDate": "20240115",
                    "InvoiceNumber": "INV-2024-001",
                    "Product": [
                        {
                            "CommodityCode": "8541.40.20.00",
                            "Description": "Electronics Components",
                            "ExportType": "F",
                            "NumberOfPackagesPerCommodity": "1",
                            "OriginCountryCode": "US",
                            "ProductWeight": {
                                "UnitOfMeasurement": {
                                    "Code": "LBS",
                                    "Description": "weight unit",
                                },
                                "Weight": "2.5",
                            },
                            "Unit": {
                                "Number": "1",
                                "UnitOfMeasurement": {
                                    "Code": "PCS",
                                    "Description": "PCS",
                                },
                                "Value": "150.0",
                            },
                        }
                    ],
                    "ReasonForExport": "SALE",
                },
                "Notification": [
                    {
                        "EMail": {"EMailAddress": "buyer@internationalbuyer.com"},
                        "NotificationCode": "8",
                    }
                ],
            },
            "Shipper": {
                "Address": {
                    "AddressLine": ["123 Export Street"],
                    "City": "New York",
                    "CountryCode": "US",
                    "PostalCode": "10001",
                    "StateProvinceCode": "NY",
                },
                "AttentionName": "John Exporter",
                "CompanyDisplayableName": "US Exporter Corp",
                "EMailAddress": "exporter@usexporter.com",
                "Name": "US Exporter Corp",
                "Phone": {"Number": "555-987-6543"},
                "ShipperNumber": "Your Account Number",
                "TaxIdentificationNumber": "123456789",
            },
            "TaxInformationIndicator": "Y",
        },
    }
}

ReturnShipmentData = {
    "shipper": {
        "company_name": "Shipper Name",
        "person_name": "Shipper Attn Name",
        "federal_tax_id": "123456",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "person_name": "Ship To Attn Name",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "parcels": [
        {
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "packaging_type": "ups_customer_supplied_package",
            "description": "Description",
            "length": 7,
            "width": 5,
            "height": 2,
            "weight": 10,
        }
    ],
    "service": "ups_express_ca",
    "options": {
        "ups_return_service": "ups_print_return_label",
    },
    "payment": {"paid_by": "sender"},
    "reference": "Return Shipment Test",
}

ReturnShipmentRequestJSON = {
    "ShipmentRequest": {
        "LabelSpecification": {
            "LabelImageFormat": {"Code": "PNG", "Description": "lable format"},
            "LabelStockSize": {"Height": "6", "Width": "4"},
        },
        "Request": {
            "RequestOption": "validate",
            "SubVersion": "v2409",
            "TransactionReference": {"CustomerContext": "Return Shipment Test"},
        },
        "Shipment": {
            "Description": "Description",
            "InvoiceLineTotal": {"CurrencyCode": "USD", "MonetaryValue": "1.0"},
            "NumOfPiecesInShipment": "0",
            "Package": [
                {
                    "Description": "Description",
                    "Dimensions": {
                        "Height": "2.0",
                        "Length": "7.0",
                        "UnitOfMeasurement": {"Code": "IN", "Description": "Dimension"},
                        "Width": "5.0",
                    },
                    "PackageWeight": {
                        "UnitOfMeasurement": {"Code": "LBS", "Description": "Weight"},
                        "Weight": "10.0",
                    },
                    "Packaging": {"Code": "02", "Description": "Packaging Type"},
                }
            ],
            "PaymentInformation": {
                "ShipmentCharge": [
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "01",
                    },
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "02",
                    },
                ]
            },
            "RatingMethodRequestedIndicator": "Y",
            "ReferenceNumber": {"Value": "Return Shipment Test"},
            "ReturnService": {"Code": "9", "Description": "Return Service"},
            "Service": {"Code": "01", "Description": "ups_next_day_air"},
            "ShipFrom": {
                "Address": {
                    "AddressLine": ["Address Line"],
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Shipper Attn Name",
                "CompanyDisplayableName": "Shipper Name",
                "Name": "Shipper Name",
                "Phone": {"Number": "1234567890"},
                "TaxIdentificationNumber": "123456",
            },
            "ShipTo": {
                "Address": {
                    "AddressLine": ["Address Line"],
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Ship To Attn Name",
                "CompanyDisplayableName": "Ship To Name",
                "Name": "Ship To Name",
                "Phone": {"Number": "1234567890"},
            },
            "ShipmentDate": ANY,
            "ShipmentRatingOptions": {"NegotiatedRatesIndicator": "Y"},
            "ShipmentServiceOptions": {},
            "Shipper": {
                "Address": {
                    "AddressLine": ["Address Line"],
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Shipper Attn Name",
                "CompanyDisplayableName": "Shipper Name",
                "Name": "Shipper Name",
                "Phone": {"Number": "1234567890"},
                "ShipperNumber": "Your Account Number",
                "TaxIdentificationNumber": "123456",
            },
            "TaxInformationIndicator": "Y",
        },
    }
}

ShipmentCancelRequestData = {"shipment_identifier": "1ZWA82900191640782"}

PackageShipmentData = {
    "shipper": {
        "company_name": "Shipper Name",
        "person_name": "Shipper Attn Name",
        "federal_tax_id": "123456",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "person_name": "Ship To Attn Name",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "parcels": [
        {
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "packaging_type": "ups_customer_supplied_package",
            "description": "Description",
            "length": 7,
            "width": 5,
            "height": 2,
            "weight": 10,
        }
    ],
    "service": "ups_express_ca",
    "options": {
        "email_notification_to": "test@mail.com",
        "signature_confirmation": True,
    },
    "payment": {"paid_by": "sender"},
    "reference": "Your Customer Context",
}

PackageShipmentWithPackagePresetData = {
    "shipper": {
        "company_name": "Shipper Name",
        "person_name": "Shipper Attn Name",
        "federal_tax_id": "123456",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "person_name": "Ship To Attn Name",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "parcels": [
        {
            "packaging_type": "ups_customer_supplied_package",
            "description": "Description",
            "package_preset": "ups_medium_express_box",
        }
    ],
    "service": "ups_express_ca",
    "payment": {"paid_by": "sender"},
    "options": {
        "signature_confirmation": True,
        "ups_saturday_delivery_indicator": True,
    },
    "reference": "Your Customer Context",
    "label_type": "ZPL",
}


NegotiatedParsedShipmentResponse = [
    {
        "carrier_name": "ups",
        "carrier_id": "ups",
        "tracking_number": "1ZWA82900191640782",
        "shipment_identifier": "1ZWA82900191640782",
        "label_type": "PDF",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1ZWA82900191640782/trackdetails"
        },
    },
    [],
]

ParsedShipmentResponse = [
    {
        "carrier_name": "ups",
        "carrier_id": "ups",
        "tracking_number": "1ZXXXXXXXXXXXXXXXX",
        "shipment_identifier": "1ZXXXXXXXXXXXXXXXX",
        "label_type": "PDF",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1ZXXXXXXXXXXXXXXXX/trackdetails",
            "tracking_numbers": ["1ZXXXXXXXXXXXXXXXX"],
        },
    },
    [],
]

ParsedShipmentResponseWithInvoice = [
    {
        "carrier_id": "ups",
        "carrier_name": "ups",
        "docs": {
            "label": ANY,
            "invoice": ANY,
        },
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1Z0FH3446831744085/trackdetails",
            "tracking_numbers": ["1Z0FH3446831744085"],
        },
        "shipment_identifier": "1Z0FH3446831744085",
        "tracking_number": "1Z0FH3446831744085",
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "ups",
        "carrier_name": "ups",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequestJSON = {
    "ShipmentRequest": {
        "LabelSpecification": {
            "LabelImageFormat": {"Code": "PNG", "Description": "lable format"},
            "LabelStockSize": {"Height": "6", "Width": "4"},
        },
        "Request": {
            "RequestOption": "validate",
            "SubVersion": "v2409",
            "TransactionReference": {"CustomerContext": "Your Customer Context"},
        },
        "Shipment": {
            "Description": "Description",
            "InvoiceLineTotal": {"CurrencyCode": "USD", "MonetaryValue": "1.0"},
            "NumOfPiecesInShipment": "0",
            "Package": [
                {
                    "Description": "Description",
                    "Dimensions": {
                        "Height": "2.0",
                        "Length": "7.0",
                        "UnitOfMeasurement": {"Code": "IN", "Description": "Dimension"},
                        "Width": "5.0",
                    },
                    "PackageWeight": {
                        "UnitOfMeasurement": {"Code": "LBS", "Description": "Weight"},
                        "Weight": "10.0",
                    },
                    "Packaging": {"Code": "02", "Description": "Packaging Type"},
                }
            ],
            "PaymentInformation": {
                "ShipmentCharge": [
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "01",
                    },
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "02",
                    },
                ]
            },
            "RatingMethodRequestedIndicator": "Y",
            "ReferenceNumber": {"Value": "Your Customer Context"},
            "Service": {"Code": "01", "Description": "ups_next_day_air"},
            "ShipFrom": {
                "Address": {
                    "AddressLine": ["Address Line"],
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Shipper Attn Name",
                "CompanyDisplayableName": "Shipper Name",
                "Name": "Shipper Name",
                "Phone": {"Number": "1234567890"},
                "TaxIdentificationNumber": "123456",
            },
            "ShipTo": {
                "Address": {
                    "AddressLine": ["Address Line"],
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Ship To Attn Name",
                "CompanyDisplayableName": "Ship To Name",
                "Name": "Ship To Name",
                "Phone": {"Number": "1234567890"},
            },
            "ShipmentDate": ANY,
            "ShipmentRatingOptions": {"NegotiatedRatesIndicator": "Y"},
            "ShipmentServiceOptions": {
                "DeliveryConfirmation": {"DCISType": "1"},
                "Notification": [
                    {
                        "EMail": {"EMailAddress": "test@mail.com"},
                        "NotificationCode": "8",
                    }
                ],
            },
            "Shipper": {
                "Address": {
                    "AddressLine": ["Address Line"],
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Shipper Attn Name",
                "CompanyDisplayableName": "Shipper Name",
                "Name": "Shipper Name",
                "Phone": {"Number": "1234567890"},
                "ShipperNumber": "Your Account Number",
                "TaxIdentificationNumber": "123456",
            },
            "TaxInformationIndicator": "Y",
        },
    }
}

ShipmentRequestWithPresetJSON = {
    "ShipmentRequest": {
        "LabelSpecification": {
            "LabelImageFormat": {"Code": "ZPL", "Description": "lable format"},
            "LabelStockSize": {"Height": "6", "Width": "4"},
        },
        "Request": {
            "RequestOption": "validate",
            "SubVersion": "v2409",
            "TransactionReference": {"CustomerContext": "Your Customer Context"},
        },
        "Shipment": {
            "Description": "Description",
            "InvoiceLineTotal": {"CurrencyCode": "USD", "MonetaryValue": "1.0"},
            "NumOfPiecesInShipment": "0",
            "Package": [
                {
                    "Description": "Description",
                    "Dimensions": {
                        "Height": "11.0",
                        "Length": "3.0",
                        "UnitOfMeasurement": {"Code": "IN", "Description": "Dimension"},
                        "Width": "16.0",
                    },
                    "PackageWeight": {
                        "UnitOfMeasurement": {"Code": "LBS", "Description": "Weight"},
                        "Weight": "30.0",
                    },
                    "Packaging": {"Code": "02", "Description": "Packaging Type"},
                }
            ],
            "PaymentInformation": {
                "ShipmentCharge": [
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "01",
                    },
                    {
                        "BillShipper": {"AccountNumber": "Your Account Number"},
                        "Type": "02",
                    },
                ]
            },
            "RatingMethodRequestedIndicator": "Y",
            "ReferenceNumber": {"Value": "Your Customer Context"},
            "Service": {"Code": "01", "Description": "ups_next_day_air"},
            "ShipFrom": {
                "Address": {
                    "AddressLine": ["Address Line"],
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Shipper Attn Name",
                "CompanyDisplayableName": "Shipper Name",
                "Name": "Shipper Name",
                "Phone": {"Number": "1234567890"},
                "TaxIdentificationNumber": "123456",
            },
            "ShipTo": {
                "Address": {
                    "AddressLine": ["Address Line"],
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Ship To Attn Name",
                "CompanyDisplayableName": "Ship To Name",
                "Name": "Ship To Name",
                "Phone": {"Number": "1234567890"},
            },
            "ShipmentDate": ANY,
            "ShipmentRatingOptions": {"NegotiatedRatesIndicator": "Y"},
            "ShipmentServiceOptions": {
                "DeliveryConfirmation": {"DCISType": "1"},
                "SaturdayDeliveryIndicator": "Y",
            },
            "Shipper": {
                "Address": {
                    "AddressLine": ["Address Line"],
                    "City": "City",
                    "CountryCode": "CountryCode",
                    "PostalCode": "PostalCode",
                    "StateProvinceCode": "StateProvinceCode",
                },
                "AttentionName": "Shipper Attn Name",
                "CompanyDisplayableName": "Shipper Name",
                "Name": "Shipper Name",
                "Phone": {"Number": "1234567890"},
                "ShipperNumber": "Your Account Number",
                "TaxIdentificationNumber": "123456",
            },
            "TaxInformationIndicator": "Y",
        },
    }
}

ShipmentResponseJSON = """{
	"ShipmentResponse": {
		"Response": {
			"ResponseStatus": {
				"Code": "1",
				"Description": "Success"
			},
			"Alert": [
				{
					"Code": "121524",
					"Description": "The payer of Duty and Tax charges is not required for UPS Letter, Documents of No Commercial Value or Qualified Domestic Shipments."
				},
				{
					"Code": "120900",
					"Description": "User Id and Shipper Number combination is not qualified to receive negotiated rates"
				}
			],
			"TransactionReference": {
				"CustomerContext": "testing",
				"TransactionIdentifier": "iewssoat2643k31L9059jT"
			}
		},
		"ShipmentResults": {
			"Disclaimer": {
				"Code": "01",
				"Description": "Taxes are included in the shipping cost and apply to the transportation charges but additional duties/taxes may apply and are not reflected in the total amount due."
			},
			"ShipmentCharges": {
				"BaseServiceCharge": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "114.05"
				},
				"TransportationCharges": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "135.15"
				},
				"ItemizedCharges": [
					{
						"Code": "178",
						"CurrencyCode": "CAD",
						"MonetaryValue": "0.00"
					},
					{
						"Code": "375",
						"CurrencyCode": "CAD",
						"MonetaryValue": "21.10"
					}
				],
				"ServiceOptionsCharges": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "0.00"
				},
				"TaxCharges": {
					"Type": "HST",
					"MonetaryValue": "20.27"
				},
				"TotalCharges": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "135.15"
				},
				"TotalChargesWithTaxes": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "155.42"
				}
			},
			"RatingMethod": "01",
			"BillableWeightCalculationMethod": "02",
			"BillingWeight": {
				"UnitOfMeasurement": {
					"Code": "LBS",
					"Description": "Pounds"
				},
				"Weight": "10.0"
			},
			"ShipmentIdentificationNumber": "1ZXXXXXXXXXXXXXXXX",
			"PackageResults": {
				"TrackingNumber": "1ZXXXXXXXXXXXXXXXX",
				"ServiceOptionsCharges": {
					"CurrencyCode": "CAD",
					"MonetaryValue": "0.00"
				},
				"ShippingLabel": {
					"ImageFormat": {
						"Code": "PNG",
						"Description": "PNG"
					},
					"GraphicImage": "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",
					"HTMLImage": "PCFET0NUWVBFIEhUTUwgUFVCTElDICItLy9JRVRGLy9EVEQgSFRNTCAzLjIvL0VOIj4KPGh0bWw+PGhlYWQ+PHRpdGxlPgpWaWV3L1ByaW50IExhYmVsPC90aXRsZT48bWV0YSBjaGFyc2V0PSJVVEYtOCI+PC9oZWFkPjxzdHlsZT4KICAgIC5zbWFsbF90ZXh0IHtmb250LXNpemU6IDgwJTt9CiAgICAubGFyZ2VfdGV4dCB7Zm9udC1zaXplOiAxMTUlO30KPC9zdHlsZT4KPGJvZHkgYmdjb2xvcj0iI0ZGRkZGRiI+CjxkaXYgY2xhc3M9Imluc3RydWN0aW9ucy1kaXYiPgo8dGFibGUgY2xhc3M9Imluc3RydWN0aW9ucy10YWJsZSIgbmFtZWJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjAiIGNlbGxzcGFjaW5nPSIwIiB3aWR0aD0iNjAwIj48dHI+Cjx0ZCBoZWlnaHQ9IjQxMCIgYWxpZ249ImxlZnQiIHZhbGlnbj0idG9wIj4KPEIgY2xhc3M9ImxhcmdlX3RleHQiPlZpZXcvUHJpbnQgTGFiZWw8L0I+CiZuYnNwOzxicj4KJm5ic3A7PGJyPgo8b2wgY2xhc3M9InNtYWxsX3RleHQiPiA8bGk+PGI+UHJpbnQgdGhlIGxhYmVsOjwvYj4gJm5ic3A7ClNlbGVjdCBQcmludCBmcm9tIHRoZSBGaWxlIG1lbnUgaW4gdGhpcyBicm93c2VyIHdpbmRvdyB0byBwcmludCB0aGUgbGFiZWwgYmVsb3cuPGJyPjxicj48bGk+PGI+CkZvbGQgdGhlIHByaW50ZWQgbGFiZWwgYXQgdGhlIGRvdHRlZCBsaW5lLjwvYj4gJm5ic3A7ClBsYWNlIHRoZSBsYWJlbCBpbiBhIFVQUyBTaGlwcGluZyBQb3VjaC4gSWYgeW91IGRvIG5vdCBoYXZlIGEgcG91Y2gsIGFmZml4IHRoZSBmb2xkZWQgbGFiZWwgdXNpbmcgY2xlYXIgcGxhc3RpYyBzaGlwcGluZyB0YXBlIG92ZXIgdGhlIGVudGlyZSBsYWJlbC48YnI+PGJyPjxsaT48Yj5HRVRUSU5HIFlPVVIgU0hJUE1FTlQgVE8gVVBTPGJyPgpDdXN0b21lcnMgd2l0aG91dCBhIERhaWx5IFBpY2t1cDwvYj48dWw+PGxpPkdyb3VuZCwgMyBEYXkgU2VsZWN0LCBhbmQgU3RhbmRhcmQgdG8gQ2FuYWRhIHNoaXBtZW50cyBtdXN0IGJlIGRyb3BwZWQgb2ZmIGF0IGFuIGF1dGhvcml6ZWQgVVBTIGxvY2F0aW9uLCBvciBoYW5kZWQgdG8gYSBVUFMgZHJpdmVyLiBQaWNrdXAgc2VydmljZSBpcyBub3QgYXZhaWxhYmxlIGZvciB0aGVzZSBzZXJ2aWNlcy4gVG8gZmluZCB0aGUgbmVhcmVzdCBkcm9wLW9mZiBsb2NhdGlvbiwgc2VsZWN0IHRoZSBEcm9wLW9mZiBpY29uIGZyb20gdGhlIFVQUyB0b29sIGJhci48bGk+CkFpciBzaGlwbWVudHMgKGluY2x1ZGluZyBXb3JsZHdpZGUgRXhwcmVzcyBhbmQgRXhwZWRpdGVkKSBjYW4gYmUgcGlja2VkIHVwIG9yIGRyb3BwZWQgb2ZmLiBUbyBzY2hlZHVsZSBhIHBpY2t1cCwgb3IgdG8gZmluZCBhIGRyb3Atb2ZmIGxvY2F0aW9uLCBzZWxlY3QgdGhlIFBpY2t1cCBvciBEcm9wLW9mZiBpY29uIGZyb20gdGhlIFVQUyB0b29sIGJhci4gPC91bD48YnI+CjxiPkN1c3RvbWVycyB3aXRoIGEgRGFpbHkgUGlja3VwPC9iPjx1bD48bGk+CllvdXIgZHJpdmVyIHdpbGwgcGlja3VwIHlvdXIgc2hpcG1lbnQocykgYXMgdXN1YWwuIDwvdWw+PGJyPgo8L29sPjwvdGQ+PC90cj48L3RhYmxlPjx0YWJsZSBib3JkZXI9IjAiIGNlbGxwYWRkaW5nPSIwIiBjZWxsc3BhY2luZz0iMCIgd2lkdGg9IjYwMCI+Cjx0cj4KPHRkIGNsYXNzPSJzbWFsbF90ZXh0IiBhbGlnbj0ibGVmdCIgdmFsaWduPSJ0b3AiPgombmJzcDsmbmJzcDsmbmJzcDsKPGEgbmFtZT0iZm9sZEhlcmUiPkZPTEQgSEVSRTwvYT48L3RkPgo8L3RyPgo8dHI+Cjx0ZCBhbGlnbj0ibGVmdCIgdmFsaWduPSJ0b3AiPjxocj4KPC90ZD4KPC90cj4KPC90YWJsZT4KCjx0YWJsZT4KPHRyPgo8dGQgaGVpZ2h0PSIxMCI+Jm5ic3A7CjwvdGQ+CjwvdHI+CjwvdGFibGU+Cgo8L2Rpdj4KPHRhYmxlIGJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjAiIGNlbGxzcGFjaW5nPSIwIiB3aWR0aD0iNjUwIiA+PHRyPgo8dGQgYWxpZ249ImxlZnQiIHZhbGlnbj0idG9wIj4KPElNRyBTUkM9Ii4vbGFiZWwxWjAwMlI0ODE0MjkyMjE0MzMucG5nIiBoZWlnaHQ9IjM5MiIgd2lkdGg9IjY1MSI+CjwvdGQ+CjwvdHI+PC90YWJsZT4KPC9ib2R5Pgo8L2h0bWw+Cg=="
				}
			}
		}
	}
}
"""

ShipmentCancelResponseJSON = """{
    "VoidShipmentResponse": {
        "Response": {
            "ResponseStatus": {"Code": "1", "Description": "Success"},
            "TransactionReference": {
                "CustomerContext": "string",
                "TransactionIdentifier": "string"
            }
        },
        "SummaryResult": {"Status": {"Code": "1", "Description": "Success"}},
        "PackageLevelResult": [
            {
                "TrackingNumber": "string",
                "Status": {"Code": "1", "Description": "Success"}
            }
        ]
    }
}
"""

ShipmentResponseWithInvoice = """{
  "ShipmentResponse": {
    "Response": {
      "ResponseStatus": {
        "Code": "1",
        "Description": "Success"
      },
      "Alert": [
        {
          "Code": "120016",
          "Description": "A Customs Invoice is required when the shipment is tendered to UPS."
        }
      ],
      "TransactionReference": {
        "CustomerContext": "x-trans-src",
        "TransactionIdentifier": "wssoa2t396v2ZsHr3Nhh7c"
      }
    },
    "ShipmentResults": {
      "Disclaimer": [
        {
          "Code": "03",
          "Description": "Additional duties/taxes may apply and are not reflected in the total amount due."
        }
      ],
      "ShipmentCharges": {
        "BaseServiceCharge": {
          "CurrencyCode": "GBP",
          "MonetaryValue": "13.24"
        },
        "TransportationCharges": {
          "CurrencyCode": "GBP",
          "MonetaryValue": "21.01"
        },
        "ItemizedCharges": [
          {
            "Code": "378",
            "CurrencyCode": "GBP",
            "MonetaryValue": "7.77"
          }
        ],
        "ServiceOptionsCharges": {
          "CurrencyCode": "GBP",
          "MonetaryValue": "0.00"
        },
        "TotalCharges": {
          "CurrencyCode": "GBP",
          "MonetaryValue": "21.01"
        }
      },
      "NegotiatedRateCharges": {
        "TotalCharge": {
          "CurrencyCode": "GBP",
          "MonetaryValue": "20.22"
        },
        "ItemizedCharges": [
          {
            "Code": "378",
            "CurrencyCode": "GBP",
            "MonetaryValue": "7.77"
          }
        ]
      },
      "RatingMethod": "01",
      "BillableWeightCalculationMethod": "02",
      "BillingWeight": {
        "UnitOfMeasurement": {
          "Code": "KGS",
          "Description": "Kilograms"
        },
        "Weight": "2.5"
      },
      "ShipmentIdentificationNumber": "1Z0FH3446831744085",
      "PackageResults": [
        {
          "TrackingNumber": "1Z0FH3446831744085",
          "ServiceOptionsCharges": {
            "CurrencyCode": "GBP",
            "MonetaryValue": "0.00"
          },
          "ShippingLabel": {
            "ImageFormat": {
              "Code": "PNG",
              "Description": "PNG"
            },
            "GraphicImage": "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",
            "HTMLImage": "PCFET0NUWVBFIEhUTUwgUFVCTElDICItLy9JRVRGLy9EVEQgSFRNTCAzLjIvL0VOIj4KPGh0bWw+PGhlYWQ+PHRpdGxlPgpWaWV3L1ByaW50IExhYmVsPC90aXRsZT48bWV0YSBjaGFyc2V0PSJVVEYtOCI+PC9oZWFkPjxzdHlsZT4KICAgIC5zbWFsbF90ZXh0IHtmb250LXNpemU6IDgwJTt9CiAgICAubGFyZ2VfdGV4dCB7Zm9udC1zaXplOiAxMTUlO30KPC9zdHlsZT4KPGJvZHkgYmdjb2xvcj0iI0ZGRkZGRiI+CjxkaXYgY2xhc3M9Imluc3RydWN0aW9ucy1kaXYiPgo8dGFibGUgY2xhc3M9Imluc3RydWN0aW9ucy10YWJsZSIgbmFtZWJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjAiIGNlbGxzcGFjaW5nPSIwIiB3aWR0aD0iNjAwIj48dHI+Cjx0ZCBoZWlnaHQ9IjM1MCIgYWxpZ249ImxlZnQiIHZhbGlnbj0idG9wIj4KPEIgY2xhc3M9ImxhcmdlX3RleHQiPlZpZXcvUHJpbnQgTGFiZWw8L0I+CiZuYnNwOzxicj4KJm5ic3A7PGJyPgo8b2wgY2xhc3M9InNtYWxsX3RleHQiPiA8bGk+PGI+UHJpbnQgdGhlIGxhYmVsOjwvYj4gJm5ic3A7ClNlbGVjdCBQcmludCBmcm9tIHRoZSBGaWxlIG1lbnUgaW4gdGhpcyBicm93c2VyIHdpbmRvdyB0byBwcmludCB0aGUgbGFiZWwgYmVsb3cuPGJyPjxicj48bGk+PGI+CkN1c3RvbXMgSW52b2ljZSA8L2I+ICZuYnNwOwotIDMgY29waWVzIG9mIGEgY29tcGxldGVkIGN1c3RvbXMgaW52b2ljZSBhcmUgcmVxdWlyZWQgZm9yIHNoaXBtZW50cyB3aXRoIGEgY29tbWVyY2lhbCB2YWx1ZSBiZWluZyBzaGlwcGVkIHRvL2Zyb20gbm9uLUVVIGNvdW50cmllcy4gIFBsZWFzZSBpbnN1cmUgdGhlIGN1c3RvbXMgaW52b2ljZSBjb250YWlucyBhZGRyZXNzIGluZm9ybWF0aW9uLCBwcm9kdWN0IGRldGFpbCAtIGluY2x1ZGluZyB2YWx1ZSwgc2hpcG1lbnQgZGF0ZSBhbmQgeW91ciBzaWduYXR1cmUuPGJyPjxicj48bGk+PGI+CkZvbGQgdGhlIHByaW50ZWQgbGFiZWwgYXQgdGhlIGRvdHRlZCBsaW5lLjwvYj4gJm5ic3A7ClBsYWNlIHRoZSBsYWJlbCBpbiBhIFVQUyBTaGlwcGluZyBQb3VjaC4gSWYgeW91IGRvIG5vdCBoYXZlIGEgcG91Y2gsIGFmZml4IHRoZSBmb2xkZWQgbGFiZWwgdXNpbmcgY2xlYXIgcGxhc3RpYyBzaGlwcGluZyB0YXBlIG92ZXIgdGhlIGVudGlyZSBsYWJlbC48YnI+PGJyPjxsaT48Yj5QaWNrdXAgYW5kIERyb3Atb2ZmPC9iPjx1bD48bGk+RGFpbHkgUGlja3VwIGN1c3RvbWVyczogSGF2ZSB5b3VyIHNoaXBtZW50KHMpIHJlYWR5IGZvciB0aGUgZHJpdmVyIGFzIHVzdWFsLiAgIDxsaT5UbyBTY2hlZHVsZSBhIFBpY2t1cCBvciB0byBmaW5kIGEgZHJvcC1vZmYgbG9jYXRpb24sIHNlbGVjdCB0aGUgUGlja3VwIG9yIERyb3Atb2ZmIGljb24gZnJvbSB0aGUgdG9vbCBiYXIuIDwvdWw+PGJyPjxsaT5UbyBhY2tub3dsZWRnZSB5b3VyIGFjY2VwdGFuY2Ugb2YgdGhlIG9yaWdpbmFsIGxhbmd1YWdlIG9mIHRoZSBhZ3JlZW1lbnQgd2l0aCBVUFMgYXMgc3RhdGVkIG9uIHRoZSBjb25maXJtIHBheW1lbnQgcGFnZSwgYW5kIHRvIGF1dGhvcml6ZSBVUFMgdG8gYWN0IGFzIGZvcndhcmRpbmcgYWdlbnQgZm9yIGV4cG9ydCBjb250cm9sIGFuZCBjdXN0b20gcHVycG9zZXMsIDxiPnNpZ24gYW5kIGRhdGUgaGVyZTo8L2I+Cjwvb2w+CjwvdGQ+Cgo8L3RyPgo8L3RhYmxlPjx0YWJsZSBib3JkZXI9IjEiIGNlbGxwYWRkaW5nPSIyIiBjZWxsc3BhY2luZz0iMCIgd2lkdGg9IjU2NCI+Cjx0cj4KPHRkIGFsaWduPSJsZWZ0IiB2YWxpZ249Im1pZGRsZSIgd2lkdGg9IjQyMyI+PGIgY2xhc3M9InNtYWxsX3RleHQiPiZuYnNwO1NoaXBwZXIncyBTaWduYXR1cmUmbmJzcDs8L2I+CjwvdGQ+Cjx0ZCBhbGlnbj0ibGVmdCIgdmFsaWduPSJtaWRkbGUiPjxiIGNsYXNzPSJzbWFsbF90ZXh0Ij4mbmJzcDtEYXRlIG9mIFNoaXBtZW50Jm5ic3A7PC9iPgo8L3RkPgo8L3RyPgo8dHI+Cjx0ZCBhbGlnbj0ibGVmdCIgaGVpZ2h0PSIyMCI+Jm5ic3A7PGJyPgo8L3RkPgo8dGQgYWxpZ249ImxlZnQiIGhlaWdodD0iMjAiPiZuYnNwOzxicj4KPC90ZD4KPC90cj4KPC90YWJsZT4KPHRhYmxlIGJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjAiIGNlbGxzcGFjaW5nPSIwIiB3aWR0aD0iNjAwIj4KPHRyPgo8dGQgY2xhc3M9InNtYWxsX3RleHQiIGFsaWduPSJsZWZ0IiB2YWxpZ249InRvcCI+CiZuYnNwOyZuYnNwOyZuYnNwOwo8YSBuYW1lPSJmb2xkSGVyZSI+Rk9MRCBIRVJFPC9hPjwvdGQ+CjwvdHI+Cjx0cj4KPHRkIGFsaWduPSJsZWZ0IiB2YWxpZ249InRvcCI+PGhyPgo8L3RkPgo8L3RyPgo8L3RhYmxlPgoKPHRhYmxlPgo8dHI+Cjx0ZCBoZWlnaHQ9IjEwIj4mbmJzcDsKPC90ZD4KPC90cj4KPC90YWJsZT4KCjwvZGl2Pgo8dGFibGUgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMCIgY2VsbHNwYWNpbmc9IjAiIHdpZHRoPSI2NTAiID48dHI+Cjx0ZCBhbGlnbj0ibGVmdCIgdmFsaWduPSJ0b3AiPgo8SU1HIFNSQz0iLi9sYWJlbDFaMEZIMzQ0NjgzMTc0NDA4NS5wbmciIGhlaWdodD0iMzkyIiB3aWR0aD0iNjUxIj4KPC90ZD4KPC90cj48L3RhYmxlPgo8L2JvZHk+CjwvaHRtbD4K"
          }
        }
      ],
      "Form": {
        "Code": "01",
        "Description": "All Requested International Forms",
        "Image": {
          "ImageFormat": {
            "Code": "PDF",
            "Description": "PDF"
          },
          "GraphicImage": "JVBERi0xLjQNCiXi48/TDQoxIDAgb2JqDQo8PC9DcmVhdG9yKEFjdGl2ZVJlcG9ydHMgMTkpL1Byb2R1Y2VyKEFjdGl2ZVJlcG9ydHMgMTkpPj4NCmVuZG9iag0KMiAwIG9iag0KPDwvVHlwZS9NZXRhZGF0YS9TdWJ0eXBlL1hNTC9MZW5ndGggMTAxNz4+DQpzdHJlYW0NCu+7vzw/eHBhY2tldCBiZWdpbj0n77u/JyBpZD0nVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkJz8+Cjx4OnhtcG1ldGEgeDp4bXB0az0iQWN0aXZlUmVwb3J0cyAxOSIgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iPgogIDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+CiAgICA8cmRmOkRlc2NyaXB0aW9uIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgcmRmOmFib3V0PSIiPgogICAgICA8ZGM6Zm9ybWF0PmFwcGxpY2F0aW9uL3BkZjwvZGM6Zm9ybWF0PgogICAgICA8ZGM6Y3JlYXRvcj4KICAgICAgICA8cmRmOlNlcT4KICAgICAgICAgIDxyZGY6bGk+PC9yZGY6bGk+CiAgICAgICAgPC9yZGY6U2VxPgogICAgICA8L2RjOmNyZWF0b3I+CiAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgIDxyZGY6RGVzY3JpcHRpb24geG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiByZGY6YWJvdXQ9IiI+CiAgICAgIDx4bXA6Q3JlYXRlRGF0ZT4yMDI1LTA2LTI2VDEwOjA0OjIxPC94bXA6Q3JlYXRlRGF0ZT4KICAgICAgPHhtcDpNb2RpZnlEYXRlPjIwMjUtMDYtMjZUMTA6MDQ6MjE8L3htcDpNb2RpZnlEYXRlPgogICAgICA8eG1wOk1ldGFkYXRhRGF0ZT4yMDI1LTA2LTI2VDEwOjA0OjIxPC94bXA6TWV0YWRhdGFEYXRlPgogICAgICA8eG1wOkNyZWF0b3JUb29sPkFjdGl2ZVJlcG9ydHMgMTk8L3htcDpDcmVhdG9yVG9vbD4KICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICAgPHJkZjpEZXNjcmlwdGlvbiB4bWxuczpwZGY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGRmLzEuMy8iIHJkZjphYm91dD0iIj4KICAgICAgPHBkZjpQcm9kdWNlcj5BY3RpdmVSZXBvcnRzIDE5PC9wZGY6UHJvZHVjZXI+CiAgICAgIDxwZGY6UERGVmVyc2lvbj4xLjQ8L3BkZjpQREZWZXJzaW9uPgogICAgPC9yZGY6RGVzY3JpcHRpb24+CiAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KPD94cGFja2V0IGVuZD0ndyc/Pg0KZW5kc3RyZWFtDQplbmRvYmoNCjMgMCBvYmoNCjw8L1R5cGUvUGFnZXMvTWVkaWFCb3hbMCAwIDYxMiA3OTJdL0NvdW50IDMvS2lkc1s0IDAgUiA1IDAgUiA2IDAgUl0+Pg0KZW5kb2JqDQo2IDAgb2JqDQo8PC9UeXBlL1BhZ2UvQ29udGVudHMgNyAwIFIvUmVzb3VyY2VzIDggMCBSL1BhcmVudCAzIDAgUj4+DQplbmRvYmoNCjggMCBvYmoNCjw8L1Byb2NTZXRbL1BERi9UZXh0L0ltYWdlQi9JbWFnZUMvSW1hZ2VJXS9Gb250PDwvRjAgOSAwIFIvRjEgMTAgMCBSL0YyIDExIDAgUj4+Pj4NCmVuZG9iag0KMTEgMCBvYmoNCjw8L1R5cGUvRm9udC9TdWJ0eXBlL1R5cGUwL0Jhc2VGb250L0FBQUFBQytMaWJlcmF0aW9uU2FucyxCb2xkL0VuY29kaW5nL0lkZW50aXR5LUgvRGVzY2VuZGFudEZvbnRzWzEyIDAgUl0vVG9Vbmljb2RlIDEzIDAgUj4+DQplbmRvYmoNCjEzIDAgb2JqDQo8PC9UeXBlL0NNYXAvQ0lEU3lzdGVtSW5mbzw8L1JlZ2lzdHJ5KEFkb2JlKS9PcmRlcmluZyhVQ1MpL1N1cHBsZW1lbnQgMD4+L0NNYXBOYW1lL0Fkb2JlLUlkZW50aXR5LVVDUy9GaWx0ZXIvRmxhdGVEZWNvZGUvTGVuZ3RoIDE0IDAgUj4+DQpzdHJlYW0NCliFXZPPboMwDMbvSLxDjt2hIgQSqFRV6ugqcdgfje0BKLgd0ggo0EPffmlspmUXrJ9FHH+f46goD6XuZha9maGpYGbnTrcGpuFqGmAnuHQ6DGLB2q6ZF3Sh6esxDKLiuR5f6h5YtG+HE6zLFvTczbf1Z1GxFs73X8pDdZtm6Et9Hth2a1PvtsI0mxtbuVMPNvVqWjCdvrCVPXlPVNdx/IbelmM8DHa7pZq98OM2AhOYiCW21QwtTGPdgKn1BcJgyzlPdgwD4iNigRgfHNrgUGQORU5YINLPSewwoVKJRMwQ09ShDYgKURHmiBtCrJxS5fToUFJliZUlVZYbRDorUYINYQC6/a9Z5OjF6dx81eavB4J7HiwqOanceJYke8+SRZYgHdJzaJFFDqVPhALxSIhtSO75JwWh8jxI8F6Zeu6q2HNXJZ67irpK0TClPLPVxjNbkfe2HYf0BCRKUCRBogRFEiRKyLg3qIwkSOwqW8aIErLUG2OmvDFmOY5xGdd9om6rfpequRpjF8Atn3v59zffafhd0HEY3Tn6/ADc9eH7DQplbmRzdHJlYW0NCmVuZG9iag0KMTQgMCBvYmoNCjQxNg0KZW5kb2JqDQoxMiAwIG9iag0KPDwvVHlwZS9Gb250L1N1YnR5cGUvQ0lERm9udFR5cGUyL0NJRFRvR0lETWFwL0lkZW50aXR5L0Jhc2VGb250L0FBQUFBQytMaWJlcmF0aW9uU2FucyxCb2xkL0ZvbnREZXNjcmlwdG9yIDE1IDAgUi9DSURTeXN0ZW1JbmZvPDwvUmVnaXN0cnkoQWRvYmUpL09yZGVyaW5nKElkZW50aXR5KS9TdXBwbGVtZW50IDA+Pi9XWzMgMyAyNzggMTFbMzMzIDMzM10yOSAyOSAzMzMgMzlbNzIyIDY2N100NCA0NCAyNzggNDlbNzIyIDc3OCA2NjddNTNbNzIyIDY2NyA2MTFdNjggNjggNTU2IDcwIDcwIDU1NiA3Mls1NTYgMzMzXTc2IDc2IDI3OCA3OVsyNzggODg5IDYxMSA2MTEgNjExXTg1WzM4OSA1NTYgMzMzXTg5IDg5IDU1NiA5MSA5MSA1NTZdPj4NCmVuZG9iag0KMTUgMCBvYmoNCjw8L1R5cGUvRm9udERlc2NyaXB0b3IvRm9udE5hbWUvQUFBQUFDK0xpYmVyYXRpb25TYW5zLEJvbGQvRmxhZ3MgMzIvRm9udEJCb3hbLTQ4MiAtMzc2IDEzMDQgMTAzM10vSXRhbGljQW5nbGUgMC9Bc2NlbnQgOTA1L0Rlc2NlbnQgMjEyL0xlYWRpbmcgMzMvQ2FwSGVpZ2h0IDY4OC9YSGVpZ2h0IDUyOC9TdGVtViAxNDQvRm9udEZpbGUyIDE2IDAgUj4+DQplbmRvYmoNCjE2IDAgb2JqDQo8PC9MZW5ndGgxIDI4MTgwL0ZpbHRlci9GbGF0ZURlY29kZS9MZW5ndGggMTcgMCBSPj4NCnN0cmVhbQ0KWIXtfHt8VMXZ/zPnspdkk92E3EiAPWFJSMyVhADhlgWSEARNQhJIQEiWXEgEkpgEEG+EVkWiGKitbb0AbWlfCwqLV7RWsdZaqwhaqbe2oKBWUaEWqVWy+/vOnLNhCQH6vp/P7z/28N1nzswzM88888wzz5yzgRgRhVM3yVRXWpGVw9587U0i1ozcuvoVnnbzfaFLifLe4Xn1q7q0FbXLfkY0YzuRdEdT+9IVt3iejCAaX0dkfnypp7OdIiiUqDgd9R1Ll69pOjjuYA7uJxMNeaC50dPgf+iDYpR9DoxrRkZ4XFgv2h6F+1HNK7quf8+1/DGiMPSf0r68rd6z+J2aqUQ16D9q4grP9e3hY9Wx4C8Bv9bqWdG4aUrn27j/I1Hog+1tnV3+Kwj34928vL2jsb3nZ8rTRAVRRMom4mOViO77T+vxWvvkryWnhfjnj7Oakzk9cG/mh2eSzvSFtFkKwWvhvOKDeuapvqtpRsiOM0nf3hDSJloK+oQM4zkhw9hcqqRryISaDspCiuSr5EpSUCorh6VnSSVS71Nz0WSCTuU3qEmKtKhSqFmR+Ec5QiH+Mrrej2YTedtjplXMII00/xn1z75ylmueyh6tI/b84X9jTBPVdXykxPU9grX2yzWPdhlpRnaWZKQlUliBkZYpnt1gpBWKYs8baZXC2VdG2kRDpFQjbaYb5FwjbaEo+R0jbaVwJdRIh7AW05dGOpSGWX5gpG2UaQ0z0mGUZ33ISIdTfEgUJGGKFXcPC6l4mmEsqpGWyMLyjLRMY1mhkVYohf3ISKs0jL1lpE2ULDEjbaZT0hQjbaEUeZeRttIw+QsjHSK9qcQb6VCaYKk20ja6xrLbSIfRtdbJRjqcxlr/ToXUQkuBLuAGaqQGzEEDeXDvQaqe2qid1lCH4GpGrkYpyE0FzaFsGgNoNBNcbShfjvoazUC6A7X4t0e020atlEkhouTireUgNdeQokTUTkdqFurXowUqbFna0tVyQ2OD1uDp8mj1be1rOlqWNndpKfWpWk72mGxtZlvb0uWN2oy2jva2Dk9XS1trZsiMgWw52lw0UeLpStdmtdaj3TkQaAm6DRZYowrctVIniluWNOqNaRWeVmRMB8dyCEnT25bjexqY6lG9FVm8EY0ygEs0Oq2zvrG1obFDy9DOa//iVbWz/Q+oqenyzBNVO/sr5kB32bgyCet0XmNHJ+fPyczOzswdvK9ATxmD9cQ7ytA7GlzOFiEjN58uUcKVsgK0g5Yhr42aLjrJGvgahUl2oqRR3DWIVnnbVeCoEFxloiZXepforVVwVQ7SYyl6bEL9emGeAc560TY3c73lNqSbjem7llYKI+0EJ68XGFsnN8Ignbd0ah6tq8PT0LjC07FMa2s617C0jsalLZ1djR3IbGnVqjIrMrUyT1dja5fmaW3QKvsrljY1tdQ3isz6xo4uD5jbupphG9eu7GjpbGip5711Zg5maYOvtrPWFbQSCJrjGlsl9HCVYOf3nXqViq7GVY3aVZ6ursZOzjwdDJ2G8vWJnSaUsgJ3fMJWQ11cOc0i7RGT3iCa46u71ai5BOtdu2jHmlHXYxhPK6428Oqj4XXSDaNoEt+dot9W9KEhHVgSnUIfLcK4gqXQxLR6hJHohrkCpV2Ctx75y3GtMTzdCuhR73WJ4ctWC8/Y3D928CeOFOZ3Vhe6STcZa04Tue1ItwnZA9rLEDPH5W8UUvGUR3jaJaixXPSjy9EsDNcjzK7RMMMuIW1ASw3GqLiE7SIng4qEyXL/2mhocj788pxBW9S1FbxsOsUyXyX0drbtViFtg8hr69cs51pu9KSPeLnw/8v6Z6VJWKOuvQbRWsYF9NskdNNl9NomJGrApc+zblFtqLtSzJq+1HVb7zpPcx6h3zajXjtKeF+6LCv0pTvd04mliIU7raNlRVu6trq5pb5ZW+3p1BoaO1uWtqJwyRrt3IWgodSDpd7a2rYKy2hVYzqWdVNHY2dzS+tSrZN73c7GjpYmowmtq9nTxR3DisaujpZ6z/Lla7BPrWhH1SXYmFa3dDXz3j3Ld2TqUsBrNMElay0r2jvaVgnxMjrrOxobW9GPp8GzpGV5SxfaaPZ0eOrhS+BQWuo7ha+Ai9DaPa0ZRSs72tobIeT8mXPOMkIs3c90ti1f1dgpuFsbGxs6uZ9qwBCXoxI6Xt7WtowPpamtA+I1dDVnBMnb1NbahaptmqehAWOGotrqV67gHgxepSsgnKe+ow1l7cs9XWhlBfdUzWKNt9NERI9ZsAR+ZYqVHuy/6g3vlWnYRxYqdnW1T8zKWr16dabHcGL18GGZECrr/94sN5F2YczBDqpDmAVvcwXM5aJdd61pbzSMpKMzs7lrxXJ9+9O7DfjJlUGeObCKKrC1zRHbULux9osNq9cGtMD93MC9ewwEHMM3HcjDjXel8Op8LitmzdFK22EmxZgjzWBI1wL7+5jMMQPVpXugFtx3iYF3ivWTKZS1FOWlkGxOvxpghC3tXZ2ZnS3LM9s6lmaVFs/RQ2naL0LwfAM76AX5VVqvdJILSDAPp1z1ZVrAPqEVKGsCJHk4mZSHaR7478R9maD5FAX+cmAdMBPIApxAATAbqAam8TLUeQl4kbcBVAl6lBab99NK9MX72wBUCjqPNqBsgylfv0c/G3i7PC3ydwhevXzeWT6kJ6E8FukbkQ43byQJNBJwIX8K+u9EW9GgQ9F/htLp/xzp6Wh7Msr5+MtAKzlFvkukj1Iv6gD+I8gXaehnveA/Kvg5rZSHi/olou2jtBZpiynf/y1oOOBQiOaCJxFngAdA09B/uaH736E8F4gG8nk9zgOahzKH+hFp0mkuK12DOpVc9zxPWeY/gTPQAqWBxiAvF0gH5isP0O2GvjcCdcBc6XNRf5HpYVpsYClk7DD0fh5wElXEXMzT5yIA6OAdyNwMuhN4GzyWwDwMBJ9fY15uPAeYC2N+eyHT2MEA/U4XczEA6HMf+u8AfYTLEqT/svMAvYAyMRfB4HOh9+3gY+VzPwgVNnARukHdJ8Zm4XMvxsPzL0GFXo4a+hmEGvbdCxoOGoIx/tTA5waeBX4LHVQDRXxdAJtNM0X7fExOlP9KtKPf9/L1Ap5rDSru5WiDHhKU+4BIo+/159Gd/s/UV+g2njbkLBtIYS+VWGtCL3wdDKATxLrE2rgQ5WvWWDexkGlo4J7bC5+z/5by9c7XnFjvfH6Ndc/X3kCKMd/NdWzaQ4S51Me6D4YPfaC9CUFzbTE9JniqhT94T8xnmXoA8yXTYuWo/3HwPSRsPQ4+p0P4CK5rCsyD4Scd5hPcb4Hf0KXpz6jjpTJzHOi/oM9pov9eY71xm69U9tMC6QOKM/RDAT2ZfoG19CqtNV1LLXz8plR9zCgbi/G5QeOBEmUcpQDjDf88Rf6WIpSfw0dzvzaFtsvf0S7lEegDe0AI/KoVMlswTitkMA+D/BhPyETkkbhfH1gjhg/YFbCB/3aODJ2es964v+Fr3mgr6Zz1AP0NtDcxtnEUhf7/J1jmQD3LDOhvrr5HGLY8WD/MyLf1y6OvUy2wXqV83xHgM/TzGvAno15J0JhvlYf7HzLsfJkxxjn9Yx5o31tgB6k0o3+db6W7YFuVqo08QKVhm4UD5DlvvQ2kAXuXfX6faSf8oY3sfL8y/4wWAZWGX+f2bOU2z+VBulT0lUpj5cOUhnJur1F83zT6tRr+5Igpt38+CONMQDkJW+v0nzD2yNuM/XMy37+MPN5fsZB/GpXB7oqAPHU99r4eYW/2fj6vsHWL8rqQba3wz/q+GwMsl6dSofQQbP9dPucoe0vswWsNwP/7fyn6P053Cb3sBH5H5aof/Q4nZxDWG+gFQpSd1CMg9m3/EQNPK+U0jM+XsdailG8Qyzx0zp7uUDZDh1x/7VTIbRGIRz7ft+YaVLfH45AX4xVjhL+Vd4r4SJa30B2GjjjvfEsBfOgGrLvdqPc99FtMQ00/AU6Ry5QHW+lBO0UUo3yP7lD/QiM5pH9SGpDO7iZFUmgcMBKwywT7yfKflj70/5vHcDy2M+K1O4347UMO8OVzGDEZRyYHykgHCwUdBdyiQ9yPBKYBvwGeMcDb+wC4LwhDoMuXQf8IjAbm4P4rYDtwCPey9IX/W5ZIY2QJMcyXfp+Qx0H3DgR4l+jwfyTiMqLvg6438JKBH+ly+Z83cMrI/3Uw5EwawYH0RKK+Q0Q+D7CZ6MxiUMTFfbA03xYifyfobwA70m7QdJ3P/yQwwbjnvA/jvvUsKAo01UAhUAee9aCfAxuBWQZmIr8CNEZ/TC76e0bvy38b0t+Bluj98fq+PXr/AluNvm8EDkDmJ0BfMu4hcx+vMwJ1Eer77zL6hyw+LyjOYP4HwINdzTdX79u3TZfdx8t+YfQXhvQUo97PgY90Pp8PeThH9EFuf5s+Jt+LRrttOnyHQe9Gw3wMMwwd4TDjr9DR96KOwD2H7259jH7eR68x3l1G35C17wTKcCz1X4H7W4E7MIfvAguAA4bvKRN7E84ZwNPyXmqFz+L2+xL22kxzAY2S/0SjTD/1f2xeRt2mx/0H4d9+HTh/KAdEXFdhxKdTArEt38+N80V44OyhJuvru/+8gn1anD3gi02bqYCfO0xrqA77c4WIlbmPPg5/9ABdBb5l4kzDfQrylA8Ri3D/9x7Nk1+jq+Td8AngUSowNs63SsRyVuUj2gRK8iZRXmbS6ArlX7QGe0qpugZt/4AieZvq02jzfgozmWkd94Po/13RF987QXke+lyKdByPGywSOTnl/hJlV6stFBW0x91knIs2cJ9lkuG/JtNwUxv6+pCciGnuhQ9uwV52M3h6QDcrb2NPnUfzBEbhrPIWzhMfoL1t6Dcc+9StlML7UP4Jnelx/RHen/wWxvAW/Pa8/ji4Uuib+9B/if16gnFGnCBipAWISaLhhzcgvUfE4ZNE7JXnP8T3Lss+sli6wUPg+VDM7R3Kt/7/8HhPzPk+I0bg9R8T58QN5kmIH2XK5LyCn9d7EH4/+My5zzgTvSx0FKt8S8z0Fs0UZ813kL+VWi0hiElGg/9rijEfEn1zGcdZ3CLtEvb6T8SPGJtchbFGiXNimfowznXYJ5F/twCju9VoihY60OP1MoOK86p8nCaK2JLEvhMu9ptfUgX2wF7TPrR7iJJNnJ/nL6OxIr3T7+8/VyEe4P2jrEzsg/ys6/a/J+KHfRRtdou+QrgcQh6+96GNkClUY5pINuxPyRhvsvl1jHUxbVbn+c9wWzY3434pziZrqAp2eLNlC3T7DsplEQsUirVhppX9scxtiDvSoWeDWk5jP3wV+bfCLuPJxfsz51FZoF/ovl7I/zAlwBf8DIDf8t+uo+8V+PMkYJmYQ8gtYvvj+hxz3ckfwZ7vwdg2YD1V4aywFfmvIK7g84854DYg5gHzL8Z+lhJoqCkW+/0ZShL2A32YrZjXJ6nXKmGctcJ2JylbaVLgHCHONvpckVjrBuU2w+fN9CbFqd+H3cF2+PwFUbEWTO9RqLoC/RqU23m/rA+C548YI+xU2IohUz/V21oUWEt8ji8Ug/efWQ8Y5x+DDtQLpzzuCdKvoBeMUWH73P74WhE2NIAGxsvXIrdHvmaErQbmx9BTP91HVSLWn0oLzDfAVh6hctPv6Sp1BnzMlXSVJR42+EuK5mcBc5NxhvAKnxmr3k8T+dmNx6QBnQXODoEzpL7vURroCtDF/DcISF8NNMPWeNyw19i3U8++e+d5faeN/GuM/Z/v4ajvv1Yv9y/Ry3xRRvlinYd/+nYYcQP2ad+fga908HuxF08x2r3GyOOINOgriJVu42XKOnYqUM73vkBaXkz3oZM8dSXm2UlzcdYuwB6QqjbTT6RraZf0OXzifbRLXUfb+b3yAI1WVsB276Fi9UXkH0CchnyZn93vhd18hbpNdJs6HvPUDB9xmELUSTj7oJ7pOspXn8N55hDaMSAX0NuKD0C0gpiWYG9zYDMJYn38FG38FGkGfwj7go1uUuw0je992Hfswv8dF2f2MsN3zjSQjDmbrvyAru5/9vMpzgHcxwFizel735WmUfCRR2hWfxzPn8kdpjz5K8j5OUUKP8jXJrc7tMH3T24b8lEaoW5G7PBzGg+Q/AtKB+8oDkWmJPkmSmIdiBP+TkNkL+XIIyhVGUlXyKtppHw9fH0yZck3ULG8ELHuw0ivpkT5RpyjovzfySpFCSRSlvIk8hMpV9Zj4mwO6QBNAMbJGo3hsbL0J0pWbkX+V5Qil4AvBOtxFvrk0CibPUtWUTYdsQHn+9T/jTyHQuUEnA8+9f9HngG+9wCLHnvjvJDJ+QVfAmUInulo1+Ax13Hd+R/la4PH3+bh/mdxz7EDZ18vB86BfpS9AH1q4jnTScj4V5pr+g5nKP0MFyPOUQ+Js1SIYjwz5bG8KUn4F+6Trgx6rsrPaEV8P5KfEc9dLWJvw3lL0Z/VBs6XZ8+VU8Uz6V49/kMdfo4cJ/SaAx1xPVmhryyuS3aSEji4vsT5qYvMXBcCSEur4OLvpgJWhnP0LNjWrZibW9FOrf9TuZbGS99ibqB7zH2GOLvkkx16D5XdZMIay5E+o1wgjetUOoaz7jH0/5yQY7T0D+Jnhx/o8K8xYvk/DEC1DnFeEPF0kL8e/Dld0LPJoGeJF6b/5TNLMZ98ns5/RnlRivjhxzooAfS9wLOcgVQJei4JvuMD6CN8z+J2MZBeRA8blIs8qwx6ZqLzzztbb5BnlwF6zaWeYQ72LHMQGvFfP9OcJ+JBS4AG9qVL0fP2yXn9zwUHfQ4q5moHOfqfa4hne9jPn9ZjZGXw5+OcWi9Rfmn639lg7IXKISd/h1JmPG897znhADr9guXGc9hL0YFzZAo8g70EPed59CBUnAEvAuN8mmv6F/ZNHVEGCjnEmXEQmEb4/81hxik6GOJseRGYenGeASxOogGI5oCu1+vwv2TgCwNPcMiMGIeyGX2di2iBwd7X8Hl40P8FcNRShb4A8ys6xP59EZi+R8zsQ50lVGze5T/Fz7cXxev+oxwWnBQ4zN8G4D/FEdB7QI8BvWDMGh93v8yB/o12/w/zGICYx0vPC/TT6//3+fPiP8Vx6XFjXv+LcV9MdiAkkIbf+Aw4rVP+vA1tDCb3xzQDKDXPpyygiPvUs88YUS/ffw/3+XyfMHAf8Jj+rsv/mfwKYqZXqDS4znl2wJ+DcBj3xntGl+ljf5/5Surg60Deiz0aQBtbBtOPuZGKYX8nzfeCvu4/aboWe/kOehv4qyJ+asp/nqpTaaf4+S6xKnGOE+/RGY+udwbOAv6/ABrwNvbvOfy9LeIkfjaeajHaEO9elvH3ev3PZns4RR8/DsKNqMOfUd8h7adpqPeB0eZVRuwvwPtGWSo7TlWI6wHobgddAyxCPPsCdHYLm+dbb5wHAvUcBiL4Pd/nAf7eOQ3IkNNouYhNJT3eEc9okTZ8f6URc5iBaGNPHmrZR1us+7FHI3IxR9LjSgLdgnJuM2IPtHh1fYnnY/rzM54ewdvCmG43RyPW/ZRSLcex/3xEGsZ0M2LEKmU/VSMt4XxQZ7zDzgU6gEr+Phv4hX6OZT9XiDkGUg75FM7zH1Ga6V56TX2cbue/QxA6yaeNSgNJyCsxH2I/UV9mQ6Ux/rXISwOGKzupQbxP5jhED6Jeg3JIGqkcYqq6039aJfaOulPaKNLn0YFg7+plnHIEl/1v8/8bQL/nQDoEulSkcYrFeG4ETNJfaAUHt0vzcbYF2Byg0JsMnv9RXqAloI8CqRzg77SksT2WZewNcxUrNhF7DyhX3DRJdSNO30dNSjTiZ6Lfm8QcwHbEe22cA476v+LvkYw4kMfsL54TQ+qxoXgfZkqAnb1LFstCxDh/F3GKS6lEXHYTeJ+mq/nagv0WAI/Ahr7hQL2fcvDfVwSA/O0c6Osbvg7kYZj/T6gO8KAv/q7Yxc+3/Nm6OLPy8y3OyoEzcvBZmJ9xjfPtAn7WDYY4Xwdw3jnb/4z0uX+/fsb2P3POGRvn68DZuv9cPciZmsvI2+X1OI9aLcY/04B4vyB81A5airH+lr1M1wFL+e9DdPD3KOJdih30ALAL4M/q5SDEnQV/B+JzGfRGA1uNdxHbgniNuoIvmHcA+LuOgbhQ/mB8Z8F//wD6OvAfg35h0N8p82nbAFwFzDUoR7HsoGLQPAOlQAZQgnxORwFJBkYDWcjn6eFALDDOQDbyU436c4KwGPlzBpGjzCgvDvAafFlAPlAQAPILjD7ygvobh/y8AX0F2mke2HZQ+wPlmAfMB2oMOg9814BOAMYb4OkJyOd0JlAUDORzus5AvoGJyOd080BcQI6B4ygFH9dldtCYub6HG3rOMuYjMDejjHkpMeavNDCnxjwWB825mH9j3s+RAzYz3rAdYT8GAnb1uniOcYkYj79rAb404mJOHw/GpWJZ8Bwy8BTH+eWIbV6hB8V7J1DjXVsR6F+NZ4bPAm8C7wNHgbeA94CniPq+1KkY18tB4PebUL5fp747jfXNsUWn+ke5x79MgPst7gPhewIQPgw+D/xTgBYO/k5L/C2NjsBf6gzjf8Ei7k0EeUmjGlEe/AklG13qM3yQvNGUYqTS+/P436Xk8mefNI7GX7A1/sSX/0VYCc0S9+LXklQK71pOc6kC6SqMZj5oDbAQweAmIbsmwkKNUmkiFaFuGWIZ/lvmJuOXmqvoer9fcKSAoxAcV6M9ztEofr/ZoXP4j17sGvh3XoN8DA36R/O/Ozv/4565cEFNdVVlxdzystKrr5oz+8pZJTOLiwpnTJ/mLpg6ZfKkifkTxo/LG5OdlZmRnjI6OWmUa2SiMy4qwmEPDwsNsVrMJlWRJUbpmpfVFXnlJC2i2OMqcnlKMtK1orjmwoz0IldxnVfzaF4QJdlVUiKyXB6vVqd5k0E8Qdl1Xjc4mwZwunVOdz8nc2iTaTLvwqV59xe6tL1sQXk10hsLXTWa9wuRvkqklWRxE4abxETUEFJxabUib/Gq5p6iOsjI9oSGzHDNaAzJSKc9IaFIhiLlTXG172EpU5lISClFE/dIZAnj3WKkRZ4Gb1l5dVFhQmJiTUb6LG+4q1AU0QzRpNc0w2sWTWotXHS6U9uTvq/nrr0OWlKXZmtwNXiuqfbKHtTtkYt6etZ7I9K8qa5Cb+oNx+Iw8kZvuquwyJvGW509t7+f2We7ZF41yeHSer4mDMf1xefn5niMHFOS42viSa80w8vmVifyT0IxdN3TU+zSinvqejx7/d1LXJrD1bPHZutpL4K6qawaTez1P3Nngrf4rhqvo66ZTawxhl48d7Z3SPnCaq+UVKw1e5CDfwWuxAkJiRH9PGUXKiaoBcqBhhMTuRru3OumJbjxdpdX6/caLUl4lNxZaTVeqY6X7AuURFfxku5ASX/1OhfmdnZFdY9XSZrV4CqCxu/0eLuXwLqu5RPjcnjDTyckunoiI7T8rBrBq0GqWQ0tmldNhpJQK7gC7IZX6XGIm/DTOvkiAR0kR0Rq+S40w9spchXVGf9WNcehAQ2KLknTDaGy2usuRMLtMWasaE92Fmp46jBhLYViMr1ZrnZvlGt6/+xysYpaKqpFFaOaN2qGl+rqjVrerCKxrrSinrpCXQTelqu8+mnK9R/ZM1ZLeCyXxlJNIWeOmQErSy7qqW5o8jrrEhqw7pq06oREr7sGM1zjqm6s4WYHDaUeSRDGUSNspbJ6doVrdvmC6gmGIHoBb05JKhrQjKs6QW8GBui1JFm0ailBrgGjAxlaMRKu6ZPx7TUnWQAHFC5yueFOn6xVswQKcEMMb6pW1Fho8PH7cxpVuTnNKAm0ZuK3aGdGSUJiTaL+yUiXUKwZHaOGhSu1JFAEN4UCC+xzRonI4rqM40avVbsaXTWuZs3rLqvmY+PqEVo2lCF0bsxV5Tl3QcqCmigRxYEbrkxvcVpCsHK9M8V9/23JgOJZgWKtx+KaXdHDG3cZDRIkn+UlbsLuCREJwhfwBe2C79UcWNJiQffscbv5Ym6eyBtxzWrocVVUTxbc8Cc3J9zA+4qk2Wx25fSMdLi26Xtc7I7yPW52R8WC6qcd2J3uqKx+VGLSjLrpNXtGoaz6aQ2bhsiVeC7P5Dcav+EtzcWNRfAnPO0m6halisgQ9/V7GYk8SyCPUf1eSc9z6B0li47cJKFE0UvcAW4FeRY9r1vkic8e4ipzh6hui9vqtklhUsIexrMeRc4z2CWtjB6zsTCWsAe15orsvax7j9WdoHN0g8OtS3hH1dmuqxZUP2YjVBPf6Gg6/8Bc4pox2dhWirQGbig31TT31NXwxUYxmBr8Y17mmoppck2FICabN8TVON0b6prO8wt4foGeb+L5Zpgoi2Go3o25L/MybgELqxOxJLX4VxJ6HF/wmaqBU+lxfJQxrYr/lTTLx0l1qkGnMzdFkZNNA3WCTqJcNhH5E0BRTtvxfQqQWA5NYWNQMgY1s0Czcc9pOkslP2qmIv8K3KcgfzToaOM+GfdJoEnGvYuNFPwjjfs0lINSGTNjRrPE926muMvYwT72fB9z9LG275j7O9b99aavt30t//NknjPr5NaTUu0JlnWi9kTbia0nDp9QPz6mOT86NsX54ZHRzg+OTHEenvK3qr9Pkavob9l/k/7G5KqsaaFsBNp24FsD3IDs38dGuFOGDiv+q+x30vvsPWWy8603hzn//Gays+6NTW/se0PmxIvEkTfUvf59j70xdHgx6ONvhIQV2/eyGLedPf9cstP9m9Rpxe7fjBxdvJclupOfnOKkvaxtL9v7VIiTnmL0lPaU+6m6p9qfUjnZ9NTBp04+pe5lmjusBKxP1D0hbXvi4BMSWnaHPxEaXmx/tPZRaY882cnFHkoFQCkgUy++GYQf6k5JTi127s7aXbB7627Fvpu5d4fHFNMj7Y90PyIfeeTkI9LOHXnOHWXJzqdZAot/dDKXKP5JZv81sz/EnmWxbAhNxjxEu28pm+zccv9o54PAA0D3/ewnxSnOrT/e/WPp3uI8p/2Hzh9K92xKdv5gc7LT3uvsbetd29vbq959V7KzdCOz38Xcd4Xai+0bnBuk22+zO2tvY+O+V/w9aRX6Xgl0AZ1AajtLaGdyOzvVzv7S/nG71NzOatrZXv9J983tUGdba4mztTjHGc/iqobmxlWZc+UqE+bFg7p1tTnOWtDFC0qc1xSPdi5ccL1zQfEY55CcyCoVs6vkyFVtMrPLBXKp3CavldXaCuauSEkvdleMGImvIXHFy+beOPfOuXJ56TBnGTC0NLVUqiltKZX2skh3RnGSc1bxUGdJcaJzJgb9TTGUwIaVJFTF5ERXRTB7lSPHXoV4tYqR37mXRTyaYAVxuDNAnfYCe619rV2x27PspfY2e6/9sN1vNxcg74RdbiNWSqw7hqlsL9u0p7IiLW32XrMfoZC5bKGX3eFNquDf7vIFXtMdXqpasLB6D2N319y2cSNNHz7bm1NR7a0bXjPb24CEmye6kXAM3xND02s6uzq7VqYZH9bZxQlx0olEZycvYjyrn0Vkd3Z2dXWRXqUzrZPS+DcKGL6pUzCChzPztox/jH8T7050wwRnZxdnEpVX8m9xx3N5Q+KDHjr7uxct6yROfU19jW5W11E0rRHf53yUifBMq/XfugZ/++b7/33J08v/4qP/XxlsKDzU13Q8qOAF+jM9Q146EMzNRrNUZgKNpGN0iv5woVbRnpPpZ77D9Aa9RE9cgE+iX7M+egfLuhuOok/kFcAVLYI8O5C3kjayM2wNS6RtzCFKx6DtcKYM0tYU5qcjkO6HdIR+yArpiNopD0XBO9JL9IC8TtpPr0Lmq6WNyPPjXPcay2ZF1EmP069EA53ob2NwizgE/px+Qt8/m6vu8j2rruvLpgj/aXoS522ugbXUw3/RZHxOsi8ZzrLSUGZhgTl9LlBoLpGvlZ6UpL57cLOZlgIe9i64N8rTBgxnh6/N18xUugcSfMjKqRet7PI97dtOi2m3dAh7xlf0KyXahF1a/oAc0rdk973FPvP/i8SvqeR6Cu2z+7/WGzOtU1ZTtPIutyH/S7610Ot++graP8SGioHy/xUlBDuCH2mJ/02jmgOblMlMTneYSVJlSbZaVFlBVsH+rP0RkSw/PyI3IndM9pDEiMQhEYkR+5XG7+6fI+9X1327Vs37Llb5VEwKNfnmSw/B0sNopNvBf0kbIoeZZdkeDjNKoIICNBWbzxvizbFkKcIROT7RxEks633wrrseZEO39N691Tf/Q/Y7FgfH/cIHx3yTfV/6TvgKPkX7EtovDLQfRmaTHEKmkPPaN4QdFxnhkEYnxnBilrZt3MSbv/POLb75n7HnWSQbwl768Khvqu9z32e+qcf4i6mXMIiPlBCuCzbd/YlsNiukWC2MHlhoZ1mslLWxXqbaZOaOGVnCFPWBhUqvldVZWZmVOa3MbmV+KzthZQetbJ+VoajWykqtLBuhlZU1H7Cy561st5VtsrJuK2u3soJAnSNWttbK2kQFcGuilcOCf5vgzxIdoJUJJwU3Wtkqelgb1L9eZ5+ooPdcINpyiJp691sDfaOKW3RvXrzI+FzX/+kIfAaWnZevF1BWGsVlpdUuXpQWbC4wFQa8xDTfEaZJJ1m87+M+Bxvq+4Tbi0QbYHvXwfasFElj3cPtagipFDXEFF5bY5JVe22NGtkdxbKjmBbF0BMVoJeC4B5YlKS4YJQasbHJaSwiNydSvW6n7+U/9f2B+VgDu9339ufvv/Htc0ekV9/z/eZhdZ3vp749R0+cmSkcm+jfhP5Dqct9pWrl/30MC4VBmUmxhamW2hq7ulbdqsp2tVf1g8hqTPQsu8qiVDXGNktVEdgptTVMJmttDUW6w1h2GNPCIOqiflEp39ALcF2aMFCkdOlzIxKjEw1sUCrP/Fk62eeQ56nrjvm2HPNtPEaGjMwr1meTu0jmf2OK/iKPqMhk21S2SWXdKitTmVtlpLKTKtsXKGpXWZ3KnCoD88FAPpgHm0998eQbUkVsYKP52g7oaAr6D6MydxaFhISZFUUNU+3hzBKKSaLIOjsrszNEh9121m5n++xsm51l25lmZ3pHovmcglxMWmDm9PEnsphodJbIkvNA5KN990X6vmXlUlskMylTttSdeUFd990zP75JzuWiwF4q/Z+rR9V7yUZxVOJOH2KGD6Ch8SGO2poQRYmprVGGbItn3fGsPZ7VxTN3PMuOZyfjmRbPAiO+gA1pFOEgYUaSa6QUHRXJLekodoB3fI/71rPrsfZL2Rrfn9958Q/v/O35P7wtvfxX36N72HpWySrYTb5u355jTPb5P/6H72uxX+m27RC2NQSyptpNJrMN0kZHqZBWVU0WC+zbIpsiu6NZezSri2bZ0cwZzQwp+20nSGdc1nDG7T0iMUdRx6ZiceWMUx03fbLV93Pfu9KaPhbhe9v3re8Ay7/hVvnFO/6y0gcRPn3v777xawIyPSjmMpoWuXOZzRZpjZRlJdxKYWFWRY6NsUVKUmRtjSSRqkZATuwCke2xbFssy45lWiyf0ev4ZJ6VjvKDvC6uyHx9ag0po6NMZiszRFXKsan9CpLuO8MiH+plN/s2+874bmffu6lbiu37VF337qs/fHtkn1d+41VfXbu+p0zCnJsw51fQXHeWjYYPGxljNplihpGSnmYbKQ8dqtXWDB8+VJFDamscZs2cbZazzW6zZDbLQ6ggNwurDhOeq4t6rqxcn0qiNmp00giWq+WNzWSjM5W8saMSNSVWzWQuLTpqBIsdIasm337o9Z++19LZ8OEP/YjlzVz31JabGopHI/KBrTJzsu/DmPW3+E7lt+98dXfTOHbvgff3vZjV3vjs5KvHJiVlTJnXNfv5V7f/dvTCax4aXzwmKW2WZz0fWyyWM3+naWaF7n8wSZHM2HmxwhWueRapu+ixVjbKyhQrO2Vlx4R7f9zKtlvZncKNN1hZpZVNCvA0fyeYXg3sG7eK4kLRit7E+6L0cVG/y8oWBiqHWhnqHheb1++t7H5RK0Hkjz8l6vxG5KLajWKrmi1qpol20ehOUbRQ5IeKTU06LDadXiGnvqtR0HZTu2jAXnP+bnNO6dktp3/X4auEcvujCr7XJOYlRsuq711fvvKk8uB39cqDx46J9TjZ/7nSrVxNyZRLK9wFo0aPNpujw+3pCE+i5byxppS5NSYT1YS3hEsZ4QwxhTNcsirhkZGh5TWRjqFZlFVaMyqRYp7PY6V5TKyCHN57nJABPr120aJIY8EGLQeIpY5Mzhs7roDljU12jTSZk6ay3Bw4vqiY3Jzx0eGya2TyaJdpiDkcbgdZU1ke2/Cg9/2Dn15ZefUsq+/9hOOv7v97arY2YmhKSsaIaxtDTKtqNi2ZmzZz0vQVU6N23v+QV1LGX7t05tzwLb/40zO+VQuLTD8xhZiU5sZDkhWurWTyVbNL1s7k9lYGHYyHDuJountUVHSI1S7L1mg5fqgprLQmJMTkoKi6KClMjooiiiitoRgSg4vLwvD0JRQUX6kjuc/EUMRaGRnhyM0ZN14Nl6S5p32nWPg3z3+r+T6y1VW/+7ey5WEs3r7uzSiWhMViY2n7fh1eUe/7ka+nsSGsbVetmB8uWwZki6Sh1OaeERviiIgJDZXliBA5IT4mdG5NTKIjosQew8LVmBgymYZgvhwUXl6z1sEc/B/FbE1gbQmsNoGVJrCsBH2fwzRlLVoUtBnzvThtgBsIDCUyIjpRTIsqMcxUYiaTrjyFLSnk1Ken+65cufxHo5m107etfpnMtltao1gii8ZwNN+rvr9YtvxsXazvPXlPz03f/z7XtQuD2oVYNZpmuEeFDcHAJSlaiVZiY0Ls5TUhfCNXSmuGqHYW/Xws644VJlWQGzApeP0c4UshYI5u2q68XNhRbk5sNLej4Sw3mr3r+8eWLQ9sLa1PTS2ZdEi+6cyt8k3PXXfP3Y4nrPklVc9xvfL/m5HH5Dy+n+ceh5iWFMViVe1KNKOKGhiF8DJe4TH0aNIZFMR6Rbx4ds3xvZxr0wgX9DgPa44L2MsjOzZU6Ttw4DtZmfjdH7gezvZf7M5A/KIqOMVE6wGLHqesDcQpJy4Up5wXn6An9bVv+X8jSXCkpi1KKdb1Pe7FsclETotzhMNsGWFJGT1SjpLLahyx8XKUw2Z3Wij6WAp7K4XdmsIqU9ikFPZ+CvtNCrs/cJuVwiRnCqMUdiSFHUxh3hS2NYV1p7A6Udbve2qDfBP3AwUFsbmGJ8rXlaJPHfbBCAfmikc5Y5NHJ45g0bl89cfmGj5ALzZHyLbtVct8n8Dp2+QQZez9y7/JM42/b/WWX/k+3T63RZVq2fBdPX3PyiXz29KH/NJ5U/vnt7S+/UpfOS/Yelffbl0PSgP0EEeliNPiHGazxRIXP9QRxVXAh4/RIzjaJAIibzzT0wiUTiA46tdyTr9LPRt0DD4GSC/PeaHp5n6p8x9e/fBeLtDuDcGSvvVaX3lgfd+D9R2KFZHtjo8w2chEsTFWe2mN1SFHldbIMQg06mLZoDEagrOR/SFaskvj3lNT7vH91efr42cLJjMrw/q75Xo/3byKydII3398h1g6lp3K0nyHff98YZdv8xO/1c8d633zlV6lHPtvIk12a3EUOdxqDaVQ18jo+NKayGhHuD0kQdZKcQqJaXcxCJQrbJ4vz4BQhlyScN9iKsfqysEKjWRCY9yVKL3v/qHj1xkmk+8TC4tQzUrtd7896Hv/cPvq1a0fSCMRVLxbv2jET3we5bOf1kVeO/Zl39/gPZf/3rv7eT3+wbxKPsxrDE11J1ng+sgeFxsWWVZjCXOodoreGsfWxrGDcWx3HKuNY1lxRtRN54rL103/9EkBJxId0WvMXqq7evq4xMKxLSvlyTWrMyOfGtGxKMN+3L7jf/q+EHKUYP6ckCOFOtxFZlNiVEJ8GFF8lElJvSIxLFaOHVFe87sEVpeAvTPBmSCFKAkJsQ45pLwmyjxKhGMxZVcw7xUs+wrmvoJlXSFC8g4RoukRmr6HXihO43oejzgtZxz20dGZknCFMbFmvvdwVSNOU5w+/9HDX4z+d/TS7lXL5zd/+av5J95/4fjw/9gWNzU0XLVw7UurZ7LJDz628UdJV7knu8dOic4qX7f4/kfuvTt++rTcyVnjI+PHz1mNsQ71fyltVifAUie5hw+x2ULCLGE4X8SGIRLFRonY3WTv3yCF7BH9619YRv++z532+Nzo3GiXsd+b2Pabbt/w42rv/v2TCxKnNEeu3yDd8pzP91zf66Wzw3eNFLrmf1Z4rTKRQliF289/OmCyYneW5FDbD22s28aW2DpsUqWNTbexsTaWbGORNqbY2Ckb+9jG3rQxts/Gttset0ndtk02qcHWZZPctjKbBGaH4FwK1oO2IzbpcdvvbdI2G7sVLUt1NlZoq7RJmo1F2dhbtmM26VUb22TbZpNutbE6W7tNMsqzbRI4ThpMXhvjffzQtt2muG1slG2sTSIbGy+127ptXts+20mbWmtjZHPY3Db5oI3t5q2yNhsrs7EsW4FNWmvrtT1vO2Hz21Rk2W1OZMpmq2Q3MW80TKQgly3uDwvhdGsXDwgUz48Sa4PDyIjI2LOLNpWxxCExsVPZkETpfZ/XdzNL/a19QsjUl1myMrHvFzl/TH1dqhPzEC586kT4LLd7FIVarCEKM5tUSZZVszVUDbPxBXgyjB0JY1vDWGmYcTwKfg6VG3CioSzRyhIT+Lece8YH53QXDpZZn3zMxoD2sjt810tZUqhvC1vS903f6+JRXvKg1zy6/VIXmzrIdQs7qF+So/+aJz0snZZOy2Xyc0rXBa/Tymm1ENfD6kl+mbLFVWc6Zh5rvsF80HzQEmXpsfzJ8ifr3bhev3xdvi5fl6/L1+Xr8nX5unxdvi5fl6/L1+Xr8nX5unxdvi5f//8uov8H772gxg0KZW5kc3RyZWFtDQplbmRvYmoNCjE3IDAgb2JqDQoxMjY3MA0KZW5kb2JqDQoxMCAwIG9iag0KPDwvVHlwZS9Gb250L1N1YnR5cGUvVHlwZTAvQmFzZUZvbnQvQUFBQUFCK0xpYmVyYXRpb25TYW5zL0VuY29kaW5nL0lkZW50aXR5LUgvRGVzY2VuZGFudEZvbnRzWzE4IDAgUl0vVG9Vbmljb2RlIDE5IDAgUj4+DQplbmRvYmoNCjE5IDAgb2JqDQo8PC9UeXBlL0NNYXAvQ0lEU3lzdGVtSW5mbzw8L1JlZ2lzdHJ5KEFkb2JlKS9PcmRlcmluZyhVQ1MpL1N1cHBsZW1lbnQgMD4+L0NNYXBOYW1lL0Fkb2JlLUlkZW50aXR5LVVDUy9GaWx0ZXIvRmxhdGVEZWNvZGUvTGVuZ3RoIDIwIDAgUj4+DQpzdHJlYW0NCliFXZTNjuIwEITvSLyDj7OHEYnTbQ8SQuJvJQ77o2X3AUJi2EhLiEI48PYbUpXReC5En0O6q8ptzzb77b6uOjP72V6LQ+jMqarLNtyu97YI5hjOVT2dpNaUVdGNODyKS95MJ7PNt7z5nl+Cma3K6zG87stQd1X3eP2zOZgynJ5/2W8Pj1sXLvv6dDWLRb/0q69w69qHeRm++tIv/WjL0Fb12bz0Xz4XDvem+RcufTmTTCfL5Vitb/j70QRjsdBrg55rGW5NXoQ2r89hOlkkSZItDR7ANXBD3AF3wDQZMOVbKwNmKTBDqYylMgW+EVfAFXEDZClBKRkRfZWlFKX0+TbU5WcbLoW946n4m7cfbdkksmWpJUFzO49c2nXk0m6JKXDMwAK/EmmajdI4kpQZWKKLEko9UIhvQCXOgY7I/DxxHaWbMs55tDNCGRYyhDIsZAhlWMgQyrCQIZRhIUMow0KGUIaFDKEMCxkyytgCuecWOQtz7iP8uOcZYhfGniF22UXDpUk0XEpHmYvmJYMjpaMMjlSjSVQfTaLOo0l0jE7QyLGRoJFjI0Ejx0aCRo6NBNE5Rifo69hXEJ1jdAIZbpSBrByzEmTlmJUiK8esFFk5ZqUYUccRVUTnk+gweTpSOPLjUYMjT0cKR56OFI48HSkceTpSOPJ0pHDk5zi14+l8HuDhXny/Fot72/ZX2HB9DnfX89aq6vB+xTbXZviOP/8B0981FA0KZW5kc3RyZWFtDQplbmRvYmoNCjIwIDAgb2JqDQo1NDkNCmVuZG9iag0KMTggMCBvYmoNCjw8L1R5cGUvRm9udC9TdWJ0eXBlL0NJREZvbnRUeXBlMi9DSURUb0dJRE1hcC9JZGVudGl0eS9CYXNlRm9udC9BQUFBQUIrTGliZXJhdGlvblNhbnMvRm9udERlc2NyaXB0b3IgMjEgMCBSL0NJRFN5c3RlbUluZm88PC9SZWdpc3RyeShBZG9iZSkvT3JkZXJpbmcoSWRlbnRpdHkpL1N1cHBsZW1lbnQgMD4+L1dbMyAzIDI3OCAxMVszMzMgMzMzXTE0IDE0IDU4NCAxNlszMzMgMjc4IDI3OCA1NTYgNTU2IDU1NiA1NTYgNTU2IDU1NiA1NTYgNTU2IDU1NiA1NTZdMzZbNjY3IDY2NyA3MjIgNzIyIDY2NyA2MTEgNzc4IDcyMiAyNzggNTAwIDY2NyA1NTYgODMzIDcyMl01MSA1MSA2NjcgNTNbNzIyIDY2NyA2MTEgNzIyXTU4IDU4IDk0NCA2MCA2MCA2NjcgNjhbNTU2IDU1NiA1MDAgNTU2IDU1NiAyNzggNTU2IDU1NiAyMjJdNzhbNTAwIDIyMiA4MzMgNTU2IDU1NiA1NTZdODVbMzMzIDUwMCAyNzggNTU2IDUwMCA3MjIgNTAwIDUwMF1dPj4NCmVuZG9iag0KMjEgMCBvYmoNCjw8L1R5cGUvRm9udERlc2NyaXB0b3IvRm9udE5hbWUvQUFBQUFCK0xpYmVyYXRpb25TYW5zL0ZsYWdzIDMyL0ZvbnRCQm94Wy01NDQgLTMwMyAxMzAyIDk4MF0vSXRhbGljQW5nbGUgMC9Bc2NlbnQgOTA1L0Rlc2NlbnQgMjEyL0xlYWRpbmcgMzMvQ2FwSGVpZ2h0IDY4OC9YSGVpZ2h0IDUyOC9TdGVtViA3Mi9Gb250RmlsZTIgMjIgMCBSPj4NCmVuZG9iag0KMjIgMCBvYmoNCjw8L0xlbmd0aDEgMzUzMjAvRmlsdGVyL0ZsYXRlRGVjb2RlL0xlbmd0aCAyMyAwIFI+Pg0Kc3RyZWFtDQpYhe19eWBTVfbwOW/L0qRZ2qShKTQlLVugLS1bAWlkqUVUylJoQGgLLbSytDYFBRWKgEARAUUcFAEVFxAhLAouSHXckREXdBxHQUedcYVh0FGgyXfufS8lLbj8ft/3/Wfi6b3vLueee7Z7zn0tAgJAPDSACGUjx2TlwCOHnwTAKmotmzqrvNZoi3sNoPdL1DZ26tx6z5V/G3EWYHA2gLB8Wu30WQvKn7IB9O0HoNs3vTxYCy4wAAw9QPOt02fOm+bOq3yTnglH9pmqyvKKiLuO9X1L0KeKGszrzBsIdzo9p1fNqr/x4/eepLXMYwG61M6smVr+z+SPBYA5zwEk9p9VfmOteaX4OY0vpPGe2eWzKr88u+Ireib8cStra4L1kW6wnuhxsf7ausra5p1XDAcYROuJQ4DtlbBtHv3lqVLLwB+EVD2wz2v+n+9l5VvrM/efe6T5LuN1ug/oUc/G8g/N0w0KXwNDjPvOPXJ2vvE6jinmY0xhLcYUHA1j4VpQaKYVsqgGwlZBAol6RelBXAMygHyvnEso3Wopvg3TBLteFuIUSWAf6QQYI0VwY4TQpjHcPS8fMwT84Imcl98Nj8Jc3SDcUwZ46Ph/AaT+8iK2U+hOPzvg7Ba6xkNIqyNYsItWF0BHnFPrIiTjbVpdojEvaHUZ4vGkVlcgXkjR6jqYL6ZpdT0kiq9odQPEiz9rdSNWK3/X6nGQom/Q6ibI1J/T6mbobViv1eMh2SgQJSiRzsBOThWrI+1Fr9UFoqefVhehFxZpdYnGPKDVZUjBt7W6QvWwVtfBGcGn1fXQRdyo1Q2QIn6k1Y3CO1J0rTjopy/Q6ia4Vn+/VjfDdYZuWj0eehnehKFQDdMJ6gnmQyVUkAwqoJyey6k2FWqgFuZBHR9VRa0e6EKtXanMgWzoSeCBK2hUDfXPpPkeGEL1OprFfpZzvDUwGzKpx8j7fh1fDtVGa3QU8vndqTacMEwlHDC0enp1ffX8ygpPRXl9uWdqTe28uurpVfWeLlO7enKye2Z7rqipmT6z0jOkpq62pq68vrpmdqbHOKTtuBzPaMJRWF7f3TN89lRCfBVRNIXWjaXZA2PoaTYEqbt6SqWKzTOmfDY1MBqnwxzacznNgdGV0+fMLKfK5TR6KvXNph0wbB7oQfAb2C8PTq2cXVFZ5+nhuWih/ylh4/jYYMvIHGJbNn0zgYx0XGVdkA3NyczOzsy9NPJLoP41SqppqIcrSz3vYduexZkyg9pqYNqvCtRD4yq5Agapp5I/VXCsDHcxjRjDRxXxmYyt9Xy12XzU2EusOJJWnEbzp3JljI6cynEzpVYx11C9ShPQdSTGOk5BBZ8X3VuQKVwMf6uDnnJPfV15ReWs8roZnppprXXIU1c5vTpYX1lHjdWzPcWZYzI9ReX1lbPrPeWzKzxjWyaOnDatemolb5xaWVdfToNr6qtI+tfNqasOVlRPZasFMy+lS5e2rQv6E6P1QJxjHJvL+XA1H86eg+qUMfWVcys9V5fX11cG2eDBNCCoMV8V7OWcKbPoiQnsBmIXY04Vr5dzoVdwdMySZ2szp5Bte351YY82t1xTntn0raGx6m7YnO6aUkzjP4N83dm0hofqqmZ6OKWMumltqPBwsZZzJVEVcxb11vOxU6l9Jn3naX5tFvFRXXWK5rlu4H6wqmXvND6tI1e/C7xQVXqaZmQe3lpL9RpOe5R7PbjkGP2VnCpWK+d+dQrNmMnXUemo4opbztWuUlPDek5tlEsV2q4YhbW8pQcM4yrLfGmlxsnx5IWvuiRGlVuxZsMkMZPTG4zBPZtTW8Hbalo4y0bN1FZSdzyTe/sZLVKZxrVR5V4Fx9bjF/g7jfOmXlu1hlNUQV9VzqpG1dDcOVxqqqmrul5/EefKOX9rtHm13A/Xa7TMUk13cHmQTJEM9/K66lk13T03VFVPrfLcUB70VFQGq6fPps4p8zytDcFDveVk6rNn18wlM5pb2Z3MelpdZbCqevZ0T5D8oCdYWVc9TUPhqa8qr2eOYVZlfV311PKZM+fRmTSrlqZOoUPohur6KrZ6+cztmSoV5DWmkQ/2VM+qrauZy8nrEZxaV1k5m9YpryifUj2zup5wVJXXlU8lX0IOpXpqkPsKchGe2vLZPYbNqauprSQix19x1YWBRJbqZ4I1M+dWBvno2ZWVFUHmpypoizNpEi08s6ZmBtvKtJo6Iq+ivqpHDL3TambX09QaT3lFBe2ZGFUzdc4s5sHIq9RHiSufWldDfbUzy+sJyyzmqaq4jddCf4oVs0gT2DeTW3qs/5qqea9MTT+yaGJ9fW3/rKwbbrghs1xzYlPJh2USUVn/e7RMRWq5Msc6qDquFgznLFKXX126fl5tpaYkdcHMqvpZM9XjT1026ifnxHjmqBWNoaPtKn4M1Wq2X6BpvacNBubn2h7WPYnAnuzQIXqY8s7hXp3Jcszwqzwja0lNCkhGHm1Ad0/0QO+Z2bMtu1QPVE3P9XzjQW4/mZxZ06l/JFF2VQsbSAmra+uDmcHqmZk1ddOzRhZcxcJmOMLD7bwWeFr4AMZLQTAQOHXtYbg8DgpxGVQJ22EhgUlsD2nSDqigsQfoeSKVz7K5NL6IYCPBdIJrCLIIRhNUEVQTBAjKtPEHCEclw8PLIIzVp8IDtJZE8Jj8KlQRPMbq0j/gMSUPprNnmndQoiyCtwepfTsfy/rLWRsv1XmTaF4m1TdR3aBbBQYqMwl6UPvlhOdObb9W8QUwSsHIp7SX6wgn2/sSWoOV49gzjWmv1e/AV2EFvhr5C/U3Ur2R1l9O7cu1/iWsFFgbQB7NS6XnpVTXya9GmqlMIpAJxgg7oKOQCPtZSfu/ltOyHU7T+GUE/QmuJ5rCbAzVg9TXQ/4CUoUfIZmex3D+E+9ZmzQjclLMhflSBe1rO3QlcBMUShvhdukqKKL6fwhuICgSvgU3m6/sgH4aDCd+LNb4fhFQ1unishinyiIKRK+B4A4hL/IOlbQ/iI/KoS0QrXdQeQWXRSyQLDT53qHx/SIg/RusyaIV0JpGgmW0/rtU6jX+366VrYH4Qmt0p/rKVsBkEYRGVrK9MrwXlbR3tv6vlI9J38A4tn+2lqaX43+rZPrMxv9SyfGSvml4aa+RAyqASQXGd877a0kPU5ldELwofwrbxVWwgtkI6ekGvh7wPTYye6GxE7VyASuFYrWd9JCVidRu1da+vW0pHYuE5dfhYVbnclXpbVWSvpSTrXH6mR1o5SKt7Mftkmzjl0pms9xuqBRBLdkz0xdmS7+35PZONsftXZUvt3tme21LZsc0J06xQaLs53tdQqWR8Z3wTYyRdbwyn48Zxf1aPZd3QJFhsnQMSqR/RF6h9iYuwzAYdSbuLxqJ/g5ROdBzIpXxOg+zgchR5ju4nfyd/FY+8fE0leOpNNA40k3N3qbQnJHSaZgpxsEQjT+JUT4pxwjXRNr7OU7jJiVT3TP1DaIyi0q29wLpWuLxtdwvT2C+WHycePwFpLN1yM+ExGtgL9lqHTsDjORXDSQzfQXJdKHqZ8WN0MjadHfQs49kq9kI6eH7pGsrojrwe2Wk2Usre2P+htn8Rfag8a+tvvG9XQtDaf07Y2mOztMX0LzT6hnBeH2Jda5gvuES9t/KXmmP1QTM7+ipPNuWDlW/I4c0PZ+p7bG6Zc9t9fta8IsLIK3Fzh+BrTLpk/Q+jbsNSjXd7NmWnl+yuxY6NH0XDke2yfNhuXAqsp+dVzoXjGHA/bqqz0y/kxk9VL+CrSU9DLniFtLvcZyurnIJPzPZukM1f/IX+cuW/bLzKjG6HrWh5m8XaOfnZQRXx/hh7rflr2A86V0hQW/ZDL0lC4yI8d/jpBvJlgTQSSfByfgSBbIbF8E44UMYKmyitWeDhZ5vk+6CxaSbKzSgczjyAD+PZ/J545QxBPm09jR+LvtiYLkGdxB4pGIaz4BkRPske4j8mcpbhcM8RkjVzvJk6XYYK5VFz3RQqLRIXehMZfwbS0C6SDCTyxrI16qlKjc/4bfQecv2OANuEzOJZwAoDqB9sL0zWyU71+2HcTo/6W4c8XkvdBVrSBZNkKqkQHv5SvIJFmgUP4N2Uj+YKi+EzgxEG5QzwILIV/gNTCfoQuAUvoYK8cPIaWFt5Acew1FsR3xbSDCX+6bt8CPBWeEN6EWQq8VkLUB9oAKmUJlL8CrB3drzEC2u+IL4s5tDFN92eCAG2pNtfEzlRg0HxSSRr6h0UvkllaKwLnIaB1NMcwC6C1tAYrSIVtjSFmjsFA1Axcvjm0UavKbBKhUY7sg/+Vos5tzO99sCxP8OBElU7w/QfB4gfDfBkwCRr6j8jtoep/Lv9PwIlawtier9qFyojXudIKA9/10be18bmEgwkiCfYDKNWUbh9iAVZ4Qi8MjVBCOoneGyqVfi5yPqemytyAaCK7WxB9X54fsJnlZpiK4bvjeG5te15wfo+QkqCWf4S5r/kDo/MpTKB6nMILiHxuyg5700yE7lVmrbSCXhiTyjrWem+hUEvalO9IQ3a3BS3Vuzk8p6Df/fNbz1KoT/RSXhhB+ovJyeD2n7GqNC88MERy48Mwg/S0BrR17S9vk3AhoTfo3gA4J21DeVYDzVSRPCT5EMfyaYQ3CKbGgQjxmp1HKUI0xX6FyVmB4oBZEflH2R06I98i8lJ/Ks8le4XJEjz5K9h6L5h1RFZ0YJXKbFp5dHY1sWZ/EzuQSM0dxDzoUJMXkHO29m8tyDfKMyBeawvEPZBWvZ+cxjZeYzt8A4cS2dyUG4juUU3KdQm3Qv90E6FluwfnEZ94vXtYxTY7l4iu1ZCeLdqt+Ul1J8sAqWiB/R8yma25VyFsIpZ0OxlAsOeR8sIz9IsU7kCF+L+RsqWRutGaS6geKGPN12SGGldBMUUd9o6S0YGnPG1dGaE1g+Rj5ruRQh/zUQchQznSH3w1SKaR4hniyRKXfmZ1oFbGXnDO13NgPpBO3rZXBSzlIuzYbh4lOQKF4BXdga0t08xhnPzhi2nrgCihho508jO7M4vxuIP6suxGW8ZPIYT/L5hugopnoTz1cmaTGxjp1d+jlg1ztozDEas42PeUx2QF9eMpn7Ndmx+TPAwuq6qZBCcd0QPoaAz/ODvVXO2QSPRPNVLnPCqThgLs81v6H2YtiiI5y6BhpfDJk6B8fB8FUzemheGT8b74Yb2fkgfEP7e5zHfuPlCaCjc7InnRd3MBAbSOaPQxznwQz1fONnlpavitvBy85i5W5+liQRzjskH8xXaCy13SED5VtNvO0OidEJ/MyzxeRVRr6+g9tOHtM3inV+4vGDn+LjBr6WkdNxI9dTmdFh3Ed6EQYL8cMh/RMcug1kI09SrFVCsQuAosuEQ/IauE15AObJN8F8/Sw4qJwi/TkGZbQ/j1JKPL71gp4psyjuMIEuWur/RDlFdygmvveRvgSfYRnMVI7C+Oi6WjxTJOkgTvVr4efIN2xWofld8qfkj87P4DIkuon/EvEgUdOtJeJXpM9XMl5EIrT/RHkSPEo54yomfyYDpgNcDiR/vvcLpUSlUT4JXaXh0IXHcsQPnYHkmgV3GFwk8x8pvlfIH/nAG80jeG7DZBXkuYAuWjKdYXLTTae4bxl0YrpD84Zp5XwqtzG7Uj6nNceS/9FKpudRWpkdkO9axfSU64pGU0up4YraEosBfikGb4k5WX4TU17El2MU51Hc08JfrfzFGJV0n+kfsxWem7UtNRqZLTJ95DbT1CIfiPKppfRT7kV4dYdgok6k8hEoU26DYvlqsq0EKNb9Gey6KyCO5QI6HadrOovB5J/JRseQHI7BaNrH8CjPonRGc0j1vAQflbOonMx+34Dq1xBUka4dIzigntuRrhfes7O25h+19mtVHJFCNQaIXKf2R6aofeFErX+yOoZ9mrer+CIh6icdDp9WgT1HLtPgWg1CGti18nWKlZayPmkRnon2k548E62LemC/R9BbVmCw9DrtfwrkSyzOtMOfKBfcKayHXHko7JTzYCt7lgqgM50jRdJlUCDPovaF0Je1i+2hkPLWXOkxsoHzdK58CqslPeUW1xIcgJvYPPkDwrWM8gE74dFATIQPpHfhA/EnOpvOQTt+z+OnmJbZRzUsIwDxG1jG9Iv5IbEcstnZJ/YBK/d/N2r+j+UZn5B9fUL50ieQRTIbLz4GQ1ryCZ/m4wi4zbGz7xXS1U9gGJX5MXdzY9ha4gzC8xF05X6Q2Wax6i/p/FzAdEPcEjkvj6RyFPQWR0X+Lv4JcsRCmlcIHtpLtjgbMnEcTBWW0HrToKdwlM56B/QSryebryF9dYFPtNBzAHpQPt1DnAvdqL2zdA5QOAsDhLORb0UJBkhvUp8MEwgGCD9rcDv0I8hm/RQrTxaeInu8GyYRvkl83DHKq6jkoMAEfJFossBEcTD42Djhzsh/RA/5LAeUCXeCQGMGiEuhv3AIJMJXyfIGGl/GxzkoxmalAQZGx+iGsrghcifjK50LB5XtkVfpeS/BeoqxNzGQIPIz9e3h+VCQ5BdH53o9XK0Mh24kx2QG1N6B5NCBcimjFL0zzaP4bB+XJ7sjscTcqy5hsT47j0RX5FEuE/Uetad2ZrXkl8yGeV7ZC0q0WOkyOrvW8rsG8k/Et/HEI7/wOuUg5yGHeNkZKR4g6M54SvlTGfHBxvIQDWxCt0iEyvEEopBLfuYuyukIREvkBeJVqRhPIEN/EcgeDkAWDo7sIr53pL4EMRn6EY8nCu/RusRL4RMYSJBJkCGcofJrGEg2zex7Cdkk2Wt4G8ErBO/FlFNUiNRE4+k2dwJLLipj7yYv3CX+cvk77yxZ3MfkdIk7yrYl4/nM6DPpw5Mkh5tZLKHFv/wup20pqfeSK9SS342x8l2tvJedWUwv2pYtdzu/UP6OO5O2/Iu9u4yW9Vo59rfuMC91l3mJUv+77zTHgUGLD3gZPZd+q7zonBzXci94yXtQVVYsZuD+kN3pjOfxwWY1Rm5zPxZb9vyN/t9T/h4d7PlL/UT3KKKVxULPMR36DZln/GJ/9B72N8q2Morewf5W2eo++hIlzwF/BaLvZZRboVsbyGfAc8ZLgNKBfGoH0OtmUmwXA9Hc8pdAWU3zVoNenwougm5aSRA5y0B9H8bfie1VAUQVIrczEBEsBHppLa3VCiJnOVzqfQ2Tw/207v20bg9ai0D3ugr8/P4VIB7odTtpjp3G74ycZPntr0IprVNKc07SeAYroxD5ikGU71E+Shdycavmq1Sao+treP9v5fg/lEsMRD5m8P9q379Geyyo7xgxUS353Z7tknTfCh0JBiv/ofI/lGOoPrWbCpGTpDPrCd4ieJ3gNYIbCB6ks+MN9t5LrKSYppLsPWbORXqwimIKBtqz9p6xh/IljNC5KPchO6B5X6sAhy/FH10lXKvcT7zoTGUpZPG7G/U96rcS/7VSHpPwUnic/6ouYDF/B87foyOLrh+P5gKR9wk8BOzu6ir23paNY6DXcPB3LzMin2p3s1FYQGNHxEChFOTn5HLhCIzSAzo1nFdrsT8Htjbh7IsNUEzxDkFkK80tIQgQzU/TvptwXJi/h4+ZZ9XAxp5pbDxBb+2uvAfFw5UUn15GcWgfHmuyO1qqEy3x2j0Me8fPfHl/7Uxup2+CTYYiyrlWQYJyGPZJbmB381aSBT8DicauFFsz39eOv98fx3nC83na032U9w2jPCRBfzc8x95z0/jnlAyYKR2BEtJVPeUHZcoOKCLoqJWXEUwiWEv7HED8eVACtLYtGYhnoJ/0BdnfeviG4s572V13lCeU++dS23jdMfyT3IROoSfFtRU0nr1HfhwqqMzn9WNwP//9hWNCR+kYyvLjkR9lwL/KjwureP2isi3gh2ofKxnE9v1P238P0AHTCoRjVE7ndcpiaT83ESjC+zCLAdNL3Te4iWBttCS+6WnMo9ILFNcfgz0EXRnQ+KDeh7v1M/BtXTEWKIB/IxhFOd0AyqsHSk0wjfIg9i7/JYXLAHJI1u1Ix1Mof/gPyT5Zi9eKyNbnt8SS0dgw+j6Mzl/K23T6q8CgPMPjlB7SJnhMnE5js0nXt8Pl2n35XtKh7xnQmA0MSLahKFD7FgY0PoXJXGygeH+ZCjS2PQOW37K7ZZ6zUn7Lc2UtR47NhXmOy/LbhTCB57qxQHOicHGeHXlGWB85rObYkWda5diUX7fk1tG8+hI5Nc/NCS+fR2NonSKA8+zdQTOV5yHqo/jv7kS+IH7fTHCrMAGuIygU/kR9DJaRjW+JfCVmgUcojPyLplwXA4UXgL0DaSYfcb5EfU/C4WPNz1lixmpz2Xj+3uSrSwN713F+JcC5b6h8i8pH1PbmWWpeFH6D2n+m5/kE06i+iUovlf3b4qJ9Lafx72vwllYyHXhRGg9b2sDVBKO1kkGBaKXzfTz01mAkQQ+CQmpnZTpBhgadCbKondXbEyQR9NEgm9q7avOvioHJ1H7VJego0voLomO1cVkEeQT5UaD2fG2N3jHr9aH23m3WiuKpaos7Bn9bOsYRjCcIaOU4Gnctlf0I+mrA6v2onZVXEAyLBWpn5SIN8jToT+2sXNsWfoGOtvsYSeMYL7Nj9sz43V7jc5Ymj6hs0jW5FGryGxmVqSbHghiZc/lrcm9FB+lM36j/YPqjAn/Xx965vc/vMX4jxqO45UWCYwQHtfLFWPitWFaLg976pfHIzt3XtXdQVBJdbxKNZJdhssfwUY3ut7R3Zh9r5V8J9pMNfauWfMyrMfBim/4n1XeDF4DFTAykyyIzODC/xXwS+Z4ocB9GPo/GdyJg7xWvZe+0+N/NqBD965sU9tcq/FmB54H9hdAE3h/7iQMT/xscACvYwA4JkAgOcEISuKAdJIObsLT+pEMGdILO0AW6QjfwQXfoAZmQxf8CBdgfSkBv6AN9oR/VyJOwm5hWn6EwDArgCvJkw+FKGMF+jxKugZHkXUfBaBhDT8W0m/FQAgGidyL7+ykKCG+kn8lEowhG2kdXWjePZhXRWLIr/pua8yIRvscu1NeDzqoiwsb6ymEG1EUikX9c+tv2r7hafTRuRTqzvye7+OO/YuKEQEnx2DGjRxWNvObqq0ZcObzwioJhQ4cMvtyfP+iygQP65/Xr26d3z+yszB7du3TulJHu7ZiW6kq0WS3x5jijQa9TZEkUELp7Qlg2LCRmeGwF5d5h3vLCHt09w1xVQ3t0H+YtKAt5yj0hKqRO3sJC3uQtD3nKPKFOVJTHNJeF/DRyWpuRfnWkv2UkWj0DYSBbwusJHRnq9RzACaNKqL5qqDfgCX3H61fzutSJP5jpIS2NZnCqGLWeYaGCuVWNw8qIRtwdZxziHVJp7NEddhvjqBpHtVAXb+1u7DIIeUXoMqz/bgH0ZrYs7XRYeUWoaFTJsKHutLRAj+7DQ/HeobwLhnCUIWVISMdReqoZ6bDSs7t7U+PtB6wwpcxnqvBWlF9bEhLLaW6jOKyxcVnI5gt19Q4NdZ3/uYt2Xhnq7h06LORjWEeMbllnxIUlMSRnWL2exh+AtuP97tvWLeVai5Jh/QFYNSQMCeHokjT2cRcQrxsbC7yegsayxvIDkYYpXo/V27jbZGqsHUbshqISQnEg8sxKd6jg9kDIWlaF/QPa1gtGjwgljJpYEhIyCjxV5dRC/+V70/q502wtY4p+qRuILcQc4nBaGmPDygN+mEIPoYZRJeqzB6a494A/yxcICWWspyna4yhmPQ3RnpbpZV6S7YgxJY0hKWN4hXcYcXxleahhCmnXdUwwXmso/kd3mrfRbvPkZQX4WA9RNbyi2hOSOxGTaFbsBNIbNqXRyh/if1SL79y0QCeb3ZPnJTQMzzDvsDLtv7lVLkLgIUYX+lRFGFsS8g+lir9ck9iw3dlZNKO8jARWPZQLM5TlrQ0lege3SJeRNax6TAmfok0LJQ4JQdlUbVYoaxi3K8+wxrKhKgkMl3dUydOQGzmxu5fHvTcXekFgKBvsHEJa1mlYY0nFtFBqmbuC7G6ap8SdFvIHSMIBb0llgKkdcajrCTdXjgDXlbElI8Z4R4yaUNJPI0TtYOikjGFt0HhL3CoaUsCQPkPvKRHcYoAGWqnBU0AV7+CB9DOky9ATWInhvJUp7uCBnhJ0Q3Q0kRHq6hlWOVQbx55bIZWZOg0pjGJT2CPhGVLoTgukqZ8e3QXq9mgL0ww9Y2phtIvcFHXoST+HFPImxksXU3pPibfSG/BWeUL+ohK2N8YezmWNGZznmqzGtnqKYRaxCdKoO/rAmBkq8LljmRu6gj+3PBa26R4e7fY06r0jxjQy5F4NISUqGcNDwFTY38/m5r6AGbSXfK/HSibNDbpxt9/PjLmqP0PiHV7R6B1TMpCPJn9yi3s+W8sOI3DE2ME9upNrG7zbi8tH7fbj8jETSp6mhN+zfGzJHgGFIWWDA7vTqa/kaQ8dGrxVYK2skT142APDNJoe9Hy8+2k/QAPvlXgDf556AIG36aNtCFMPCGqbVV2oE1/IDwL1SGqPPzpaoja92tbA2/hnNzCW+Y2yX+83+E2CWXDvRta0h1qeofPRgLDXhGZ076ZZo3nzAWzYbfC71RENNMKvUri8+MLSxRNK9pqApvGftNBg9iF1cVWRsOlYGeapYIpyc6CqsSzAjA2cJBr6D0PoHURi8g4iQhRTyOitHByK8w5m7fmsPV9tV1i7jlQUnUjTG0j2RSFkGjCxJI1M0pP8urvR+h2TVICcSqP1ix6XpxGx+YCYB8U4SCsHo5/inlS8nMpUKgdALvan9n5UUj/4UUecTuU/N6Pk345NzbirGaEZjSPPoecc/lDUJfV0QZfUfxd0Sz1V4EstPbnwpGA5OfJk6cnVJ3edlOO++LxD6j8+K0i1fIb+zwqcqZ+eKEh968TxEydPiP4TuX0KThS4Ur//LpL6Hf6r+NvCb4q/zoHir/71r+J/FkLxlxBJ/fiy48XHUSz+5DKx+O9iJNVyLPWYwH/433C5C956EQ82DUx9oahT6nPPd0mNPI1FB2oPNBwQD0Sa/JED9pyC1P35+0fur9m/cP/m/bv261xPYe2eLXtCe0TLHlzzJIaeRMuTqLfszd97cq/YEFoTEkKhptDRkJi1K3+XsOWJ0BNC0xNHnxCyduTvEDY/jk3bj24XRm5bvU3I2laz7dC2yDZp433pqUX3Yc16PLQe1xe0T717XVKqZV3quoXrVq+LrJOz1/rXCg1rsXZ1w2phzWpsWn10tTDy9tLba24XbyuIpG5eiksW90ytD+anBmkjNbMHps4u6J2ajK7idrmuYl2uWKzQ1suor5Tg2oKeqRMnFKZOoDIhx14sE3ukHLF4pogmcaB4lThTvFmUT46K+CtGCf5RvfsV+EdldCl4qwiHF3hSCwnzFQS7CvB4wckCoaEAnTmOYhtaiq05lmKKyooRMDXVkm8ptSy0SBZLlmWkpcay2nLcErHo8qntpEWsARwJ2OBEGQ/gmt1jx/h8Iw7oInTC64omhnB5KGMM++kfNSGkLA9B8YSJJbsR7wgsXbUKBrcfEcoZUxIqax8YEaqgip9VGqhibb/bCYMDwfpg/Rwf+6BagXqfLxhkNWRPPrWP19AXpG4aRpPooX4OBH3BegwG6yFYT+1BnEz1YBCC1B5EmkIQ9Gn4WzDRApMJEf2oV5cIBmlekPAEteVck0F+U34TbpEXUaYwj/9s9ZH6ky3dQFHztzx2bvkZHv8rkfb/4qP+uw2wDw7CLpZXxnyWwwL6uaNV2yH4s3ZvfB+s+hW0T8N2rbYONsCyXxx3HSwmPFtp/QufMmqdB3+ilQ/AowDYEXNp1Rla70fw+qVR4af4OtxJeeYM+rmfft4HINwknIY7hdEwW/hAXAS3wgra42ashtU0vgy24kSYTK3qZzJUQk0bpI2wBh6G+dBwoUleFPkPmM/vJcpXEJ71lDddT5K0nO8QOQ29pC/BHH4PDompRPtOeJJPWRSdqysUrxOeEoTmu+hhLUwnKMcPic5V4uW/ws3/64+ySKqCROkw06HIu+GFRPtHJKFniBuUf1OGxv6FDhsgZX8i1Y7QLnNIJ0XQQarfLCiyqIgGvSxK1JR/JOuIzY55ebZcW27P7IQ0W1qCLc12RKo8d99V4hF50dmFcu9zSdJXbGGEheESYRPxJx46+q06iDOKkpHQWKxGNyWG+fmEKomj4sis9r65imCz2pO8nQTbwief2/nsricO7jy4T0jENHzz8NFw9/DX4W/Cme++iUcwlfCbCL/vAn5RijOCZGT4QXS3xY9WQeftY7dZhc65TrtN8NECz+3c9SxbwBo+Hu51+B18G5Po+87bb4Zzw5+qe6iAfdIV0ibK84f4OxmInaJoNm0TULQIpYJgUgSQZOmJgOF9HfbVLdMJOnkv5OdOmpTrs0FubunkSaWTGMdsuSoRNq8trXcaUZTmEDbfFS7Bx+7Cx4Sy8FjccSfuCI+9k605EY8KI4VaYniq30bbkhGeDWzGt1DIQkTImnS9j0uBmNY7zTERz+DRLVto3rM0eQGwf5MjyW8kDksy4H0TAbJ8Kgk9s3N75zqe/fNHH6l7I40Q8oh/IiTsF2SQqCWBsQ05rQ7MRbxvU7g6UT5x1sNeJBVFvpW88nriRRJ08SfaFRMo4GpnsAQDBp3oCAbEdpDvA1e+L0ZJiO/ejkysaTl2MVrPzbFL3p//858z3yH8/N3+VQ8+svauLZvXCS+EN4dvxzqcijPwuvCd4Q3YE+3h0+HD4ffCXyP7V1Q20rYspJ9G8PkTJb0gxJlkSRIVRU+HTX0AXEQBcd6Vn5ublatxnu07zSb3zmBs34jTwy/i1Y/g+A3SwH9s/+Kci/3TOWSPIJlobx1gkN+TAvEWvaO9wwJSqkefEm+3xwUDdh1CCqRE17BDnosvZc9rpWe5vQfJvXt18nZUdJ0HYW6O05EYjzr6L80xPfeuBzc3jFw+L3i3+UDif1889sWIdW8Hl3cQji+cs3ftzTcvH1ffcMv1tm2vvf706Acf3D75noINXE7XEN/bEW1dYKo/T6e4UxwdTQAdM6wpitK1W4bNarPWB2yuhFuvph94tcWGVtlmE92pqa5gIFUnGoIBHRNNriobRrIri1STDiO2jRjyucASFW/HTp37OtNy+tBGfNg7l1did6ToHB1QavfTl+9HXM+ko2X5fbsfnTZl3UNLF99wl+lJ2tp739yzZlMIl/75/RcO2s7etiS4aOOiuusXz6+Jf+LFl0PLtnWQbHuA6VQW8b0vl6cd+viTbbJdEPQUDCQkgmSTggG9zYZxioLE83yiO4vblaZeUYK5UTGldSDxGS2YJl6/vblKWHrwlfAaoZc5fE8fK57G/PALmH+7+NT5q+4Qb1AmJzR/e2Ui5+9o4m97oiEFJvt72xNcSYmJkKBTXAnEZWeCIrXvkEwqnpwsJiYm1QcSFcbQ6Tp06jCoW0wmz3k7adIkTfVJMbjFtTDVnsd/MNaCytoLHPUmpDnSxD7EVal9+L/fvHza81Tet2u3Pnz78AX5oSwxrXmxe87Oo//Fw8cjsOMhx9u7NizdmtlX+HFD+PIJZ4h/VZpuOKEjFPl97W2KKS4JIE4Rvem25MTkOYHERNFgiA8GLKbVJsEom8hUPRdMlbmoFpo5Z6Nkc1VQ7RVyPQm6TqzK5a/jpDsS2TakdqePfX8eFWLvmB299967reee4J+/2L/+tgX3PbDg1nV45Hg4jFNwNM7G5eFPU3eEPw2fmlh65v0Nj9y16KGjuzj/q7ntLSK/0s2fqJdkGQwGMJnBYDTUB4yKxGR/QeyMmzlEm1FweK12JHcqmf66J/DcF2hqjhMfkk6Gnwo3htf9GeOFYly6gbxbgHiUTDxqB+mkb8X+TJ+Sak5OyCB35zSYFSW7p9PQsUvHLnMClo6YoHTsKFqtKXMCVp3YY06sTwPNbFjt0lbTu1efvr0zkYoLZiL2SosyK0FlnJUsS0r+6V+fRTbdFFz678NH/31b/bL1n4TPLly64paFS70bV624F7vetQZX/Plv77/c+Fyi5N4374HXXnp03r4kyfm0YD554w3zFs5pPr946epbwh+vYnZURnu00x6TaI9j/Zkd7KS/pL6KXczoZEqzpJH8LakWIV60WESHwx0MOLhfSNKhpr5t99iiCy3nZ4vu2hPikZSB79IeowyDULKH//vDw6/6dvQ5cN92qcuL9c9//tPH35x+aePiW9evb7jmtquFj8N3h+evvM8dQg/GTZiF0gcfN4e37tr+1u577t17xa3cJ7BfNxpN+qADK0z09zHTSS+Iiqyno1DS60S7zSSUBkwmHpTYQ3YssuMpOzbZcY0dy+yYbccsO07in+uvh/yc/Ny8FoPMoQ3Z8/Ls7PRME9NEL+YaUKfoqNqps7T6geYFD74i5H8o9GmeaGjXc59geTIlBTeGK1hsI/07Zcyt4Z749rDxPHJ6jPT2a6LTTNbXAar8/eMS9AlutxSvJwvUS2KqJy4hOSG5NJCQniBcbUlAcVACSlRa5YQEUnN7aYC24C4NSPa2OlY6qfT6S3hnzYtIXoq8PDbSrw6IxH96YsrVFVkpfR3+/kzzSwLgqdsbHnsq/P3GdeFDePmGe0aFHwxvxOCuLbjqubflReHtt2xvn/g0nq2bEh4cbI78HJZuVeMC8inyPG4vk/15ojXJqTcYnFYx2W1JQrOYlJSQALQnCfRWvV9fpF+j36I/qj+h15tEApNCsknwuHGSdhKz7VyotY7JOoLqXJIUydsxXehthbQcKUmXiaLr6/B5tPwTu9y9cXz45aPHwq8/hDNx8KeYecWTPT+UzobfDZ8NN4dfxoxrnnp+Nw7/FEfhgtATA2/iexCYbORKko2BQpru/iSLbAQZEh1KfGlAEWULcd7ucXAa28YriYLKXmBv8ThH7XLl9vBrbzb/G9/Babi0ifmw8L+x/33fLBDe+lv46Z3EzA3hJ1HBhHO7lyPnIdONMPdpY/05Mvkzo6gjL2eW9aWB1TI+I+M8eYUsWGTUi+TwEKXSAIpgKA2A3WOOIUxTiElq0JekUckimTQNHpN6nL9TzDn/F/EeedHG8MB7w46NLTSs5Tzo42+PsqzoBUU0xvGlUNbpSIo6kfgQx5a7+ORiJytbgU5XB04X7ee/PyR+JX3RfGZT88u0kKor00lXtvC4aYp/gE4xQ4LLpThY3OR00F6c6BKdTrfotpYG3AmisTSQrfPrhDW6E3Ru6kSpwYNlHvR4mLmSF2KhbVtf2ypHiOqHV9WcHHK3LJ5W1Wc61uLVX2P6yKcGvnv/GTp37KcbT14ZnigU14afff7jcNM24VUcjzdu2tnnxtnhD8Nnwj+ED48tDG8JJ9fdEsIRGs9kD5dbnT9JJ4rs35mIk+JMZh35nCIdniCHeSDyqT8zYfg83QqdYNGhXqczcFdEcmsyY8iMW8zYYMZaM5aZsciMTJ7aJ+qOSKC+aBh/4RAhaRK3SbYEUnmzcuiQcPaQsKo5KC9q3iGMPbtQ5flB+nEzz9Fu95fzOJ80x+6XMVtGj0zeBUHGvFMyhmTcImOtjGUyFsno5x3U3hTtUhut0fZdMq5pPZ7QtZCufeq0z2TeqqZZanJBVB88xBwl0eiJfCtWEY1WKPB3EwVDfHycINrspjjyDiKQj/CLKFLi4eEumzy4344e1WszHmVFz6MWXZQ9Yt8OyAInnkElKvh6+N4hz9oXlFbdSMZ45JNErEutv3V1ozhs43nvkW80WeZzWfbyuyFOb2DyjDMYJbJDow4FOk1kEZjzzaXYMqntkZ6GOi4NdkJIo5uPHCBxPPpp82MCfW9v/pxkMkh4sXnj+X9EbS2L1pIpZ4tnMlF0JBSRmbNqypqoVTaR0R4SXpMXnXNvVOcqAs1NxtH+ky5Itprjk+NT3KLRZbRQHp4oxtvXpOCSFKxNwYoUHJqCvVLQk4KJKXgmBY+m4EspuJUPqE/BshQcywdYU1BKwemf8+59KbiOdxfx+em8jya/x7uWxOBVkaoYV/IpKjoa35dwHY7BpSKKiyJ6NopoRBTRuRT8PIqrIQWFWr6+PwXzOf2QgjpVi+i8+2UVu0THhZ6YTshPIjnyUzKaHnCb6tWXZOHFLExlmUIudsCkQdiX8gV5nKFn5/C628Kr+6WJ0vZzeENihqInadf+IO7YuGZv5Xm/2LR9ds3B82PlReezBizr0OUhh/g21++onzBT1J0FRqNZJ0myWbbEx6Ei6oG8qgWbLBiy4BYLNliw1oJlFiyyILXHOINcTnEbLxAltFNv5gf6N8fL8vZPhLOmHVKo/NHzJaQ2hS+ViBuJDqElBjGCDQb6PRby8nGUldsTLOTlLRby8vGal09A+o+tGevp8y6cxTyqIF+fI+ms7NzzUCBx7kR4yiFh1HcoNYUPhJfiYvSLH772bfNH8qJP3kRb83stZ22VFgeN92ehyZRgSCBTizeA2WyQxCSXSUgg90lxQzToAXuDC2td6HGpnj8n/9JJiJY9MaZoxLGommJqLeiRbg/fGR5+SLjnexT3P4Brfnr0/vAAPHLPw8Lw5v3yomPP3/9+SvMD4rc3LWr+aRWz00kUJ/9E51UPuMOfaoL2KV6nIsvOFLLeTJM1wVk43BQwVZtEiwm9ByKn/HnUVOAd553mFc1eNEkmr9iunac0UNMeA+1xRHsy8vZokNu3k0Q6u8sUHK3gUIV0IOFCTqheA03SEodS7vtbnWwa/9NaXFyvTKFzpti7V3pajlM97ijCJr3tIEs/hd8Kf9PcPPppz9G9T7+eX7ep7NEnKnqjA4VT4dznUnfeu23PsFtfvHzR3OlX+Vj+jdMyFt6w8KZh4/p1cmZcOXH+yCdfumt3Wm1lbc3lxQN8llRf/7F1xJdM0qN9LObGbP+H5BopqzXo2d0WExfabzLgCAMOMGC6Ac8Z8LABnzXgfQZcacCFBhRKDTjSgNkGtBhw+nEDvmXAkAFXG1DtoNZTBlTbdxlwM1kY7/IbMNWAJ3kXNdbwxnzeCAbsSx1HDbjGgA28r8iAWbzjKMeyhi+tthMijwGtBowY8IQBDxlwCx9QxrvyeS8RoZt8sdf4ZWdzfWxH6YW+C9loUl7MpZ5DOPp8OEW6TfrinFv6YqMWH22i+Kgr8TUBhvu7m606yUoaHE/HDoVCdPo5sMmBIQducWCDA2sdWObAIgey0PSCk+A6FBOiyh3TuWvgOSWvKJLw0RPh8B2HXnr6+XefXxv+b+KCU4+Ii86vfuG1t14VK86vffynxSo9BgDdbURPOzzvj7ja6dmFYqLOhnor2qyUXekwTtSZjQaDWUpsJ7uTV7rR3XTzwsI8N3ZzYzs3Gt34sxu/duOHbnzDjQfcuMK9wb3NLd7oxmo39ndf6Z7gFru6MdmNJjdWNbvxWzd+7MY33XjQjY+7caMbCevNbpzhxmvdOMKNA93oc2OKG+PceN6N37jx72487MbnouNhlRsXunGWG0vdeLUbs9z5bqG9Gy1uJPwnOf63OP5dbrzfjavZ2FvcwkQ+eoAbe9A23Gh2Y79zbvzOjR+58YjbX4PPuvEJN97nRlrgJr7ACPdEt5DHCWrHCfqZE/QxJ0jdwP18A7fwDUziG7jMjWxCqptMwb3Qvdl9yH3cHXEr4Ea9yyoZxESzGfUs0CAB0o9cJKUqvf760utjP3WtP7FnXKxell56eOvxbIDveptddTHkc9hpOGkS+8HdqZfS3Xhk6W+CM6mPPYEVfQch5sr//PyMKzM5PfJ5uPzV5h6dXPk/7v+hn8fg7oj6V8WFYz+s33iesuHzix7bMxslcfr5uz642xtcK+5R9asHnQVM3/UY8kcUREGQdHpZ0ktGgwKiXnSJhaJoEpHSY7TPNeIUI441YoER+xgx3YhOI0pGPG1EPGHEo0Z8yYghI24x4joj1hqxwoh+I/biQxONyP6t7DNG/Dw6dJ8RtxpxjREbjFhvxDIjFhlxqBE9fDQhpsGE970o3q0cbz3HO5ajzuaogY98iaNawgeM5XjSo3jyVCxbeXdtdL5Kl7oM0dTkz+UkqUjUfnX653z2sxwBzRbK+MJZRrQY8eJoKFbSl3Jgv607pTExErtFncz0oMWhsAOW3yuQH2Oxbq5oeL75s3fwCXz8HaGw+YBQKOY1lwub+Vk/ns7PoHQNeCGbTtBxnq5ddTpHvCVTFC2OZCmnZ3vXqEB7pwdsuq6jAjqdDfLj0RJfEy/EifHxNltcUYDytvQiygybcnBLDq7JwYYcrM3BshwsysFs3hhDbvTKmmeDpM/8Jke9em8VJXC3yO7f8jF6V22nw9PBnWRfB7/S9sZj55xBeBnq4gVHohM3PbT14x//U3vjvNlxz2Xikjf/0m1ActrQKyomKsqw/ROm3ht4eeHigtLEHesf26dIA5bUjZ5gw/Rnd4czi0bpaq3VtTdPXzbh/jEBSciuGFVSpt47LOF3yW9CEnFokr9vBzk+3uyiyCg9Q7YJDoe7KOCwmsHoENKKAoIzlIH5GbgmA2szMDUDIxl4IgObMlAVb12dun8tYsuLidf4hVwa2xOFQ171ENDlsttZuxh7O9s+XHfTQ7mCXtip7JOknIfnH3nh4I3L/rRy+Ybl84SOzW8EpqYuNPbZJn0XDlxeUjUh/G34s3+8dPSzY4dfJ1smWYtvkKzbwTT/MDAnJig6XYJZTHZbk4oCqYkLE1cnHk+UEhOtVo9SqzQoR5UTigyKVSnjj03UoDOIimI0ikUBozO19Z3Q9Szdb53fIye6bxK/XuSviaLRDyYsX1G2yPKU48SOf5w8deKRj1Kejq+rXt0gdPzr0aqZpo3PUMycgDZM3XFP/ITrnldlMY7oP0myYHfj4/w920N8vCVJsSjpXrsjntJ6Ua/3FAX0VjG5KCA616RjbTqmpmMkHU+kY1O6JoWYmxhSu/zWQsjQSGVxWm5nJoUkbyb2VjeiKqLYm7Md77hpa44g7FN2iLrmv924bENj4z3L5+2smoCJ6BL6TJgyD184l7Ctj7W+G9b+46X3jn/w2uuavblIBnaSwg3+ggSbomsHYDLpbKI7WSGX2g6KAuZ2FD22a2ewWJxFAYvVQOw2OI+6scmNW9y4xo0Nbqx1Y5kbi9yY7cbr29pXq6ttV9ZFoakqFiFNlYrH5ujMpaLDxHvXzVnVblN5+LFT5859hR8/Y1mzbPEGBf/7zBuTC3tEgJKtZDRhh+YXXI2P379LfZ/VnoQzUH4DHLDaX2VOQIVOCYfkkJKcRgspCoCo0A4SFAs6UpOykkYmlSYtTFqdtDlJZ0nKp+qupENJx5NOJukGlFJNUPtECw3dxdvlJP+4isIkf+fuhZ6k7KSyJNGfRD7F55t0PTlG7gPVd4Q8A8rhGUau+lKBXKC3dy6/2U5yMOm1x1wHVu/7059uvW1Erx7eYYPeFfefHy7uXzx/3a2mFfqCa8sXq7oWHi+elEaAhyLpzf6KtCSDIVUSu9hsYqqYnZViSTImxidmFAUSrfG+okC8E3TkCSRUJIyTwO3PRk82vpWNoWxcw+uQjUXHs7EpG0dm45ZsbMjGrGy0ZOOpbDzKK/rJ2iHQ4u75Zfdk7T1UjM62Eie/du3UmSUaHltvb6yp5fbq0zdXcdisYi8t5eCX+kL67nc6PGm/qQLNQu6eG1599vUjwW2Zgl56XNlbuHhM44K5q4uXFIbHr2xIHjEKB+ysqkY9ulkSW13eYZ2uz/bzL4f7ia8sOVT52olPXqx4luvAHSTl78k2XVDmH+Cw2ex6nV3XLjmBmu06h2gmi7QeTcamZAwl4yn+M5KMJ5KxpXFLMtYmY8thWBf1lnSW5bfObNWXliRabVv8VoelkZf1f+iW0KNPdisrXrhh3z5KKxddN3XXX5qzhJ11Nb1CdzffKr8ZXnDZrUaS7woi+jL+rlwHs/2Fok4HkqQ3yBbJgTAmgKBmHpTINPHcZzPPWmqjucypmC41NRnJuyZddHxrLj/mlwYSeuc6RKJ4xb59+2TPjh1nT0j9z7H/c0gj5Wwi0RQHq/zT9QY0GowSxMXpREkym1LN+WaB/Sg1R8ySxaxWF5rlPLN/zLjCMnODeYu5yXzULB83I5jVZwnMVnO22a91njCfMht0AuqMkt4ig+Qgk6XTKD8pj+JXItpHP+tU88lhMUTexRdnYnb4ziX79uFH74aH41/w+1nhhfKb58sFczir+R51DziI83Wuf5TI/s4cARynZDwh4/HoTeVmGRv4vWSqjBZ+U3k85hJzjYwjZYzwKUd5e8vg1qFSLJNb3Vo27pPfPNuL6+VyAMVL/rYrLqD8qCtAmiHNY9cbPAZftxSy3xSrywYOh8TOcZMlzQCOCh+O8GE+++UvTPWhxYff+PC4D5/14eM+XOnDm3xY48MBvDfOh9dR92HevYt3L/ThRB+O9KHbh+d8eJJPbhmwzofqAj4+QPLhGR9+FEVNc2f4sBfvooXzzvE+mrmFz6znqEdESYvjC6jLb+V0qb1ujvSoD4UmPnOND8sYRf44zPZhlg/Bp3qb6FXdJYLOCwHnJaPSi+JW8lQ5+S0eynfhyk5VJ35v10kz1l6dczsISTy6cWoFb1b7RRhXG7xtr7IdBVEQ+6+fedPqFLHf5uu33r1nXO3cxcLO+28MbWleJY452E3unjcyOGHKjFllew4zK7//xl0PNK+Kyl38nuSeDOX+gXaDwQjJxmR3it0JTrko4LSaLUZwHE3BphQMpeAp/jOSgif4/avauIVf0LZ2SNE9tnJIaTGOKHZvtJe8btcGbl2/T9vMoIfm7XlY2Dljbq89my7soHbS7jebs9T4RmpPNBspwin0d7fxm78klz6eBzWJLKjZ4sI1LlTv2spcWOTCbBced7X4nV/+fZ20tpHk2e+/O41f/PT1waX3b1q18u4HVwodwp+Hv8Y0tAnZ4ZPhT08cfuvv739wVIuDw+OJtqv5+2iKg12QatPrDWDolGGTHIIaB5sserfQkcfBnTC/E67phLWdMLUTRjrhiU7Y1Om34mCN4LSOnb3OFmY6YsLgeLwQB58dJ0v7lJ0oyVL2pkWvvXJw/tIZ8/KXb7jtJhYIP6d/MByQlUf7SD2nJVRMCp8Jf/zZixMObTj2xstR/RCWE68TwOu3Kgl0TpkSHRbFaJUsqlPMjb2hyWWkOFVK1DjCYbtD2a6XfLXT0jPSB9bOFQfVNR7IWDnN+LDxhX3Nb/I18ihefYpiiG5Q4R+oUzo6UtxmALdDkXzdzR1FlyuV/I/LKhqLAjrRae2O0B1PdccT3bGpO5Z1x4bumN8dqb0lMNB+5yf3V35loXP0yrFTFmaq7/RbXzmK4lP/PPrGR2mbk9Y0rFhYMmXRfYuvfPeNve+mPGhZPHt+ffbke1YvGN4FfRseWboqdfyosWP9Rckdu1w9u2jdfQtWJhZefeWIzIHdMtIvu7Kc7TE1ckogLYZEGOZPNycmxlksBklyOuJlPdlZnMWAJtHg11sEO9OLBmf0TWjyEXaHEf0tEDVeY5vIoD30ZjFb31xHrsOrpntCt8Ckv96ypPeNr72Wm58+VO/6QXhn8enTi5uLr8mPV+8plhKvv5H6k72X+gfY9fo4bBfXLsVtl7m5O80OA1j+l+YOua3DD1ui9t5KzQ6Ezjzo6tTbhv0vtnapf/Nobu9C8PwTF+xdeJto1pGP+ploNuK1/p8QFINRFATFKMaZDIJFQcd9JlxiwjITjjXhUBN6TJhoQsmEJ0z4nglfMuEWE65rPUYdMF3tVvtiOz7i7Sreibzd3bp9JW8fwdvjTNiXOg637sj/fYS0jLl4gFBkwiwTWk0IJu0Kt/RXjppffmt06ZdGufltfuspTb0Uy8eEXKHyWPiGpu/N/bydfzxEovF3eXnOXOFFQPY37PKb7De1cac/gmDTKSZLvJhgMIk2MVGvS6ScSa/HOL1DjE8Q9RY02USdY64TpzlxrBMLnNjHielOdDpRcuIZJ37pxJecuMeJW5243om3RUcO5SMTnag4sfpHJ37mxPec+IoTn+Ljljixng+NxahEMT7F0a3j6KqdOC6KjgZ87sT3+ZI05hEnrnBinROxjK+Zzonqd4Yv9RLH0cDXGeHEbN5N9JzjXVsYespebnJiBcfey4luJ57iCxx24j6+/BLem+9EwepEcPJgovSieKGNBEvb9re95Gp9x3VBoEm59B8Fn+yWaxK7AWWeIrflfaBXvHDx2TchN4H9kNa/fTDd0Onpo+G39+zXpds+e+FgZuqRkNC8rce25mwSfJpr55XixOZ2z68Uk7n/SCJb/JrkH4dj/VvYu2WjhDpFFkRR1hniZLNpiRnnmnGoeay5wiz2MWO6GZ1mlMz4oxk/N+P7ZnzJjE+ZcSsbd5t5vVmsMKNidpo7mQvM48zydIWXrOcV8/vmL836DeYPzQINGsfQYixK1v2jWXyJIehk7kMTpb7TzI+Yn+Ltspn9DUufywYX5pmxoxmRBfnCGfbLCkcpxBf3sd9WWEMBv1jPf2NhrBn9ZuzFf2+BT+1odxVuMaPA5hWZa81stEI5AUo6UdArFhAcLa/Q2c126SRfjMxK6+p8dZNjJHRxrBi9piYBRUMkA3oN/DKSUoi08Mfhj17EReG1r2I8ml4Pr8Xb8LnwUKG7EB+eiA83n2l+h8lEphz8PMmElM8fSdBbbHajwSBa7JIrSZ9gSUiyGSxA3h3cd7rwVhfWu7DChaNdONiFvVyY7kK7CwUXnnHh5y58x4UvunCfC7e6MHb8uJjxTj5+ujrh/ZgJ6391Qux4DLmQgrR1LlwSDdLGunAoj9M8Lkx0oeTCUy484cL3XPiS63eN73vC5Z+gjW8Z3DKyZVgLztgxQlEUF7iwKRo+UmOWC628seUtGhPdpV5GtH1x0cpPl15syL86I/r6S3uxH+OnEzp27k2nfT6SKVMMTWaM8cKhK3M6ZT42xRYe0/S5HH+VWPDd8+GyIfWrwuPjlin/9Um9m7fHd/7E/LKw+9wrT2wbw/9EotMlv+Mo5lsOL9L3E/iR9K4Ib8Y3hH7CfOGvYn/xOvHv0uA23/WyIFfIW+UvFZfSoLyjS9dN023UPaNfp/+r/q+GZPrWGs4bHzOeMp4yeUwesqbW3y3xSvy0+NcsOZaN1l7W263vW9+39bM12G+2v5+QnnA7fZ9PzE6sT/yLY51zXdJk1/w/vn98//j+8f3j+8f3j+8f3z++f3z/+P7x/eP7x/eP7x/fP75/fP/4/v/6AvwfuVX1jQ0KZW5kc3RyZWFtDQplbmRvYmoNCjIzIDAgb2JqDQoxNzM5OQ0KZW5kb2JqDQo5IDAgb2JqDQo8PC9UeXBlL0ZvbnQvU3VidHlwZS9UeXBlMC9CYXNlRm9udC9BQUFBQUErTGliZXJhdGlvblNlcmlmLEJvbGQvRW5jb2RpbmcvSWRlbnRpdHktSC9EZXNjZW5kYW50Rm9udHNbMjQgMCBSXS9Ub1VuaWNvZGUgMjUgMCBSPj4NCmVuZG9iag0KMjUgMCBvYmoNCjw8L1R5cGUvQ01hcC9DSURTeXN0ZW1JbmZvPDwvUmVnaXN0cnkoQWRvYmUpL09yZGVyaW5nKFVDUykvU3VwcGxlbWVudCAwPj4vQ01hcE5hbWUvQWRvYmUtSWRlbnRpdHktVUNTL0ZpbHRlci9GbGF0ZURlY29kZS9MZW5ndGggMjYgMCBSPj4NCnN0cmVhbQ0KWIVdlM2OmzAUhfeR8g5eThejAP4bpChShsxILPqjpn0AAk6K1AByyCJvX/A5jOrZJPqM7evvcPGmKA9l145i88P39dGN4tx2jXe3/u5rJ07u0nbrVZqJpq3HBcNffa2G9WpTfK2Gb9XVic2+6U/uuWxcN7bj4/l3cRSNO89TysPxcRvdtezOvdhup6Gf0w630T/EU1j1ZRr67hvn2+4inqaV88DxPgx/3XXaTiTr1W637DYV/PUYnMgwMJ0N5+kbdxuq2vmqu7j1apskidwJ/AVMk4BpRlRARTwAD8AMTzM+zQywIL4HlNxZauAeqLBWcbJ6C6g5WWOyzomvwHmy65rPGspC73Su/1T+f60sibQyHjxNgW/EDPgeScs0kl4OTmmVRtKKB88scInkBaiJOdAQ90BLhKV6IRbAPIpzCUzCSNFIwkjRSMJI0UgiDZ1Er0LzJUsTZS+hoKkgoaCpIKGgqSChoG30Vg3DUShkWEihkGEhhUKGhRQKGRZSKGRYSKGQWQohK8OsFLIyedRN5pWI6Ayj04jOMDqN6Ayj04jOMDqN6GwSNaalkYaRXdoWRpZGGkaWRhpG1kRNbamgoWBz9PjSy3O7h1vk4xKp795PH3y4bMKXPn/jbec+LqShH8I6/vwDwYQOQA0KZW5kc3RyZWFtDQplbmRvYmoNCjI2IDAgb2JqDQo0OTANCmVuZG9iag0KMjQgMCBvYmoNCjw8L1R5cGUvRm9udC9TdWJ0eXBlL0NJREZvbnRUeXBlMi9DSURUb0dJRE1hcC9JZGVudGl0eS9CYXNlRm9udC9BQUFBQUErTGliZXJhdGlvblNlcmlmLEJvbGQvRm9udERlc2NyaXB0b3IgMjcgMCBSL0NJRFN5c3RlbUluZm88PC9SZWdpc3RyeShBZG9iZSkvT3JkZXJpbmcoSWRlbnRpdHkpL1N1cHBsZW1lbnQgMD4+L1dbMyAzIDI1MCAxNlszMzMgMjUwIDI3OF0yMCAyMCA1MDAgMjkgMjkgMzMzIDM2IDM2IDcyMiAzOFs3MjIgNzIyIDY2NyA2MTEgNzc4IDc3OCAzODldNDdbNjY3IDk0NCA3MjIgNzc4IDYxMV01M1s3MjIgNTU2IDY2NyA3MjIgNzIyIDEwMDBdNjhbNTAwIDU1NiA0NDQgNTU2IDQ0NCAzMzMgNTAwIDU1NiAyNzhdNzhbNTU2IDI3OCA4MzMgNTU2IDUwMCA1NTZdODVbNDQ0IDM4OSAzMzMgNTU2IDUwMF05MVs1MDAgNTAwXV0+Pg0KZW5kb2JqDQoyNyAwIG9iag0KPDwvVHlwZS9Gb250RGVzY3JpcHRvci9Gb250TmFtZS9BQUFBQUErTGliZXJhdGlvblNlcmlmLEJvbGQvRmxhZ3MgMzQvRm9udEJCb3hbLTU0NCAtMzAzIDEzNDQgMTAwOF0vSXRhbGljQW5nbGUgMC9Bc2NlbnQgODkxL0Rlc2NlbnQgMjE2L0xlYWRpbmcgNDIvQ2FwSGVpZ2h0IDY1NS9YSGVpZ2h0IDQ1OS9TdGVtViAxNDQvRm9udEZpbGUyIDI4IDAgUj4+DQplbmRvYmoNCjI4IDAgb2JqDQo8PC9MZW5ndGgxIDMzNjMyL0ZpbHRlci9GbGF0ZURlY29kZS9MZW5ndGggMjkgMCBSPj4NCnN0cmVhbQ0KWIXtvXlgVNX1OH7Oe2/2TObNZJbMxrwwCQFCmEDYwpYhJCEsJoGwZMKSBJKQCCExCVBBC7bWBVygWrUulVprVVAGpRW7KFatXfSj/Si2VilY7WLVgtb6USEzv3PvexMmIS6f7+eP3z/M88y5+z33nHPPPee+CQICQCbsBBGaauoiEw3Cr38GgO1U2rSus7nblG1ZDzD5GSpbum5Ln9J0ec3XAMqmAQh/bOte3/n15p/YAaZS3nB4fXNvNzjBBFAhU395/cZL20qXj6qgvAIwNtDe2tzy8UVv9FLdewRT2qnA+pfMOho7l/K57Z19X/ufvmN/A7DuBBhdvrFrXfOiq1fsAuiaCeDM7Wz+Wre1Qiqk9lXUXtnU3Nn6aPeEsZT/NYDlSHdXb18yF54merJZfXdPa7fn/olTAGbTfOJ8YGsVANYfLmtttM38jxAyAvs86W8+zfCLt0TeOnNf/03mp4wytTWytvxD/Qw5iQpYYQmeue+zE+an+EhpH7OdlZjtuASWwh7QU08ZIrCKprtY8BJvEUTpLuHnoAPQ3a4rpiHzVCzugzbBgTpBMIoGnU4QpZNgTtbC15I0bA4be8KcurmggJI8q9uQqMRiQw7+rAnwyRP/Q70P6GaxlZIEAUbgpgG6lsPDWhpBxnwtLYCEZVpaBD/u0NISuPA5La2DTDyjpfXgFCZpaQNsE0u1tBGc4tta2gSZkkdLm3GTQdLSFggYH9LSGTDeNFpLW2Gy6WktnQk+c4RxRyKdgQOcKpZGUFCnpQUw4jQtLcIUnKelJRiLd2hpHQTwuJbWw2jBrKUN8JEwX0sbYbT4Uy1tgoD4qZY2C29Io7S0BaYZe7V0Bqwy/lZLW+Fi0wotnQmTTJ9COXTAeoI+gm3QCi0kgxZopnwzpdZBF3TDpdDDW7VTqQKjqXQM4YlQBBMIFJhHrbqofiP1V2AupXuoF/tu5uN2wSYYD2Ze88WjTaTUEo2KKt57HKXmU/91NAKUd6zv6OvY1tqitDT3NSvrurov7elY396njF43RplYNKFImdfVtX5jqzK3q6e7q6e5r6Nr03jz3KHNJipLaIiq5r5xyvxN62jcRUTQWpo2nWAF6nhJB7RRg461repwSl1rTweVlFGjjUQnlHVtpO850EsktlK/Ft5LgUKCLx13Tu+61k0trT1KoXL+FF/WWzlHxNDOikrVct62d6DvRGJiET3jgTbs8taeXtZh4viiovHFw093brLC4SbjcxWqcw1PbQfNrnBV6uM1jDudhHtgA5V18VV8vsAVatfK1bOXalp5roWPysZeRi3qeKta3pNxv4/Ptom3WjrMjDU0Yxv1X8dVNdVyHR+bqbw6chel2zU5XgybOQt6qSXrl1pbL1PINL539CrNSl9Pc0trZ3PPBqWrbbCSKT2t6zt6+1p7qLBjk7JsfN14pba5r3VTn9K8qUVZOtCxpq2tY10rL1zX2tPXTI27+tpJRS7e3NPR29Kxjs3WO344lRt+551TsrRdAcQ5xrEtnA8X8eYs36t2qetr3dKqXNTc19fayxqXUYNejfmqYJdyVnVRKRPYVmIXY047Tzdzobfw4dhO36T1XEt7X/nCiRWtb7OmPJv4HFu01bA+4zSlaOPfvXzeTTSHwulLbYz0uRUuzGauGqo6dlJtH2+7jso30nOpZus6iXvqXGs1a7aV28Z2bcWdfFwFqglv5arbxZVrU85IrojnuKIqd5u2ARXet5vSXXwVKT4WchmylbRySlmqmdvftdRjI59bpa2dq3AzV8BWTSH7+ApS/GrRVsqo7uYlhVDBlZdZ3VaNpyvIWi8adkSVg+kbqJfv+C3amlNjb+LUtgysUeU2a7VRm0ld8UZ+KmwYkE8b10uVoy18tMLP4Xkb502fNmsXp6iFHlXiqm51Ud/NXB7qple1vu88zjVz/nZp/bqphs2l0tKpbuKy5l7alLSFl3Zs6uodp2xt71jXrmxt7lVaWns71m+iyrWXKoO3hEK1zbTpN23q2kIbakvrONrgbT2tve0dm9YrvdwGq72VvvbmPmYdOlv7ejrWNW/ceCkdXJ3d1GstnVRbO/raaeLO1l6lunWrsqSrs3nTg+NVUsiItJGRVjo6u3u6tnAaC3vX9bS2bqLJmlua13Zs7Oij0dqbe5rXkWkh+9KxrpebDrIYSnfzpsKKzT1d3a1E6Yp5i841JAJVs9PbtXELzcxab2ptbWEzEtlbWjdSJ5p4Y1fXBraetq4eIrSlr70wjfK2rk191LVLaW5poYUTt7rWbe5kBo2MTF+KuOZ1PV1U172xuY9G6WSGq51v+W6YTo5lhNSBPeP5xk83Z+s0YzZeU5IIdezr654eiWzdunV8s2bT1pFJG09ERf7fh2V60s01Ot1e9XDdYGN2ks584dR9l3a3aprS0zu+va9zo3oaqtOmzObmNEOd2kp1dNIt4qdSt2YAKjXVV4aMwMze0NN8AhE4gZ1BRA/T4M3cyDNZ1s1fpNR0k5pUkowUrcE4JXXiTxg/YSi7VDPUQfk+vvBevonGc2atp/oaomzRABtICTu6+3rH93ZsHN/Vsz5SU7kI9CWgueYaPAgPS5fAWxKAn2A+RSj/rX8QtgglcCfVNRCUUfky6UbYSO39lF9IuEEoSb5H5dUE9xIsJ7iIIECwhKCSYDNBOcE06nM/wcU0RpsG7VR+meES2KB7Dpy65TCScAtBLqXD0lsQJjpbCMJiECqo7UqWZnWG6wk/B/msPtWO8mGpFzqpXqF0MYGH1hEkPEobcy3NfxujmfAC6T7YJkHyNKXraewy6usTryeae6GOYSq3UfkUyhcTHwqFB5OntPRo4s1USk/la6d+BEupz1Siczb1y6F8SGJhzXOgJ2wkcFL9aDEfyvBpuJ1wrTQG5AHeA8Q0ni0lEFgbwt+gusm6z6BeaOM85bxjvGdlRPspsRjWSi2wnOqnERCNsFe6k/iwBJqF/XCQ8tupfJFwL5QwWvUkI4IagibGe873YYD4lsllsVzldwqYHNJB43O+JqdBQLTepsmleAjkkswKiEcFnO/DALUpYzIYCiS7j7gsSpJvEBY1/k/VdHAwtHB9rOSySAeSBeFMhtlatfmG4hY23xfgXN2foY6th+kL5w0r/xLM+UI69QWY6XCxhgXi8Uxa6wuM14Tf1vBHKobCFNZ/h/bHBihke4TpaWocBmxuprPpWDyq4bFQoJUzXuQzXp6Hj4FVnw+jWVqjs3ooJn25hNoXsT3I9sFQzPYl2xufh9meZfuGYalAxTyv8jf0VbG23/Vcx1T58n3P9t5QTGs2UB+r3kz7dAHn1zYNs317Z5qsi/XX8DbLmKylfJhJY3To3oGZUgnZkbeSzH7crOm6Rz+HbEQfjGey0eQwnebyiP8Ch+Eq8OqeS65L8ZLzbxPxrxcW6MdCte4GAKrzM5tGeAWNMVE3A+ZKPhiv8QdSfNKvoTW/ACF9O6zWTSUa67Q1a+uTfgTjCOaL+6Fc3Mdt8HLJBGNEJwg0hkV6FuaRndkr3AadwkywMjtkCUKuaSnkEh/rTKQXhJkdHm0iXTBeAvmGIJcp3yOaLr6V0oGvKiONp4P2m2ZvyrSxYJj9MEjf2NpoXTlM19NpTvUzPE32aqx6Rmi6PNw8KToCA/So+1RK7VcxmDxIa5ygrfVdrZ8pbc3ULvmHNH0ftNah+k2yniMkoCS1Lt0Jjut0HbR/RRovpaOD6an8vH2XRgeXPemZka1XeAvc3A58h/TsOzBNs+usbUyz5Qqji+tJGXxX/CnMojJOt+7nkJGad8CefBfm07iRtHXy+QhC0ndpT3wXxrP9Q3XFBHP4PlHP0ckMdBLMEzfQfBtgpPQEjBTvh3IaNyR1UDsGP4NLmNylXNJZlW/8fKX1gLCd7P1FLJ18gedLaK7X1TM4BVJv8hu8TxHxmPEli3jyGrfPC2n+wjSYymEyFBF8neguYcDP7Q3JbxNNh4UXkx8LNySeYPIaOMtP03lbxM8Oo3amu6Ry9UyX/HSuky4SMH7OH4AzmtyWEA9ovXyNd8IUmmM90fuZlEm2Q/Ubchno3yL9/QzqyB+q00Vo3oW0zx+AHP3vyA/5lOZ5hsBLvHuN7M8ymMRAuJ18iNvBgT3JvwsmcBBkCDkEv4EscTNIQgtYhChcLX4Cz9Navk+wg+Amgg84iBBkMOCP3Ug2+UbuwzhUwBGEmb+3l/lJafm1HErgIQ6p8R6EXRrcqrXLJ/gFwTcJuggkWv9bTKfETIgIrQC4AXLwF6SvC4jvRIsowy1DYWA+lS7mo15E+OsavKjBTrVNcj/BM+pc3Af6YTqI4yHAgNJOgP7XABLFBD/nN9KQ+BWVJQi/DJBsI3ySwEPpQsI3qO2SvyEgS5xoVdvxto3ngH2SIQ3KVEhsJ3yK4A6CyRqUqfMlTml9tPnYXHwsir+So9T5WP/Et9X5OWjzJh4+RzOnOy2fUAh+ps7J559K+FbCYYKdWpvZ6tysH5sz8QPC69X2rJ6tk/d7OA3+RWUUlfSz9V2qjf+yNu42FRivWDm8Q3gs5Wm+ZC7B74bAEQ3XCcvBKzjAz/RBIN0nvbYLWaRDd1I56bl4iuu3Ax+hMuI86cv/kAzf1nTrZ5qtYX7iZBZnEHxCevAJs31MD/QtyYcMlcmHpMLkY/qS5Hb9u8mn9e3JVcL25B8H4g8P5JGtCmg2ci2z02wPp85yZhtTsYduAzRrZ/hodl6zc1qLPXL190ANizv0s8DAzmfNV86VtpI92gDTpN0QIrsWIl9iBCuTpkKf+ETyP5Tn9WI1nXHURiqEZcz+UWyWR/5DtnQtxSg3JfvFvdSHnYNrKfaoIrvbBIukBqgW40QLGzNB9ueR5Ke6K2AEs4O0xrO8nPXJV8vYnNLvwM98FsM6QIapXy3VgfQDCKSdLS00/kLukzSSf/40bKJ5qvUimKUuOqs/Jv+fbLDuBdgi0fy6d2EGyYC9dNorHYL7dX0UE/4RGnXP03miQBHZwzLxdqhic9D4tWqsxX3WFnENRAj8WnzAzuo+zu9eisOqeHy4j5VxrMUk+jbiOZNbJ9GrnrcVqXjRqAcdBV/UJvk3oi/MZXgCphMeyWW+gI+hyv0K9dwzvAMS+XVrNNmHWT/dx6BjdKT0YUDmaoyk8DFPaDJnPvYJ8Bp/Q/4TgT5EftPr1JbN1Qk3mATeT9RinVp+PtxD68sAL/eNXgBJnApedlZoME66nPzGXi3PZHgnj0t5vEp64eV+37Uwj8earO6bMEL/FPlPBBLFsfpSwjNgCp0JxfogpZeCKxVTSYsozriH11Xyc5DHVyBymcwCr76JzyVwOtT5nQybkfj9b9DpAzCW/FCv0UY6XsN9gwxGB629Ql8EU4mf42lNmeY3ocLQT2c0xd/i1ORfaGwgnsOAL3MV6d8fKK9h0whoMKyCcv2tkCcdhBzT23CZfgssSc2b8s+Fw5BF9uV7BLefs8H9lD5bQFDEfS2il/ifSzwIa761j+LvPFrvOCZ7tn7dr2ieu8h3JPkzGTAdYHJg8mdrH4r13ye5W4g/2viGRq5LU4zvkm9ylMZ7FWZJFTwmatFiQIXJSvOdIA2PYvzSn4YV0gmun14mvzRcyHxFg4V8gm9CTgozHU/Rqvsb0fAkzUl6ynQlRdPA2rWxUnuJx4Gf44MPxKwU33DfTcND+UJ4CfN7hs71uT4q6T7TP7ZXuL6ej9X1avJge4bp7YB8ND4N4AWwhPmY+t+TPx+FAtLTcpqjSPol2duDMMNwGenmTPCyWEAfAxfRsY58sC26n1KM+QGnfwGtY2Iaz5j9WJqKIdUzDiibXEq4mqCU0qS1yQWka88S3E/p9wjkc+/kWVmC+jLfIlmujpGsIlhEsFbrs1SFhDYHr6tS+/dfq53/39N0+kMCssjJfQRBDVZpY+xTgZ+9LH2EfKVvsXrpCnwrVU+yvnQgfTtLk0zDJMPX6Ry9l87V14gXt0ObQPZHmAEXSz+H3dIxWC54yZcnfRXfIZ/sieR7dDbsI989IpjpfCWfU7oe1kpXU5yTR7a8gXS9gPpOgAlkpy/hev4g2ak3SZfYGJ9QOxoPX4NZopnajgJZt4/rfhmzf+Rb10rfI0wgHiMg/SK6R4gROiv/QfkTRHO6/SuCRpLVRRrI7O6B4qfygbufGXR+kI3jdo7Zx0ba2zWwUPdjOgNreFzD7+b4ndxqigt+DN20hkXcDv6Vzso7ub0soPMRmG6IF1PZr5IfiwXg5tBNENLgcdIjOjvxr5An3EBtf09lheCWvkNrv4pihFdoHXdCg5gLLuHvkCneQOACEL9BY/8y+S/u9zB4lGhpgJEUj5u5z0O+EEFI0JGvqqO+a8BOvlFAOER2hPlCfdSW+UnMR1oAYzjcoflHzHe6nOR2CrK4r3QzjKU5RgvR5L+FlTTG6zR+pep787iBtWftUm0WUnutjV5g8VjyCNtrdCacprPeQWmC5JMsVqY4SiJbZKS6v/J4CLi/FSA/o1r/NBgodvNyH4bZXLKRFEsFtTvTOn7HemLgjvXcvap6tvH7VPGB5Lcl1Tk3auOX8ZhTu6dNxZXc7yvhMV6x8Dfqw+4a9tNZ9iiM4DzKgmxa10jGS9yTPMNAKAMT8y2JD2a8A0KERxE48NXkKcJ5nD/tpH+nYCzn5e3JJ6j9WOEWipuI9+JKUCh2IbkknyO+Z3E+/gnGE3YKlxKfW0EnzKIYiMF1BLMhLDQA88tvUSF5L+E9aX79EEhGVB87cUPancBIxp/zcNrdJL9T+DL8Fe8s2XnJ5PQ5d5Sfi0l20ylmf1m7oxQ/r93g+8nk7zX8Tw2/y/0u0ouh+HPvKzX8ZXcmA36Ahj/v7vKr3mEOd5c5LP7qd5oezU5xnDqXvgyfd04+N/hecCjme0+lS6/d6ZSxu1G9zP3Uz7sfJ5z84IvrvwL+SjqYfOXz6s+7B/9CmSc/+sL6TV+Oh8po4A72S3D6ffRwmMeAXwDa/Z1Tvz75PgPdpxSvfUr4ORa3JY/zmHEY0HcAMjD8czDw2PILwLAo+U/DIkDjC8MDv5PjkHxZBbJ3HJIfMJCKkv+kMxp1h4aHYd/XEBgwecqApMuX0zwEhr+rwGPXLwD9v6j9ynPA7/6+AAweGpfAeJsG7sGQ4nuKjym+pNY9QLM2f2rc/6sc/69y+Yrrhi9b9xfRng5kN37L7l40zO7bpOHopngI9a/Q3D8geIrSJfxMcWogEU+ZTjGcpULyXQYDsfzVRNsPqU1an/P0oAq2cUjJhL37ITB00pxbiTcfs/7JT1SAnwzLn/VE2xXJ9w23EL6ToB1WsbYEv9dsMKSwsF99d47L1DKepqgT9qdigeSrBHTWJymaTSxi723JBn3IwKgBe/eivYNO3c1uZvezNN46SX2XPkPDkxkIL8BimvtBbcyLCDtSwOamurHsvlfaAM8TrEvdkZI//zC7E8Xlid3sPU9aP1kDO8sLbeAmmEgwmSAk/Bo8qXs57muyO1oHBHTZPI5t0d4phAmWaGdywHAUnKYf83dHQek4fFPy8fffPpK5mZ2BxtP8nkJP565Ze2fG3seOY2PRmlbQONNEAIvRDPnsPTd/r5NHfHgB6g315Fccgyu099izNFxFUElwJfMBjYD3SIDyUMxA/IhihL+CrL8F6nWHYRX7PQPnCUCD1EK+yGEoMRzD23RH0S1MSH6Hysbx98jsfpxhBi/Ad3n+mDBSOoY63f7kx7r9wvUqpNLpeCjga2odwwzS6/635V8FyIcYBMIxwut5+hjp7jHYTqAXXoVOBky3De/i9wj2pjDxzUhtfiQ9RTHfMXiEYAwDat9rLMBDxg34e8MyJBngnwgWS1GYoYvCTOko8cnF77me0XMZ0L5czmO70dpvPKzMv+I+x4OgDOMbch+F5DWf5AbGIxDUH6K47RTpYCH5AH+m2CEB86nvRNLfIoKFmu/8No25nQHVXZeClN+tvUc4KCTBR7Qs5/AgPEBz2hiw2JfddbOYlcW4PF7W4uT0eJjHlhTjSjuggcW7g4D6pOD8WDv5F2FG8ndqnJ18bVCczWLsVHydiq2HiatZvM7GZf1YG12Y3UWcZfft/YTPgman+E/t19I6H0z+ntZ4F0GciurTYO85YO86+skWnK3XTB2DfAJmK2xpbbW+rD2DgbZD4GySYDfAmXcJv0j4PrW8v5P6XUnwWyr/lPLbCNoo/T3CYcLTh47F/Dv13UaSzEPiJcI67f3Jz6UVsG8IXESwRMMMKkWZYpkVZEdVqCEoJKiicoZzCfI0yCeIUDlLBwk8BFM0KKLyMVr/RWmwhsoXDUNHrVZfmWqrtYsQlBCUpoDKS7U5JqfNN4XKJw+ZKzVO+9Cx08YfSsdyghUEMQ0vp3arCE8jmKoBS0+jcobnEVSkA5UzfIUGJRpMp3KG9w6Fz6Fj6DpqqB3jZVHamhm/gxqfI5o8UrLJ1eRSpcmvJiVTTY6VaTLn8tfkPogO0pkI2w+En9MgFXM/pepW4jn2rvnL/DnyVdj7aeEcTp4hnEn4H4QtX+a3av0YeBicV89imnzux+QTZu/h3ia9DxDQ1k7QPk+QVUyihiX13Vzij9r7T7KFyVp23qlr6/932jr/nAY/J7szlwOzQ8zGkC1JAbNJzIZROx8Be0e4gr2n4n83o8Ib2l/WBPjfHLG8Hp4A9hdCDbx++I8MdmZV2E3pkE9wUC6XYBTZoNEwBsZCAYzjpRHtb1CK2X0mTCHeTIMSmD7MPOVQAZUwD6pgPiwguhcBu82tgVpYDEugjnLLYDmsIGsWo/RK9vdTZHG+Rt8+olEEM60jQnNNhzk0Qi21ZD+93AKXJpN8jYVa3VwaeQk0wwboga8lk8m3hn+G/hXXoI/GrWQO+3uy8z/ReSsbYvXLltYtWVxbU33RooUL5lfNq6won1s2J1o6e9bMGdNLpk2dMnlCUWR84bjR+aPycsMjc0LZTrtsy7RazCajQa+TRAFhnBLHpoq4mKfYK5vDFeHmqsJxSkV2e3nhuIpwZVNcaVbihKRR4aoqXhRujitNSnwUoea04qZ4lFq2DWkZVVtGB1qirMyEmWyKsBJ/oTysHMGGxfWUvr48HFPi7/P0RTwtjeIZK2VycqgHp4pRq1TEK7e076poIhrxkMU8Nzy31Vw4Dg6ZLZS0UCo+Otx9CEfPRp4QRldMPySA0cqmpZVWNLfEaxfXV5T7c3JihePmxzPD5bwK5vIh4/q5cQMfUulgpMNu5dC4o7uuOyLD2qaCjJZwS/Oq+rjYTH13iRW7dl0dtxfEx4TL42O2vZ1NK2+NjwuXV8QL2KgLlwzMs/DclBjX5clhZdd/gJYTfv+9wSXNWok+T/4PsGRcmBvHJfU57OOvJF7v2lUZVip3Ne1qPpLcuTasyOFdhzIydnVXELuhtp6GOJL86W5/vPK6WFxuasfpMW3plUsWxrMWr6yPC3mVSnszldB/peGcaf4c+0Cb2s+rBmILMYc4nJPD2LD7SBTWUia+c3G9mldgrf8RiEYKYnGhidUcTdW4lrGanamage5NYZLtwrr6XXEpb35LuII4vrs5vnMtadfFTDBhOZ75sT8nvMthV0oiMd5WIarmt3Qocd0oYhL1Su9AesO67JJ5JvNjFb3vpwlG2R1KSZiGYeNUhCuatP+2tGfTAAoxuqpAVYSl9fFoOSWizZrEKg4VRahHcxMJrKOcCzMeCXfHneGyAekysio66up5F61b3Dk3Dk3rtF7xSAXfV0rFrqZylQQ2Vnhx/eNQnDx5aJLif7QYJkGsnDV2zyUtG1Wxq76lLR5q8rfQvmtT6v058WiMJBwL17fGmNoRh8ac9HPliHFdWVq/sC68cHFD/TSNELWCDSflVQwZJlzvV4chBYwb84xKveAXY9RQpgKlkhLhspn0HTfkGQlkYjgvZYpbNlOpRz+kWhMZ8TFKRWu51o7lBw2qY+o0tyo1mp5laZy5Vf6cWI76KRwnULWiTUw9jIypVakqMlNUYST9nFvFixgvs5nSK/Xh1nAs3K7Eo7X1bG2MPZzLGjM4zzVZLR2US2MWsQlyqDqVYcyMVxb405kbn8fzA9mqIdXzU9XKLmN4Yd0uNnhYGxCI8vlxYCocnWb3c1vANnSYbK8i05bmG3rXoWiUbeb26WyQ8PyWXeG6+pm8NdmTy/3b2FwOWIgLl5YVjiPTVnYojNcsPhTFa+oa6h+nQ165Zmn9IwIKc5vKYodyqa7+cYUODV4qsFJWyDIKy7CRllDGyNv7H48C7OS1Ei/g+XVHEHiZMVWGsO6IoJbJ6kSj+ERREKhGUmuiqdYSlRnVsp28jH8OAWNZ1KyLGqOmaIZgFfyHkBU9QiU/pfPRhPBoBlrRf4h6LeHFR3DnIVPUr7bYSS2iKoXXLDs39bKG+kczgLrxb5qojH1IXbLbSdh0rFQoLUxRLou172qKsc0GbhIN/YdxDM8mMYVnEyH6jLg53FoWt4TLWHkpKy9Vy/Ws3EAqim6k7jtJ9rVxZBqwsj6HtqTi+41/l/w+k1SMjMou+a+Fc9ohhK2wg+AggYjtuJ48ixA2QTU2wjKcA7MwSph4i2WE51Ke4fE4C3ZSu1lUPpvyM6l8BvkqNvqOEJQS7CCQiBkztDZF1CZCOKLlCyk/jvocpG/kwEpLqZThBZSvIjxPw5VUXkG4QsvPpzxhiKKB5B7i33ejFK3Co/14sB+hH82RMwhn0PqXk5NDJ4qPL/tz8RvL4DjRerzoeO3xncfjx3XHUVz2hugOdb2MjS+felmoeRlLf4mhX574pXAkeTR651GztbL2yaYnu58Un5g3NgRHMPJY42M3PnbwsROP6bp+jLbDocNC12EMPVrzaPJR8eEDZSHb/TvuFw7ej933Y+n9KN+m3FZ0m9h9G956SyAU+U7pdwT/t3Hvt1pCB2/A62pCIfhW07eEPd/C0LdwzzfxG1TSvgXlzcpmoa8pGeptTIa6aeIugk3zkiFvcfYyQ7G4TC8mQ4zAH60bX1x5dC2ebMamxkmhRjbgGoyuMVkrd6y6cdXdq8SVDQWhSANCQ1ODsKfhdIMQasCsYscyHa1copFsYkgsFWvELvFG8UnRYKxbkBOqpWG6qndU31gtXjQvHFowTwnZqjBaZbFVVhIhtnmheUKgyr/MXexaZkfbMrnYtowct2VYDMsitqRNsNkabTtsog1KQdjjRh0ewT2HltYVFCw8YkjSgW+oXRnHa+J5dew7urghrr8mDssaVtYfQrwh9q3rr4ey4ML4xLr6eFMwtjDeQokoS+ykhBw85IayWG9vXwH/YG9BQV8BEBSs6eX53r7NlOuDgoLeXt6CgDJ9vUgFvVTeS5jSfcCyBb3Y29cLvX1YAL0M+ii/mXVmw1HBml5KUQcCUKcs4MPy2dQs+8cVdNeDC7p0s8CmfQ92ng+AFx5Rf5OR/p1YlPzsC3zu//VHvVVBB+bAs/ApFqMAl2EWxTrsLx0vg11YnN4aZ+AiqrucoqIW2ATX0y763nCjYg6OQiuN0MDbXQ4vwF+Gnf4Siq1OD56Dym6Be+EAK0f2Xv9mfBoXYQuNwUZmEc+q4YYSLqavGwm+Rt+dghaZCKfgefgjrBKeEN6GPey2mI+SCe9hOeGFROFj2gALefw0+HOEqDDDergUrqLe/KObdfZPYEr+m8ZaABRhUxy1Ha4f6PEJ8jlEMyQHylakEoYq8WLhJ4LQfxOwm6f1BM34GlF5vThnWP78P3zEZXRejBHz2L8icv5HmAS2xGfCxOQpMZeiwWXJ06my5MLkv8XmrzaHfq/USb0h+dfE9kSLLqLLQD/mk8T/Ca8zEvi//GEFpKiSRdELcbfQyN6bgytqAlHSIfw0hhApsDuwpGRCUdbkHNdCwYm7H2a8I9uTfAvvI7tvgeyoxSSK1gzQ37ESsqCU97AXTyjSjRw1edKU4olul1OPQF5tJUGQfxPQzO8l3xOqdRU0Z4BOZaJC1KEkSGyQUjsW2/kzocgTxuJLr8dXr3PqYnzue4n8W3RVtLqp0YABdLoMi95kBINsEEyiwWDSg07U9cXEbEYMFGeXFkca16wudpSolNGQeR5XzuSpdsPkvGLhoXf6M//xd9x2w6bs5cuzxX8vWvZn4sz9tL5/i0dpfR4oivpcJpNNFL3Zjow7Vjpkdan7vLjHi6tX0yyQnVp28dCVi+lcuKiysZGvv7JxddW8RsaNyibGDWEvSzVXEF8EdkOhO0Lrs4EDro3WWR0ZGRRI2zNlm02SZIPozLJm2jObYg67HWWdZMiwiRJKjTEzOuJO3OPEnU6sdWLUiYoTZSeedOJLTtzHy7udWOQkotnnEvUDpcXEJg/jk6MkwtLFtBYPLcbuKCmZOJEw04A8xjKyGpx1Yo6IYg4eSLS34HEcia+39e+/Y2d//3a84jgenj9/vl96+0zATxhXJn4o+foPktxaku/pCnSLwA+rolNl0WwyebLF7EBQb22MLTejWS/d58FbPVjhQRE8RR7BqvMAZDXGSCOC2B3ESJAov0SVKkm0kdZARK9WdZTznnNfAbsMORM9WeH8UeGRgl12FE+cUorFol4SI4mDiauwA5vf+UzfELjy4D9ePfnqJQ8UKSv1DQniUxvOwnpsnZt44pcNiROJlxJ/T/xp5pg3EgfCE/jWhNzkWd06OgvMkA0TowHI1LkyXT5vtrsxli01xbLFLFdjLMvQFMtyEJ1cMVLkMdpQFgrQ7i6eOBtRJTMvTIqYP1nyvHJqQVP1N26tTOwi8mKJnyQeSZT+7cAB4XvEXtuZHxi7T4l9iccT8cSPEgcl4u8WH/u3fsIA0vtEjx+ui9Zlew36TLtdznA6EWW9VwoGMrMysppi9sIMYmmGnCGY9BkZktfvdzbF/NgY8zskS1PMIElCY0wSbw5iXxCXBjEaRKEoiArjN+PyapXn2nKA9CQ7wgUwSFsGnglFpUhryrGTAGi5OVOLKZVjL1aYEHLCBw5IW1Yq3a+8hI2hWCyU+H4/CrUlK7POzFeXldj/WmbCeXOi5bb+M/IniV2grfMKWmc2zoq+6kDUOz0ed4bF4taLXp+TNkpTzNPo6HIIhQ5aqUN2CCadw2GSTPammC0DbWJGhslkaIyZRNRLelqsY58Pd/qwxocRH9p8mPThKR8e9OEOHzb5MOpD8OFpH5704VEf3ujDLh828valvP10tcOLvM8e3qfWh0U+lPlYJ3z4JK9qTHU4xQupfZy3pxG7eReaSeGTrT730XZmT+qzZtialHnj30wepGmQksywoiEFtKumT5XOeBwQj2A+0T/v7gPSmjXKhL/M+SHOY6IRZiZG+1NSufV9g6H/9QcTMw+oe1mPtJdHwn3RER6DbAsA2AxiODea2517NFe05aKcq+Q25Yq5zKldvHhF1cFc3JOLjbkIuUXUTJwWzz2ZezpXfDE3mUsbqzZ3Z+6eXOnuXKylbt1siFCuYBRHBkPBxlgoZBbNzsaYbJZEX2NMzFKtbrG2ZLZWbFzDGaRyq4B4ZHekFk/mSy+FR+YKk5llGIEevviUceDscBl0X78sceSbryceP4RXYOuKGy+7ryG75onWd469eayv44Bw8Tcrx0zYhxN/j4txY2Z2JPH8w1NmJv5MRuKvieNhvNK3YIEPNF3Ve/ie7I3OMbvddpPXK9iFYMCUTcpoQotoMoFOthhFndgYs+pEr9suAO1A0uOmIJKtiwdxXxBr+UZUpQ6lE9kai4v5mlnCrm3Cc+ZFXWjxZG059hwNqxLPIUxbT7jpgJB7QPjOQw/1bzjQ/8aBBT5pMxNxQsbTDJ/ZzdYhePrf8VG8BhXs30CjtVhgZbSEHbVWi95I+8coskOWBOE4acWjVuy2YtSKRVZUeDZuxZ1WbEwVpunuIK1NuQp5A0rpMgjjDvR3cjpbGCUqdSm+6oD74fOiowWL3mAxyHbMyMxojGWKJktjTG8yCU0xk2OfHbvtGLVjkR2HWC9t0pQ5JiZNnJpFRkmdXXjtRbQfa1nSMOrM/AP7hR9LH/nO0HnqSWzQDG6KDsMSbotGRJ9CsFqNvgxRNGZ6PA6jw+sDq2wVZIkYZTdZTI0xISMzW7KIosMjGvVGOs3QJeodBT70+9DiwzM+fNeHr/vwdz78GTcZd3PrIJRy0yRzm/FkqnRHmiEKcbtSkkzrZEu1PpjWuoYbn5e4IYunCmtTNm5Y03LO4LDixkvO1UGpJ+UueDQTU0JaOEgJqYi7WTnhNHNjwnO6KPZMTdgPJ5g62nAHXi34Dhzobz0sdZ75n5S5OXuD2DPfd2YXz5s43/NJ/uzfgssi+ec6yJxTXpeZ6XTpwOawkU4KDtGUmZHJDuAMR60LSfDFxZoLqO4aRqaD0zmRy1/dIOlkovTNw3j8wOazz3L68HfCXulPvvlEyihpytnxA+T9SPUHmE9zjOygBdzMT4QMvT3D7sl20sZ2ZmWS9DOl0myMZA/2Ewe8ATI+DrsskCFCOUd1CBTA+MEnfnHw4C+eOJg4LDxO/khT4s7EgcRDiduFfYmnEqcoFJxNfoo58XHiaeFA4ofk0uxPfB/XMHrYOfkA8chI/snH0Qd0ZrMN3Da312fS084wOawO8lIccmPMIZptVmKa9f+/g3DgCDynhf/Lg2/A+p/TPuLqJOZ0kMunOydVRXLJOeL6rbfU1O3+euLeE/2Vdx8QajCIvoRbjO/b0f/QdZ8llqeE++TziVUqL3WvES+dEIT10alOm83nslppWVky6vXyiJDTBj5yPHw+8jO8xF7uX8iqg5ElOV4KYVGIC15VvnSCNV3UiGYq6SgZcj4zmnXM3TYNrEiwHOi/lCi/AkdjbuJDbNubqCZ/0XDZD6/be/s3hGmJcakl/OSpxMklCdk/X5iG192yuf8PO1Xb1Zl8TwqQvo6G7dGFFIAHbG6XyxC2hceM9RsKDAIEigLRQDwgWSVDIM+RRyZ+CWI5ogvJr0LM0GNelsPbGFvhRrdDqhmLpWMxMha5lSVXnJ3JmmvO18psw+p0/5yLKKvYMwKLlcmTRuWPF3l4xA5kctb1LqfbM0IgYY0cld9ZXzj2wZUY6tx84Nb22R/84/7nY4Vt12y/ctPmv+5vSJh6Ty3HO/4woey9BW2jS+Y1Xdty6PGCxFNHFqxcM7cxb2HXvV2JZfkKWzN96aZyu9EZLSOf0W4wGu2C4HTJoklsimUYTaJ6/oIj6sIiF8ouBBeeduFRF+5x4U4XdruQ7AnVKi5M18iBCLP43HE2cBIzOYZH2jBsT3nCHhdOOVb819X+lTrPKn/dfyYcI2l1OT/FrYlrP3Wcuck/n9FbnHxfdzPR6yU7N8ZDgZJs9pENdIv2LDsdclmiFZpj1qx9fuz2Y60fo34s8qtkDXhFZKDTDE3exCmTNWfAKYWV3IGMW6y85d7D+OvbEh99mvh34s3bhB0HfrDt/h+ILmbyzv77H5+ceV/U8fT732d+nyf5pi5OtGViIPqMKFksugzBrBN0sk0wZ4g6A+lLpkEssmCOBZ0WFC2YKVpEKStXRqeMH8n4ioxxGe+V8UoZ+2RskbFcxkkySjJ2Ut0zMt4s4wwZqcPvZDws4x0yrpSxgPenRm/zNvfyZtR/KW9J5bOoaDcfifrskVHYKWOtjFEZFRllGU/K+JKM+2Sk8m4Zm2Qsktk/GzrIvjRyA7NmOJsz6ERk5wr3NlcP5bV28qHLgGH1dDER0sV39H/2rf4Tm4R5u/FSbLpaN4s8LaP0CduuZ/eKXX4WywWTbxpOMnuD/ujTNqdZ59S5XTszcacFMwSwokm0Wg1Os01ls8NuYFcmlkydlDXJjblu/MiN97qxz41L3TiDl1jcuOEVN/6MV1DRu27c78btVOpG6uN0o+TGt9142I13uPFKN7bwcj8vn0GtX+FNC3gLqq51Y5RnqSe4UTjtxpNuPOrGuBv3uHGnG7vd2OTGIjdG3GkBTWMaJ4fj7po0znqK1d1ETFWjmuLi1avTdFkXNp1jbTFmqa778e0UL/94e6J8s9BwF47A6ZfjjPcfwEc2h8QZZ5+VPuUq/KYon/1QDLI0OyvLku+Jb4pPkZ+eB9dGaz3Z2Rl2Q16eqGSIGfmjPB6w2wPVMbsdzObw4pjBTLFmdUzvAmd1DGTIx4W1+XgyH3fmY1M+UjqaTz6KlqX0wBJpedrZPyhi4SjtEEidAIqXGf38TAwr9kmzsRQnT+JWZPJszDJkIllIiliEkdi8JnGfu/rr0cTx5fc8vG330vZRZbfesGtp88KZReW14lOJs/13ZZdVTc7H7It3zJLEax+ctPktT0bCI0prOpbVhlX/xUfngaK7nvyXIHRHK2WDIQjZwewRIb+pJuZ3O1wusTbmkjMzqmOZACFUQiiH2MuZGXS61YbwaAjjIdwXwm6ejWpHHv+ocr0k5feoTv+Qk5pMvoHdh0xhErU7DbORX5WRR5QnnFnZPqohGF29rql/RxNeYR59a9XzP//g9XsSv8YPHj9gt/dPkJ+SQp45iR+tbsopPPmfDxP/YhfGUJl8X2wQnyW5zo6OdOszrVa/3h8Imh01MatZ9ouid3FMdJ8K4otBPBjEgQBBFU4afXkkA3Z9x4hKRYwpAYgNhXcvPfPpJf+9+7ofVo0dWTZlRtPky6/ZtbYkd/SHn95xfHM48c8fep1r9m/9zYEg8bmO+LyK+OyGHLgsepHHkAmBQJYha2TYnVUdc7vsNtI0MIdqYhlmWfLVxkByQxiVMMphijiI3WGsDePRMMbDuC+M3TwbDWNR+Dx2F6t6pincuSVpaxLC2pWkZ9QsznXSNuRrsjNxCMenzVw0/qXnX3+ps0tPbF+fuCVx1Zr62uXVtQ0tk3M9mac++Sjhz9n2r+yyz17ILsPXf/ZsgfCM61lVnxjv68WnwUX61Byd7tXpsnwZUpY0IuSTashTAlk2L47JbnDX0CY6FcIXQ/hkCA+GcEcIu0LYGMLSEEZC54zHgNuc7umlFGiiO0hhhZOciYlTXZq0pnjIjSieNB7xX0/uT2QVbVxTf9XUg3V/P/7yb2fO+JOjQHz6+T8skb/z9bLgRTkFH/R//GHrN354Veck1T+y0SKe0N1DHumM6GsOl8VsN9MW8PkCfpcv21cdy6btb3fWxES7zZBZG7MYcEMALQE8E8DXA3hHABcGsCCAIV7Y8VEAfxbA/bxidwC3B3AlbzEjgBHe513e7Xe8mdpmQ6pNaQAFWwCTATwVwBMBfDGABwO4I4BdAWzkM1BtCdW9FMAnA7gngLUBjAawKIBKAIH3pD77eJ/TAdwZwKZUtwH7O4yjvfpcuJfeYJCNLk55GYPieFXFHOxtQXjyVFXFXNytC2KxK6x6tnfdcMMzj62bGw1m57c8+eR3+0+2ieUV+a1HX8g62ZmdvLa9351dVpbN31BMScwU35P8MAomwCzYGi01W8HhmDHZOkMQrKNEJd8bHjt23DjFq5TOdoDFKOlkeWJNLDyGnCZ6dMFgpDYWDOim1cR0slKKl6SpEulShOkQy3hKBkWvjiE3Ztr9vWeqx8Au8cMj8w0jcAYqdmdK4aaOx8k4KZyj56ZhCpK3NUlzZhEf+dPvCq4OvRnumf2H/6pZkC1UFr+OK7b+/cDzJ+d3zKgTHtuReLp++4a9dyWOLyibs7CidDauXPinOx+wmbsK7ln0jbv3ZywKFic+6byrfnNb4dJZnp7SxC8ao4uj0TXCzb29vZ2d7B0mst8lSkvJvgTh7mg7OJ1eq9HoHREKksoGwWh1il6PtzrmcVlcOvuSGPlruSFcGUJnCKUQlrwSwmdCeGUI+7gVF1QzfjqEJ7l5b+KlocHWPrVHU3rSOKAlKQUp1e4Jhhh9p2HqlGL1kCMHmTHKkBZ+H9ZX3HAJSmsShUvnlS1atDxRuIqMkPhxWUO4KvFu/4NMO4TI0jUj++ewpPRadhmzO4X05af1m8jyNEZnymYz6HRuj8JeI0Q9Oz17PGLSg3s8+zxHPaLNE/J0ecgvzbLWxbJMUZO+OmaysQut6pjoGoguwZct/1eBdq3Yo15qDL6twtSbHdIDPLw+4WgjWhPHVpZGY/Vzog0NnNhPyEhWzamPRUtXqu+vmKy6iVYvPhJNGjIzDTa9DVhIaTXKLqPL7/O6q2NekK1GV5aLfA2bZMlysaiyOibZOvy43I/lfpziR7cf/+bHV/34jB8f8eO9frzFj1v82MLbVPpxlB+9fjT5seNj3u5KXt3GK5x+lPz4UWqI+3jnPl5LPXP56Ho/vuPH1/z4m9QEN/NB+lJzlPmRxR5KargSGu9tP77ix6N+PMx7bPdjkx+X+rHAjxY/nuYNXuI002DRcVfyMIaaCGooE+FtqMEOP3b5sdGPpXwC8KMx3XdsPN9EqTaqcXWaLTvfkqVZulSDgePfUVKSumUddGza+XVrCXsNZuKupw2192AGV5rqYlcLtm08iXOXJmZO/Xnv6sSYGOkDPk16V1bmfq//Q6YPOL/203Oay/RhNOmum+tuW3Quqa3ZYiRRGyGlkHEL7rPgHgsLBGotGLWgWtJkwZAFT1rwKC+50YKlFoxY0m5be4a8JzjvuhUPakrbMEASst99668m/6kQfxJN6rKzg8ExNpsZcnPHmMdExo8bWx0bZ8sNZtvMY/LHVMd81nyXIWtJTGeQxZwlMRDlLRFcG8GlEayM4JQIjoqgJYIfRfDtCL4awV9F8L4IfjeCV0WwL4ItqZbeCEoRbP8wrd3NvFFbBEv4KPpU1WE+xJUR3ML7L4/gpAjmRtAdwb9F8JepBtdG8NIIdvAG5ZwUmsMUwWk0yn9HEI/yhvdGcHcEmzgZ5XyYAWpfimA08kwE4xHcH8FuPlk5J/OVCOstUMVOXlEbwdIIQmRARRvTdW9APxuHqN8XHrSDmqR7ddpd5hA11a5duYmdyo5egkFGlpzM4U3uI+XXdd0/7YXrE8zozilbsNysJsqWMeu7CjtFsr3btqVb37Fjp57L5PdXpgwd1+ep7Czi/vfd0fUWPZ3ZHr0nGPBlk7LYHBa9x+WpjrlcJpdo4/qSG8SVQXQGUQrSURTEZ4J4JX8TWRukoyiIRUE8HcST/LVIEy8NBfFo6i1J6r3wlx5F5/FLZdTnnkTElu7BB5HGimGOIW3tAlRTTPkIrZ39buDKaH0GOPSg92abbDUxkyy6yHF053rxbS+2eLHci5O8SFmnFyUvLd2Lz6TlP/LiSS8KL3nxqBebvBj1Ih0Zd/PEoPuKNN9smDtmfjipLowu5ZWQkyI+8tqJP77yh+Mnfp94fU7tRTNnLaohX77/w/989ukHn37wxgP3vPX3ex/SYsTEIkmhNbkhBDujNQGwWh0enUOn5LgodnHZHFabtTpm8xtH1MbMRrfgpehFkCEHlRyUc5ASM17KwdocPJqD8Rzcl4PdPBvNwaKcL4pezgsZ2XqmpALEfPL9z0lLZsKjheF3N3z3mSf//NLFG/W7+k+1rcfLseXh1dWL6+PiZfP/9snHiTP+siUvcGt3ILssMQm3jOqf4Urprdgs/hac0BWVwWKR9TqdDq2irHO53ewtZvGESVXs2gPcsrvIXetucne74+6T7tNuk0102qtjTptFzpQpVHaZwZA0oEGS2a0oEZ5aDPMmGi8pYKcJe2uS0sPZ5FBSgMmC4XNLemHj/nlTps0o3Tfr1v7/2rYNdwvvfK0j8cDXp+b1P3tO6RBmJ98T3iX5jIbeaKXRYHAF/H4bhF02V8gVcYnsT18UEK16cI0dE7Zli9lKdSyQLYsU0xtFt20sHhyLO8Zi11hsHIs1qevcQdLgLjMXBL/PLU675VQVLN/Or3S550tx8oDzz0Jm9VIXhXefOrLosUjZqHDPjBXLluzae+kTt6x/uEwJdkSqKpZf9e1tOPau7+c4EK4MRxZOn1pWUHhnz87bgh9sCubNKJ5cPrrwJlprDq31+9IVpIsl0YCZfCdRzPJkS1azlTZY1GC2OQHsi2NUnzrTfS+kvfQb+HmOPTy5lIISFpbw0JeCR/zJ1Tdt37v5ll/9asq4yReN2Ovc1itsmJN/7Fh7/4/mlMnLXCPZr1KTf5dmigdod38vut6sA5vNqXNmez1O5lzLeuZJOkgZrMywsZ2+csjuvtKLfV6spX1Nu7jIi7IXT/N9Hud7nCpCfL9Tdp8Xu70Y8Q62bcMYt+Lh7lbyDPowmTZ+q+LWXnEz3RKeIrOWOLsGd3CrhltXJW5aEq5Cl7A8u6x/K1k04cnssrMPa7Yc2L+4TuvNhKPRbxoEU6aQaZMzDSZRkITqmEWyGQHdd8i4nd/SlqduYwduaa9MXfGq5TPe5qUt/Db3bX4b/Ay/sVULl/KmH/Gq11P9ozIKRfwaV72ubRx8dg5zp8iuZ8+/BNdpt4Z+FQnllya2luGb3R+8tgmLy51iG+0pX/8/BB9hJ/D/NxaI/6G1+yEZrXRY9ZYMnS9L8ju9xiw06NDs9buy7KLOYLGagwElWBsUbEHcQkfVjcG7gweDYpQVnQieCgoQlIMCVQSZFcmKrarqUluwciUollH5zmhg1pwqJcg67QzuCR4N6qOU2EeJk0Ed6/hoycwqjidM4Tg6Zsz4qhD/vYBJtDq8otNNWpjly9BJKLtdkt4i+tFPexxt6T/x8pTwJA9rCgoKVl9SwBKrUzff7DcT2hY/FwOzX/8ZPFO1S1duofINHJkwhB93XPvjNRitS3yCYxsS5o57/7QmcXQpjkt8KG6YM8f/8jHvnDmuxG8TU1xz5nj6k/QtYxN+n+uXM1Epvkc8DmJp9A2DMdNAhUar2+XSoxVDYMgURzjoPHE7AnqjVUQRKQYyW0TRVsoD0mQIT/ALpLv5BVJjCGtSF0hUawvhBmpxijcauGgaaPp5Q6jl7I5TjYCbUqHwS2kR8J4Q7uRxcFPq4lPhfQaa7eMNmngVhAa/Z0j3+oa84jzfB1QvxVPy4zjtEoxHpezORTdIu5Fd8+VPLvaw35oJ+F+Ja5iqH3+WqXri+mjT5oWLl84sCBaOml48Pih2cdX/RDAz1T/b9YOb5md9+HVPbvm6r/RT02yYDsvpuea851fpD06k52Z8Q6gVs8X7pAxpCX9u0S3R3al7W7+Lno8Mmwy/MjqNvzRtG+Y5a24zxy25liszFmSctDZZf2L9SeYTNr08Sr7Xnmn/Bj1/dix13JyVkbUra5dzpivzwnPhufBceC48F54Lz4XnwnPhufBceC48F54Lz4XnwnPhufD835//D3RQB3wNCmVuZHN0cmVhbQ0KZW5kb2JqDQoyOSAwIG9iag0KMTU4OTMNCmVuZG9iag0KNyAwIG9iag0KPDwvRmlsdGVyL0ZsYXRlRGVjb2RlL0xlbmd0aCAzMCAwIFI+Pg0Kc3RyZWFtDQpYhcVaWW8cxxFugI8xAommbEm2gXlgeIke9X0YeQp4rCjC4k3ZZJ6SGIYhGXBe8vfzVc3ZszM7ZCw4XCx3prequrq6jq969rdCFRKvb+kjJF3842Pxt6tuUOsyWFs4VSofrS+uPhavj2SRiqufih1xvyuc0ELuFle/FIdXQ04fdJFCGZy2jjh3xJa4EOfiVhyII/xfEwpXZ2IhvlkhQStTxhhrCUa8ZRkTPNGW1kapaN6kXEyVxqrReE+8w5Q34gRCfoQCnsVdrpheKVVa5UjQ3Y4I4n5HvKZ/XrwS+8LsFiqW0nurIH0NX+0LiTfTbe/+/epkSqy2ZQwpVat6Jl7U1jiHcgv8J9VuxTWuF2ypZ+KJ+GKVmt41ao4scw/8n+PzJZT2q2wtZWlMIyVCj1PMvhDH4C1xfQ6Jx5B5NibD2TLpiP2ypWw1+bP4Ei+a+Suxgfea+AKafI0rvBopsnTFfwpdnBQ6+dLbwupS2QjH+wiV4HrdwIfish5yDpQ1TcXVjhCRkQpSe4JclP0BohkMNTQae2NkrGj6KzReIUhKLK5e3ecUAq+wJFrklvgrtvA78oll4xhpyhQ8sUujlyKJ/PBUXHIwnPOG74vtzsWNkmXUtoixDOC2BbbL2+Qdvil9LP79r+InXMKlYP2OSmEztY0mp4plVAiMIZXOqDTcKSozI0un0oYYOypsPaxnQ0ZloJcxYUl7n1FZ2lXjZ2a0rnQq+hlZTpdazolyFIEyzYjycCMX5wzhbam1maVKpQsw9OoZA+JIRjUjKwTIMnrJ9CmjQj7UXs6ZK0KvJN3MjMmUbmSv8wlTLJPVM0a1EmoFHVdPaGUElTSrZ7QoD147PSMLXp+oLqymosA3Ts1oryPxuhm9DPSKYTlmc1km4NouR2OulzXIGmnOXoiNIO3MDllnUNLTTDRah7ptg5qR5U2ppJ6zqo8l5M1MGDSIrJ2ZEF4fZZqjilDL25k4szGASoUZWUkj4fiZXALZoLIzjuNQkqKd8QgHr3dGzSzRMSjyM7keiiN5qZkZq0rZK6dVFcyq6UhdrkYma2WFKBBxSI3wSkaABKB2i6TKkDwyyQ4wyl1d6tYJMO2jfq6LBEyFEEvSa5Bs7hZIiFrF4Apmz/CWAhh5ijpZA60BWGjQQ6bkEjCoBqaLfl25CWAlz5Ub6/hulwykAvI5r+P+Xhyigr/Di7R6j0p+iFp+3emWycSSHEn0NZToQdTVmOK8+K3TyCMasMe0ZRAYlO6GPnRDioKUh1rGbujn4nav+HWmCzAyMZ9CtrJS1RojviqNt7F+QonfiLVR6GOoGushu2rYCfyui28BN2n3Cag+E8/HMVSthvUlsvRQjX0gpx/gD6doLha1b0yp1EjCHppaI+ot9APZqNxXClQu3fNQ2vMzQO81iHnDMP4APkH6/Ik1PML4bU31GU805h/NRMHAdI1+DmyE6i+4P3iDz2t8Im7ugBzp5nZSccIBEnCxL7C3BV5sclfT97Jll+jB9DysOM40wAhhhITq3uaMEG1GhrZMI/JNQlKLyAlNQFqf0Rn0IdR3ZvIoLQ3oaAhJL6cbC15t4DIR0KsHu+9o3Rrr3iaj9dJKnmQ0ZyhFUamxBXKYkfClFmqq1cPMKDNt+mu7xl7yWDl5ntkyUy7n35rIKgJqDZH1SMLtWGNwbFaPjuxo9BRdbu+KLs+ozW7VuzqxMUu73/gNMN7sDproEXP+YccABuALrqeYy0QzzLFdV/ocr5e4es4jL9CVvljVvqE3Bkzp2uwqjqltRwGgEIeXULtM4wdcCyhoL1EPDnFHmemzleKN7omXYDtnprcQ9BUSI72/XCVAo7gm9CuVgA1moFOJBZ1y4P0Out3wwQIlkhuxWCksEHBzvhK2CXJqUm9YGzqrOMH7eqUA5MlIQCxvdh91CkStlaEsgs+UlB/s5P+ilSO3rg6UerlgGpn8DkCSnY8kiqZP5ZGcXAxQc0paf2J3rGT3Aq63eTORV7GiE2nU6q3xEf5ciZEEudBe/B5nhiRHp1IUGKmppI/wGlROYzkUnA6PZ69qAAWSlENTPvo0tO+6f4TH0pxSUrpHo+cpO/Py73e4Eu73mEcUBhJNQH0GUBtpP6mhx2+MMaG/s9xndCzkclsTp5ZOlj75PjnM8pJE9xa8ASy9Ib6G8/BrFG+ZyD1Bf9Y9FPWROemMgDuonHqDhT/lCca4qOSh43wcl5KhdMOZENIUuncV9IPb4VWdzN6wDOKUpXTWg+GfsAeFyAVc7HvxZGiZT3SXd182EhpoUIBR6HDasQ6l0ImMsg0IqPlS6p3MVpwdWSatpWSoiviWyFaaqRASvrn/0Nwbykhgwgioe3eTDRAwjeNBvmgwjgcyd7b63tNfACQmYExvAFfC16hWdPehvVN0WBcxQMPtzc9/nPaVhed0R4X1ttW9vvs/6J6FuOGEgDa51JSx8gy6iQpwzM8oTjmXVjWO8upZe5R+M5FPDXXgivxS1hVmGxxH/OTkmjva07rT8pyjqWlrZE5JJFW9kWXSwQ3SHWXLt1yIFyi+XJ6P+JbmeVMN3ILigEvBLdOucWBXjd5ZplL1/7auQhVdv/etRqk0vud7ggTHI+kBih2x+Gte+21D2lPhqK5SjTU7ih/Y3tUEVbPbKXSz9EDjtOatvm0sOqHUAWx0gQkW4umoqWMRkLJllEOPaB6kXJJtR3NqVBlve3wx+kgLBYaTvcfmGh+G6HMmfzuPoJGBfMIDCAffPDWa5mgnxIVpOR48D+r0w+ZpORDR5nEcST5yLUHa1WvpDhaqo8cgEZbUZjaHc+3AsDt0BilN2yIAqnRT7Im/TDyFC4QCpeb91Db3nrvlI6TXHFiL5Ra9h7su2JffTR30gU0CBJEH9DMNRQNF1nuOjnXG5YfNOdq46khYHgiUPKNWfURjz9j+yWN0pCcoKiCtk/eEVjJwxnW27AUmOUF43U6IkdSLRPYo3a50n59ov+eMes46jq6OyrwD3GHv6uyk6yx0PWETFwGH0VSRh3U2GV/72tBW2SHMJjJVsxvjO2lhdoX8RK42P1fvCHiAt6tMaRj1f8+tw4Jr1JhJsdXJ5949h6At/eJCwpI9PfsuvsWbMdxZ2hqUoPGVJzq/RRcfULzD3Mozwfkp+ZwDNavFNNGoYQGlnPGcf4ew13UD9U8BEoWE7WPEZqiFiKtRhieUCUmUp7XWoTGaliNny+PJjo6EsUxIkFrK4ZmHqXd6rdu1B6gVYEl0Q8BtStlh+9j8PONmopHSln5f0mcmnvXxn+tQq2FsNZd2za9tttk3j7jDuMzgxxv+VckFXtSDr/P6rusu9mKiaKN51QN9XjHbGba2gm3HEydSJlbnjjn3FiYOeOvxlILptDV9nrvOarmjpkErzbBm1EnR+MhckbuRI9zZyFg5YV4P2Z8NALAJvXapHRi0S75UTvaOVmM31jVfS9LaNiuT1iNbbsiWSzEqHAosP7e31reJJ8Khpo7YFgwHyXlOAQXr5Z//F9m2DlENCmVuZHN0cmVhbQ0KZW5kb2JqDQozMCAwIG9iag0KMjYzNA0KZW5kb2JqDQo1IDAgb2JqDQo8PC9UeXBlL1BhZ2UvQ29udGVudHMgMzEgMCBSL1Jlc291cmNlcyAzMiAwIFIvUGFyZW50IDMgMCBSPj4NCmVuZG9iag0KMzIgMCBvYmoNCjw8L1Byb2NTZXRbL1BERi9UZXh0L0ltYWdlQi9JbWFnZUMvSW1hZ2VJXS9Gb250PDwvRjAgOSAwIFIvRjEgMTAgMCBSL0YyIDExIDAgUj4+Pj4NCmVuZG9iag0KMzEgMCBvYmoNCjw8L0ZpbHRlci9GbGF0ZURlY29kZS9MZW5ndGggMzMgMCBSPj4NCnN0cmVhbQ0KWIXFWllvHMcRboCPMQKJpmxJtoF5YHiJHvV9GHkKeKwowuJN2WSekhiGIRlwXvL381XN2bMzO2QsOFwsd6a3qrq6uo6veva3QhUSr2/pIyRd/ONj8berblDrMlhbOFUqH60vrj4Wr49kkYqrn4odcb8rnNBC7hZXvxSHV0NOH3SRQhmcto44d8SWuBDn4lYciCP8XxMKV2diIb5ZIUErU8YYawlGvGUZEzzRltZGqWjepFxMlcaq0XhPvMOUN+IEQn6EAp7FXa6YXilVWuVI0N2OCOJ+R7ymf168EvvC7BYqltJ7qyB9DV/tC4k3023v/v3qZEqstmUMKVWreiZe1NY4h3IL/CfVbsU1rhdsqWfiifhilZreNWqOLHMP/J/j8yWU9qtsLWVpTCMlQo9TzL4Qx+AtcX0OiceQeTYmw9ky6Yj9sqVsNfmz+BIvmvkrsYH3mvgCmnyNK7waKbJ0xX8KXZwUOvnS28LqUtkIx/sIleB63cCH4rIecg6UNU3F1Y4QkZEKUnuCXJT9AaIZDDU0GntjZKxo+is0XiFISiyuXt3nFAKvsCRa5Jb4K7bwO/KJZeMYacoUPLFLo5ciifzwVFxyMJzzhu+L7c7FjZJl1LaIsQzgtgW2y9vkHb4pfSz+/a/iJ1zCpWD9jkphM7WNJqeKZVQIjCGVzqg03CkqMyNLp9KGGDsqbD2sZ0NGZaCXMWFJe59RWdpV42dmtK50KvoZWU6XWs6JchSBMs2I8nAjF+cM4W2ptZmlSqULMPTqGQPiSEY1IysEyDJ6yfQpo0I+1F7OmStCryTdzIzJlG5kr/MJUyyT1TNGtRJqBR1XT2hlBJU0q2e0KA9eOz0jC16fqC6spqLAN07NaK8j8boZvQz0imE5ZnNZJuDaLkdjrpc1yBppzl6IjSDtzA5ZZ1DS00w0Woe6bYOakeVNqaSes6qPJeTNTBg0iKydmRBeH2Wao4pQy9uZOLMxgEqFGVlJI+H4mVwC2aCyM47jUJKinfEIB693Rs0s0TEo8jO5HoojeamZGatK2SunVRXMqulIXa5GJmtlhSgQcUiN8EpGgASgdoukypA8MskOMMpdXerWCTDto36uiwRMhRBL0muQbO4WSIhaxeAKZs/wlgIYeYo6WQOtAVho0EOm5BIwqAami35duQlgJc+VG+v4bpcMpALyOa/j/l4cooK/w4u0eo9Kfohaft3plsnEkhxJ9DWU6EHU1ZjivPit08gjGrDHtGUQGJTuhj50Q4qClIdaxm7o5+J2r/h1pgswMjGfQrayUtUaI74qjbexfkKJ34i1UehjqBrrIbtq2An8rotvATdp9wmoPhPPxzFUrYb1JbL0UI19IKcf4A+naC4WtW9MqdRIwh6aWiPqLfQD2ajcVwpULt3zUNrzM0DvNYh5wzD+AD5B+vyJNTzC+G1N9RlPNOYfzUTBwHSNfg5shOovuD94g89rfCJu7oAc6eZ2UnHCARJwsS+wtwVebHJX0/eyZZfowfQ8rDjONMAIYYSE6t7mjBBtRoa2TCPyTUJSi8gJTUBan9EZ9CHUd2byKC0N6GgISS+nGwtebeAyEdCrB7vvaN0a694mo/XSSp5kNGcoRVGpsQVymJHwpRZqqtXDzCgzbfpru8Ze8lg5eZ7ZMlMu59+ayCoCag2R9UjC7VhjcGxWj47saPQUXW7vii7PqM1u1bs6sTFLu9/4DTDe7A6a6BFz/mHHAAbgC66nmMtEM8yxXVf6HK+XuHrOIy/Qlb5Y1b6hNwZM6drsKo6pbUcBoBCHl1C7TOMHXAsoaC9RDw5xR5nps5Xije6Jl2A7Z6a3EPQVEiO9v1wlQKO4JvQrlYANZqBTiQWdcuD9Drrd8MECJZIbsVgpLBBwc74StglyalJvWBs6qzjB+3qlAOTJSEAsb3YfdQpErZWhLILPlJQf7OT/opUjt64OlHq5YBqZ/A5Akp2PJIqmT+WRnFwMUHNKWn9id6xk9wKut3kzkVexohNp1Oqt8RH+XImRBLnQXvweZ4YkR6dSFBipqaSP8BpUTmM5FJwOj2evagAFkpRDUz76NLTvun+Ex9KcUlK6R6PnKTvz8u93uBLu95hHFAYSTUB9BlAbaT+pocdvjDGhv7PcZ3Qs5HJbE6eWTpY++T45zPKSRPcWvAEsvSG+hvPwaxRvmcg9QX/WPRT1kTnpjIA7qJx6g4U/5QnGuKjkoeN8HJeSoXTDmRDSFLp3FfSD2+FVnczesAzilKV01oPhn7AHhcgFXOx78WRomU90l3dfNhIaaFCAUehw2rEOpdCJjLINCKj5UuqdzFacHVkmraVkqIr4lshWmqkQEr65/9DcG8pIYMIIqHt3kw0QMI3jQb5oMI4HMne2+t7TXwAkJmBMbwBXwteoVnT3ob1TdFgXMUDD7c3Pf5z2lYXndEeF9bbVvb77P+iehbjhhIA2udSUsfIMuokKcMzPKE45l1Y1jvLqWXuUfjORTw114Ir8UtYVZhscR/zk5Jo72tO60/Kco6lpa2ROSSRVvZFl0sEN0h1ly7dciBcovlyej/iW5nlTDdyC4oBLwS3TrnFgV43eWaZS9f+2rkIVXb/3rUapNL7ne4IExyPpAYodsfhrXvttQ9pT4aiuUo01O4of2N7VBFWz2yl0s/RA47Tmrb5tLDqh1AFsdIEJFuLpqKljEZCyZZRDj2gepFySbUdzalQZb3t8MfpICwWGk73H5hofhuhzJn87j6CRgXzCAwgH3zw1muZoJ8SFaTkePA/q9MPmaTkQ0eZxHEk+ci1B2tVr6Q4WqqPHIBGW1GY2h3PtwLA7dAYpTdsiAKp0U+yJv0w8hQuEAqXm/dQ295675SOk1xxYi+UWvYe7LtiX300d9IFNAgSRB/QzDUUDRdZ7jo51xuWHzTnauOpIWB4IlDyjVn1EY8/Y/sljdKQnKCogrZP3hFYycMZ1tuwFJjlBeN1OiJHUi0T2KN2udJ+faL/njHrOOo6ujsq8A9xh7+rspOssdD1hExcBh9FUkYd1Nhlf+9rQVtkhzCYyVbMb4ztpYXaF/ESuNj9X7wh4gLerTGkY9X/PrcOCa9SYSbHVyefePYegLf3iQsKSPT37Lr7FmzHcWdoalKDxlSc6v0UXH1C8w9zKM8H5KfmcAzWrxTTRqGEBpZzxnH+HsNd1A/VPARKFhO1jxGaohYirUYYnlAlJlKe11qExmpYjZ8vjyY6OhLFMSJBayuGZh6l3eq3btQeoFWBJdEPAbUrZYfvY/DzjZqKR0pZ+X9JnJp718Z/rUKthbDWXds2vbbbZN4+4w7jM4Mcb/lXJBV7Ug6/z+q7rLvZiomijedUDfV4x2xm2toJtxxMnUiZW54459xYmDnjr8ZSC6bQ1fZ67zmq5o6ZBK82wZtRJ0fjIXJG7kSPc2chYOWFeD9mfDQCwCb12qR0YtEu+VE72jlZjN9Y1X0vS2jYrk9YjW27IlksxKhwKLD+3t9a3iSfCoaaO2BYMB8l5TgEF6+Wf/xfZtg5RDQplbmRzdHJlYW0NCmVuZG9iag0KMzMgMCBvYmoNCjI2MzQNCmVuZG9iag0KNCAwIG9iag0KPDwvVHlwZS9QYWdlL0NvbnRlbnRzIDM0IDAgUi9SZXNvdXJjZXMgMzUgMCBSL1BhcmVudCAzIDAgUj4+DQplbmRvYmoNCjM1IDAgb2JqDQo8PC9Qcm9jU2V0Wy9QREYvVGV4dC9JbWFnZUIvSW1hZ2VDL0ltYWdlSV0vRm9udDw8L0YwIDkgMCBSL0YxIDEwIDAgUi9GMiAxMSAwIFI+Pj4+DQplbmRvYmoNCjM0IDAgb2JqDQo8PC9GaWx0ZXIvRmxhdGVEZWNvZGUvTGVuZ3RoIDM2IDAgUj4+DQpzdHJlYW0NCliFxVpZbxzHEW6AjzECiaZsSbaBeWB4iR71fRh5CnisKMLiTdlknpIYhiEZcF7y9/NVzdmzMztkLDhcLHemt6q6urqOr3r2t0IVEq9v6SMkXfzjY/G3q25Q6zJYWzhVKh+tL64+Fq+PZJGKq5+KHXG/K5zQQu4WV78Uh1dDTh90kUIZnLaOOHfElrgQ5+JWHIgj/F8TCldnYiG+WSFBK1PGGGsJRrxlGRM80ZbWRqlo3qRcTJXGqtF4T7zDlDfiBEJ+hAKexV2umF4pVVrlSNDdjgjifke8pn9evBL7wuwWKpbSe6sgfQ1f7QuJN9Nt7/796mRKrLZlDClVq3omXtTWOIdyC/wn1W7FNa4XbKln4on4YpWa3jVqjixzD/yf4/MllParbC1laUwjJUKPU8y+EMfgLXF9DonHkHk2JsPZMumI/bKlbDX5s/gSL5r5K7GB95r4App8jSu8GimydMV/Cl2cFDr50tvC6lLZCMf7CJXget3Ah+KyHnIOlDVNxdWOEJGRClJ7glyU/QGiGQw1NBp7Y2SsaPorNF4hSEosrl7d5xQCr7AkWuSW+Cu28DvyiWXjGGnKFDyxS6OXIon88FRccjCc84bvi+3OxY2SZdS2iLEM4LYFtsvb5B2+KX0s/v2v4idcwqVg/Y5KYTO1jSanimVUCIwhlc6oNNwpKjMjS6fShhg7Kmw9rGdDRmWglzFhSXufUVnaVeNnZrSudCr6GVlOl1rOiXIUgTLNiPJwIxfnDOFtqbWZpUqlCzD06hkD4khGNSMrBMgyesn0KaNCPtRezpkrQq8k3cyMyZRuZK/zCVMsk9UzRrUSagUdV09oZQSVNKtntCgPXjs9Iwten6gurKaiwDdOzWivI/G6Gb0M9IphOWZzWSbg2i5HY66XNcgaac5eiI0g7cwOWWdQ0tNMNFqHum2DmpHlTamknrOqjyXkzUwYNIisnZkQXh9lmqOKUMvbmTizMYBKhRlZSSPh+JlcAtmgsjOO41CSop3xCAevd0bNLNExKPIzuR6KI3mpmRmrStkrp1UVzKrpSF2uRiZrZYUoEHFIjfBKRoAEoHaLpMqQPDLJDjDKXV3q1gkw7aN+rosETIUQS9JrkGzuFkiIWsXgCmbP8JYCGHmKOlkDrQFYaNBDpuQSMKgGpot+XbkJYCXPlRvr+G6XDKQC8jmv4/5eHKKCv8OLtHqPSn6IWn7d6ZbJxJIcSfQ1lOhB1NWY4rz4rdPIIxqwx7RlEBiU7oY+dEOKgpSHWsZu6Ofidq/4daYLMDIxn0K2slLVGiO+Ko23sX5Cid+ItVHoY6ga6yG7atgJ/K6LbwE3afcJqD4Tz8cxVK2G9SWy9FCNfSCnH+APp2guFrVvTKnUSMIemloj6i30A9mo3FcKVC7d81Da8zNA7zWIecMw/gA+Qfr8iTU8wvhtTfUZTzTmH81EwcB0jX4ObITqL7g/eIPPa3wibu6AHOnmdlJxwgEScLEvsLcFXmxyV9P3smWX6MH0PKw4zjTACGGEhOre5owQbUaGtkwj8k1CUovICU1AWp/RGfQh1Hdm8igtDehoCEkvpxsLXm3gMhHQqwe772jdGuveJqP10kqeZDRnKEVRqbEFcpiR8KUWaqrVw8woM236a7vGXvJYOXme2TJTLuffmsgqAmoNkfVIwu1YY3BsVo+O7Gj0FF1u74ouz6jNbtW7OrExS7vf+A0w3uwOmugRc/5hxwAG4Auup5jLRDPMsV1X+hyvl7h6ziMv0JW+WNW+oTcGTOna7CqOqW1HAaAQh5dQu0zjB1wLKGgvUQ8OcUeZ6bOV4o3uiZdgO2emtxD0FRIjvb9cJUCjuCb0K5WADWagU4kFnXLg/Q663fDBAiWSG7FYKSwQcHO+ErYJcmpSb1gbOqs4wft6pQDkyUhALG92H3UKRK2VoSyCz5SUH+zk/6KVI7euDpR6uWAamfwOQJKdjySKpk/lkZxcDFBzSlp/YnesZPcCrrd5M5FXsaITadTqrfER/lyJkQS50F78HmeGJEenUhQYqamkj/AaVE5jORScDo9nr2oABZKUQ1M++jS077p/hMfSnFJSukej5yk78/Lvd7gS7veYRxQGEk1AfQZQG2k/qaHHb4wxob+z3Gd0LORyWxOnlk6WPvk+OczykkT3FrwBLL0hvobz8GsUb5nIPUF/1j0U9ZE56YyAO6iceoOFP+UJxrio5KHjfByXkqF0w5kQ0hS6dxX0g9vhVZ3M3rAM4pSldNaD4Z+wB4XIBVzse/FkaJlPdJd3XzYSGmhQgFHocNqxDqXQiYyyDQio+VLqncxWnB1ZJq2lZKiK+JbIVpqpEBK+uf/Q3BvKSGDCCKh7d5MNEDCN40G+aDCOBzJ3tvre018AJCZgTG8AV8LXqFZ096G9U3RYFzFAw+3Nz3+c9pWF53RHhfW21b2++z/onoW44YSANrnUlLHyDLqJCnDMzyhOOZdWNY7y6ll7lH4zkU8NdeCK/FLWFWYbHEf85OSaO9rTutPynKOpaWtkTkkkVb2RZdLBDdIdZcu3XIgXKL5cno/4luZ5Uw3cguKAS8Et065xYFeN3lmmUvX/tq5CFV2/961GqTS+53uCBMcj6QGKHbH4a177bUPaU+GorlKNNTuKH9je1QRVs9spdLP0QOO05q2+bSw6odQBbHSBCRbi6aipYxGQsmWUQ49oHqRckm1Hc2pUGW97fDH6SAsFhpO9x+YaH4bocyZ/O4+gkYF8wgMIB988NZrmaCfEhWk5HjwP6vTD5mk5ENHmcRxJPnItQdrVa+kOFqqjxyARltRmNodz7cCwO3QGKU3bIgCqdFPsib9MPIULhAKl5v3UNveeu+UjpNccWIvlFr2Huy7Yl99NHfSBTQIEkQf0Mw1FA0XWe46Odcblh8052rjqSFgeCJQ8o1Z9RGPP2P7JY3SkJygqIK2T94RWMnDGdbbsBSY5QXjdToiR1ItE9ijdrnSfn2i/54x6zjqOro7KvAPcYe/q7KTrLHQ9YRMXAYfRVJGHdTYZX/va0FbZIcwmMlWzG+M7aWF2hfxErjY/V+8IeIC3q0xpGPV/z63DgmvUmEmx1cnn3j2HoC394kLCkj09+y6+xZsx3FnaGpSg8ZUnOr9FFx9QvMPcyjPB+Sn5nAM1q8U00ahhAaWc8Zx/h7DXdQP1TwEShYTtY8RmqIWIq1GGJ5QJSZSntdahMZqWI2fL48mOjoSxTEiQWsrhmYepd3qt27UHqBVgSXRDwG1K2WH72Pw842aikdKWfl/SZyae9fGf61CrYWw1l3bNr2222TePuMO4zODHG/5VyQVe1IOv8/qu6y72YqJoo3nVA31eMdsZtraCbccTJ1ImVueOOfcWJg546/GUgum0NX2eu85quaOmQSvNsGbUSdH4yFyRu5Ej3NnIWDlhXg/Znw0AsAm9dqkdGLRLvlRO9o5WYzfWNV9L0to2K5PWI1tuyJZLMSocCiw/t7fWt4knwqGmjtgWDAfJeU4BBevln/8X2bYOUQ0KZW5kc3RyZWFtDQplbmRvYmoNCjM2IDAgb2JqDQoyNjM0DQplbmRvYmoNCjM3IDAgb2JqDQo8PC9NZXRhZGF0YSAyIDAgUi9UeXBlL0NhdGFsb2cvUGFnZXMgMyAwIFIvVmVyc2lvbi8xLjQvTWFya0luZm88PC9NYXJrZWQgZmFsc2U+Pj4+DQplbmRvYmoNCnhyZWYNCjAgMzgNCjAwMDAwMDAwMDAgNjU1MzUgZg0KMDAwMDAwMDAxNyAwMDAwMCBuDQowMDAwMDAwMDkzIDAwMDAwIG4NCjAwMDAwMDExOTIgMDAwMDAgbg0KMDAwMDA1Nzg3NiAwMDAwMCBuDQowMDAwMDU0OTU5IDAwMDAwIG4NCjAwMDAwMDEyODAgMDAwMDAgbg0KMDAwMDA1MjIyNCAwMDAwMCBuDQowMDAwMDAxMzU3IDAwMDAwIG4NCjAwMDAwMzQ3MTggMDAwMDAgbg0KMDAwMDAxNTYwOCAwMDAwMCBuDQowMDAwMDAxNDU4IDAwMDAwIG4NCjAwMDAwMDIyMTkgMDAwMDAgbg0KMDAwMDAwMTYwMyAwMDAwMCBuDQowMDAwMDAyMTk2IDAwMDAwIG4NCjAwMDAwMDI2MDEgMDAwMDAgbg0KMDAwMDAwMjgyMSAwMDAwMCBuDQowMDAwMDE1NTgzIDAwMDAwIG4NCjAwMDAwMTY0OTcgMDAwMDAgbg0KMDAwMDAxNTc0OCAwMDAwMCBuDQowMDAwMDE2NDc0IDAwMDAwIG4NCjAwMDAwMTY5ODkgMDAwMDAgbg0KMDAwMDAxNzIwMiAwMDAwMCBuDQowMDAwMDM0NjkzIDAwMDAwIG4NCjAwMDAwMzU1NTMgMDAwMDAgbg0KMDAwMDAzNDg2MyAwMDAwMCBuDQowMDAwMDM1NTMwIDAwMDAwIG4NCjAwMDAwMzU5OTMgMDAwMDAgbg0KMDAwMDAzNjIxNCAwMDAwMCBuDQowMDAwMDUyMTk5IDAwMDAwIG4NCjAwMDAwNTQ5MzUgMDAwMDAgbg0KMDAwMDA1NTE0MCAwMDAwMCBuDQowMDAwMDU1MDM4IDAwMDAwIG4NCjAwMDAwNTc4NTIgMDAwMDAgbg0KMDAwMDA1ODA1NyAwMDAwMCBuDQowMDAwMDU3OTU1IDAwMDAwIG4NCjAwMDAwNjA3NjkgMDAwMDAgbg0KMDAwMDA2MDc5MyAwMDAwMCBuDQp0cmFpbGVyDQo8PC9TaXplIDM4L1Jvb3QgMzcgMCBSL0luZm8gMSAwIFIvSURbPDhDNzdGM0Q5N0UwNkRENDU4RjNBRkM5NTIyNTVDRjQ3Pjw4Qzc3RjNEOTdFMDZERDQ1OEYzQUZDOTUyMjU1Q0Y0Nz5dPj4NCnN0YXJ0eHJlZg0KNjA4OTUNCiUlRU9GDQo="
        },
        "FormGroupId": "2025-06-26-06.04.21.610820"
      }
    }
  }
}"""
