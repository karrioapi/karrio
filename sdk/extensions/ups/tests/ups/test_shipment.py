import unittest
import logging
from unittest.mock import patch, ANY
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from karrio import Shipment
from .fixture import gateway, LABEL


class TestUPSShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**package_shipment_data)
        self.ShipmentCancelRequest = ShipmentCancelRequest(
            **shipment_cancel_request_data
        )

    def test_create_package_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequestXML)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequestXML)

    def test_create_package_shipment_with_package_preset_request(self):
        request = gateway.mapper.create_shipment_request(
            ShipmentRequest(**package_shipment_with_package_preset_data)
        )
        self.assertEqual(request.serialize(), ShipmentRequestWithPresetXML)

    @patch("karrio.mappers.ups.proxy.lib.request", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        Shipment.create(self.ShipmentRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/webservices/Ship")

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = NegotiatedShipmentResponseXML
            parsed_response = (
                Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                DP.to_dict(parsed_response), NegotiatedParsedShipmentResponse
            )

    def test_parse_publish_rate_shipment_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = (
                Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponseXML
            parsed_response = (
                Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedShipmentCancelResponse
            )


if __name__ == "__main__":
    unittest.main()


shipment_cancel_request_data = {"shipment_identifier": "1ZWA82900191640782"}

package_shipment_data = {
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
    "service": "ups_express",
    "options": {"email_notification_to": "test@mail.com"},
    "payment": {"paid_by": "sender"},
    "reference": "Your Customer Context",
}

package_shipment_with_package_preset_data = {
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
    "service": "ups_express",
    "payment": {"paid_by": "sender"},
    "options": {"email_notification_to": "test@mail.com"},
    "reference": "Your Customer Context",
    "label_type": "ZPL",
}


NegotiatedParsedShipmentResponse = [
    {
        "carrier_name": "ups",
        "carrier_id": "ups",
        "tracking_number": "1ZWA82900191640782",
        "shipment_identifier": "1ZWA82900191640782",
        "docs": {"label": ANY},
    },
    [],
]

ParsedShipmentResponse = [
    {
        "carrier_name": "ups",
        "carrier_id": "ups",
        "tracking_number": "1ZWA82900191640782",
        "shipment_identifier": "1ZWA82900191640782",
        "docs": {"label": ANY},
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


NegotiatedShipmentResponseXML = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header />
    <soapenv:Body>
        <ship:ShipmentResponse xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0">
            <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                <common:ResponseStatus>
                    <common:Code>1</common:Code>
                    <common:Description>Success</common:Description>
                </common:ResponseStatus>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Response>
            <ship:ShipmentResults>
                <ship:ShipmentCharges>
                    <ship:TransportationCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>88.12</ship:MonetaryValue>
                    </ship:TransportationCharges>
                    <ship:ServiceOptionsCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>0.00</ship:MonetaryValue>
                    </ship:ServiceOptionsCharges>
                    <ship:TotalCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>88.12</ship:MonetaryValue>
                    </ship:TotalCharges>
                </ship:ShipmentCharges>
                <ship:NegotiatedRateCharges>
                    <ship:TotalCharge>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>70.00</ship:MonetaryValue>
                    </ship:TotalCharge>
                </ship:NegotiatedRateCharges>
                <ship:BillingWeight>
                    <ship:UnitOfMeasurement>
                        <ship:Code>LBS</ship:Code>
                        <ship:Description>Pounds</ship:Description>
                    </ship:UnitOfMeasurement>
                    <ship:Weight>10.0</ship:Weight>
                </ship:BillingWeight>
                <ship:ShipmentIdentificationNumber>1ZWA82900191640782</ship:ShipmentIdentificationNumber>
                <ship:PackageResults>
                    <ship:TrackingNumber>1ZWA82900191640782</ship:TrackingNumber>
                    <ship:ServiceOptionsCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>0.00</ship:MonetaryValue>
                    </ship:ServiceOptionsCharges>
                    <ship:ShippingLabel>
                        <ship:ImageFormat>
                            <ship:Code>GIF</ship:Code>
                            <ship:Description>GIF</ship:Description>
                        </ship:ImageFormat>
                        <ship:GraphicImage>{LABEL}</ship:GraphicImage>
                        <ship:HTMLImage>PCFET0NUWVBFIEhUTUwgUFVCTElD(Truncated)</ship:HTMLImage>
                    </ship:ShippingLabel>
                </ship:PackageResults>
            </ship:ShipmentResults>
        </ship:ShipmentResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentResponseXML = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header />
    <soapenv:Body>
        <ship:ShipmentResponse xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0">
            <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                <common:ResponseStatus>
                    <common:Code>1</common:Code>
                    <common:Description>Success</common:Description>
                </common:ResponseStatus>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Response>
            <ship:ShipmentResults>
                <ship:ShipmentCharges>
                    <ship:TransportationCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>88.12</ship:MonetaryValue>
                    </ship:TransportationCharges>
                    <ship:ServiceOptionsCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>0.00</ship:MonetaryValue>
                    </ship:ServiceOptionsCharges>
                    <ship:TotalCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>88.12</ship:MonetaryValue>
                    </ship:TotalCharges>
                </ship:ShipmentCharges>
                <ship:BillingWeight>
                    <ship:UnitOfMeasurement>
                        <ship:Code>LBS</ship:Code>
                        <ship:Description>Pounds</ship:Description>
                    </ship:UnitOfMeasurement>
                    <ship:Weight>10.0</ship:Weight>
                </ship:BillingWeight>
                <ship:ShipmentIdentificationNumber>1ZWA82900191640782</ship:ShipmentIdentificationNumber>
                <ship:PackageResults>
                    <ship:TrackingNumber>1ZWA82900191640782</ship:TrackingNumber>
                    <ship:ServiceOptionsCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>0.00</ship:MonetaryValue>
                    </ship:ServiceOptionsCharges>
                    <ship:ShippingLabel>
                        <ship:ImageFormat>
                            <ship:Code>GIF</ship:Code>
                            <ship:Description>GIF</ship:Description>
                        </ship:ImageFormat>
                        <ship:GraphicImage>{LABEL}</ship:GraphicImage>
                        <ship:HTMLImage>PCFET0NUWVBFIEhUTUwgUFVCTElDICI(Truncated)</ship:HTMLImage>
                    </ship:ShippingLabel>
                </ship:PackageResults>
            </ship:ShipmentResults>
        </ship:ShipmentResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentRequestXML = """<tns:Envelope xmlns:auth="http://www.ups.com/schema/xpci/1.0/auth" xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0" xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0" xmlns:ifs="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0">
    <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <ship:ShipmentRequest>
            <common:Request>
                <common:RequestOption>validate</common:RequestOption>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Request>
            <ship:Shipment>
                <ship:Description>Description</ship:Description>
                <ship:Shipper>
                    <ship:Name>Shipper Name</ship:Name>
                    <ship:AttentionName>Shipper Attn Name</ship:AttentionName>
                    <ship:TaxIdentificationNumber>123456</ship:TaxIdentificationNumber>
                    <ship:Phone>
                        <ship:Number>1234567890</ship:Number>
                    </ship:Phone>
                    <ship:ShipperNumber>Your Account Number</ship:ShipperNumber>
                    <ship:Address>
                        <ship:AddressLine>Address Line</ship:AddressLine>
                        <ship:City>City</ship:City>
                        <ship:StateProvinceCode>StateProvinceCode</ship:StateProvinceCode>
                        <ship:PostalCode>PostalCode</ship:PostalCode>
                        <ship:CountryCode>CountryCode</ship:CountryCode>
                    </ship:Address>
                </ship:Shipper>
                <ship:ShipTo>
                    <ship:Name>Ship To Name</ship:Name>
                    <ship:AttentionName>Ship To Attn Name</ship:AttentionName>
                    <ship:Phone>
                        <ship:Number>1234567890</ship:Number>
                    </ship:Phone>
                    <ship:Address>
                        <ship:AddressLine>Address Line</ship:AddressLine>
                        <ship:City>City</ship:City>
                        <ship:StateProvinceCode>StateProvinceCode</ship:StateProvinceCode>
                        <ship:PostalCode>PostalCode</ship:PostalCode>
                        <ship:CountryCode>CountryCode</ship:CountryCode>
                    </ship:Address>
                </ship:ShipTo>
                <ship:PaymentInformation>
                    <ship:ShipmentCharge>
                        <ship:Type>01</ship:Type>
                        <ship:BillShipper>
                            <ship:AccountNumber>Your Account Number</ship:AccountNumber>
                        </ship:BillShipper>
                    </ship:ShipmentCharge>
                </ship:PaymentInformation>
                <ship:ReferenceNumber>
                    <ship:Code>CountryCode</ship:Code>
                    <ship:Value>Your Customer Context</ship:Value>
                </ship:ReferenceNumber>
                <ship:Service>
                    <ship:Code>01</ship:Code>
                </ship:Service>
                <ship:ShipmentServiceOptions>
                    <ship:Notification>
                        <ship:NotificationCode>8</ship:NotificationCode>
                        <ship:EMail>
                            <ship:EMailAddress>test@mail.com</ship:EMailAddress>
                        </ship:EMail>
                    </ship:Notification>
                </ship:ShipmentServiceOptions>
                <ship:Package>
                    <ship:Description>Description</ship:Description>
                    <ship:Packaging>
                        <ship:Code>02</ship:Code>
                    </ship:Packaging>
                    <ship:Dimensions>
                        <ship:UnitOfMeasurement>
                            <ship:Code>IN</ship:Code>
                        </ship:UnitOfMeasurement>
                        <ship:Length>7.0</ship:Length>
                        <ship:Width>5.0</ship:Width>
                        <ship:Height>2.0</ship:Height>
                    </ship:Dimensions>
                    <ship:PackageWeight>
                        <ship:UnitOfMeasurement>
                            <ship:Code>LBS</ship:Code>
                        </ship:UnitOfMeasurement>
                        <ship:Weight>10.0</ship:Weight>
                    </ship:PackageWeight>
                </ship:Package>
            </ship:Shipment>
            <ship:LabelSpecification>
                <ship:LabelImageFormat>
                    <ship:Code>GIF</ship:Code>
                </ship:LabelImageFormat>
                <ship:LabelStockSize>
                    <ship:Height>6</ship:Height>
                    <ship:Width>4</ship:Width>
                </ship:LabelStockSize>
            </ship:LabelSpecification>
        </ship:ShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""

ShipmentRequestWithPresetXML = """<tns:Envelope xmlns:auth="http://www.ups.com/schema/xpci/1.0/auth" xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0" xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0" xmlns:ifs="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0">
    <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <ship:ShipmentRequest>
            <common:Request>
                <common:RequestOption>validate</common:RequestOption>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Request>
            <ship:Shipment>
                <ship:Description>Description</ship:Description>
                <ship:Shipper>
                    <ship:Name>Shipper Name</ship:Name>
                    <ship:AttentionName>Shipper Attn Name</ship:AttentionName>
                    <ship:TaxIdentificationNumber>123456</ship:TaxIdentificationNumber>
                    <ship:Phone>
                        <ship:Number>1234567890</ship:Number>
                    </ship:Phone>
                    <ship:ShipperNumber>Your Account Number</ship:ShipperNumber>
                    <ship:Address>
                        <ship:AddressLine>Address Line</ship:AddressLine>
                        <ship:City>City</ship:City>
                        <ship:StateProvinceCode>StateProvinceCode</ship:StateProvinceCode>
                        <ship:PostalCode>PostalCode</ship:PostalCode>
                        <ship:CountryCode>CountryCode</ship:CountryCode>
                    </ship:Address>
                </ship:Shipper>
                <ship:ShipTo>
                    <ship:Name>Ship To Name</ship:Name>
                    <ship:AttentionName>Ship To Attn Name</ship:AttentionName>
                    <ship:Phone>
                        <ship:Number>1234567890</ship:Number>
                    </ship:Phone>
                    <ship:Address>
                        <ship:AddressLine>Address Line</ship:AddressLine>
                        <ship:City>City</ship:City>
                        <ship:StateProvinceCode>StateProvinceCode</ship:StateProvinceCode>
                        <ship:PostalCode>PostalCode</ship:PostalCode>
                        <ship:CountryCode>CountryCode</ship:CountryCode>
                    </ship:Address>
                </ship:ShipTo>
                <ship:PaymentInformation>
                    <ship:ShipmentCharge>
                        <ship:Type>01</ship:Type>
                        <ship:BillShipper>
                            <ship:AccountNumber>Your Account Number</ship:AccountNumber>
                        </ship:BillShipper>
                    </ship:ShipmentCharge>
                </ship:PaymentInformation>
                <ship:ReferenceNumber>
                    <ship:Code>CountryCode</ship:Code>
                    <ship:Value>Your Customer Context</ship:Value>
                </ship:ReferenceNumber>
                <ship:Service>
                    <ship:Code>01</ship:Code>
                </ship:Service>
                <ship:ShipmentServiceOptions>
                    <ship:Notification>
                        <ship:NotificationCode>8</ship:NotificationCode>
                        <ship:EMail>
                            <ship:EMailAddress>test@mail.com</ship:EMailAddress>
                        </ship:EMail>
                    </ship:Notification>
                </ship:ShipmentServiceOptions>
                <ship:Package>
                    <ship:Description>Description</ship:Description>
                    <ship:Packaging>
                        <ship:Code>02</ship:Code>
                    </ship:Packaging>
                    <ship:Dimensions>
                        <ship:UnitOfMeasurement>
                            <ship:Code>IN</ship:Code>
                        </ship:UnitOfMeasurement>
                        <ship:Length>3.0</ship:Length>
                        <ship:Width>16.0</ship:Width>
                        <ship:Height>11.0</ship:Height>
                    </ship:Dimensions>
                    <ship:PackageWeight>
                        <ship:UnitOfMeasurement>
                            <ship:Code>LBS</ship:Code>
                        </ship:UnitOfMeasurement>
                        <ship:Weight>30.0</ship:Weight>
                    </ship:PackageWeight>
                </ship:Package>
            </ship:Shipment>
            <ship:LabelSpecification>
                <ship:LabelImageFormat>
                    <ship:Code>ZPL</ship:Code>
                </ship:LabelImageFormat>
                <ship:LabelStockSize>
                    <ship:Height>6</ship:Height>
                    <ship:Width>4</ship:Width>
                </ship:LabelStockSize>
            </ship:LabelSpecification>
        </ship:ShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""

ShipmentCancelRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:void="http://www.ups.com/XMLSchema/XOLTWS/Void/v1.1">
    <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <void:VoidShipmentRequest>
            <common:Request>
                <common:TransactionReference>
                    <common:CustomerContext>1ZWA82900191640782</common:CustomerContext>
                </common:TransactionReference>
            </common:Request>
            <void:VoidShipment>
                <void:ShipmentIdentificationNumber>1ZWA82900191640782</void:ShipmentIdentificationNumber>
            </void:VoidShipment>
        </void:VoidShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""

ShipmentCancelResponseXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header/>
    <soapenv:Body>
        <void:VoidShipmentResponse xmlns:void="http://www.ups.com/XMLSchema/XOLTWS/Void/v1.1">
            <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                <common:ResponseStatus>
                    <common:Code>1</common:Code>
                    <common:Description>Success</common:Description>
                </common:ResponseStatus>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Response>
            <void:SummaryResult>
                <void:Status>
                    <void:Code>1</void:Code>
                    <void:Description>Voided</void:Description>
                </void:Status>
            </void:SummaryResult>
        </void:VoidShipmentResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""
