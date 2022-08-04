import unittest
from unittest.mock import patch, ANY
from tests.dpdhl.fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLParcelGermanyShipping(unittest.TestCase):
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
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = ""
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {}

ShipmentCancelPayload = {
    "shipment_identifier": "222201040006351204",
}

ParsedShipmentResponse = [{}, []]

ParsedCancelShipmentResponse = [{}, []]


ShipmentRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:cis="http://dhl.de/webservice/cisbase"
    xmlns:ns="http://dhl.de/webservices/businesscustomershipping/3.0">
    <soapenv:Header>
        <cis:Authentification>
            <cis:user>2222222222_01</cis:user>
            <cis:signature>pass</cis:signature>
        </cis:Authentification>
    </soapenv:Header>
    <soapenv:Body>
        <ns:CreateShipmentOrderRequest>
            <ns:Version>
                <majorRelease>3</majorRelease>
                <minorRelease>1</minorRelease>
            </ns:Version>
            <ShipmentOrder>
                <sequenceNumber></sequenceNumber>
                <Shipment>
                    <ShipmentDetails>
                        <product>V01PAK</product>
                        <cis:accountNumber>22222222220104</cis:accountNumber>
                        <customerReference>Ref. 123456</customerReference>
                        <shipmentDate>2020-12-29</shipmentDate>
                        <costCentre></costCentre>
                        <ShipmentItem>
                            <weightInKG>5</weightInKG>
                            <lengthInCM>60</lengthInCM>
                            <widthInCM>30</widthInCM>
                            <heightInCM>15</heightInCM>
                        </ShipmentItem>
                        <Service>
                        </Service>
                        <Notification>
                            <recipientEmailAddress>empfaenger@dhl.local</recipientEmailAddress>
                        </Notification>
                    </ShipmentDetails>
                    <Shipper>
                        <Name>
                            <cis:name1>Absender Zeile 1</cis:name1>
                            <cis:name2>Absender Zeile 2</cis:name2>
                            <cis:name3>Absender Zeile 3</cis:name3>
                        </Name>
                        <Address>
                            <cis:streetName>Vegesacker Heerstr.</cis:streetName>
                            <cis:streetNumber>111</cis:streetNumber>
                            <cis:zip>28757</cis:zip>
                            <cis:city>Bremen</cis:city>
                            <cis:Origin>
                                <cis:country></cis:country>
                                <cis:countryISOCode>DE</cis:countryISOCode>
                            </cis:Origin>
                        </Address>
                        <Communication>
                            <cis:phone>+49421987654321</cis:phone>
                            <cis:email>absender@dhl.local</cis:email>
                            <cis:contactPerson>Kontaktperson Absender</cis:contactPerson>
                        </Communication>
                    </Shipper>
                    <Receiver>
                        <cis:name1>Empfänger Zeile 1</cis:name1>
                        <Address>
                            <cis:name2>Empfänger Zeile 2</cis:name2>
                            <cis:name3>Empfänger Zeile 3</cis:name3>
                            <cis:streetName>An der Weide</cis:streetName>
                            <cis:streetNumber>50a</cis:streetNumber>
                            <cis:zip>28195</cis:zip>
                            <cis:city>Bremen</cis:city>
                            <cis:Origin>
                                <cis:country></cis:country>
                                <cis:countryISOCode>DE</cis:countryISOCode>
                            </cis:Origin>
                        </Address>
                        <Communication>
                            <cis:phone>+49421123456789</cis:phone>
                            <cis:email>empfaenger@dhl.local</cis:email>
                            <cis:contactPerson>Kontaktperson Empfänger </cis:contactPerson>
                        </Communication>
                    </Receiver>
                </Shipment>
                <PrintOnlyIfCodeable active="1"/>
            </ShipmentOrder>
            <labelResponseType>URL</labelResponseType>
            <groupProfileName></groupProfileName>
            <labelFormat></labelFormat>
            <labelFormatRetoure></labelFormatRetoure>
            <combinedPrinting>0</combinedPrinting>
        </ns:CreateShipmentOrderRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""

InternationalShipmentRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:cis="http://dhl.de/webservice/cisbase"
    xmlns:ns="http://dhl.de/webservices/businesscustomershipping/3.0">
    <soapenv:Header>
        <cis:Authentification>
            <cis:user>2222222222_01</cis:user>
            <cis:signature>pass</cis:signature>
        </cis:Authentification>
    </soapenv:Header>
    <soapenv:Body>
        <ns:CreateShipmentOrderRequest>
            <ns:Version>
                <majorRelease>3</majorRelease>
                <minorRelease>2</minorRelease>
            </ns:Version>
            <ShipmentOrder>
                <sequenceNumber>1</sequenceNumber>
                <Shipment>
                    <ShipmentDetails>
                        <product>V66WPI</product>
                        <cis:accountNumber>22222222226601</cis:accountNumber>
                        <customerReference>123456789</customerReference>
                        <shipmentDate>2022-01-19</shipmentDate>
                        <ShipmentItem>
                            <weightInKG>1</weightInKG>
                        </ShipmentItem>
                        <Service>
                            <Premium active="0"/>
                        </Service>
                        <Notification>
                            <recipientEmailAddress>Max.muster@dhl.local</recipientEmailAddress>
                        </Notification>
                    </ShipmentDetails>
                    <Shipper>
                        <Name>
                            <cis:name1>Absender Zeile 1</cis:name1>
                            <cis:name2>Absender Zeile 2</cis:name2>
                            <cis:name3>Absender Zeile 3</cis:name3>
                        </Name>
                        <Address>
                            <cis:streetName>Vegesacker Heerstr.111</cis:streetName>
                            <cis:zip>28757</cis:zip>
                            <cis:city>Bremen</cis:city>
                            <cis:Origin>
                                <cis:country/>
                                <cis:countryISOCode>DE</cis:countryISOCode>
                            </cis:Origin>
                        </Address>
                        <Communication>
                            <cis:phone>+49421987654321</cis:phone>
                            <cis:email>absender@dhl.local</cis:email>
                            <cis:contactPerson>Kontaktperson Absender</cis:contactPerson>
                        </Communication>
                    </Shipper>
                    <ShipperReference>1234578</ShipperReference>
                    <Receiver>
                        <cis:name1>Empfaenger Zeile 1</cis:name1>
                        <Address>
                            <cis:name2>Empfaenger Zeile 2</cis:name2>
                            <cis:name3>Empfaenger Zeile 3</cis:name3>
                            <cis:streetName>Shanti Path</cis:streetName>
                            <cis:streetNumber>No. 6/50G</cis:streetNumber>
                            <cis:addressAddition/>
                            <cis:dispatchingInformation/>
                            <cis:zip>110021</cis:zip>
                            <cis:city>New Delhi</cis:city>
                            <cis:province/>
                            <cis:Origin>
                                <cis:country>Indien</cis:country>
                                <cis:countryISOCode>IN</cis:countryISOCode>
                                <cis:state/>
                            </cis:Origin>
                        </Address>
                        <Communication>
                            <cis:phone>+49421123456789</cis:phone>
                            <cis:email>empfaenger@dhl.local</cis:email>
                            <cis:contactPerson>Kontaktperson Empfaenger</cis:contactPerson>
                        </Communication>
                    </Receiver>
                    <ExportDocument>
                        <invoiceNumber>999999999</invoiceNumber>
                        <exportType>OTHER</exportType>
                        <exportTypeDescription>Permanent</exportTypeDescription>
                        <placeOfCommital>Deutschland</placeOfCommital>
                        <additionalFee>1.00</additionalFee>
                        <ExportDocPosition>
                            <description>ExportPositionOne</description>
                            <countryCodeOrigin>DE</countryCodeOrigin>
                            <customsTariffNumber>12345678</customsTariffNumber>
                            <amount>3</amount>
                            <netWeightInKG>0.2</netWeightInKG>
                            <customsValue>24.96</customsValue>
                        </ExportDocPosition>
                        <ExportDocPosition>
                            <description>ExportPositionTwo</description>
                            <countryCodeOrigin>DE</countryCodeOrigin>
                            <customsTariffNumber>12345678</customsTariffNumber>
                            <amount>2</amount>
                            <netWeightInKG>0.15</netWeightInKG>
                            <customsValue>24.96</customsValue>
                        </ExportDocPosition>
                    </ExportDocument>
                </Shipment>
                <PrintOnlyIfCodeable active="1"/>
            </ShipmentOrder>
            <labelResponseType>URL</labelResponseType>
            <groupProfileName/>
            <labelFormat></labelFormat>
        </ns:CreateShipmentOrderRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentCancelRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:cis="http://dhl.de/webservice/cisbase"
    xmlns:ns="http://dhl.de/webservices/businesscustomershipping/3.0">
    <soapenv:Header>
        <cis:Authentification>
            <cis:user>2222222222_01</cis:user>
            <cis:signature>pass</cis:signature>
        </cis:Authentification>
    </soapenv:Header>
    <soapenv:Body>
        <ns:DeleteShipmentOrderRequest>
            <ns:Version>
                <majorRelease>3</majorRelease>
                <minorRelease>1</minorRelease>
                <build>?</build>
            </ns:Version>
            <cis:shipmentNumber>222201040006351204</cis:shipmentNumber>
        </ns:DeleteShipmentOrderRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentResponse = """<soap:Envelope xmlns:bcs="http://dhl.de/webservices/businesscustomershipping/3.0"
    xmlns:cis="http://dhl.de/webservice/cisbase"
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <soap:Header/>
    <soap:Body>
        <bcs:CreateShipmentOrderResponse>
            <bcs:Version>
                <majorRelease>3</majorRelease>
                <minorRelease>0</minorRelease>
            </bcs:Version>
            <Status>
                <statusCode>0</statusCode>
                <statusText>ok</statusText>
            </Status>
            <CreationState>
                <sequenceNumber/>
                <shipmentNumber>222201040006351662</shipmentNumber>
                <LabelData>
                    <Status>
                        <statusCode>0</statusCode>
                        <statusText>ok</statusText>
                        <statusMessage>Der Webservice wurde ohne Fehler ausgeführt.</statusMessage>
                    </Status>
                    <labelUrl>https://cig.dhl.de/gkvlabel/SANDBOX/dhl-vls/gw/shpmntws/printShipment?token=x5xzrHE7ctmqPqk33k%2BKkBwbvIfYP4elMQsBFM%2BJOdiT2bmoaXXzris%2Ftz9jBtdVFLY5cCENit0Jnd9aXuxoNEjfzNllkalXEA%2FzsC0FSzg%2F48gfdIvdzv5GGLzGJwoX</labelUrl>
                </LabelData>
            </CreationState>
        </bcs:CreateShipmentOrderResponse>
    </soap:Body>
</soap:Envelope>
"""

ShipmentCancelResponse = """<soap:Envelope xmlns:bcs="http://dhl.de/webservices/businesscustomershipping/3.0"
    xmlns:cis="http://dhl.de/webservice/cisbase"
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <soap:Header/>
    <soap:Body>
        <bcs:DeleteShipmentOrderResponse>
            <bcs:Version>
                <majorRelease>3</majorRelease>
                <minorRelease>0</minorRelease>
            </bcs:Version>
            <Status>
                <statusCode>0</statusCode>
                <statusText>ok</statusText>
                <statusMessage>Der Webservice wurde ohne Fehler ausgeführt.</statusMessage>
            </Status>
            <DeletionState>
                <cis:shipmentNumber>222201040006351204</cis:shipmentNumber>
                <Status>
                    <statusCode>0</statusCode>
                    <statusText>ok</statusText>
                    <statusMessage/>
                </Status>
            </DeletionState>
        </bcs:DeleteShipmentOrderResponse>
    </soap:Body>
</soap:Envelope>
"""
