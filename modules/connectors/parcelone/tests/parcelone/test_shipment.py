"""ParcelOne shipment tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestParcelOneShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
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
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            print(parsed_response)
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_shipment_error_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = ShipmentErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedShipmentErrorResponse
            )

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "company_name": "Test Shipper",
        "address_line1": "Teststrasse 123",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "email": "shipper@test.com",
        "phone_number": "+49301234567",
    },
    "recipient": {
        "person_name": "Test Recipient",
        "address_line1": "Empfangerweg 456",
        "city": "Munich",
        "postal_code": "80331",
        "country_code": "DE",
        "email": "recipient@test.com",
        "phone_number": "+498912345678",
    },
    "parcels": [
        {
            "weight": 5.0,
            "weight_unit": "KG",
            "length": 30.0,
            "width": 20.0,
            "height": 15.0,
            "dimension_unit": "CM",
        }
    ],
    "service": "parcelone_dhl_paket",
}

ShipmentCancelPayload = {
    "shipment_identifier": "123456789012",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "docs": {"label": "JVBERi0xLjQKJeLjz9MKMSAwIG9iag=="},
        "label_type": "PDF",
        "meta": {
            "currency": "EUR",
            "shipment_id": "SHIP001",
            "total_charge": 5.99,
            "tracking_numbers": ["123456789012"],
        },
        "shipment_identifier": "SHIP001",
        "tracking_number": "123456789012",
    },
    [],
]

ParsedShipmentErrorResponse = [
    None,
    [
        {
            "carrier_id": "parcelone",
            "carrier_name": "parcelone",
            "code": "E001",
            "message": "Invalid postal code",
        }
    ],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = """<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:tns="http://tempuri.org/"
    xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF"
    xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
    <soapenv:Header>
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <wsse:UsernameToken>
                <wsse:Username>test_user</wsse:Username>
                <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">test_password</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soapenv:Header>
    <soapenv:Body>
        <tns:registerShipments>
            <tns:ShippingData>
                <wcf:Shipment xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <CEPID>DHL</CEPID>
    <ConsignerID>TEST_CONSIGNER</ConsignerID>
    <tns:LabelFormat>
        <Size>100x150</Size>
        <Type>PDF</Type>
    </tns:LabelFormat>
    <MandatorID>TEST_MANDATOR</MandatorID>
    <tns:Packages>
        <tns:ShipmentPackage>
            <tns:PackageDimensions>
                <Height>15.0</Height>
                <Length>30.0</Length>
                <Measurement>CM</Measurement>
                <Width>20.0</Width>
            </tns:PackageDimensions>
            <PackageRef>1</PackageRef>
            <tns:PackageWeight>
                <Unit>KG</Unit>
                <Value>5.0</Value>
            </tns:PackageWeight>
        </tns:ShipmentPackage>
    </tns:Packages>
    <PrintLabel>1</PrintLabel>
    <ProductID>PAKET</ProductID>
    <tns:ShipFromData>
        <Name1>Test Shipper</Name1>
        <tns:ShipmentAddress>
            <City>Berlin</City>
            <Country>DE</Country>
            <PostalCode>10115</PostalCode>
            <Street>123 Teststrasse</Street>
            <Streetno>123</Streetno>
        </tns:ShipmentAddress>
        <tns:ShipmentContact>
            <Company>Test Shipper</Company>
            <Email>shipper@test.com</Email>
            <Phone>+49301234567</Phone>
        </tns:ShipmentContact>
    </tns:ShipFromData>
    <tns:ShipToData>
        <Name1>Test Recipient</Name1>
        <PrivateAddressIndicator>0</PrivateAddressIndicator>
        <tns:ShipmentAddress>
            <City>Munich</City>
            <Country>DE</Country>
            <PostalCode>80331</PostalCode>
            <Street>456 Empfangerweg</Street>
            <Streetno>456</Streetno>
        </tns:ShipmentAddress>
        <tns:ShipmentContact>
            <Email>recipient@test.com</Email>
            <Phone>+498912345678</Phone>
        </tns:ShipmentContact>
    </tns:ShipToData>
    <ShipmentRef></ShipmentRef>
    <Software>Karrio</Software>
</wcf:Shipment>

            </tns:ShippingData>
        </tns:registerShipments>
    </soapenv:Body>
</soapenv:Envelope>"""


ShipmentCancelRequest = """<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:tns="http://tempuri.org/"
    xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF"
    xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
    <soapenv:Header>
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <wsse:UsernameToken>
                <wsse:Username>test_user</wsse:Username>
                <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">test_password</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soapenv:Header>
    <soapenv:Body>
        <tns:voidShipments>
            <tns:ShippingData>
                <wcf:identifyShipment xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <ShipmentRefField>ShipmentID</ShipmentRefField>
    <ShipmentRefValue>123456789012</ShipmentRefValue>
</wcf:identifyShipment>

            </tns:ShippingData>
        </tns:voidShipments>
    </soapenv:Body>
</soapenv:Envelope>"""


ShipmentResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <soap:Body>
        <registerShipmentsResponse xmlns="http://tempuri.org/">
            <registerShipmentsResult>
                <wcf:ShipmentResult>
                    <wcf:ActionResult>
                        <wcf:Success>1</wcf:Success>
                        <wcf:ShipmentID>SHIP001</wcf:ShipmentID>
                        <wcf:TrackingID>123456789012</wcf:TrackingID>
                    </wcf:ActionResult>
                    <wcf:PackageResults>
                        <wcf:ShipmentPackageResult>
                            <wcf:PackageID>PKG001</wcf:PackageID>
                            <wcf:TrackingID>123456789012</wcf:TrackingID>
                            <wcf:Label>JVBERi0xLjQKJeLjz9MKMSAwIG9iag==</wcf:Label>
                        </wcf:ShipmentPackageResult>
                    </wcf:PackageResults>
                    <wcf:TotalCharges>
                        <wcf:Value>5.99</wcf:Value>
                        <wcf:Currency>EUR</wcf:Currency>
                    </wcf:TotalCharges>
                    <wcf:LabelsAvailable>1</wcf:LabelsAvailable>
                </wcf:ShipmentResult>
            </registerShipmentsResult>
        </registerShipmentsResponse>
    </soap:Body>
</soap:Envelope>"""


ShipmentErrorResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <soap:Body>
        <registerShipmentsResponse xmlns="http://tempuri.org/">
            <registerShipmentsResult>
                <wcf:ShipmentResult>
                    <wcf:ActionResult>
                        <wcf:Success>0</wcf:Success>
                        <wcf:Errors>
                            <wcf:Error>
                                <wcf:ErrorNo>E001</wcf:ErrorNo>
                                <wcf:Message>Invalid postal code</wcf:Message>
                            </wcf:Error>
                        </wcf:Errors>
                    </wcf:ActionResult>
                </wcf:ShipmentResult>
            </registerShipmentsResult>
        </registerShipmentsResponse>
    </soap:Body>
</soap:Envelope>"""


ShipmentCancelResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <soap:Body>
        <voidShipmentsResponse xmlns="http://tempuri.org/">
            <voidShipmentsResult>
                <wcf:ShipmentActionResult>
                    <wcf:Success>1</wcf:Success>
                    <wcf:ShipmentID>SHIP001</wcf:ShipmentID>
                    <wcf:TrackingID>123456789012</wcf:TrackingID>
                </wcf:ShipmentActionResult>
            </voidShipmentsResult>
        </voidShipmentsResponse>
    </soap:Body>
</soap:Envelope>"""
