import unittest
from unittest.mock import patch
from gds_helpers import to_xml, to_dict, export
from pyups.freight_ship import FreightShipRequest
from purplship.domain import Types as T
from tests.ups.freight.fixture import gateway
from tests.utils import strip, get_node_from_xml


class TestUPSShipment(unittest.TestCase):
    def setUp(self):
        self.FreightShipRequest = FreightShipRequest()
        self.FreightShipRequest.build(
            get_node_from_xml(FreightShipmentRequestXML, "FreightShipRequest")
        )

    def test_create_freight_shipment_request(self):
        payload = T.ShipmentRequest(**freight_shipment_data)
        Shipment_ = gateway.mapper.create_shipment_request(payload)
        self.assertEqual(export(Shipment_), export(self.FreightShipRequest))

    @patch("purplship.freight.mappers.ups.proxy.http", return_value="<a></a>")
    def test_create_freight_shipment(self, http_mock):
        gateway.proxy.create_shipment(self.FreightShipRequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(FreightShipmentRequestXML))

    def test_parse_freight_shipment_response(self):
        parsed_response = gateway.mapper.parse_shipment_response(
            to_xml(FreightShipmentResponseXML)
        )
        self.assertEqual(
            to_dict(parsed_response), to_dict(ParsedFreightShipmentResponse)
        )


if __name__ == "__main__":
    unittest.main()


freight_shipment_data = {
    "shipper": {
        "company_name": "Ship From Name",
        "address_lines": ["Address Line"],
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
        "person_name": "Attention Name",
        "phone_number": "Shipper Phone number",
        "account_number": "Your Shipper Number",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "address_lines": ["Address Line"],
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
        "person_name": "Attention Name",
    },
    "shipment": {
        "weight_unit": "LB",
        "references": ["Your Customer Context"],
        "items": [
            {
                "description": "Commodity Description",
                "weight": 180,
                "quantity": 1,
                "extra": {"FreightClass": "FreightClass"},
            }
        ],
        "extra": {
            "Payer": {
                "company_name": "Payer Name",
                "address_lines": ["Address Line"],
                "city": "City",
                "state_code": "StateProvinceCode",
                "postal_code": "PostalCode",
                "country_code": "CountryCode",
                "person_name": "Attention Name",
                "phone_number": "Phone Number",
                "account_number": "Payer Shipper Number",
            },
            "ShipmentBillingOption": {"Code": "ShipmentBillingOption"},
            "HandlingUnitOne": {
                "Quantity": "HandlingUnitOne quantity",
                "Type": {"Code": "HandlingUnitOne type"},
            },
        },
    },
}

ParsedFreightShipmentResponse = [
    {
        "carrier": "UPS",
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
        "services": ["Service code"],
        "shipment_date": None,
        "total_charge": {
            "amount": "MonetaryValue",
            "currency": "CurrencyCode",
            "name": "Shipment charge",
        },
        "tracking_numbers": ["Shipment Number"],
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

FreightShipmentRequestXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:fsp="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0" xmlns:IF="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0" >
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
      <fsp:FreightShipRequest>
         <common:Request>
            <common:RequestOption>1</common:RequestOption>
            <common:TransactionReference>
               <common:CustomerContext>Your Customer Context</common:CustomerContext>
            </common:TransactionReference>
         </common:Request>
         <fsp:Shipment>
            <fsp:ShipFrom>
               <fsp:Name>Ship From Name</fsp:Name>
               <fsp:Address>
                  <fsp:AddressLine>Address Line</fsp:AddressLine>
                  <fsp:City>City</fsp:City>
                  <fsp:StateProvinceCode>StateProvinceCode</fsp:StateProvinceCode>
                  <fsp:PostalCode>PostalCode</fsp:PostalCode>
                  <fsp:CountryCode>CountryCode</fsp:CountryCode>
               </fsp:Address>
               <fsp:AttentionName>Attention Name</fsp:AttentionName>
               <fsp:Phone>
                  <fsp:Number>Shipper Phone number</fsp:Number>
               </fsp:Phone>
            </fsp:ShipFrom>
            <fsp:ShipperNumber>Your Shipper Number</fsp:ShipperNumber>
            <fsp:ShipTo>
               <fsp:Name>Ship To Name</fsp:Name>
               <fsp:Address>
                  <fsp:AddressLine>Address Line</fsp:AddressLine>
                  <fsp:City>City</fsp:City>
                  <fsp:StateProvinceCode>StateProvinceCode</fsp:StateProvinceCode>
                  <fsp:PostalCode>PostalCode</fsp:PostalCode>
                  <fsp:CountryCode>CountryCode</fsp:CountryCode>
               </fsp:Address>
               <fsp:AttentionName>Attention Name</fsp:AttentionName>
            </fsp:ShipTo>
            <fsp:PaymentInformation>
               <fsp:Payer>
                  <fsp:Name>Payer Name</fsp:Name>
                  <fsp:Address>
                     <fsp:AddressLine>Address Line</fsp:AddressLine>
                     <fsp:City>City</fsp:City>
                     <fsp:StateProvinceCode>StateProvinceCode</fsp:StateProvinceCode>
                     <fsp:PostalCode>PostalCode</fsp:PostalCode>
                     <fsp:CountryCode>CountryCode</fsp:CountryCode>
                  </fsp:Address>
                  <fsp:ShipperNumber>Payer Shipper Number</fsp:ShipperNumber>
                  <fsp:AttentionName>Attention Name</fsp:AttentionName>
                  <fsp:Phone>
                     <fsp:Number>Phone Number</fsp:Number>
                  </fsp:Phone>
               </fsp:Payer>
               <fsp:ShipmentBillingOption>
                  <fsp:Code>ShipmentBillingOption</fsp:Code>
               </fsp:ShipmentBillingOption>
            </fsp:PaymentInformation>
            <fsp:HandlingUnitOne>
               <fsp:Quantity>HandlingUnitOne quantity</fsp:Quantity>
               <fsp:Type>
                  <fsp:Code>HandlingUnitOne type</fsp:Code>
               </fsp:Type>
            </fsp:HandlingUnitOne>
            <fsp:Commodity>
               <fsp:Description>Commodity Description</fsp:Description>
               <fsp:Weight>
                  <fsp:UnitOfMeasurement>
                     <fsp:Code>LBS</fsp:Code>
                  </fsp:UnitOfMeasurement>
                  <fsp:Value>180</fsp:Value>
               </fsp:Weight>
               <fsp:NumberOfPieces>1</fsp:NumberOfPieces>
               <fsp:FreightClass>FreightClass</fsp:FreightClass>
            </fsp:Commodity>
         </fsp:Shipment>
      </fsp:FreightShipRequest>
   </tns:Body>
</tns:Envelope>
"""
