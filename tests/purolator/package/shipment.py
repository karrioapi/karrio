import re
import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import ShipmentRequest
from purplship.package import shipment
from tests.dhl.package.fixture import gateway


class TestDHLShipment(unittest.TestCase):
    def setUp(self):
        self.ShipmentRequest = ShipmentRequest(**SHIPMENT_REQUEST_PAYLOAD)


if __name__ == "__main__":
    unittest.main()

SHIPMENT_REQUEST_PAYLOAD = {}

SHIPMENT_REQUEST_XML = """SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:ns1="http://purolator.com/pws/datatypes/v1">
    <SOAP-ENV:Header>
        <ns1:RequestContext>
            <ns1:Version>1.0</ns1:Version>
            <ns1:Language>en</ns1:Language>
            <ns1:GroupID>xxx</ns1:GroupID>
            <ns1:RequestReference>Rating Example</ns1:RequestReference>
        </ns1:RequestContext>
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
        <ns1:CreateShipmentRequest>
            <ns1:Shipment>
                <ns1:SenderInformation>
                    <ns1:Address>
                        <ns1:Name>Aaron Summer</ns1:Name>
                        <ns1:StreetNumber>1234</ns1:StreetNumber>
                        <ns1:StreetName>Main Street</ns1:StreetName>
                        <ns1:City>Mississauga</ns1:City>
                        <ns1:Province>ON</ns1:Province>
                        <ns1:Country>CA</ns1:Country>
                        <ns1:PostalCode>L4W5M8</ns1:PostalCode>
                        <ns1:PhoneNumber>
                            <ns1:CountryCode>1</ns1:CountryCode>
                            <ns1:AreaCode>905</ns1:AreaCode>
                            <ns1:Phone>5555555</ns1:Phone>
                        </ns1:PhoneNumber>
                    </ns1:Address>
                </ns1:SenderInformation>
                <ns1:ReceiverInformation>
                    <ns1:Address>
                        <ns1:Name>Aaron Summer</ns1:Name>
                        <ns1:StreetNumber>2245</ns1:StreetNumber>
                        <ns1:StreetName>Douglas Road</ns1:StreetName>
                        <ns1:City>Burnaby</ns1:City>
                        <ns1:Province>BC</ns1:Province>
                        <ns1:Country>CA</ns1:Country>
                        <ns1:PostalCode>V5C5A9</ns1:PostalCode>
                        <ns1:PhoneNumber>
                            <ns1:CountryCode>1</ns1:CountryCode>
                            <ns1:AreaCode>604</ns1:AreaCode>
                            <ns1:Phone>2982181</ns1:Phone>
                        </ns1:PhoneNumber>
                    </ns1:Address>
                </ns1:ReceiverInformation>
                <ns1:PackageInformation>
                    <ns1:ServiceID>PurolatorExpress</ns1:ServiceID>
                    <ns1:TotalWeight>
                        <ns1:Value>10</ns1:Value>
                        <ns1:WeightUnit>lb</ns1:WeightUnit>
                    </ns1:TotalWeight>
                    <ns1:TotalPieces>1</ns1:TotalPieces>
                </ns1:PackageInformation>
                <ns1:PaymentInformation>
                    <ns1:PaymentType>Sender</ns1:PaymentType>
                    <ns1:RegisteredAccountNumber>YOUR_ACCOUNT_HERE</ns1:RegisteredAccountNumber>
                    <ns1:BillingAccountNumber>YOUR_ACCOUNT_HERE</ns1:BillingAccountNumber>
                </ns1:PaymentInformation>
                <ns1:PickupInformation>
                    <ns1:PickupType>DropOff</ns1:PickupType>
                </ns1:PickupInformation>
                <ns1:TrackingReferenceInformation>
                    <ns1:Reference1>Reference For Shipment</ns1:Reference1>
                </ns1:TrackingReferenceInformation>
            </ns1:Shipment>
            <ns1:PrinterType>Thermal</ns1:PrinterType>
        </ns1:CreateShipmentRequest>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

SHIPMENT_RESPONSE_XML = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Header>
        <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <h:ResponseReference>Rating Example</h:ResponseReference>
        </h:ResponseContext>
    </s:Header>
    <s:Body>
        <CreateShipmentResponse xmlns="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <ResponseInformation>
                <Errors/>
                <InformationalMessages i:nil="true"/>
            </ResponseInformation>
            <ShipmentPIN>
                <Value>329014521622</Value>
            </ShipmentPIN>
            <PiecePINs>
                <PIN>
                    <Value>329014521622</Value>
                </PIN>
            </PiecePINs>
            <ReturnShipmentPINs/>
            <ExpressChequePIN>
                <Value/>
            </ExpressChequePIN>
        </CreateShipmentResponse>
    </s:Body>
</s:Envelope>
"""

VOID_SHIPMENT_REQUEST_XML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:ns1="http://purolator.com/pws/datatypes/v1">
    <SOAP-ENV:Header>
        <ns1:RequestContext>
            <ns1:Version>1.0</ns1:Version>
            <ns1:Language>en</ns1:Language>
            <ns1:GroupID>xxx</ns1:GroupID>
            <ns1:RequestReference>Rating Example</ns1:RequestReference>
        </ns1:RequestContext>
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
        <ns1:VoidShipmentRequest>
            <ns1:PIN>
                <ns1:Value>329014837473</ns1:Value>
            </ns1:PIN>
        </ns1:VoidShipmentRequest>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

VOID_SHIPMENT_RESPONSE_XML = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Header>
        <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1" 
            xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <h:ResponseReference>Rating Example</h:ResponseReference>
        </h:ResponseContext>
    </s:Header>
    <s:Body>
        <VoidShipmentResponse xmlns="http://purolator.com/pws/datatypes/v1" 
            xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <ResponseInformation>
                <Errors/>
                <InformationalMessages i:nil="true"/>
            </ResponseInformation>
            <ShipmentVoided>true</ShipmentVoided>
        </VoidShipmentResponse>
    </s:Body>
</s:Envelope>
"""
