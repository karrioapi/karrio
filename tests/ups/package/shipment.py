import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import ShipmentRequest
from purplship.package import shipment
from tests.ups.package.fixture import gateway


class TestUPSShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**package_shipment_data)

    def test_create_package_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(request.serialize(), ShipmentRequestXML)

    @patch("purplship.package.mappers.ups.proxy.http", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        shipment.create(self.ShipmentRequest).with_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/Ship")

    def test_parse_shipment_response(self):
        with patch("purplship.package.mappers.ups.proxy.http") as mock:
            mock.return_value = NegotiatedShipmentResponseXML
            parsed_response = (
                shipment.create(self.ShipmentRequest).with_(gateway).parse()
            )
            self.assertEqual(
                to_dict(parsed_response), to_dict(NegotiatedParsedShipmentResponse)
            )

    def test_parse_publish_rate_shipment_response(self):
        with patch("purplship.package.mappers.ups.proxy.http") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = (
                shipment.create(self.ShipmentRequest).with_(gateway).parse()
            )
            self.assertEqual(to_dict(parsed_response), to_dict(ParsedShipmentResponse))


if __name__ == "__main__":
    unittest.main()


package_shipment_data = {
    "shipper": {
        "company_name": "Shipper Name",
        "person_name": "Shipper Attn Name",
        "federal_tax_id": "123456",
        "phone_number": "1234567890",
        "address_line_1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "person_name": "Ship To Attn Name",
        "phone_number": "1234567890",
        "address_line_1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "parcel": {
        "reference": "Your Customer Context",
        "services": ["ups_express"],
        "dimension_unit": "IN",
        "weight_unit": "LB",
        "packaging_type": "ups_customer_supplied_package",
        "description": "Description",
        "length": 7,
        "width": 5,
        "height": 2,
        "weight": 10,
        "options": {
            "notification": {
                "email": "test@mail.com"
            }
        }
    },
    "payment": {"paid_by": "sender"},
    "label": {"format": "GIF"},
}


NegotiatedParsedShipmentResponse = [
    {
        "carrier": "UPS",
        "charges": [
            {"amount": "88.12", "currency": "USD", "name": None},
            {"amount": "0.00", "currency": "USD", "name": None},
        ],
        "documents": ["R0lGODdheAUgA+cAAAAAAAEBAQIC (Truncated)"],
        "reference": {"type": "CustomerContext", "value": "Your Customer Context"},
        "service": None,
        "shipment_date": None,
        "total_charge": {
            "amount": "70.00",
            "currency": "USD",
            "name": "Shipment charge",
        },
        "tracking_number": "1ZWA82900191640782",
    },
    [],
]

ParsedShipmentResponse = [
    {
        "carrier": "UPS",
        "charges": [
            {"amount": "88.12", "currency": "USD", "name": None},
            {"amount": "0.00", "currency": "USD", "name": None},
        ],
        "documents": ["R0lGODdheAUgA+c(Truncated)"],
        "reference": {"type": "CustomerContext", "value": "Your Customer Context"},
        "service": None,
        "shipment_date": None,
        "total_charge": {
            "amount": "88.12",
            "currency": "USD",
            "name": "Shipment charge",
        },
        "tracking_number": "1ZWA82900191640782",
    },
    [],
]


NegotiatedShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
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
                        <ship:GraphicImage>R0lGODdheAUgA+cAAAAAAAEBAQIC (Truncated)</ship:GraphicImage>
                        <ship:HTMLImage>PCFET0NUWVBFIEhUTUwgUFVCTElD(Truncated)</ship:HTMLImage>
                    </ship:ShippingLabel>
                </ship:PackageResults>
            </ship:ShipmentResults>
        </ship:ShipmentResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
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
                        <ship:GraphicImage>R0lGODdheAUgA+c(Truncated)</ship:GraphicImage>
                        <ship:HTMLImage>PCFET0NUWVBFIEhUTUwgUFVCTElDICI(Truncated)</ship:HTMLImage>
                    </ship:ShippingLabel>
                </ship:PackageResults>
            </ship:ShipmentResults>
        </ship:ShipmentResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentRequestXML = """<tns:Envelope  xmlns:auth="http://www.ups.com/schema/xpci/1.0/auth" xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0" xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0" xmlns:ifs="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0" >
    <tns:Header>
        <upss:UPSSecurity>
            <UsernameToken>
                <Username>username</Username>
                <Password>password</Password>
            </UsernameToken>
            <ServiceAccessToken>
                <AccessLicenseNumber>FG09H9G8H09GH8G0</AccessLicenseNumber>
            </ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <ship:ShipmentRequest>
            <common:Request>
                <RequestOption>validate</RequestOption>
                <TransactionReference>
                    <CustomerContext>Your Customer Context</CustomerContext>
                </TransactionReference>
            </common:Request>
            <Shipment>
                <Description>Description</Description>
                <Shipper>
                    <Name>Shipper Name</Name>
                    <AttentionName>Shipper Attn Name</AttentionName>
                    <TaxIdentificationNumber>123456</TaxIdentificationNumber>
                    <Phone>
                        <Number>1234567890</Number>
                    </Phone>
                    <ShipperNumber>Your Account Number</ShipperNumber>
                    <Address>
                        <AddressLine>Address Line</AddressLine>
                        <City>City</City>
                        <StateProvinceCode>StateProvinceCode</StateProvinceCode>
                        <PostalCode>PostalCode</PostalCode>
                        <CountryCode>CountryCode</CountryCode>
                    </Address>
                </Shipper>
                <ShipTo>
                    <Name>Ship To Name</Name>
                    <AttentionName>Ship To Attn Name</AttentionName>
                    <Phone>
                        <Number>1234567890</Number>
                    </Phone>
                    <Address>
                        <AddressLine>Address Line</AddressLine>
                        <City>City</City>
                        <StateProvinceCode>StateProvinceCode</StateProvinceCode>
                        <PostalCode>PostalCode</PostalCode>
                        <CountryCode>CountryCode</CountryCode>
                    </Address>
                </ShipTo>
                <Service>
                    <Code>01</Code>
                </Service>
                <ShipmentServiceOptions>
                    <Notification>
                        <NotificationCode>8</NotificationCode>
                        <EMail>
                            <EMailAddress>test@mail.com</EMailAddress>
                        </EMail>
                    </Notification>
                </ShipmentServiceOptions>
                <Package>
                    <Description>Description</Description>
                    <Packaging>
                        <Code>02</Code>
                    </Packaging>
                    <Dimensions>
                        <UnitOfMeasurement>
                            <Code>IN</Code>
                        </UnitOfMeasurement>
                        <Length>7.0</Length>
                        <Width>5.0</Width>
                        <Height>2.0</Height>
                    </Dimensions>
                    <PackageWeight>
                        <UnitOfMeasurement>
                            <Code>LBS</Code>
                        </UnitOfMeasurement>
                        <Weight>10.0</Weight>
                    </PackageWeight>
                </Package>
            </Shipment>
            <LabelSpecification>
                <LabelImageFormat>
                    <Code>GIF</Code>
                    <Description>GIF</Description>
                </LabelImageFormat>
            </LabelSpecification>
        </ship:ShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""
