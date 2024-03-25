import re
import unittest
import logging
from unittest.mock import patch, ANY
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from karrio import Shipment
from .fixture import gateway

logger = logging.getLogger(__name__)


class TestFedExShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)
        self.ShipmentCancelRequest = ShipmentCancelRequest(**shipment_cancel_data)
        self.MultiPieceShipmentRequest = ShipmentRequest(**multi_piece_shipment_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        # Remove timeStamp for testing
        serialized_request = re.sub(
            "<v26:ShipTimestamp>[^>]+</v26:ShipTimestamp>",
            "",
            request.serialize()[0].replace(
                "                <v26:ShipTimestamp>", "<v26:ShipTimestamp>"
            ),
        )

        self.assertEqual(serialized_request, ShipmentRequestXml)

    def test_create_multi_piece_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.MultiPieceShipmentRequest)
        # Remove timeStamp for testing
        [master_request, second_shipment_request] = [
            re.sub(
                "<v26:ShipTimestamp>[^>]+</v26:ShipTimestamp>",
                "",
                request.replace(
                    "                <v26:ShipTimestamp>", "<v26:ShipTimestamp>"
                ),
            )
            for request in request.serialize()
        ]

        self.assertEqual(master_request, MasterShipmentRequestXml)
        self.assertEqual(second_shipment_request, SecondPieceShipmentRequestXml)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequestXML)

    @patch("karrio.mappers.fedex_ws.proxy.lib.request", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        Shipment.create(self.ShipmentRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/ship")

    @patch("karrio.mappers.fedex_ws.proxy.lib.request", return_value="<a></a>")
    def test_cancel_shipment(self, http_mock):
        Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/ship")

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = (
                Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_multi_piece_shipment_response(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mocks:
            mocks.side_effect = [ShipmentResponseXML, ShipmentResponseXML]
            parsed_response = (
                Shipment.create(self.MultiPieceShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response),
                ParsedMultiPieceShipmentResponse,
            )

    def test_parse_shipment_cancel_response(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = (
                Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedShipmentCancelResponse)
            )


if __name__ == "__main__":
    unittest.main()

shipment_data = {
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

multi_piece_shipment_data = {
    **shipment_data,
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

shipment_cancel_data = {
    "shipment_identifier": "794947717776",
    "service": "express",
}

ParsedShipmentResponse = [
    {
        "carrier_name": "fedex_ws",
        "carrier_id": "carrier_id",
        "tracking_number": "794604790138",
        "shipment_identifier": "794604790138",
        "meta": {
            "tracking_numbers": ["794604790138"],
            "carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=794604790138",
        },
        "docs": {"label": ANY, "invoice": ANY},
    },
    [],
]

ParsedMultiPieceShipmentResponse = [
    {
        "carrier_name": "fedex_ws",
        "carrier_id": "carrier_id",
        "tracking_number": "794604790138",
        "shipment_identifier": "794604790138",
        "meta": {
            "tracking_numbers": ["794604790138", "794604790138"],
            "carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=794604790138",
        },
        "docs": {"label": ANY, "invoice": ANY},
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "fedex_ws",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequestXml = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v26="http://fedex.com/ws/ship/v26">
    <tns:Body>
        <v26:ProcessShipmentRequest>
            <v26:WebAuthenticationDetail>
                <v26:UserCredential>
                    <v26:Key>user_key</v26:Key>
                    <v26:Password>password</v26:Password>
                </v26:UserCredential>
            </v26:WebAuthenticationDetail>
            <v26:ClientDetail>
                <v26:AccountNumber>2349857</v26:AccountNumber>
                <v26:MeterNumber>1293587</v26:MeterNumber>
            </v26:ClientDetail>
            <v26:TransactionDetail>
                <v26:CustomerTransactionId>IE_v26_Ship</v26:CustomerTransactionId>
            </v26:TransactionDetail>
            <v26:Version>
                <v26:ServiceId>ship</v26:ServiceId>
                <v26:Major>26</v26:Major>
                <v26:Intermediate>0</v26:Intermediate>
                <v26:Minor>0</v26:Minor>
            </v26:Version>
            <v26:RequestedShipment>

                <v26:DropoffType>REGULAR_PICKUP</v26:DropoffType>
                <v26:ServiceType>INTERNATIONAL_PRIORITY</v26:ServiceType>
                <v26:PackagingType>YOUR_PACKAGING</v26:PackagingType>
                <v26:TotalWeight>
                    <v26:Units>LB</v26:Units>
                    <v26:Value>20</v26:Value>
                </v26:TotalWeight>
                <v26:PreferredCurrency>USD</v26:PreferredCurrency>
                <v26:Shipper>
                    <v26:AccountNumber>2349857</v26:AccountNumber>
                    <v26:Contact>
                        <v26:PersonName>Input Your Information</v26:PersonName>
                        <v26:CompanyName>Input Your Information</v26:CompanyName>
                        <v26:PhoneNumber>Input Your Information</v26:PhoneNumber>
                        <v26:EMailAddress>Input Your Information</v26:EMailAddress>
                    </v26:Contact>
                    <v26:Address>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:City>MEMPHIS</v26:City>
                        <v26:StateOrProvinceCode>TN</v26:StateOrProvinceCode>
                        <v26:PostalCode>38117</v26:PostalCode>
                        <v26:CountryCode>US</v26:CountryCode>
                        <v26:CountryName>United States</v26:CountryName>
                        <v26:Residential>false</v26:Residential>
                    </v26:Address>
                </v26:Shipper>
                <v26:Recipient>
                    <v26:Contact>
                        <v26:PersonName>Input Your Information</v26:PersonName>
                        <v26:CompanyName>Input Your Information</v26:CompanyName>
                        <v26:PhoneNumber>Input Your Information</v26:PhoneNumber>
                        <v26:EMailAddress>Input Your Information</v26:EMailAddress>
                    </v26:Contact>
                    <v26:Address>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:City>RICHMOND</v26:City>
                        <v26:StateOrProvinceCode>BC</v26:StateOrProvinceCode>
                        <v26:PostalCode>V7C4v7</v26:PostalCode>
                        <v26:CountryCode>CA</v26:CountryCode>
                        <v26:CountryName>Canada</v26:CountryName>
                        <v26:Residential>false</v26:Residential>
                    </v26:Address>
                </v26:Recipient>
                <v26:ShippingChargesPayment>
                    <v26:PaymentType>THIRD_PARTY</v26:PaymentType>
                    <v26:Payor>
                        <v26:ResponsibleParty>
                            <v26:AccountNumber>2349857</v26:AccountNumber>
                        </v26:ResponsibleParty>
                    </v26:Payor>
                </v26:ShippingChargesPayment>
                <v26:SpecialServicesRequested>
                    <v26:EventNotificationDetail>
                        <v26:EventNotifications>
                            <v26:Events>ON_DELIVERY</v26:Events>
                            <v26:Events>ON_ESTIMATED_DELIVERY</v26:Events>
                            <v26:Events>ON_EXCEPTION</v26:Events>
                            <v26:Events>ON_SHIPMENT</v26:Events>
                            <v26:Events>ON_TENDER</v26:Events>
                            <v26:NotificationDetail>
                                <v26:NotificationType>EMAIL</v26:NotificationType>
                                <v26:EmailDetail>
                                    <v26:EmailAddress>Input Your Information</v26:EmailAddress>
                                    <v26:Name>Input Your Information</v26:Name>
                                </v26:EmailDetail>
                                <v26:Localization>
                                    <v26:LanguageCode>EN</v26:LanguageCode>
                                </v26:Localization>
                            </v26:NotificationDetail>
                            <v26:FormatSpecification>
                                <v26:Type>HTML</v26:Type>
                            </v26:FormatSpecification>
                        </v26:EventNotifications>
                    </v26:EventNotificationDetail>
                </v26:SpecialServicesRequested>
                <v26:CustomsClearanceDetail>
                    <v26:DutiesPayment>
                        <v26:PaymentType>SENDER</v26:PaymentType>
                        <v26:Payor>
                            <v26:ResponsibleParty>
                                <v26:AccountNumber>2349857</v26:AccountNumber>
                            </v26:ResponsibleParty>
                        </v26:Payor>
                    </v26:DutiesPayment>
                    <v26:CustomsValue>
                        <v26:Currency>USD</v26:Currency>
                        <v26:Amount>100</v26:Amount>
                    </v26:CustomsValue>
                    <v26:CommercialInvoice>
                        <v26:CustomerReferences>
                            <v26:CustomerReferenceType>INVOICE_NUMBER</v26:CustomerReferenceType>
                            <v26:Value>123456789</v26:Value>
                        </v26:CustomerReferences>
                        <v26:OriginatorName>Input Your Information</v26:OriginatorName>
                        <v26:TermsOfSale>DDU</v26:TermsOfSale>
                    </v26:CommercialInvoice>
                    <v26:Commodities>
                        <v26:NumberOfPieces>1</v26:NumberOfPieces>
                        <v26:Description>test</v26:Description>
                        <v26:CountryOfManufacture>US</v26:CountryOfManufacture>
                        <v26:HarmonizedCode>00339BB</v26:HarmonizedCode>
                        <v26:Weight>
                            <v26:Units>LB</v26:Units>
                            <v26:Value>10</v26:Value>
                        </v26:Weight>
                        <v26:Quantity>1</v26:Quantity>
                        <v26:QuantityUnits>EA</v26:QuantityUnits>
                        <v26:UnitPrice>
                            <v26:Currency>USD</v26:Currency>
                        </v26:UnitPrice>
                    </v26:Commodities>
                </v26:CustomsClearanceDetail>
                <v26:LabelSpecification>
                    <v26:LabelFormatType>COMMON2D</v26:LabelFormatType>
                    <v26:ImageType>PDF</v26:ImageType>
                    <v26:LabelStockType>STOCK_4X6</v26:LabelStockType>
                    <v26:LabelPrintingOrientation>TOP_EDGE_OF_TEXT_FIRST</v26:LabelPrintingOrientation>
                    <v26:LabelOrder>SHIPPING_LABEL_FIRST</v26:LabelOrder>
                </v26:LabelSpecification>
                <v26:ShippingDocumentSpecification>
                    <v26:ShippingDocumentTypes>COMMERCIAL_INVOICE</v26:ShippingDocumentTypes>
                    <v26:CommercialInvoiceDetail>
                        <v26:Format>
                            <v26:ImageType>PDF</v26:ImageType>
                            <v26:StockType>PAPER_LETTER</v26:StockType>
                        </v26:Format>
                    </v26:CommercialInvoiceDetail>
                </v26:ShippingDocumentSpecification>
                <v26:PackageCount>1</v26:PackageCount>
                <v26:RequestedPackageLineItems>
                    <v26:SequenceNumber>1</v26:SequenceNumber>
                    <v26:Weight>
                        <v26:Units>LB</v26:Units>
                        <v26:Value>20</v26:Value>
                    </v26:Weight>
                    <v26:Dimensions>
                        <v26:Length>12</v26:Length>
                        <v26:Width>12</v26:Width>
                        <v26:Height>12</v26:Height>
                        <v26:Units>IN</v26:Units>
                    </v26:Dimensions>
                    <v26:CustomerReferences>
                        <v26:CustomerReferenceType>CUSTOMER_REFERENCE</v26:CustomerReferenceType>
                        <v26:Value>#Order 11111</v26:Value>
                    </v26:CustomerReferences>
                    <v26:SpecialServicesRequested>
                        <v26:SpecialServiceTypes>SIGNATURE_OPTION</v26:SpecialServiceTypes>
                        <v26:SignatureOptionDetail>
                            <v26:OptionType>SERVICE_DEFAULT</v26:OptionType>
                        </v26:SignatureOptionDetail>
                    </v26:SpecialServicesRequested>
                </v26:RequestedPackageLineItems>
            </v26:RequestedShipment>
        </v26:ProcessShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""

MasterShipmentRequestXml = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v26="http://fedex.com/ws/ship/v26">
    <tns:Body>
        <v26:ProcessShipmentRequest>
            <v26:WebAuthenticationDetail>
                <v26:UserCredential>
                    <v26:Key>user_key</v26:Key>
                    <v26:Password>password</v26:Password>
                </v26:UserCredential>
            </v26:WebAuthenticationDetail>
            <v26:ClientDetail>
                <v26:AccountNumber>2349857</v26:AccountNumber>
                <v26:MeterNumber>1293587</v26:MeterNumber>
            </v26:ClientDetail>
            <v26:TransactionDetail>
                <v26:CustomerTransactionId>IE_v26_Ship</v26:CustomerTransactionId>
            </v26:TransactionDetail>
            <v26:Version>
                <v26:ServiceId>ship</v26:ServiceId>
                <v26:Major>26</v26:Major>
                <v26:Intermediate>0</v26:Intermediate>
                <v26:Minor>0</v26:Minor>
            </v26:Version>
            <v26:RequestedShipment>

                <v26:DropoffType>REGULAR_PICKUP</v26:DropoffType>
                <v26:ServiceType>INTERNATIONAL_PRIORITY</v26:ServiceType>
                <v26:PackagingType>YOUR_PACKAGING</v26:PackagingType>
                <v26:TotalWeight>
                    <v26:Units>LB</v26:Units>
                    <v26:Value>3</v26:Value>
                </v26:TotalWeight>
                <v26:PreferredCurrency>USD</v26:PreferredCurrency>
                <v26:Shipper>
                    <v26:AccountNumber>2349857</v26:AccountNumber>
                    <v26:Contact>
                        <v26:PersonName>Input Your Information</v26:PersonName>
                        <v26:CompanyName>Input Your Information</v26:CompanyName>
                        <v26:PhoneNumber>Input Your Information</v26:PhoneNumber>
                        <v26:EMailAddress>Input Your Information</v26:EMailAddress>
                    </v26:Contact>
                    <v26:Address>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:City>MEMPHIS</v26:City>
                        <v26:StateOrProvinceCode>TN</v26:StateOrProvinceCode>
                        <v26:PostalCode>38117</v26:PostalCode>
                        <v26:CountryCode>US</v26:CountryCode>
                        <v26:CountryName>United States</v26:CountryName>
                        <v26:Residential>false</v26:Residential>
                    </v26:Address>
                </v26:Shipper>
                <v26:Recipient>
                    <v26:Contact>
                        <v26:PersonName>Input Your Information</v26:PersonName>
                        <v26:CompanyName>Input Your Information</v26:CompanyName>
                        <v26:PhoneNumber>Input Your Information</v26:PhoneNumber>
                        <v26:EMailAddress>Input Your Information</v26:EMailAddress>
                    </v26:Contact>
                    <v26:Address>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:City>RICHMOND</v26:City>
                        <v26:StateOrProvinceCode>BC</v26:StateOrProvinceCode>
                        <v26:PostalCode>V7C4v7</v26:PostalCode>
                        <v26:CountryCode>CA</v26:CountryCode>
                        <v26:CountryName>Canada</v26:CountryName>
                        <v26:Residential>false</v26:Residential>
                    </v26:Address>
                </v26:Recipient>
                <v26:ShippingChargesPayment>
                    <v26:PaymentType>THIRD_PARTY</v26:PaymentType>
                    <v26:Payor>
                        <v26:ResponsibleParty>
                            <v26:AccountNumber>2349857</v26:AccountNumber>
                        </v26:ResponsibleParty>
                    </v26:Payor>
                </v26:ShippingChargesPayment>
                <v26:SpecialServicesRequested>
                    <v26:SpecialServiceTypes>ELECTRONIC_TRADE_DOCUMENTS</v26:SpecialServiceTypes>
                    <v26:EventNotificationDetail>
                        <v26:EventNotifications>
                            <v26:Events>ON_DELIVERY</v26:Events>
                            <v26:Events>ON_ESTIMATED_DELIVERY</v26:Events>
                            <v26:Events>ON_EXCEPTION</v26:Events>
                            <v26:Events>ON_SHIPMENT</v26:Events>
                            <v26:Events>ON_TENDER</v26:Events>
                            <v26:NotificationDetail>
                                <v26:NotificationType>EMAIL</v26:NotificationType>
                                <v26:EmailDetail>
                                    <v26:EmailAddress>Input Your Information</v26:EmailAddress>
                                    <v26:Name>Input Your Information</v26:Name>
                                </v26:EmailDetail>
                                <v26:Localization>
                                    <v26:LanguageCode>EN</v26:LanguageCode>
                                </v26:Localization>
                            </v26:NotificationDetail>
                            <v26:FormatSpecification>
                                <v26:Type>HTML</v26:Type>
                            </v26:FormatSpecification>
                        </v26:EventNotifications>
                    </v26:EventNotificationDetail>
                    <v26:EtdDetail>
                        <v26:Confirmation>CONFIRMED</v26:Confirmation>
                        <v26:Attributes>POST_SHIPMENT_UPLOAD_REQUESTED</v26:Attributes>
                    </v26:EtdDetail>
                </v26:SpecialServicesRequested>
                <v26:CustomsClearanceDetail>
                    <v26:DutiesPayment>
                        <v26:PaymentType>SENDER</v26:PaymentType>
                        <v26:Payor>
                            <v26:ResponsibleParty>
                                <v26:AccountNumber>2349857</v26:AccountNumber>
                            </v26:ResponsibleParty>
                        </v26:Payor>
                    </v26:DutiesPayment>
                    <v26:CustomsValue>
                        <v26:Currency>USD</v26:Currency>
                        <v26:Amount>100</v26:Amount>
                    </v26:CustomsValue>
                    <v26:Commodities>
                        <v26:NumberOfPieces>1</v26:NumberOfPieces>
                        <v26:Description>test</v26:Description>
                        <v26:CountryOfManufacture>US</v26:CountryOfManufacture>
                        <v26:HarmonizedCode>00339BB</v26:HarmonizedCode>
                        <v26:Weight>
                            <v26:Units>LB</v26:Units>
                            <v26:Value>10</v26:Value>
                        </v26:Weight>
                        <v26:Quantity>1</v26:Quantity>
                        <v26:QuantityUnits>EA</v26:QuantityUnits>
                        <v26:UnitPrice>
                            <v26:Currency>USD</v26:Currency>
                        </v26:UnitPrice>
                    </v26:Commodities>
                </v26:CustomsClearanceDetail>
                <v26:LabelSpecification>
                    <v26:LabelFormatType>COMMON2D</v26:LabelFormatType>
                    <v26:ImageType>PDF</v26:ImageType>
                    <v26:LabelStockType>STOCK_4X6</v26:LabelStockType>
                    <v26:LabelPrintingOrientation>TOP_EDGE_OF_TEXT_FIRST</v26:LabelPrintingOrientation>
                    <v26:LabelOrder>SHIPPING_LABEL_FIRST</v26:LabelOrder>
                </v26:LabelSpecification>
                <v26:PackageCount>2</v26:PackageCount>
                <v26:RequestedPackageLineItems>
                    <v26:SequenceNumber>1</v26:SequenceNumber>
                    <v26:Weight>
                        <v26:Units>LB</v26:Units>
                        <v26:Value>1</v26:Value>
                    </v26:Weight>
                    <v26:Dimensions>
                        <v26:Length>12</v26:Length>
                        <v26:Width>12</v26:Width>
                        <v26:Height>12</v26:Height>
                        <v26:Units>IN</v26:Units>
                    </v26:Dimensions>
                    <v26:CustomerReferences>
                        <v26:CustomerReferenceType>CUSTOMER_REFERENCE</v26:CustomerReferenceType>
                        <v26:Value>#Order 11111</v26:Value>
                    </v26:CustomerReferences>
                    <v26:SpecialServicesRequested>
                        <v26:SpecialServiceTypes>SIGNATURE_OPTION</v26:SpecialServiceTypes>
                        <v26:SignatureOptionDetail>
                            <v26:OptionType>SERVICE_DEFAULT</v26:OptionType>
                        </v26:SignatureOptionDetail>
                    </v26:SpecialServicesRequested>
                </v26:RequestedPackageLineItems>
            </v26:RequestedShipment>
        </v26:ProcessShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""

SecondPieceShipmentRequestXml = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v26="http://fedex.com/ws/ship/v26">
    <tns:Body>
        <v26:ProcessShipmentRequest>
            <v26:WebAuthenticationDetail>
                <v26:UserCredential>
                    <v26:Key>user_key</v26:Key>
                    <v26:Password>password</v26:Password>
                </v26:UserCredential>
            </v26:WebAuthenticationDetail>
            <v26:ClientDetail>
                <v26:AccountNumber>2349857</v26:AccountNumber>
                <v26:MeterNumber>1293587</v26:MeterNumber>
            </v26:ClientDetail>
            <v26:TransactionDetail>
                <v26:CustomerTransactionId>IE_v26_Ship</v26:CustomerTransactionId>
            </v26:TransactionDetail>
            <v26:Version>
                <v26:ServiceId>ship</v26:ServiceId>
                <v26:Major>26</v26:Major>
                <v26:Intermediate>0</v26:Intermediate>
                <v26:Minor>0</v26:Minor>
            </v26:Version>
            <v26:RequestedShipment>

                <v26:DropoffType>REGULAR_PICKUP</v26:DropoffType>
                <v26:ServiceType>INTERNATIONAL_PRIORITY</v26:ServiceType>
                <v26:PackagingType>YOUR_PACKAGING</v26:PackagingType>
                <v26:TotalWeight>
                    <v26:Units>LB</v26:Units>
                    <v26:Value>3</v26:Value>
                </v26:TotalWeight>
                <v26:PreferredCurrency>USD</v26:PreferredCurrency>
                <v26:Shipper>
                    <v26:AccountNumber>2349857</v26:AccountNumber>
                    <v26:Contact>
                        <v26:PersonName>Input Your Information</v26:PersonName>
                        <v26:CompanyName>Input Your Information</v26:CompanyName>
                        <v26:PhoneNumber>Input Your Information</v26:PhoneNumber>
                        <v26:EMailAddress>Input Your Information</v26:EMailAddress>
                    </v26:Contact>
                    <v26:Address>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:City>MEMPHIS</v26:City>
                        <v26:StateOrProvinceCode>TN</v26:StateOrProvinceCode>
                        <v26:PostalCode>38117</v26:PostalCode>
                        <v26:CountryCode>US</v26:CountryCode>
                        <v26:CountryName>United States</v26:CountryName>
                        <v26:Residential>false</v26:Residential>
                    </v26:Address>
                </v26:Shipper>
                <v26:Recipient>
                    <v26:Contact>
                        <v26:PersonName>Input Your Information</v26:PersonName>
                        <v26:CompanyName>Input Your Information</v26:CompanyName>
                        <v26:PhoneNumber>Input Your Information</v26:PhoneNumber>
                        <v26:EMailAddress>Input Your Information</v26:EMailAddress>
                    </v26:Contact>
                    <v26:Address>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:StreetLines>Input Your Information</v26:StreetLines>
                        <v26:City>RICHMOND</v26:City>
                        <v26:StateOrProvinceCode>BC</v26:StateOrProvinceCode>
                        <v26:PostalCode>V7C4v7</v26:PostalCode>
                        <v26:CountryCode>CA</v26:CountryCode>
                        <v26:CountryName>Canada</v26:CountryName>
                        <v26:Residential>false</v26:Residential>
                    </v26:Address>
                </v26:Recipient>
                <v26:ShippingChargesPayment>
                    <v26:PaymentType>THIRD_PARTY</v26:PaymentType>
                    <v26:Payor>
                        <v26:ResponsibleParty>
                            <v26:AccountNumber>2349857</v26:AccountNumber>
                        </v26:ResponsibleParty>
                    </v26:Payor>
                </v26:ShippingChargesPayment>
                <v26:SpecialServicesRequested>
                    <v26:SpecialServiceTypes>ELECTRONIC_TRADE_DOCUMENTS</v26:SpecialServiceTypes>
                    <v26:EventNotificationDetail>
                        <v26:EventNotifications>
                            <v26:Events>ON_DELIVERY</v26:Events>
                            <v26:Events>ON_ESTIMATED_DELIVERY</v26:Events>
                            <v26:Events>ON_EXCEPTION</v26:Events>
                            <v26:Events>ON_SHIPMENT</v26:Events>
                            <v26:Events>ON_TENDER</v26:Events>
                            <v26:NotificationDetail>
                                <v26:NotificationType>EMAIL</v26:NotificationType>
                                <v26:EmailDetail>
                                    <v26:EmailAddress>Input Your Information</v26:EmailAddress>
                                    <v26:Name>Input Your Information</v26:Name>
                                </v26:EmailDetail>
                                <v26:Localization>
                                    <v26:LanguageCode>EN</v26:LanguageCode>
                                </v26:Localization>
                            </v26:NotificationDetail>
                            <v26:FormatSpecification>
                                <v26:Type>HTML</v26:Type>
                            </v26:FormatSpecification>
                        </v26:EventNotifications>
                    </v26:EventNotificationDetail>
                    <v26:EtdDetail>
                        <v26:Confirmation>CONFIRMED</v26:Confirmation>
                        <v26:Attributes>POST_SHIPMENT_UPLOAD_REQUESTED</v26:Attributes>
                    </v26:EtdDetail>
                </v26:SpecialServicesRequested>
                <v26:CustomsClearanceDetail>
                    <v26:DutiesPayment>
                        <v26:PaymentType>SENDER</v26:PaymentType>
                        <v26:Payor>
                            <v26:ResponsibleParty>
                                <v26:AccountNumber>2349857</v26:AccountNumber>
                            </v26:ResponsibleParty>
                        </v26:Payor>
                    </v26:DutiesPayment>
                    <v26:CustomsValue>
                        <v26:Currency>USD</v26:Currency>
                        <v26:Amount>100</v26:Amount>
                    </v26:CustomsValue>
                    <v26:Commodities>
                        <v26:NumberOfPieces>1</v26:NumberOfPieces>
                        <v26:Description>test</v26:Description>
                        <v26:CountryOfManufacture>US</v26:CountryOfManufacture>
                        <v26:HarmonizedCode>00339BB</v26:HarmonizedCode>
                        <v26:Weight>
                            <v26:Units>LB</v26:Units>
                            <v26:Value>10</v26:Value>
                        </v26:Weight>
                        <v26:Quantity>1</v26:Quantity>
                        <v26:QuantityUnits>EA</v26:QuantityUnits>
                        <v26:UnitPrice>
                            <v26:Currency>USD</v26:Currency>
                        </v26:UnitPrice>
                    </v26:Commodities>
                </v26:CustomsClearanceDetail>
                <v26:LabelSpecification>
                    <v26:LabelFormatType>COMMON2D</v26:LabelFormatType>
                    <v26:ImageType>PDF</v26:ImageType>
                    <v26:LabelStockType>STOCK_4X6</v26:LabelStockType>
                    <v26:LabelPrintingOrientation>TOP_EDGE_OF_TEXT_FIRST</v26:LabelPrintingOrientation>
                    <v26:LabelOrder>SHIPPING_LABEL_FIRST</v26:LabelOrder>
                </v26:LabelSpecification>
                <v26:MasterTrackingId>
                    <v26:TrackingIdType>[MASTER_ID_TYPE]</v26:TrackingIdType>
                    <v26:TrackingNumber>[MASTER_TRACKING_ID]</v26:TrackingNumber>
                </v26:MasterTrackingId>
                <v26:PackageCount>2</v26:PackageCount>
                <v26:RequestedPackageLineItems>
                    <v26:SequenceNumber>2</v26:SequenceNumber>
                    <v26:Weight>
                        <v26:Units>LB</v26:Units>
                        <v26:Value>2</v26:Value>
                    </v26:Weight>
                    <v26:Dimensions>
                        <v26:Length>11</v26:Length>
                        <v26:Width>11</v26:Width>
                        <v26:Height>11</v26:Height>
                        <v26:Units>IN</v26:Units>
                    </v26:Dimensions>
                    <v26:CustomerReferences>
                        <v26:CustomerReferenceType>CUSTOMER_REFERENCE</v26:CustomerReferenceType>
                        <v26:Value>#Order 11111</v26:Value>
                    </v26:CustomerReferences>
                    <v26:SpecialServicesRequested>
                        <v26:SpecialServiceTypes>SIGNATURE_OPTION</v26:SpecialServiceTypes>
                        <v26:SignatureOptionDetail>
                            <v26:OptionType>SERVICE_DEFAULT</v26:OptionType>
                        </v26:SignatureOptionDetail>
                    </v26:SpecialServicesRequested>
                </v26:RequestedPackageLineItems>
            </v26:RequestedShipment>
        </v26:ProcessShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""

ShipmentResponseXML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header/>
    <SOAP-ENV:Body>
        <ProcessShipmentReply xmlns="http://fedex.com/ws/ship/v26">
            <HighestSeverity>SUCCESS</HighestSeverity>
            <Notifications>
                <Severity>SUCCESS</Severity>
                <Source>ship</Source>
                <Code>0000</Code>
                <Message>Success</Message>
                <LocalizedMessage>Success</LocalizedMessage>
            </Notifications>
            <TransactionDetail>
                <CustomerTransactionId>IE_v26_Ship</CustomerTransactionId>
            </TransactionDetail>
            <Version>
                <ServiceId>ship</ServiceId>
                <Major>26</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <JobId>20q11454j07f4e64280587587</JobId>
            <CompletedShipmentDetail>
                <UsDomestic>false</UsDomestic>
                <CarrierCode>FDXE</CarrierCode>
                <MasterTrackingId>
                    <TrackingIdType>FEDEX</TrackingIdType>
                    <FormId>0430</FormId>
                    <TrackingNumber>794604790138</TrackingNumber>
                </MasterTrackingId>
                <ServiceDescription>
                    <ServiceType>INTERNATIONAL_ECONOMY</ServiceType>
                    <Code>03</Code>
                    <Names>
                        <Type>long</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx International EconomyÂ®</Value>
                    </Names>
                    <Names>
                        <Type>long</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx International Economy</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx International EconomyÂ®</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx International Economy</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>IE</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>ascii</Encoding>
                        <Value>IE</Value>
                    </Names>
                    <Names>
                        <Type>abbrv</Type>
                        <Encoding>ascii</Encoding>
                        <Value>IE</Value>
                    </Names>
                    <Description>International Two Day</Description>
                    <AstraDescription>IE</AstraDescription>
                </ServiceDescription>
                <PackagingDescription>
                    <PackagingType>YOUR_PACKAGING</PackagingType>
                    <Code>01</Code>
                    <Names>
                        <Type>long</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>Your Packaging</Value>
                    </Names>
                    <Names>
                        <Type>long</Type>
                        <Encoding>ascii</Encoding>
                        <Value>Your Packaging</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>Your Packaging</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>ascii</Encoding>
                        <Value>Your Packaging</Value>
                    </Names>
                    <Names>
                        <Type>small</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>Your Pkg</Value>
                    </Names>
                    <Names>
                        <Type>small</Type>
                        <Encoding>ascii</Encoding>
                        <Value>Your Pkg</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>Your</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>ascii</Encoding>
                        <Value>Your</Value>
                    </Names>
                    <Names>
                        <Type>abbrv</Type>
                        <Encoding>ascii</Encoding>
                        <Value>YP</Value>
                    </Names>
                    <Description>Customer Packaging</Description>
                    <AstraDescription>CST PKG</AstraDescription>
                </PackagingDescription>
                <SpecialServiceDescriptions>
                    <Identifier>
                        <Id>EP1000000060</Id>
                        <Type>DELIVER_WEEKDAY</Type>
                        <Code>02</Code>
                    </Identifier>
                    <Names>
                        <Type>long</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>Deliver Weekday</Value>
                    </Names>
                    <Names>
                        <Type>long</Type>
                        <Encoding>ascii</Encoding>
                        <Value>Deliver Weekday</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>Deliver Weekday</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>ascii</Encoding>
                        <Value>Deliver Weekday</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>WDY</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>ascii</Encoding>
                        <Value>WDY</Value>
                    </Names>
                </SpecialServiceDescriptions>
                <OperationalDetail>
                    <UrsaPrefixCode>SW</UrsaPrefixCode>
                    <UrsaSuffixCode>FLXA </UrsaSuffixCode>
                    <OriginLocationId>YQMA </OriginLocationId>
                    <OriginLocationNumber>0</OriginLocationNumber>
                    <OriginServiceArea>AM</OriginServiceArea>
                    <DestinationLocationId>FLXA </DestinationLocationId>
                    <DestinationLocationNumber>0</DestinationLocationNumber>
                    <DestinationServiceArea>A1</DestinationServiceArea>
                    <DestinationLocationStateOrProvinceCode>NV</DestinationLocationStateOrProvinceCode>
                    <IneligibleForMoneyBackGuarantee>false</IneligibleForMoneyBackGuarantee>
                    <AstraPlannedServiceLevel>4:30P</AstraPlannedServiceLevel>
                    <AstraDescription>INTL ** 2DAY **</AstraDescription>
                    <PostalCode>89109</PostalCode>
                    <StateOrProvinceCode>NV</StateOrProvinceCode>
                    <CountryCode>US</CountryCode>
                    <AirportId>LAS</AirportId>
                    <ServiceCode>03</ServiceCode>
                    <PackagingCode>01</PackagingCode>
                </OperationalDetail>
                <ShipmentRating>
                    <ActualRateType>PAYOR_ACCOUNT_SHIPMENT</ActualRateType>
                    <ShipmentRateDetails>
                        <RateType>PAYOR_ACCOUNT_SHIPMENT</RateType>
                        <RateScale>US001DFA_03_YOUR_PACKAGING</RateScale>
                        <RateZone>US001D</RateZone>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>USD</FromCurrency>
                            <IntoCurrency>USD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>139</DimDivisor>
                        <DimDivisorType>COUNTRY</DimDivisorType>
                        <FuelSurchargePercent>5.0</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>11.5</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>11.5</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>USD</Currency>
                            <Amount>246.24</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>USD</Currency>
                            <Amount>246.24</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>USD</Currency>
                            <Amount>76.99</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>USD</Currency>
                            <Amount>323.23</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>USD</Currency>
                            <Amount>323.23</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>323.23</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>PEAK</SurchargeType>
                            <Description>Peak Surcharge</Description>
                            <Amount>
                                <Currency>USD</Currency>
                                <Amount>2.6</Amount>
                            </Amount>
                        </Surcharges>
                        <Surcharges>
                            <SurchargeType>OUT_OF_PICKUP_AREA</SurchargeType>
                            <Description>Out of Pickup Area Tier C</Description>
                            <Amount>
                                <Currency>USD</Currency>
                                <Amount>59.0</Amount>
                            </Amount>
                        </Surcharges>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>USD</Currency>
                                <Amount>15.39</Amount>
                            </Amount>
                        </Surcharges>
                    </ShipmentRateDetails>
                </ShipmentRating>
                <ExportComplianceStatement>1</ExportComplianceStatement>
                <DocumentRequirements>
                    <RequiredDocuments>AIR_WAYBILL</RequiredDocuments>
                    <GenerationDetails>
                        <MinimumCopiesRequired>3</MinimumCopiesRequired>
                        <Letterhead>OPTIONAL</Letterhead>
                        <ElectronicSignature>OPTIONAL</ElectronicSignature>
                    </GenerationDetails>
                    <GenerationDetails>
                        <Type>PRO_FORMA_INVOICE</Type>
                        <MinimumCopiesRequired>3</MinimumCopiesRequired>
                        <Letterhead>OPTIONAL</Letterhead>
                        <ElectronicSignature>OPTIONAL</ElectronicSignature>
                    </GenerationDetails>
                    <GenerationDetails>
                        <Type>COMMERCIAL_INVOICE</Type>
                        <MinimumCopiesRequired>3</MinimumCopiesRequired>
                        <Letterhead>OPTIONAL</Letterhead>
                        <ElectronicSignature>OPTIONAL</ElectronicSignature>
                    </GenerationDetails>
                    <GenerationDetails>
                        <Type>AIR_WAYBILL</Type>
                        <MinimumCopiesRequired>2</MinimumCopiesRequired>
                    </GenerationDetails>
                </DocumentRequirements>
                <ShipmentDocuments>
                    <Type>COMMERCIAL_INVOICE</Type>
                    <ShippingDocumentDisposition>RETURNED</ShippingDocumentDisposition>
                    <ImageType>PDF</ImageType>
                    <Resolution>200</Resolution>
                    <CopiesToPrint>3</CopiesToPrint>
                    <Parts>
                        <DocumentPartSequenceNumber>1</DocumentPartSequenceNumber>
                        <Image>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4MecIfpOT4LHlwhJm6jTZgvFRNt9khx2rcEsnTp3ImyXHbDZSd/IUw02/wswAA1J/TcKZW5kc3RyZWFtCmVuZG9iago0MyAwIG9iaiA8PC9TdWJ0eXBlL0Zvcm0vTWF0cml4WzEgMCAwIDEgMCAwXS9UeXBlL1hPYmplY3QvRm9ybVR5cGUgMS9SZXNvdXJjZXM8PC9Qcm9jU2V0Wy9QREZdPj4vQkJveFswIDAgMzM1LjEyOCA4LjA0NTkxXS9MZW5ndGggMjk+PnN0cmVhbQoxIGcKMCAwIDMzNS4xMjc5IDguMDQ1OSByZQpmCgplbmRzdHJlYW0KZW5kb2JqCjQ4IDAgb2JqIDw8L1N1YnR5cGUvRm9ybS9NYXRyaXhbMSAwIDAgMSAwIDBdL1R5cGUvWE9iamVjdC9Gb3JtVHlwZSAxL1Jlc291cmNlczw8L1Byb2NTZXRbL1BERl0+Pi9CQm94WzAgMCAyNTYuNzE4IDkuMjVdL0xlbmd0aCAyNz4+c3RyZWFtCjEgZwowIDAgMjU2LjcxODIgOS4yNSByZQpmCgplbmRzdHJlYW0KZW5kb2JqCjUxIDAgb2JqIDw8L1N1YnR5cGUvRm9ybS9NYXRyaXhbMSAwIDAgMSAwIDBdL1R5cGUvWE9iamVjdC9Gb3JtVHlwZSAxL1Jlc291cmNlczw8L1Byb2NTZXRbL1BERl0+Pi9CQm94WzAgMCAyMzkuOTA1IDEwLjM3MV0vTGVuZ3RoIDI5Pj5zdHJlYW0KMSBnCjAgMCAyMzkuOTA1MSAxMC4zNzEgcmUKZgoKZW5kc3RyZWFtCmVuZG9iago1MiAwIG9iaiA8PC9TdWJ0eXBlL0Zvcm0vTWF0cml4WzEgMCAwIDEgMCAwXS9UeXBlL1hPYmplY3QvRm9ybVR5cGUgMS9SZXNvdXJjZXM8PC9Qcm9jU2V0Wy9QREZdPj4vQkJveFswIDAgMTc1LjI0OSA4Ljk2NTAzXS9MZW5ndGggMjg+PnN0cmVhbQoxIGcKMCAwIDE3NS4yNDkyIDguOTY1IHJlCmYKCmVuZHN0cmVhbQplbmRvYmoKNTMgMCBvYmogPDwvU3VidHlwZS9Gb3JtL01hdHJpeFsxIDAgMCAxIDAgMF0vVHlwZS9YT2JqZWN0L0Zvcm1UeXBlIDEvUmVzb3VyY2VzPDwvUHJvY1NldFsvUERGXT4+L0JCb3hbMCAwIDIzNi4zMjMgMTAuMzcxXS9MZW5ndGggMjk+PnN0cmVhbQoxIGcKMCAwIDIzNi4zMjI4IDEwLjM3MSByZQpmCgplbmRzdHJlYW0KZW5kb2JqCjU4IDAgb2JqIDw8L1N1YnR5cGUvRm9ybS9NYXRyaXhbMSAwIDAgMSAwIDBdL1R5cGUvWE9iamVjdC9Gb3JtVHlwZSAxL1Jlc291cmNlczw8L1Byb2NTZXRbL1BERl0+Pi9CQm94WzAgMCAxMjMuOTM0IDEwLjIxNDFdL0xlbmd0aCAyOT4+c3RyZWFtCjEgZwowIDAgMTIzLjkzNCAxMC4yMTQxIHJlCmYKCmVuZHN0cmVhbQplbmRvYmoKNjAgMCBvYmogPDwvU3VidHlwZS9Gb3JtL01hdHJpeFsxIDAgMCAxIDAgMF0vVHlwZS9YT2JqZWN0L0Zvcm1UeXBlIDEvUmVzb3VyY2VzPDwvUHJvY1NldFsvUERGXT4+L0JCb3hbMCAwIDI1Ni4yMDIgOS4yNV0vTGVuZ3RoIDI3Pj5zdHJlYW0KMSBnCjAgMCAyNTYuMjAyMyA5LjI1IHJlCmYKCmVuZHN0cmVhbQplbmRvYmoKNjEgMCBvYmogPDwvU3VidHlwZS9Gb3JtL01hdHJpeFsxIDAgMCAxIDAgMF0vVHlwZS9YT2JqZWN0L0Zvcm1UeXBlIDEvUmVzb3VyY2VzPDwvUHJvY1NldFsvUERGXT4+L0JCb3hbMCAwIDM5MS45ODkgMjAuNzA3Nl0vTGVuZ3RoIDMwPj5zdHJlYW0KMSBnCjAgMCAzOTEuOTg5MSAyMC43MDc2IHJlCmYKCmVuZHN0cmVhbQplbmRvYmoKNjMgMCBvYmogPDwvU3VidHlwZS9Gb3JtL01hdHJpeFsxIDAgMCAxIDAgMF0vVHlwZS9YT2JqZWN0L0Zvcm1UeXBlIDEvUmVzb3VyY2VzPDwvUHJvY1NldFsvUERGXT4+L0JCb3hbMCAwIDE1My42MjMgMTkuNTQ5XS9MZW5ndGggMjg+PnN0cmVhbQoxIGcKMCAwIDE1My42MjMgMTkuNTQ5IHJlCmYKCmVuZHN0cmVhbQplbmRvYmoKNzEgMCBvYmogPDwvU3VidHlwZS9Gb3JtL01hdHJpeFsxIDAgMCAxIDAgMF0vVHlwZS9YT2JqZWN0L0Zvcm1UeXBlIDEvUmVzb3VyY2VzPDwvUHJvY1NldFsvUERGXT4+L0JCb3hbMCAwIDI3OC4xMTIgOS4yNV0vTGVuZ3RoIDI2Pj5zdHJlYW0KMSBnCjAgMCAyNzguMTEyIDkuMjUgcmUKZgoKZW5kc3RyZWFtCmVuZG9iago3MiAwIG9iaiA8PC9TdWJ0eXBlL0Zvcm0vTWF0cml4WzEgMCAwIDEgMCAwXS9UeXBlL1hPYmplY3QvRm9ybVR5cGUgMS9SZXNvdXJjZXM8PC9Qcm9jU2V0Wy9QREZdPj4vQkJveFswIDAgMjI2LjI5OSA3LjkyNjk0XS9MZW5ndGggMjk+PnN0cmVhbQoxIGcKMCAwIDIyNi4yOTg4IDcuOTI2OSByZQpmCgplbmRzdHJlYW0KZW5kb2JqCjczIDAgb2JqIDw8L1N1YnR5cGUvRm9ybS9NYXRyaXhbMSAwIDAgMSAwIDBdL1R5cGUvWE9iamVjdC9Gb3JtVHlwZSAxL1Jlc291cmNlczw8L1Byb2NTZXRbL1BERl0+Pi9CQm94WzAgMCAxNTkuOTkyIDMyLjUyNV0vTGVuZ3RoIDI5Pj5zdHJlYW0KMSBnCjAgMCAxNTkuOTkxOSAzMi41MjUgcmUKZgoKZW5kc3RyZWFtCmVuZG9iago3NCAwIG9iaiA8PC9TdWJ0eXBlL0Zvcm0vTWF0cml4WzEgMCAwIDEgMCAwXS9UeXBlL1hPYmplY3QvRm9ybVR5cGUgMS9SZXNvdXJjZXM8PC9Qcm9jU2V0Wy9QREZdPj4vQkJveFswIDAgMjU2LjM2NiA5LjI1XS9MZW5ndGggMjc+PnN0cmVhbQoxIGcKMCAwIDI1Ni4zNjU5IDkuMjUgcmUKZgoKZW5kc3RyZWFtCmVuZG9iago3OCAwIG9iaiA8PC9TdWJ0eXBlL0Zvcm0vTWF0cml4WzEgMCAwIDEgMCAwXS9UeXBlL1hPYmplY3QvRm9ybVR5cGUgMS9SZXNvdXJjZXM8PC9Qcm9jU2V0Wy9QREZdPj4vQkJveFswIDAgMjc4LjE5NCA5LjI1XS9MZW5ndGggMjc+PnN0cmVhbQoxIGcKMCAwIDI3OC4xOTM4IDkuMjUgcmUKZgoKZW5kc3RyZWFtCmVuZG9iago4NyAwIG9iaiA8PC9TdWJ0eXBlL0Zvcm0vTWF0cml4WzEgMCAwIDEgMCAwXS9UeXBlL1hPYmplY3QvRm9ybVR5cGUgMS9SZXNvdXJjZXM8PC9Qcm9jU2V0Wy9QREZdPj4vQkJveFswIDAgNjcuMjUgMTUuNzQ2XS9MZW5ndGggMjY+PnN0cmVhbQoxIGcKMCAwIDY3LjI1IDE1Ljc0NiByZQpmCgplbmRzdHJlYW0KZW5kb2JqCjg4IDAgb2JqIDw8L1N1YnR5cGUvRm9ybS9NYXRyaXhbMSAwIDAgMSAwIDBdL1R5cGUvWE9iamVjdC9Gb3JtVHlwZSAxL1Jlc291cmNlczw8L1Byb2NTZXRbL1BERl0+Pi9CQm94WzAgMCA4OC4xMjMgOC45NjUwM10vTGVuZ3RoIDI2Pj5zdHJlYW0KMSBnCjAgMCA4OC4xMjMgOC45NjUgcmUKZgoKZW5kc3RyZWFtCmVuZG9iago5MSAwIG9iaiA8PC9TdWJ0eXBlL0Zvcm0vTWF0cml4WzEgMCAwIDEgMCAwXS9UeXBlL1hPYmplY3QvRm9ybVR5cGUgMS9SZXNvdXJjZXM8PC9Qcm9jU2V0Wy9QREZdPj4vQkJveFswIDAgMTYwLjYyMyA5LjM0MDAzXS9MZW5ndGggMjY+PnN0cmVhbQoxIGcKMCAwIDE2MC42MjMgOS4zNCByZQpmCgplbmRzdHJlYW0KZW5kb2JqCjk1IDAgb2JqIDw8L1N1YnR5cGUvRm9ybS9NYXRyaXhbMSAwIDAgMSAwIDBdL1R5cGUvWE9iamVjdC9Gb3JtVHlwZSAxL1Jlc291cmNlczw8L1Byb2NTZXRbL1BERl0+Pi9CQm94WzAgMCAzMTkuMTEgNi4yMTkwNF0vTGVuZ3RoIDI2Pj5zdHJlYW0KMSBnCjAgMCAzMTkuMTEgNi4yMTkgcmUKZgoKZW5kc3RyZWFtCmVuZG9iago5NiAwIG9iaiA8PC9TdWJ0eXBlL0Zvcm0vTWF0cml4WzEgMCAwIDEgMCAwXS9UeXBlL1hPYmplY3QvRm9ybVR5cGUgMS9SZXNvdXJjZXM8PC9Qcm9jU2V0Wy9QREZdPj4vQkJveFswIDAgMjQxLjUgOF0vTGVuZ3RoIDIxPj5zdHJlYW0KMSBnCjAgMCAyNDEuNSA4IHJlCmYKCmVuZHN0cmVhbQplbmRvYmoKOTggMCBvYmogPDwvU3VidHlwZS9Gb3Jt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</Image>
                    </Parts>
                </ShipmentDocuments>
                <CompletedPackageDetails>
                    <SequenceNumber>1</SequenceNumber>
                    <TrackingIds>
                        <TrackingIdType>FEDEX</TrackingIdType>
                        <FormId>0430</FormId>
                        <TrackingNumber>794604790138</TrackingNumber>
                    </TrackingIds>
                    <GroupNumber>0</GroupNumber>
                    <OperationalDetail>
                        <OperationalInstructions>
                            <Number>2</Number>
                            <Content>TRK#</Content>
                        </OperationalInstructions>
                        <OperationalInstructions>
                            <Number>3</Number>
                            <Content>0430</Content>
                        </OperationalInstructions>
                        <OperationalInstructions>
                            <Number>5</Number>
                            <Content>SW FLXA </Content>
                        </OperationalInstructions>
                        <OperationalInstructions>
                            <Number>7</Number>
                            <Content>1010069744090008910900794604790138</Content>
                        </OperationalInstructions>
                        <OperationalInstructions>
                            <Number>8</Number>
                            <Content>56DJ4/F289/FE4A</Content>
                        </OperationalInstructions>
                        <OperationalInstructions>
                            <Number>10</Number>
                            <Content>7946 0479 0138</Content>
                        </OperationalInstructions>
                        <OperationalInstructions>
                            <Number>12</Number>
                            <Content>4:30P</Content>
                        </OperationalInstructions>
                        <OperationalInstructions>
                            <Number>13</Number>
                            <Content>INTL ** 2DAY **</Content>
                        </OperationalInstructions>
                        <OperationalInstructions>
                            <Number>15</Number>
                            <Content>89109</Content>
                        </OperationalInstructions>
                        <OperationalInstructions>
                            <Number>16</Number>
                            <Content>NV-US</Content>
                        </OperationalInstructions>
                        <OperationalInstructions>
                            <Number>17</Number>
                            <Content>LAS</Content>
                        </OperationalInstructions>
                        <Barcodes>
                            <BinaryBarcodes>
                                <Type>COMMON_2D</Type>
                                <Value>Wyk+HjAxHTAyODkxMDkdODQwHTAzHTc5NDYwNDc5MDEzODA0MzAdRkRFHTUxMDA4NzE2MB0wMjcdHTEvMR00LjAwS0cdTh1Db252ZW50aW9uIENlbnRlciBEch1MYXMgVmVnYXMdTlYdQ29udmVudGlvbiBjZW50ZXIeMDYdMTBaRUlJMDgdMTJaMTUxNDAwMDAwMDAdMTVaMTE4ODI5NDY1HTMxWjEwMTAwNjk3NDQwOTAwMDg5MTA5MDA3OTQ2MDQ3OTAxMzgdMzJaMDIdMzlaWVFNQR05OVpFSTAwMDYcQ0EcHFVTRBxSZWQgTGVhdGhlciBDb2F0HBwdHjA5HUZEWB16HTgdHwIoKTcrf0AeBA==</Value>
                            </BinaryBarcodes>
                            <StringBarcodes>
                                <Type>FEDEX_1D</Type>
                                <Value>1010069744090008910900794604790138</Value>
                            </StringBarcodes>
                        </Barcodes>
                    </OperationalDetail>
                    <Label>
                        <Type>OUTBOUND_LABEL</Type>
                        <ShippingDocumentDisposition>RETURNED</ShippingDocumentDisposition>
                        <ImageType>PDF</ImageType>
                        <Resolution>200</Resolution>
                        <CopiesToPrint>1</CopiesToPrint>
                        <Parts>
                            <DocumentPartSequenceNumber>1</DocumentPartSequenceNumber>
                            <Image>JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMyAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL091dGxpbmVzCi9Db3VudCAwCj4+CmVuZG9iagozIDAgb2JqCjw8Ci9UeXBlIC9QYWdlcwovQ291bnQgMwovS2lkcyBbMTggMCBSIDE5IDAgUiAyMCAwIFJdCj4+CmVuZG9iago0IDAgb2JqClsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXQplbmRvYmoKNSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iago2IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0hlbHZldGljYS1Cb2xkCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKNyAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EtT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjggMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhLUJvbGRPYmxpcXVlCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKOSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9Db3VyaWVyCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTAgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1Cb2xkCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTEgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1PYmxpcXVlCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTIgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllci1Cb2xkT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjEzIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLVJvbWFuCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTQgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvVGltZXMtQm9sZAovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjE1IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLUl0YWxpYwovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjE2IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLUJvbGRJdGFsaWMKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iagoxNyAwIG9iaiAKPDwKL0NyZWF0aW9uRGF0ZSAoRDoyMDAzKQovUHJvZHVjZXIgKEZlZEV4IFNlcnZpY2VzKQovVGl0bGUgKEZlZEV4IFNoaXBwaW5nIExhYmVsKQ0vQ3JlYXRvciAoRmVkRXggQ3VzdG9tZXIgQXV0b21hdGlvbikNL0F1dGhvciAoQ0xTIFZlcnNpb24gNTEyMDEzNSkKPj4KZW5kb2JqCjE4IDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMSAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjE5IDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMiAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjIwIDAgb2JqCjw8Ci9UeXBlIC9QYWdlDS9QYXJlbnQgMyAwIFIKL1Jlc291cmNlcyA8PCAvUHJvY1NldCA0IDAgUiAKIC9Gb250IDw8IC9GMSA1IDAgUiAKL0YyIDYgMCBSIAovRjMgNyAwIFIgCi9GNCA4IDAgUiAKL0Y1IDkgMCBSIAovRjYgMTAgMCBSIAovRjcgMTEgMCBSIAovRjggMTIgMCBSIAovRjkgMTMgMCBSIAovRjEwIDE0IDAgUiAKL0YxMSAxNSAwIFIgCi9GMTIgMTYgMCBSIAogPj4KL1hPYmplY3QgPDwgL0ZlZEV4RXhwcmVzcyAyMyAwIFIKL0V4cHJlc3NFIDI0IDAgUgovYmFyY29kZTAgMjUgMCBSCi9GZWRFeEV4cHJlc3MgMjYgMCBSCi9FeHByZXNzRSAyNyAwIFIKPj4KPj4KL01lZGlhQm94IFswIDAgMjg4IDQzMl0KL1RyaW1Cb3hbMCAwIDI4OCA0MzJdCi9Db250ZW50cyAyMiAwIFIKL1JvdGF0ZSAwPj4KZW5kb2JqCjIxIDAgb2JqCjw8IC9MZW5ndGggMjYwNwovRmlsdGVyIFsvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGVdIAo+PgpzdHJlYW0KR2F0PS45bGpPSigjPHJOcnJGcTMsYiJRSVxAQjxYWyVnJUNWQl86XjhCWFJQUmw1NyZTVS9eRlBMZTJpaFpMTV1STl9gZSs7XjQnbCtEKGYKTWk3SDVjalozczUiOk0qYGVsL3BFUjlUXSRwKj1XKCw9ZVcudWdJbGR0Y1ckYlM5TUJpOz89aSJUTDRPMyVcdEU9J21eS3M1P1RsXVNzPjQKXClQPT0uaVUxSCR0NFkkaDxcYCw/NWFSLm1kRHJPQ0E1SzIxKCNILTFkOiZZQkhPO1lrMjZxUClYWnRROVJYNnFddC46J3EvMUo7Slw3RFMKTTglZ0VBJSgxYzEpZGk9XVVeXllQcWFGWUFGRWo7aHU5amM/TCdoUUlCRWZiLCFJLzBrRnJIXi9KZEEzXVw9RUlPTVswRixpbS9cbyEwLD8KUlM1SyhwM1ZbaF4zUjNkbC5gKm1bQHRaJF5MVlcxUUFlaGAqREVuZ3EhTHAqLExQW289TSpgVWoqYyk8b1o6R2E0LSVVJSNLKTw4Nix0SXMKcnIpWlttZXMzQltESyNQcVgybUZGU1tcYGBUbGphPiQ6XkdyaiooIXA/YmRGVz1eJS0nIWRSTzokLFNVTi1pRXNqaV9GXiMpT0NLW1BDUEMKLCRQUWZnMmpASE51KWc+XCooOVlTNDJEXEEvbXR0NjhaXnNNcmpwKlBiX3BNMyJUX1gkLyJRJUM9KU8mNydrXWYrYUEpLT09OVtjcF4kW1AKQkA+SykyKVw1JWQ8ayY6IV9NSyJbU24wJiM4SHVyIW8jWlEpTWQtSUs9L2U3M2VGUVo0OkVpdDdXcl9RbFwxP0RlRTEzNEM6LipDYFYjO0wKXlJfISo4ITFWODZSKDxrIm0lSFYoNWcvO1QrUi83X3RwWmloSj9OJWVSR2t0TjkxXSRrM0AtXUUnSVVHbm4lXDlFcEVBa104LC5tQzpoKjIKYj02dTFBPyEzXyVORzAwQXBxO0dYVCxCUTJlbSZFcShMXF42TWNqQGYoMCdoMXF0Ry5mbC40YjJsalBQWzldcE9iRC5rZCQnbzhLZismQj0KNnQzPlJaR1c9bmxjOCs1XChbcTYvVWgnTmtaU2tfPlFQazU2Vy9oODduJjIxPyFaaWBnUllwRmhebjZHRjgzQE5EZyFURiU5SFVJUDNbYDQKbilkaklcOXMiJmxVUVolV1QtISlkY11IUFlmTUQ1bCZWI3RAcz5oXUM0aVE0a1YjIzRxZC10S3FyKTghXydIIz1GZSE2U2k1Zmtycmc5WFQKNEVBXTE4LWZzJHBfN2tRRUBHQTU5Jy1dXFNSOSQ8TGtrY2JqY1xkUyIqMFktPVdZVW4zL0NaTTBtY2xjSFRqX3VWRExxRmc9WkFkVXFyIjUKJTUrO1s2M1g3Y3FlU2AjTDUoWzlWUDE3LWNFWjhBTFNAbFAlLl5aXFVEJyJucypRYFo1K0BzPSxcOCw6LFg5Oi47PXQ2MVNbcVhTQ0MvWkMKUyJePCpwLixDTktJZUgyVkNqWD80ISFUSS0qL0NrMms5UE5tMDVQal5pNkVlOUVGSDgpc11mXCxgdWkoWWxkVWJXX05gTC4+LmxNIjMlPGwKLEZPOV0hVUROXExFWV91YFpSOVAxaDZxcWhlWitAcSVUKnVoaDdObyVASWpbLj4tMHFnWCdbPFt0XmZPSyktYFQ+LEdRLlluYD1vVnI7ODcKWERfQ1dTUVpVMWtPQmFVME1vVklCLVgxQClSMlNkQmduTChlcm8hZGpiQVpGWi5xOE1dc2JwO2xSRjNeRF9lN1gzPmonTFRONFM3UXFSaFAKUF9sMCEmdSI+czlzKihfWVdlSV83bE1fNWkoOWRYQipxVjFTIldnKWRjOlBJNmkwPWMtdC5OYSEiR1lxIkdDJ09YUFQ9PCQxIiZpLlZiR1MKMk1lW1JGQSZLXW9yU1luZTwkXlAkXExFU2k4ZG4vJEVkSU8lUTZJP0Q4SVJII1xZTmNjWVEoK0VSaC4lRk1Yb1Q9dWxoaTtvaz5XbzA/SGsKQDEnK0NRKzEtRDJgZSY1TjlaK3JpPF42KGs2ZFY6XHVfMFE/UDZTRzp1WE5LNnJTZVJAbC9wLjJzUHIkWSZkJ2M3OEBpXCVCOllbJVpPRm4KXzAram1IbnEmN1U+U2JpWis1XWA+YzZbN2lkSURxZGxzRSFbWSt1bVZcIVVXSGpbYUlVKDxQanJEQ0UoJEpGc3JMSyFOISh1KkohS2xxXEMKYk1cUkg3cyQ/OltxYGVmWSM+VXM7RzlrLFNpXW88WFZFPSpTVkQyPEdDP0R0WG4sOTU1IjUuJWA6OXFTK2ZJKVhFaGJnc2kmWlFncjhpb2wKZ3U4b0QpV2FeI2xdbWtKcFJHbjJSKEFdPjhtSjlVOVA5YzxrVy9GYj4rWkdaLyopRilPUlUjOE5rTUU1JEw8dDZpdXNtTi5IajpSTUpzbEUKO15nI1ZZVD1nRUYwOmVwJDxYTFVGRjQxY1VObEw7alRtMDg7XmUqblMwIzpvbFA4RixBTmMza1ZjTk9qX0tvZTFmVlNFLUxfMClcTl9uYTMKS0YhOFMtLU0yaSldPVc9aiVRQWhvYTpOQkFQb0NpTzEoPj0uXyY0c1VXN3VsQElzWV4/MGRgVGA6WEpKbltVVjEhRmcqcEMwLEFmNj1GdD4KJlBDU2pDY0hWQmYtcytQMD1fW05VTHVwZGUuPSpMXWc9SlxRdCgxPypPcUE5LyVBPXRYJTBXLllRZ1tsYjhFb1dZN000PyViNGIuOnVYTUgKQDtRaUNbdCJJNT8vSVtcV1NmZ01gKUMuZWAwY2U1PXJYb2dGajtEa1RrPUVEKyxxX1ddV1QxcWMzVkJzZXJTUCNLajFILy0qNlJySnQqcEQKXio5NlA1V1JKWzNKRFVFJUUyXmklIT1zYlBSXXJeMThoP09VTm1jPWZIUSpIaGU0Myw9QSghdU0+NjxeYiVVYkdRQTU+LGpLKExNZ2AxM0cKZTw6RE0+Q0QhS2RGKEQpblgrRitoVkcwMy5uLEJsTzZZdSM9ZChbaktkRGstciswP09eOUxxVDpCSDBQMTUrblw5WUBdYlxobmdXa0stXF0KZ0dWOlBEOlBTai8jJGtnYUktL2xHU2w/QjU8YVMrNGVbdVYlSWw5US1tXCYhX2w9UTZtSyJccUonWEBjX3RYaiI2K1luckhiKmNyU2VRVz0KUkFwRiFwJShbJUosIVVOSDI3OENUMEUySFJwLF9OcWBdIiYyZltxRCVLUz5aX29eZjU7SWgxV24mUF5TMkVFLzI2b09RZCVuJWFSJ18xQiMKMTlEaSVpUEc/OystQj9QVHAnQmdvKU1YLiwrcUtocjdiUkNyVll0Nys4IVc3Py9OM1hGZUhmMElMM25PZURSPTIxXkI1WjhMTSM5ZzdbbzEKaHU+TGNtSmxTS1M4QX4+CmVuZHN0cmVhbQplbmRvYmoKMjIgMCBvYmoKPDwgL0xlbmd0aCAzMDY0Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0gCj4+CnN0cmVhbQpHYXQ9Lj1gWUxsKDROLzJzNT9yNVFeTGguZEQjKykhSU1vP2ZPTldURWJmIS1FJG82KUJGZzNEcFhlO3QoPDAhPzI2QTMqTD5eREBlKEtmMwozb1YiWFh1NjJoYGFmM1pQUjhSaVYkNzNTJF8rR0dnY09MUTVkWipxPGwtXWwoWSFIXUhbZUF1NWxSVVgtMDUqbCE8bilULitoNSheRVNnUApWKEpBSiJFUjVaPSQ/Pz9pYkVLcFJETkxhczg5cTUhLltaa0xrI0FsczRuWFdNMz1pZVBsLjVkPkptQmhdODdcbEBLbk5pMllVPyUuPjBvWApUaE4+bW1iOz8mI0lAXFA9a3AjST1lNVFJXF4oNk5IKnM3NFdxQUhAKmxGP1RgSUNUQEpiMmd0RSVpO2sjNEdxWnBpZiMnbztxWWgtSCZOTgooazNTOFplbSpyMEgwJDQ0dHVxRDBQLj5UNnQyYj0yWDFDQGBcOHAtSSIqc0wxdVtfMkJKSC9nXFtpOG9VOF9bJEM5RSs6SFddTUFTPUchRwpeZTZzRmY+a2c8SUAlXkBwLTJuaD9OR1c+aVdkQzVEVEsjMXMlYSNEMSQrKnNTbG05ZFZwQXFFPDFERGdnUTVKJVRfO2NeYVlaNTdbcjZoVwojK3RHIVA7cjkjSiJrOTJBW2FAZExRaVlibzorNEElaUIhYGcvcEJZTm5acGtOW0VxcTUmZzNvVzFWa1xuQFk1VUYmNm0+UkQvXFxeXWhIWAooKDVGQic/M1VBPT1fZWU+aTgzYTxVWyRBX1QyNF9aLFFZPyNmXWJPPkJpQz9tZko0aWhHRCtcI0FqOWBfX1YyVWNgJyhrRnU7SS9XRTRcJgolVmQiW2NIXWZVU3JVZmwwQGQ8LjsuTGJFPCxgN2UuZSklcCpFIk4pQk9SIWFPZTUjTVg3YzQtXWoiSE9SLGBQKEJkJlU5ajdQNF5DKmcqWQo0STZuIUhPNmE6M29tSUkhQCI+cllaOzkoRCk7WS1qYkc3MXFfZlBCRV0+IVhPM2NfaTdNZGJsYU1DbVM8XSknSFMvcj02SDkwMGcsRklURgo0KGRzPkhNMENeNnFGLD1xWy44KzJRZFpWYkcuOk9cWHJjcUNDO1NNI1ZYLk4tSl9kN0pEITpVKlNfV1k4ZnIsQSooSnVBT1M1bSM+PCItawpoJlNPZD07PERXTGsmO1JUKm82LzotdE9dZWQ6OlVMIV0hTDcpKXFGUSYjNThrXGNQdDxdYnBPNz9QcWhxIWs1WjFdRiprOD1WO1tGKklaNwomdEtRNitBQy5LMEYjXVpeIkprXCVsUSI/WUU6VDhLZColQk0qZV4/LUQmV11DRjIidWIhbjJwXmddRFdVTCYzaiU0Qjo4Y1FiNUhCOlUzbwo4OmQkVjY1NzNdQzg8WiVYYT1KXFVtL2xUUl1uVWk3UGFER1ZRUSg5LSY7Zz9LbENiN0EsRC1QVjhBQks9TiFdMT1KQTo7XTNmMj9PPTVXUAplND0vakxUVFFuKUEyTDohMSdSR2FfWFx0WGpnT0FSI0BFOzFgaTA2Tk11R1NFRltCTS5TTFBuLHIwSjQrNSIqTWEnLi4lOyVvODosUEdJcApMPipgRjlTQjtNOThgcTUvaUdSLFtvSm1HUixPTDw3IickJVcrMixsTWNqTSpOJHMzTEBtW1EpbyxXVF1CYmNVUTsjbHAnX3FSJkQmMicpOgpxKD4kUzEoZks3KGY6czRhSjFRSFtHYWFsOTo6YnNdYDlUOGsoTkQxYUpjT0g4PGIlVEJ1ODxqT2opLW0qJSxuVWQ0L1JyISVhNjsjRmFCOQo3UyMuSyxaVT40NmwrYFtPOWtjZGxTJnA+LTdtRCdkXjg6XyFFYmRTTVlKZ0QnVW1mXC02a28lPmFlLT5bSF9vOT1KQTolW2tXVGNOKyMrRQpcbTU8JWFKNC9tRTM6WS1uZUs5PSElYThRcUJncnJMTkFaOFEwXEslTkNXSG5MKXM6R2FEQFs/IkNQcWBUUzkhQFY4UnRFMGNRZyNURyJZMAo0dSFvQlBtZ2haW1JZJksnIidHWDAtbkg0OVhvc19YVS5ZTGB0NGpZYmFpaVBhczBhcEowamRVPG8jLCc5Qjs0YS8mZUc0PUdVT2E+UitZbgo0PVpRP0QqaERHQVQ1KnVpRyQuQUgkISkqVVRBRnAxUVJnSyElYThRW2NxZyw8KkU3Km1jUWcyVjhETEcsPz4yZmReNjloY2BRMFc6aF9XbAosPFNcJiwqMjxaVlpfSFlRJk5wMCFFYylQOVdLM05KPkppcjBSbkM5L0AxKWtYczgqRmRfbUgnPTpqRklLNihnZjBYNXBFX1BRTy49dURyYQovc1UvTktMQUghcW9WJ0hOQSo1ME0rajAxJSlFRi5tNnVvIjonIlRMJzVRLmY2RmFzaUUwI1I/IktmJnNBZ1YtJyElcTghajdjRmc6PiFkdApNTXRYXD5VZ0Q1XG0/b00jKCpfNmpcbC9HYU1fYm1gWVpMZzE5amxeMDgpdTBnKW8hYGJeVCEqJFh1ZSg+W20lU201JVhaLl8vUzJiMStBKwpsPUJpSl07PFhvNFAla0hcM3VtdDU2SmBMXzMpTionKF0kJVFbNmUrSHEqKmI3KE5VU1ohJjNhVikjI05TJDNHVmVVI2cwJCVBb2FmLj5BKAo2YiNPVCJEYCxzKHJFKylNMD5GREo0akk6bTVlWVVRY2MsWUZpIiwyUS0jWVQ6YEw7QTJgMHMjLTgoUypxTVxzPjtnODNSZVoiQnVJO1p0Wgo9YSdzViJEPiIyaTtiRSssOlZDP18jUSpROGMqbkIpWV1ANlgnMUldTStiNEhfQTFGRGNjKTtPPmZZaElKNG5CYG0xMWRmaSVcM08qWlA+awowcVM+Qmk4RDlgQ145Vk8uJHFwbEJuPFAsVUxbJT4iW20jM21VWCNjL0xER0ZwPHAxJ1teXEdVNCM+ZE1RL0VRJFYkKjBgcWQjRTdCY2wmOQorYCdAJklaY1MkXD1WaGFUQWZfL1prKCVUNWA9QU4hST0lcjo+PT1MQThqU2FPK1hlKUVQSiFRVm4yckhsV0pbVjUnck1gY21XaXIpZypzcApAP0xCX0AzOSkoV09xWU9VIlcpblpPNzAwbzAtRW1kVCFYJjw7QSpsRmx1QzliRGIuLm4/MVE0MFgiTlhsPzlGOlBoVURkLypELUJDMD50NQpHUiliJ1thZ2AjTygpJilOdFFyLDVPWVl0WS5USEFScWdKYipSXmkkUSw2dWNDL2lOS15LOztdIllBNSRiaWRPPVtUTGs8RU8hLS5oOyc7KwonWHQtXkhFbDpDTVleQiFWWXA6LT1iIzQ9U1gpVi5tJUtSW2dzUC5nSFoudWFwTiFVQkRgKE8xak91YDNZKEN0Tk1kZC49aVduN1dXazY1VwokYWA4KkJMMC1XMlZbNF1RU2w7OTpBI08wbi5AKk9qNkckbEdfImZRSVlnO0BbcUxvYycjJURWXmlmVSpbK0Q+M21VMEA7YjpQN11YMldAJQpYT0JmPiknbm9XYWI+KSdtJEciRzRkVilfIiZyWGNVcUE5PGA9ZzBUbWwwP08kWFlTTVE1K2thcFkwXmtlMCtMcj07PjE5WnMmZj1FMStDYwpiJDsuMVUmJ01LR2RrMWlUal1eRElKYEAhRWtaVWRFPDFaX0VvRHE9aTBMVkkjKDhHZl1vJWQ8VjZwMjgkY0BQO0QwbGw3XWVRYV4mOEFdJgpIY01ZODgpbUIhXDJmPCZgVDpfbEskMUxqP29IJDZfL0tnSC45cDFhJXRFPjRybUx1OW0lMi5cQV9eY0wwOixlMi5lKEUuaiFfI01bP2E4cApBZWlOa1xCc2VpcjpBPVlVVDQnRFBEK2JdWktfdG5GaydaWzU5YiwwOWwnJCVATEJHNztKXVE0ZW0/U1FiQWU+Ymw2YEc8bUxtJVtcLTIxOwpPTHFHbj9fMlVhT287aTZTPkQ4JCRDRSIwKGRXL1ZgaiFTQ29gJyJicVpDPzJbR2xSZyxMKl5kSFcwaGFxVlxOKX4+CmVuZHN0cmVhbQplbmRvYmoKMjMgMCBvYmoKPDwgL1R5cGUgL1hPYmplY3QKL1N1YnR5cGUgL0ltYWdlCi9XaWR0aCAxMTgKL0hlaWdodCA0OQovQ29sb3JTcGFjZSAvRGV2aWNlR3JheQovQml0c1BlckNvbXBvbmVudCA4Ci9MZW5ndGggNDYxCi9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiL2VKSV1SPyNYblhrVDZBPlhLbkRiV0IiTVpFYWpQcGQ0XScoXkBSbHQia0IiUzAkZiU/PW09NEM7Oy4kTihqUmNZUiVzZCZsOSRPdF4KKSY3PUwoNy1lcXFlQC4oL1NDOTg0LWZMWGVMWjVxY1o1bEFFQjU1PjNAMD1rIjtSaDJoQmNRTDMmSj81b1tjSDBiU0ZOXjw7O0A0MVNZOW0KYyJaST1ZbCNjNClgXyJZbG1OMyUuQS5sTlNgVmUvWTwlPy43KCgpLy5kQls7ayFKWyUnJURKXEk/K2E3OjVvTmtZXHFFUz4zPEk1YlptKEkKJWQ8QEIpOERidDNwS0djbGJRazEnaVpWczdOTTBcbyZSKnFVPmdIdS1GckNraDxrSEZHKlwkTT1fc1YvLSRcSkY6ZS8/PmZYQStDQ21wRGUKZFNQNkdjdSxcWCdBTD1hNUpDWzQ2Ry5ocDI9VTRlXiRlb1xRI2IqbTdDOCQtSkEoY1o/WWAnQzs2SnBIZVBsXCRIRUMhdV4qUWErNmdFTWsKW2ZFVipiLiM+cHI+LVdTZiM+aCZXP3Vra1RzaFlgPS9YLjY2QSo7YmlzL2RnQFFYWHNyOG07fj4KZW5kc3RyZWFtCmVuZG9iagoyNCAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDU0Ci9IZWlnaHQgNTQKL0NvbG9yU3BhY2UgL0RldmljZUdyYXkKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDc3Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiMEpkMFRkcSRqNG9GXlUsIkhUczlFSUU7MEFULF9FKkxaJW9AN0psNVY7SCdDcz1UcnFEYUguNEJmI2M0T1ZUOyhkI2Y8R0U5fj4KZW5kc3RyZWFtCmVuZG9iagoyNSAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDI3NwovSGVpZ2h0IDczCi9Db2xvclNwYWNlIC9EZXZpY2VHcmF5Ci9CaXRzUGVyQ29tcG9uZW50IDgKL0xlbmd0aCAxMzk0Ci9GaWx0ZXIgWy9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZV0KPj5zdHJlYW0KR2IiL2NnUSE0LSRxJ2pqNUwjcFpHdTY9I0g/JWghJFonRWs9WCZuTU9vK0xPY1gvbXImKVZsP0ttSitFbkU5ISNrSSNwOTYyYy02LE11dUEKb0ZaSG08JnBIZ1NgJEAobS03LVVRKDckSV1fSl5ZU0E3bScpQiY5LVo7Oz1aNT03Xj5KZEhedFRxcWYqXz1JLWQqb0BVWjpjT1soIWFJTGEKYjByalFXUDslUFhjP3M8cFRbTzFiI0trUEVgdUVCV1xKUl47dVxrPjRSVjlmNGdoIjYzSnU2ZUgtQit1QzE8IjdpVVdbU1cqOllYalpjIygKQjdfQFpCWmM1T1w8cEQ8Q0RrTmVMYTE3O0o+TV5qMmovMWUrJV9sLTctSStaV1U0NCkvWDFzMCZXMEsiUElwOWZWPyYpSUMqWkNiNWtrZ1MKL1JgMGlGNkNibS4/RyZQJiZMRnNVKkZsWlVgbSpBKDxaWi9pb1lEWmFdL2phJ1I5Jjk5SUhLVF8uVTA4LzZlZ1NBZkI8NF9dQT8jO1wsJi0KIkQiZkBrJTVDTzZGZDhyXW8ldU1hOCdFcXEmTS5hOFxgJFRpciMvdCwvO1NWMFAiOjkkX2VuNFBpaVhFUW4hY1BeLyxUZjlkaEJkJ0kuZUEKUW9QISkmMj42IUUqKlgrVTtcbWBKYWVhRyUiY3BdMidaNV9dTUtEVUc2WVpVKDxUbzJCbXMjdDlZbG5uWG83IzMkJDAhbSluLFJQYGApcm8KN09gNT5LYjcrdCYyJFRST0M0YjVQXFgpYCs/PStmLXJtc10yQj0/bzJXWnVgVmBHbjdrYG4sdFVJYjtzckJxRUw3NjJdIyFTYGMoRGtTX0gKWCYrc1lyVFw7PU1MRD1cZCp1S2ZWWXRmKkUjS0A8bFRbO24vbjNNLyw+LSFZQmpoKm41Vjg0U0VaJ2FlUC1Hb14pSCdwI1cvNHJuRTQraTEKK0lCRlA1Uys0PThGOSU3Tyo6ZipuM0otYTc2MmIzYiFOV0hWKWhGK21iLC1VLUU5U05oST4sVSo8LkdtcC0pMiQvLztJOm4+W2I3cUljKDYKcElAI05UZSlHY0s3YFliUFRmZERhbiNLbVBdV145KDZqbGNMQlFlVzdxTCMjPDNlNW8rPC0pNGNsNFR1XFwoYFNiJm8qRUAnYytqam1aUCoKNE5nRkdFXiQmOi4mXyVQRkBONWQ1dSFgR1Y2bylVS0c3OCsmW1A6TGIlMnRRNC9DbF9OTltXI3A/XkxqNCRtVlZTZCZOMCwzPUA4J0xRKHQKTGBuZWAvWXM4aiwlbSVQOl9xMnItbWRjPVhYNSY+OiNZO24+LipHcGZtVyc8OE9fRWtsPSkkTi9HRCtRSFhyWD5HLCVpYUtzRlBDNjVfLE0KQD8yXic5Mk1JVz8kZ2s1aEQ+YGtuOzFPLSViazVuXVteOj5QX0YsaWIzM3ErW249OCFibkBBbGViMltVU2NoT0VrXVdpV189KCQxOjM4KTsKIklWbHFLNDFOK1BsNjxBOmk4Uyg0PSc1cChjV2RCQmQtZSNgMVdoOzs6QXQzQ3Q+YURLQklQaWNdKzMyXTtnXTRXWEVDM2drPFBMMnFnLHMKJG5FSDJqP14haFMrUztVTGR0U2pAYV9fYjtsQGprRlxvPUs1PCgxUSRzP3BjJGZzLi5abUE9dD47X0UpRzVjNzkocyokJFZCITA2WyEoLGUKLVUzTFJKbCQwWFxKT1loQjYtdSsoV28oVCMsVD0qLVVkPiU8V3FTXmVqKyUrZWRqXksiVnNIMi5wSCZXYT5sdUxOMDRPWUo0TkJoZz9DcSwKLi9zS19UPElEX1AkQCc0fj4KZW5kc3RyZWFtCmVuZG9iagoyNiAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDExOAovSGVpZ2h0IDQ5Ci9Db2xvclNwYWNlIC9EZXZpY2VHcmF5Ci9CaXRzUGVyQ29tcG9uZW50IDgKL0xlbmd0aCA0NjEKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIvZUpJXVI/I1huWGtUNkE+WEtuRGJXQiJNWkVhalBwZDRdJyheQFJsdCJrQiJTMCRmJT89bT00Qzs7LiROKGpSY1lSJXNkJmw5JE90XgopJjc9TCg3LWVxcWVALigvU0M5ODQtZkxYZUxaNXFjWjVsQUVCNTU+M0AwPWsiO1JoMmhCY1FMMyZKPzVvW2NIMGJTRk5ePDs7QDQxU1k5bQpjIlpJPVlsI2M0KWBfIllsbU4zJS5BLmxOU2BWZS9ZPCU/LjcoKCkvLmRCWztrIUpbJSclREpcST8rYTc6NW9Oa1lccUVTPjM8STViWm0oSQolZDxAQik4RGJ0M3BLR2NsYlFrMSdpWlZzN05NMFxvJlIqcVU+Z0h1LUZyQ2toPGtIRkcqXCRNPV9zVi8tJFxKRjplLz8+ZlhBK0NDbXBEZQpkU1A2R2N1LFxYJ0FMPWE1SkNbNDZHLmhwMj1VNGVeJGVvXFEjYiptN0M4JC1KQShjWj9ZYCdDOzZKcEhlUGxcJEhFQyF1XipRYSs2Z0VNawpbZkVWKmIuIz5wcj4tV1NmIz5oJlc/dWtrVHNoWWA9L1guNjZBKjtiaXMvZGdAUVhYc3I4bTt+PgplbmRzdHJlYW0KZW5kb2JqCjI3IDAgb2JqCjw8IC9UeXBlIC9YT2JqZWN0Ci9TdWJ0eXBlIC9JbWFnZQovV2lkdGggNTQKL0hlaWdodCA1NAovQ29sb3JTcGFjZSAvRGV2aWNlR3JheQovQml0c1BlckNvbXBvbmVudCA4Ci9MZW5ndGggNzcKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIwSmQwVGRxJGo0b0ZeVSwiSFRzOUVJRTswQVQsX0UqTFolb0A3Smw1VjtIJ0NzPVRycURhSC40QmYjYzRPVlQ7KGQjZjxHRTl+PgplbmRzdHJlYW0KZW5kb2JqCnhyZWYKMCAyOAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA1OCAwMDAwMCBuIAowMDAwMDAwMTA0IDAwMDAwIG4gCjAwMDAwMDAxNzYgMDAwMDAgbiAKMDAwMDAwMDIyOCAwMDAwMCBuIAowMDAwMDAwMzI2IDAwMDAwIG4gCjAwMDAwMDA0MjkgMDAwMDAgbiAKMDAwMDAwMDUzNSAwMDAwMCBuIAowMDAwMDAwNjQ1IDAwMDAwIG4gCjAwMDAwMDA3NDEgMDAwMDAgbiAKMDAwMDAwMDg0MyAwMDAwMCBuIAowMDAwMDAwOTQ4IDAwMDAwIG4gCjAwMDAwMDEwNTcgMDAwMDAgbiAKMDAwMDAwMTE1OCAwMDAwMCBuIAowMDAwMDAxMjU4IDAwMDAwIG4gCjAwMDAwMDEzNjAgMDAwMDAgbiAKMDAwMDAwMTQ2NiAwMDAwMCBuIAowMDAwMDAxNjM2IDAwMDAwIG4gCjAwMDAwMDIwNTMgMDAwMDAgbiAKMDAwMDAwMjQ3MCAwMDAwMCBuIAowMDAwMDAyODg3IDAwMDAwIG4gCjAwMDAwMDU1ODYgMDAwMDAgbiAKMDAwMDAwODc0MiAwMDAwMCBuIAowMDAwMDA5Mzg5IDAwMDAwIG4gCjAwMDAwMDk2NTAgMDAwMDAgbiAKMDAwMDAxMTIzMSAwMDAwMCBuIAowMDAwMDExODc4IDAwMDAwIG4gCnRyYWlsZXIKPDwKL0luZm8gMTcgMCBSCi9TaXplIDI4Ci9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgoxMjEzOQolJUVPRgo=</Image>
                        </Parts>
                    </Label>
                    <SignatureOption>SERVICE_DEFAULT</SignatureOption>
                </CompletedPackageDetails>
            </CompletedShipmentDetail>
        </ProcessShipmentReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

ShipmentCancelRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v23="http://fedex.com/ws/ship/v23">
    <tns:Body>
        <v23:DeleteShipmentRequest>
            <v23:WebAuthenticationDetail>
                <v23:UserCredential>
                    <v23:Key>user_key</v23:Key>
                    <v23:Password>password</v23:Password>
                </v23:UserCredential>
            </v23:WebAuthenticationDetail>
            <v23:ClientDetail>
                <v23:AccountNumber>2349857</v23:AccountNumber>
                <v23:MeterNumber>1293587</v23:MeterNumber>
            </v23:ClientDetail>
            <v23:TransactionDetail>
                <v23:CustomerTransactionId>Delete Shipment</v23:CustomerTransactionId>
            </v23:TransactionDetail>
            <v23:Version>
                <v23:ServiceId>ship</v23:ServiceId>
                <v23:Major>23</v23:Major>
                <v23:Intermediate>0</v23:Intermediate>
                <v23:Minor>0</v23:Minor>
            </v23:Version>
            <v23:TrackingId>
                <v23:TrackingIdType>EXPRESS</v23:TrackingIdType>
                <v23:TrackingNumber>794947717776</v23:TrackingNumber>
            </v23:TrackingId>
            <v23:DeletionControl>DELETE_ALL_PACKAGES</v23:DeletionControl>
        </v23:DeleteShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""

ShipmentCancelResponseXML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header/>
   <SOAP-ENV:Body>
      <ShipmentReply xmlns="http://fedex.com/ws/ship/v26">
         <HighestSeverity>SUCCESS</HighestSeverity>
         <Notifications>
            <Severity>SUCCESS</Severity>
            <Source>ship</Source>
            <Code>0000</Code>
            <Message>Success</Message>
            <LocalizedMessage>Success</LocalizedMessage>
         </Notifications>
         <TransactionDetail>
            <CustomerTransactionId>DeleteShipmentRequest_v26</CustomerTransactionId>
         </TransactionDetail>
         <Version>
            <ServiceId>ship</ServiceId>
            <Major>26</Major>
            <Intermediate>0</Intermediate>
            <Minor>0</Minor>
         </Version>
      </ShipmentReply>
   </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""
