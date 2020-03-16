import re
import unittest
from datetime import datetime
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import ShipmentRequest
from purplship.package import shipment
from tests.purolator.package.fixture import gateway


class TestDHLShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**SHIPMENT_REQUEST_PAYLOAD)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize()['validate'], SHIPMENT_REQUEST_PIPELINE['validate'])
        self.assertEqual(request.serialize()['create'], SHIPMENT_REQUEST_PIPELINE['create'])

    def test_create_shipment(self):
        with patch("purplship.package.mappers.purolator.proxy.http") as mocks:
            mocks.side_effect = [False, '']
            shipment.create(self.ShipmentRequest).with_(gateway)

            url = mocks.call_args[1]["url"]
            self.assertEqual(
                url, f"{gateway.settings.server_url}/EWS/V2/Shipping/ShippingService.asmx"
            )

    def test_parse_shipment_response(self):
        with patch("purplship.package.mappers.purolator.proxy.http") as mocks:
            mocks.side_effect = ['true', SHIPMENT_RESPONSE_XML]
            parsed_response = (
                shipment.create(self.ShipmentRequest).with_(gateway).parse()
            )
            self.assertEqual(
                to_dict(parsed_response), to_dict(PARSED_SHIPMENT_RESPONSE)
            )

    def test_parse_invalid_shipment_response(self):
        with patch("purplship.package.mappers.purolator.proxy.http") as mocks:
            mocks.side_effect = ['false']
            parsed_response = (
                shipment.create(self.ShipmentRequest).with_(gateway).parse()
            )
            self.assertEqual(
                to_dict(parsed_response), to_dict(PARSED_INVALID_SHIPMENT_RESPONSE)
            )


if __name__ == "__main__":
    unittest.main()

SHIPMENT_REQUEST_PAYLOAD = {
    "shipper": {
        "person_name": "Aaron Summer",
        "state_code": "ON",
        "city": "Mississauga",
        "country_code": "CA",
        "postal_code": "L4W5M8",
        "address_line_1": "Main Street",
        "phone_number": "5555555",
    },
    "recipient": {
        "person_name": "Aaron Summer",
        "state_code": "BC",
        "city": "Burnaby",
        "country_code": "CA",
        "postal_code": "V5C5A9",
        "address_line_1": "Douglas Road",
        "phone_number": "2982181",
    },
    "parcel": {
        "reference": "Reference For Shipment",
        "weight": 10,
        "weight_unit": "LB",
        "services": ["purolator_express"],
        "options": {"printing": "thermal"},
    },
}

PARSED_SHIPMENT_RESPONSE = [
    {
        "carrier": "purolator",
        "shipment_date": str(datetime.now().strftime("%Y-%m-%d")),
        "tracking_numbers": ["329014521622"],
    },
    [],
]

PARSED_INVALID_SHIPMENT_RESPONSE = [None, [{'carrier': 'purolator', 'code': '000000', 'message': 'Invalid Shipment Request'}]]

SHIPMENT_REQUEST_XML = f"""<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://purolator.com/pws/datatypes/v1">
    <SOAP-ENV:Header>
        <ns1:RequestContext>
            <Version>2.1</Version>
            <Language>en</Language>
            <UserToken>token</UserToken>
        </ns1:RequestContext>
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
        <ns1:CreateShipmentRequest>
            <Shipment>
                <SenderInformation>
                    <Address>
                        <Name>Aaron Summer</Name>
                        <StreetName>Main Street</StreetName>
                        <City>Mississauga</City>
                        <Province>ON</Province>
                        <Country>CA</Country>
                        <PostalCode>L4W5M8</PostalCode>
                        <PhoneNumber>
                            <Phone>5555555</Phone>
                        </PhoneNumber>
                    </Address>
                </SenderInformation>
                <ReceiverInformation>
                    <Address>
                        <Name>Aaron Summer</Name>
                        <StreetName>Douglas Road</StreetName>
                        <City>Burnaby</City>
                        <Province>BC</Province>
                        <Country>CA</Country>
                        <PostalCode>V5C5A9</PostalCode>
                        <PhoneNumber>
                            <Phone>2982181</Phone>
                        </PhoneNumber>
                    </Address>
                </ReceiverInformation>
                <ShipmentDate>{str(datetime.now().strftime("%Y-%m-%d"))}</ShipmentDate>
                <PackageInformation>
                    <ServiceID>PurolatorExpress</ServiceID>
                    <TotalWeight>
                        <Value>10</Value>
                        <WeightUnit>lb</WeightUnit>
                    </TotalWeight>
                    <TotalPieces>1</TotalPieces>
                    <PiecesInformation>
                        <Piece>
                            <Weight>
                                <Value>10.</Value>
                                <WeightUnit>lb</WeightUnit>
                            </Weight>
                        </Piece>
                    </PiecesInformation>
                </PackageInformation>
                <PickupInformation>
                    <PickupType>DropOff</PickupType>
                </PickupInformation>
                <TrackingReferenceInformation>
                    <Reference1>Reference For Shipment</Reference1>
                </TrackingReferenceInformation>
            </Shipment>
            <PrinterType>Thermal</PrinterType>
        </ns1:CreateShipmentRequest>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

VALIDATE_SHIPMENT_REQUEST_XML = (
    re.sub(
        "<PrinterType>[^>]+</PrinterType>", "<removal-anchor>",
        SHIPMENT_REQUEST_XML.replace('CreateShipmentRequest', 'ValidateShipmentRequest')
    ).replace('            <removal-anchor>\n', '')
)

SHIPMENT_REQUEST_PIPELINE = dict(
    validate=VALIDATE_SHIPMENT_REQUEST_XML,
    create=SHIPMENT_REQUEST_XML,
)

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
