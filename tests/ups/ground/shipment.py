import unittest
from unittest.mock import patch, ANY
from purplship.core.utils import DP
from purplship.core.models import ShipmentRequest, ShipmentCancelRequest
from purplship import Shipment
from tests.ups.fixture import freight_gateway, LABEL


class TestUPSShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**package_shipment_data)
        self.ShipmentCancelRequest = ShipmentCancelRequest(
            **shipment_cancel_request_data
        )

    def test_create_package_shipment_request(self):
        request = freight_gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequestXML)

    def test_create_cancel_shipment_request(self):
        request = freight_gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequestXML)

    @patch("purplship.mappers.ups_ground.proxy.http", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        Shipment.create(self.ShipmentRequest).from_(freight_gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{freight_gateway.settings.server_url}/ShipFreight")

    def test_parse_publish_rate_shipment_response(self):
        with patch("purplship.mappers.ups_ground.proxy.http") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = (
                Shipment.create(self.ShipmentRequest).from_(freight_gateway).parse()
            )
            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("purplship.mappers.ups_ground.proxy.http") as mock:
            mock.return_value = ShipmentCancelResponseXML
            parsed_response = (
                Shipment.cancel(self.ShipmentCancelRequest).from_(freight_gateway).parse()
            )
            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentCancelResponse)


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


ParsedShipmentResponse = [
    {
        "carrier_name": "ups",
        "carrier_id": "ups",
        "label": ANY,
        "tracking_number": "1ZWA82900191640782",
        "shipment_identifier": "1ZWA82900191640782",
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


ShipmentRequestXML = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"
    xmlns:wsf="http://www.ups.com/schema/wsf"
    xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
    <env:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>Your User Id</upss:Username>
                <upss:Password>Your Password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>Your Access License Number</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </env:Header>
    <env:Body>
        <FreightShipRequest xmlns="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0"
            xmlns:IF="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0">
            <common:Request>
                <common:RequestOption>1</common:RequestOption>
                <common:SubVersion>SubVersion</common:SubVersion>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Request>
            <XOLTWS:Shipment xmlns:XOLTWS="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0">
                <XOLTWS:ShipFrom>
                    <XOLTWS:Name>Ship From Name</XOLTWS:Name>
                    <XOLTWS:Address>
                        <XOLTWS:AddressLine>Address Line</XOLTWS:AddressLine>
                        <XOLTWS:City>City</XOLTWS:City>
                        <XOLTWS:StateProvinceCode>StateProvinceCode</XOLTWS:StateProvinceCode>
                        <XOLTWS:PostalCode>PostalCode</XOLTWS:PostalCode>
                        <XOLTWS:CountryCode>CountryCode</XOLTWS:CountryCode>
                    </XOLTWS:Address>
                    <XOLTWS:AttentionName>Attention Name</XOLTWS:AttentionName>
                    <XOLTWS:Phone>
                        <XOLTWS:Number>Shipper Phone number</XOLTWS:Number>
                    </XOLTWS:Phone>
                </XOLTWS:ShipFrom>
                <XOLTWS:ShipperNumber>Your Shipper Number</XOLTWS:ShipperNumber>
                <XOLTWS:ShipTo>
                    <XOLTWS:Name>Ship To Name</XOLTWS:Name>
                    <XOLTWS:Address>
                        <XOLTWS:AddressLine>Address Line</XOLTWS:AddressLine>
                        <XOLTWS:City>City</XOLTWS:City>
                        <XOLTWS:StateProvinceCode>StateProvinceCode</XOLTWS:StateProvinceCode>
                        <XOLTWS:PostalCode>PostalCode</XOLTWS:PostalCode>
                        <XOLTWS:CountryCode>CountryCode</XOLTWS:CountryCode>
                    </XOLTWS:Address>
                    <XOLTWS:AttentionName>Attention Name</XOLTWS:AttentionName>
                </XOLTWS:ShipTo>
                <XOLTWS:PaymentInformation>
                    <XOLTWS:Payer>
                        <XOLTWS:Name>Payer Name</XOLTWS:Name>
                        <XOLTWS:Address>
                            <XOLTWS:AddressLine>Address Line</XOLTWS:AddressLine>
                            <XOLTWS:City>City</XOLTWS:City>
                            <XOLTWS:StateProvinceCode>StateProvinceCode</XOLTWS:StateProvinceCode>
                            <XOLTWS:PostalCode>PostalCode</XOLTWS:PostalCode>
                            <XOLTWS:CountryCode>CountryCode</XOLTWS:CountryCode>
                        </XOLTWS:Address>
                        <XOLTWS:ShipperNumber>Payer Shipper Number</XOLTWS:ShipperNumber>
                        <XOLTWS:AccountType>Your Account Type</XOLTWS:AccountType>
                        <XOLTWS:AttentionName>Attention Name</XOLTWS:AttentionName>
                        <XOLTWS:Phone>
                            <XOLTWS:Number>Phone Number</XOLTWS:Number>
                        </XOLTWS:Phone>
                    </XOLTWS:Payer>
                    <XOLTWS:ShipmentBillingOption>
                        <XOLTWS:Code>ShipmentBillingOption</XOLTWS:Code>
                    </XOLTWS:ShipmentBillingOption>
                </XOLTWS:PaymentInformation>
                <XOLTWS:Service>
                    <XOLTWS:Code>Service code</XOLTWS:Code>
                </XOLTWS:Service>
                <XOLTWS:HandlingUnitOne>
                    <XOLTWS:Quantity>HandlingUnitOne quantity</XOLTWS:Quantity>
                    <XOLTWS:Type>
                        <XOLTWS:Code>HandlingUnitOne type</XOLTWS:Code>
                    </XOLTWS:Type>
                </XOLTWS:HandlingUnitOne>
                <XOLTWS:Commodity>
                    <XOLTWS:Description>Commodity Description</XOLTWS:Description>
                    <XOLTWS:Weight>
                        <XOLTWS:UnitOfMeasurement>
                            <XOLTWS:Code>UnitOfMeasurement code</XOLTWS:Code>
                        </XOLTWS:UnitOfMeasurement>
                        <XOLTWS:Value>Weight</XOLTWS:Value>
                    </XOLTWS:Weight>
                    <XOLTWS:NumberOfPieces>NumberOfPieces</XOLTWS:NumberOfPieces>
                    <XOLTWS:PackagingType>
                        <XOLTWS:Code>PackagingType code</XOLTWS:Code>
                    </XOLTWS:PackagingType>
                    <XOLTWS:FreightClass>FreightClass</XOLTWS:FreightClass>
                </XOLTWS:Commodity>
                <XOLTWS:DensityEligibleIndicator/>
                <XOLTWS:TimeInTransitIndicator/>
            </XOLTWS:Shipment>
        </FreightShipRequest>
    </env:Body>
</env:Envelope>
"""

ShipmentResponseXML = f"""<<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header/>
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
                <freightShip:OriginServiceCenterCode>OriginServiceCenterCode</freightShip:OriginServiceC enterCode>
                <freightShip:ShipmentNumber>Shipment Number</freightShip:ShipmentNumber>
                <freightShip:BOLID>BOLID</freightShip:BOLID>
                <freightShip:GuaranteedIndicator/>
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
                    <freightShip:Code>Service code</freightShip:Code>
                </freightShip:Service>
                <freightShip:TimeInTransit>
                    <freightShip:DaysInTransit>DaysInTransit</freightShip:DaysInTransit>
                </freightShip:TimeInTransit>
            </freightShip:ShipmentResults>
        </freightShip:FreightShipResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentCancelRequestXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:void="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0">
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
            <common:Request/>
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
