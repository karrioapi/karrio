import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import ShipmentRequest
from tests.ups.freight.fixture import gateway
from purplship.freight import shipment


class TestUPSShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**freight_shipment_data)

    def test_create_freight_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(request.serialize(), FreightShipmentRequestXML)

    @patch("purplship.freight.mappers.ups.proxy.http", return_value="<a></a>")
    def test_create_freight_shipment(self, http_mock):
        shipment.create(self.ShipmentRequest).with_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/FreightShip")

    def test_parse_freight_shipment_response(self):
        with patch("purplship.freight.mappers.ups.proxy.http") as mock:
            mock.return_value = FreightShipmentResponseXML
            parsed_response = (
                shipment.create(self.ShipmentRequest).with_(gateway).parse()
            )
            self.assertEqual(
                to_dict(parsed_response), to_dict(ParsedFreightShipmentResponse)
            )


if __name__ == "__main__":
    unittest.main()


freight_shipment_data = {
    "shipper": {
        "company_name": "Ship From Name",
        "address_line_1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
        "person_name": "Attention Name",
        "phone_number": "Shipper Phone number",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "address_line_1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
        "person_name": "Attention Name",
    },
    "parcel": {
        "description": "Commodity Description",
        "weight_unit": "LB",
        "weight": 180,
        "reference": "Your Customer Context",
        "options": {
            "ups_freight_class": "ups_freight_class_50",
            "notification": {
                "email": "test@mail.com"
            }
        },
    },
}

ParsedFreightShipmentResponse = [
    {
        "carrier": "UPS Freight",
        "charges": [
            {"amount": "Value", "currency": "UnitOfMeasurement code", "name": "DSCNT"},
            {
                "amount": "Value",
                "currency": "UnitOfMeasurement code",
                "name": "DSCNT_RATE",
            },
            {"amount": "Value", "currency": "UnitOfMeasurement code", "name": "2"},
            {
                "amount": "Value",
                "currency": "UnitOfMeasurement code",
                "name": "LND_GROSS",
            },
            {
                "amount": "Value",
                "currency": "UnitOfMeasurement code",
                "name": "AFTR_DSCNT",
            },
        ],
        "documents": [],
        "reference": {"type": "CustomerContext", "value": "Your Customer Context"},
        "service": "ups_worldwide_express",
        "shipment_date": None,
        "total_charge": {
            "amount": "MonetaryValue",
            "currency": "CurrencyCode",
            "name": "Shipment charge",
        },
        "tracking_number": "Shipment Number",
    },
    [],
]


FreightShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header />
    <soapenv:Body>
        <freightShip:FreightShipResponse xmlns:freightShip="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0">
            <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                <common:ResponseStatus>
                    <common:Code>1</common:Code>
                    <common:Description>Success</common:Description>
                </common:ResponseStatus>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Response>
            <freightShip:ShipmentResults>
                <freightShip:OriginServiceCenterCode>OriginServiceCenterCode</freightShip:OriginServiceCenterCode>
                <freightShip:ShipmentNumber>Shipment Number</freightShip:ShipmentNumber>
                <freightShip:BOLID>BOLID</freightShip:BOLID>
                <freightShip:GuaranteedIndicator />
                <freightShip:Rate>
                    <freightShip:Type>
                        <freightShip:Code>DSCNT</freightShip:Code>
                        <freightShip:Description>DSCNT</freightShip:Description>
                    </freightShip:Type>
                    <freightShip:Factor>
                        <freightShip:Value>Value</freightShip:Value>
                        <freightShip:UnitOfMeasurement>
                            <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                        </freightShip:UnitOfMeasurement>
                    </freightShip:Factor>
                </freightShip:Rate>
                <freightShip:Rate>
                    <freightShip:Type>
                        <freightShip:Code>DSCNT_RATE</freightShip:Code>
                        <freightShip:Description>DSCNT_RATE</freightShip:Description>
                    </freightShip:Type>
                    <freightShip:Factor>
                        <freightShip:Value>Value</freightShip:Value>
                        <freightShip:UnitOfMeasurement>
                            <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                        </freightShip:UnitOfMeasurement>
                    </freightShip:Factor>
                </freightShip:Rate>
                <freightShip:Rate>
                    <freightShip:Type>
                        <freightShip:Code>2</freightShip:Code>
                        <freightShip:Description>2</freightShip:Description>
                    </freightShip:Type>
                    <freightShip:Factor>
                        <freightShip:Value>Value</freightShip:Value>
                        <freightShip:UnitOfMeasurement>
                            <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                        </freightShip:UnitOfMeasurement>
                    </freightShip:Factor>
                </freightShip:Rate>
                <freightShip:Rate>
                    <freightShip:Type>
                        <freightShip:Code>LND_GROSS</freightShip:Code>
                        <freightShip:Description>LND_GROSS</freightShip:Description>
                    </freightShip:Type>
                    <freightShip:Factor>
                        <freightShip:Value>Value</freightShip:Value>
                        <freightShip:UnitOfMeasurement>
                            <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                        </freightShip:UnitOfMeasurement>
                    </freightShip:Factor>
                </freightShip:Rate>
                <freightShip:Rate>
                    <freightShip:Type>
                        <freightShip:Code>AFTR_DSCNT</freightShip:Code>
                        <freightShip:Description>AFTR_DSCNT</freightShip:Description>
                    </freightShip:Type>
                    <freightShip:Factor>
                        <freightShip:Value>Value</freightShip:Value>
                        <freightShip:UnitOfMeasurement>
                            <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                        </freightShip:UnitOfMeasurement>
                    </freightShip:Factor>
                </freightShip:Rate>
                <freightShip:TotalShipmentCharge>
                    <freightShip:CurrencyCode>CurrencyCode</freightShip:CurrencyCode>
                    <freightShip:MonetaryValue>MonetaryValue</freightShip:MonetaryValue>
                </freightShip:TotalShipmentCharge>
                <freightShip:BillableShipmentWeight>
                    <freightShip:UnitOfMeasurement>
                        <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                    </freightShip:UnitOfMeasurement>
                    <freightShip:Value>BillableShipmentWeight</freightShip:Value>
                </freightShip:BillableShipmentWeight>
                <freightShip:Service>
                    <freightShip:Code>07</freightShip:Code>
                </freightShip:Service>
                <freightShip:TimeInTransit>
                    <freightShip:DaysInTransit>DaysInTransit</freightShip:DaysInTransit>
                </freightShip:TimeInTransit>
            </freightShip:ShipmentResults>
        </freightShip:FreightShipResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

FreightShipmentRequestXML = f"""<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:fsp="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0" xmlns:IF="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0" >
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
        <fsp:FreightShipRequest>
            <common:Request>
                <RequestOption>1</RequestOption>
                <TransactionReference>
                    <CustomerContext>Your Customer Context</CustomerContext>
                </TransactionReference>
            </common:Request>
            <Shipment>
                <ShipFrom>
                    <Name>Ship From Name</Name>
                    <Address>
                        <AddressLine>Address Line</AddressLine>
                        <City>City</City>
                        <StateProvinceCode>StateProvinceCode</StateProvinceCode>
                        <PostalCode>PostalCode</PostalCode>
                        <CountryCode>CountryCode</CountryCode>
                    </Address>
                    <AttentionName>Attention Name</AttentionName>
                    <Phone>
                        <Number>Shipper Phone number</Number>
                    </Phone>
                </ShipFrom>
                <ShipperNumber>{gateway.settings.account_number}</ShipperNumber>
                <ShipTo>
                    <Name>Ship To Name</Name>
                    <Address>
                        <AddressLine>Address Line</AddressLine>
                        <City>City</City>
                        <StateProvinceCode>StateProvinceCode</StateProvinceCode>
                        <PostalCode>PostalCode</PostalCode>
                        <CountryCode>CountryCode</CountryCode>
                    </Address>
                    <AttentionName>Attention Name</AttentionName>
                </ShipTo>
                <Commodity>
                    <Description>Commodity Description</Description>
                    <Weight>
                        <UnitOfMeasurement>
                            <Code>LBS</Code>
                        </UnitOfMeasurement>
                        <Value>180.0</Value>
                    </Weight>
                    <FreightClass>50</FreightClass>
                </Commodity>
                <ShipmentServiceOptions>
                    <EMailInformation>
                        <EMailAddress>test@mail.com</EMailAddress>
                        <EventType>001</EventType>
                        <EventType>002</EventType>
                        <EventType>003</EventType>
                        <EventType>004</EventType>
                    </EMailInformation>
                </ShipmentServiceOptions>
            </Shipment>
        </fsp:FreightShipRequest>
    </tns:Body>
</tns:Envelope>
"""
