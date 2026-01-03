"""ParcelOne rate tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestParcelOneRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            print(parsed_response)
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_rate_error_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = RateErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            print(parsed_response)
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateErrorResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "company_name": "Test Shipper",
        "address_line1": "Teststrasse 123",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
    },
    "recipient": {
        "person_name": "Test Recipient",
        "address_line1": "Empfangerweg 456",
        "city": "Munich",
        "postal_code": "80331",
        "country_code": "DE",
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
    "services": ["parcelone_dhl_paket"],
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "parcelone",
            "carrier_name": "parcelone",
            "currency": "EUR",
            "extra_charges": [
                {"amount": 4.99, "currency": "EUR", "name": "Base shipping"},
                {"amount": 1.0, "currency": "EUR", "name": "Fuel surcharge"},
            ],
            "meta": {"service_name": "parcelone_dhl_paket"},
            "service": "parcelone_dhl_paket",
            "total_charge": 5.99,
        }
    ],
    [],
]

ParsedRateErrorResponse = [
    [],
    [
        {
            "carrier_id": "parcelone",
            "carrier_name": "parcelone",
            "code": "E002",
            "message": "Route not available",
        }
    ],
]


RateRequest = """<?xml version="1.0" encoding="utf-8"?>
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
        <tns:getCharges>
            <tns:ChargesData>
                <wcf:Charges xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <CEPID>DHL</CEPID>
    <ConsignerID>TEST_CONSIGNER</ConsignerID>
    <MandatorID>TEST_MANDATOR</MandatorID>
    <tns:Packages>
        <tns:ShipmentPackage>
            <tns:PackageDimensions>
                <Height>15.0</Height>
                <Length>30.0</Length>
                <Measurement>CM</Measurement>
                <Width>20.0</Width>
            </tns:PackageDimensions>
            <tns:PackageWeight>
                <Unit>KG</Unit>
                <Value>5.0</Value>
            </tns:PackageWeight>
        </tns:ShipmentPackage>
    </tns:Packages>
    <PrivateAddressIndicator>0</PrivateAddressIndicator>
    <ProductID>PAKET</ProductID>
    <tns:ShipToAddress>
        <City>Munich</City>
        <Country>DE</Country>
        <PostalCode>80331</PostalCode>
    </tns:ShipToAddress>
</wcf:Charges>

            </tns:ChargesData>
        </tns:getCharges>
    </soapenv:Body>
</soapenv:Envelope>"""


RateResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <soap:Body>
        <getChargesResponse xmlns="http://tempuri.org/">
            <getChargesResult>
                <wcf:ChargesResult>
                    <wcf:ActionResult>
                        <wcf:Success>1</wcf:Success>
                    </wcf:ActionResult>
                    <wcf:TotalCharges>
                        <wcf:Value>5.99</wcf:Value>
                        <wcf:Currency>EUR</wcf:Currency>
                    </wcf:TotalCharges>
                    <wcf:ShipmentCharges>
                        <wcf:Amount>
                            <wcf:Value>4.99</wcf:Value>
                            <wcf:Currency>EUR</wcf:Currency>
                            <wcf:Description>Base shipping</wcf:Description>
                        </wcf:Amount>
                        <wcf:Amount>
                            <wcf:Value>1.00</wcf:Value>
                            <wcf:Currency>EUR</wcf:Currency>
                            <wcf:Description>Fuel surcharge</wcf:Description>
                        </wcf:Amount>
                    </wcf:ShipmentCharges>
                    <wcf:PackageResults>
                        <wcf:ChargesPackageResult>
                            <wcf:PackageID>PKG001</wcf:PackageID>
                            <wcf:Charges>
                                <wcf:Amount>
                                    <wcf:Value>5.99</wcf:Value>
                                    <wcf:Currency>EUR</wcf:Currency>
                                </wcf:Amount>
                            </wcf:Charges>
                        </wcf:ChargesPackageResult>
                    </wcf:PackageResults>
                </wcf:ChargesResult>
            </getChargesResult>
        </getChargesResponse>
    </soap:Body>
</soap:Envelope>"""


RateErrorResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <soap:Body>
        <getChargesResponse xmlns="http://tempuri.org/">
            <getChargesResult>
                <wcf:ChargesResult>
                    <wcf:ActionResult>
                        <wcf:Success>0</wcf:Success>
                        <wcf:Errors>
                            <wcf:Error>
                                <wcf:ErrorNo>E002</wcf:ErrorNo>
                                <wcf:Message>Route not available</wcf:Message>
                            </wcf:Error>
                        </wcf:Errors>
                    </wcf:ActionResult>
                </wcf:ChargesResult>
            </getChargesResult>
        </getChargesResponse>
    </soap:Body>
</soap:Envelope>"""
