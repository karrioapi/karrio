import unittest
from unittest.mock import patch, ANY
from tests.chronopost.fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestChronopostShipping(unittest.TestCase):
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
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_error_response(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
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
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = []

ParsedCancelShipmentResponse = []


ShipmentRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.shipping.soap.chronopost.fr/">
    <soapenv:Header />
    <soapenv:Body>
        <cxf:shippingMultiParcelV5>
            <headerValue>
                <accountNumber>19869502</accountNumber>
                <idEmit>CHRFR</idEmit>
                <subAccount>123</subAccount>
            </headerValue>
            <shipperValue>
                <shipperAdress1>28 rue du Clair Bocage</shipperAdress1>
                <shipperAdress2>28 rue du Clair Bocage</shipperAdress2>
                <shipperCity>La Seyne-sur-mer</shipperCity>
                <shipperCivility>M</shipperCivility>
                <shipperContactName>Jean Dupont</shipperContactName>
                <shipperCountry>FR</shipperCountry>
                <shipperCountryName>France</shipperCountryName>
                <shipperEmail></shipperEmail>
                <shipperMobilePhone>0447110494</shipperMobilePhone>
                <shipperPreAlert>0</shipperPreAlert>
                <shipperZipCode>83500</shipperZipCode>
            </shipperValue>
            <customerValue>
                <customerAdress1>28 rue du Clair Bocage</customerAdress1>
                <customerAdress2>28 rue du Clair Bocage</customerAdress2>
                <customerCity>La Seyne-sur</customerCity>
                <customerCivility>M</customerCivility>
                <customerContactName>Jean Dupont</customerContactName>
                <customerCountry>FR</customerCountry>
                <customerCountryName>France</customerCountryName>
                <customerName>Chef Royale</customerName>
                <customerPreAlert>0</customerPreAlert>
                <customerZipCode>83500</customerZipCode>
                <printAsSender>N</printAsSender>
            </customerValue>
            <recipientValue>
                <recipientAdress1>72 rue Reine Elisabeth</recipientAdress1>
                <recipientAdress2>72 rue Reine Elisabet</recipientAdress2>
                <recipientCity>Menton</recipientCity>
                <recipientContactName>Lucas Dupont</recipientContactName>
                <recipientCountry>FR</recipientCountry>
                <recipientCountryName>France</recipientCountryName>
                <recipientName>HauteSide</recipientName>
                <recipientPreAlert>0</recipientPreAlert>
                <recipientZipCode>06500</recipientZipCode>
            </recipientValue>
            <refValue></refValue>
            <skybillValue>
                <bulkNumber>1</bulkNumber>
                <codValue>EUR</codValue>
                <evtCode>DC</evtCode>
                <objectType>MAR</objectType>
                <productCode>01</productCode>
                <service>0</service>
                <shipDate>2022-7-18T09:11:00.000Z</shipDate>
                <shipHour>9</shipHour>
                <height>10</height>
                <length>10</length>
                <width>10</width>
                <subAccount>123</subAccount>
            </skybillValue>
            <skybillParamsValue>
                <mode>PDF</mode>
                <withReservation>0</withReservation>
            </skybillParamsValue>
            <password>255562</password>
            <modeRetour>1</modeRetour>
            <numberOfParcel>1</numberOfParcel>
            <version>2.0</version>
            <multiParcel></multiParcel>
        </cxf:shippingMultiParcelV5>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentCancelRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.tracking.soap.chronopost.fr/">
    <soapenv:Header />
    <soapenv:Body>
        <cxf:cancelSkybill>
            <accountNumber>19869502</accountNumber>
            <password>255562</password>
            <language>en_GB</language>
            <skybillNumber>XP695852974FR</skybillNumber>
        </cxf:cancelSkybill>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns1:shippingMultiParcelV5Response xmlns:ns1="http://cxf.shipping.soap.chronopost.fr/">
            <return>
                <errorCode>0</errorCode>
                <errorMessage />
                <resultMultiParcelValue>
                    <codeDepot>27422240</codeDepot>
                    <codeService>226</codeService>
                    <destinationDepot>0477</destinationDepot>
                    <geoPostCodeBarre>%0006500XP696808230248226250</geoPostCodeBarre>
                    <geoPostNumeroColis>XP6968082302480</geoPostNumeroColis>
                    <groupingPriorityLabel>SIA1</groupingPriorityLabel>
                    <pdfEtiquette>R0lGODdhIAOwBPAAAA==</pdfEtiquette>
                    <serviceMark />
                    <serviceName>AM2-NO</serviceName>
                    <signaletiqueProduit>13H</signaletiqueProduit>
                    <skybillNumber>XP696808230FR</skybillNumber>
                </resultMultiParcelValue>
            </return>
        </ns1:shippingMultiParcelV5Response>
    </soap:Body>
</soap:Envelope>
"""

ShipmentCancelErrorResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns2:cancelSkybillResponse xmlns:ns2="http://cxf.tracking.soap.chronopost.fr/">
            <return>
                <errorCode>2</errorCode>
                <errorMessage>the parcel doesn't match account or parcel information not found</errorMessage>
                <statusCode>0</statusCode>
            </return>
        </ns2:cancelSkybillResponse>
    </soap:Body>
</soap:Envelope>
"""
