import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDPDHLShipping(unittest.TestCase):
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
                f"{gateway.settings.server_url}/soap",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/soap",
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
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = ShipmentErrorResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedErrorResponse,
            )

    def test_parse_html_error_response(self):
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = HTMLErrorResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedHTMLErrorResponse,
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "dpdhl_paket",
    "shipper": {
        "company_name": "Vegesacker Heerstr.",
        "person_name": "Kontaktperson Absender",
        "address_line1": "Absender Zeile 1",
        "address_line2": "Absender Zeile 2",
        "street_number": "111",
        "city": "Bremen",
        "postal_code": "28757",
        "country_code": "DE",
        "phone_number": "+49421987654321",
        "email": "absender@dhl.local",
    },
    "recipient": {
        "company_name": "An der Weide",
        "person_name": "Kontaktperson Empfänger",
        "address_line1": "50a Empfänger Zeile 1",
        "city": "Bremen",
        "postal_code": "28195",
        "country_code": "DE",
        "phone_number": "+49421123456789",
        "email": "empfaenger@dhl.local",
    },
    "parcels": [
        {
            "height": 15,
            "length": 60.0,
            "width": 30,
            "weight": 5.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "options": {
        "email_notification": True,
        "shipment_date": "2020-12-29",
        "dpdhl_premium": True,
    },
    "label_type": "PDF",
    "reference": "Ref. 123456",
}

ShipmentCancelPayload = {
    "shipment_identifier": "222201040006351204",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "dpdhl",
        "carrier_name": "dpdhl",
        "docs": {"label": ANY},
        "label_type": "PDF",
        "shipment_identifier": "222201040023121880",
        "tracking_number": "222201040023121880",
        "meta": {
            "carrier_tracking_link": "https://www.dhl.de/en/privatkunden/pakete-empfangen/verfolgen.html?piececode=222201040023121880"
        },
    },
    [
        {
            "carrier_id": "dpdhl",
            "carrier_name": "dpdhl",
            "code": 0,
            "details": {"statusText": "Weak validation error occured."},
            "message": "Weak validation error occured.",
        },
        {
            "carrier_id": "dpdhl",
            "carrier_name": "dpdhl",
            "code": 0,
            "details": {"statusText": "Weak validation error occured."},
            "message": ANY,
        },
    ],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "dpdhl",
        "carrier_name": "dpdhl",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "dpdhl",
            "carrier_name": "dpdhl",
            "code": 1101,
            "details": {"statusText": "Hard validation error occured."},
            "message": "Hard validation error occured.",
        },
        {
            "carrier_id": "dpdhl",
            "carrier_name": "dpdhl",
            "code": 1101,
            "details": {"statusText": "Hard validation error occured."},
            "message": "Bitte geben Sie ein gültiges Sendungsdatum an.",
        },
    ],
]

ParsedHTMLErrorResponse = [
    None,
    [
        {
            "carrier_id": "dpdhl",
            "carrier_name": "dpdhl",
            "code": "Unauthorized",
            "message": "This server could not verify that you\n            are authorized to access the document\n            requested. Either you supplied the wrong\n            credentials (e.g., bad password), or your\n            browser doesn't understand how to supply\n            the credentials required.",
        }
    ],
]


ShipmentRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cis="http://dhl.de/webservice/cisbase" xmlns:ns="http://dhl.de/webservices/businesscustomershipping/3.0">
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
                <minorRelease>4</minorRelease>
            </ns:Version>
            <ShipmentOrder>
                <sequenceNumber>1</sequenceNumber>
                <Shipment>
                    <ShipmentDetails>
                        <product>V01PAK</product>
                        <cis:accountNumber>22222222220101</cis:accountNumber>
                        <shipmentDate>2020-12-29</shipmentDate>
                        <returnShipmentAccountNumber>22222222220101</returnShipmentAccountNumber>
                        <ShipmentItem>
                            <weightInKG>5</weightInKG>
                            <lengthInCM>60</lengthInCM>
                            <widthInCM>30</widthInCM>
                            <heightInCM>15</heightInCM>
                        </ShipmentItem>
                        <Service>
                            <Premium>1</Premium>
                        </Service>
                        <Notification>
                            <recipientEmailAddress>empfaenger@dhl.local</recipientEmailAddress>
                        </Notification>
                    </ShipmentDetails>
                    <Shipper>
                        <Name>
                            <cis:name1>Absender Zeile 1</cis:name1>
                            <cis:name2>Absender Zeile 2</cis:name2>
                        </Name>
                        <Address>
                            <cis:streetName>Absender Zeile 1</cis:streetName>
                            <cis:streetNumber>111</cis:streetNumber>
                            <cis:zip>28757</cis:zip>
                            <cis:city>Bremen</cis:city>
                            <cis:Origin>
                                <cis:country>Germany</cis:country>
                                <cis:countryISOCode>DE</cis:countryISOCode>
                            </cis:Origin>
                        </Address>
                        <Communication>
                            <cis:phone>+49421987654321</cis:phone>
                            <cis:email>absender@dhl.local</cis:email>
                            <cis:contactPerson>Kontaktperson Absender</cis:contactPerson>
                        </Communication>
                    </Shipper>
                    <ShipperReference>Ref. 123456</ShipperReference>
                    <Receiver>
                        <cis:name1>50a Empfänger Zeile 1</cis:name1>
                        <Address>
                            <cis:streetName>Empfänger Zeile 1</cis:streetName>
                            <cis:streetNumber>50a</cis:streetNumber>
                            <cis:zip>28195</cis:zip>
                            <cis:city>Bremen</cis:city>
                            <cis:Origin>
                                <cis:country>Germany</cis:country>
                                <cis:countryISOCode>DE</cis:countryISOCode>
                            </cis:Origin>
                        </Address>
                        <Communication>
                            <cis:phone>+49421123456789</cis:phone>
                            <cis:email>empfaenger@dhl.local</cis:email>
                            <cis:contactPerson>Kontaktperson Empfänger</cis:contactPerson>
                        </Communication>
                    </Receiver>
                </Shipment>
            </ShipmentOrder>
            <labelResponseType>B64</labelResponseType>
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
                <minorRelease>4</minorRelease>
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

ShipmentCancelRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cis="http://dhl.de/webservice/cisbase" xmlns:ns="http://dhl.de/webservices/businesscustomershipping/3.0">
    <soapenv:Header>
        <cis:Authentification>
            <cis:user>2222222222_01</cis:user>
            <cis:signature>pass</cis:signature>
        </cis:Authentification>
    </soapenv:Header>
    <soapenv:Body>
        <ns:DeleteShipmentOrderRequest>
            <ns:Version>
                <ns:majorRelease>3</ns:majorRelease>
                <ns:minorRelease>4</ns:minorRelease>
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
                <minorRelease>4</minorRelease>
            </bcs:Version>
            <Status>
                <statusCode>0</statusCode>
                <statusText>Weak validation error occured.</statusText>
            </Status>
            <CreationState>
                <sequenceNumber>1</sequenceNumber>
                <shipmentNumber>222201040023121880</shipmentNumber>
                <LabelData>
                    <Status>
                        <statusCode>0</statusCode>
                        <statusText>Weak validation error occured.</statusText>
                        <statusMessage>Der eingegebene Wert ist zu lang und wurde gekürzt.</statusMessage>
                        <statusMessage>Die angegebene Straße kann nicht gefunden werden.</statusMessage>
                        <statusMessage>Die angegebene Straße kann nicht gefunden werden.</statusMessage>
                        <statusMessage>Der eingegebene Wert ist zu lang und wurde gekürzt.</statusMessage>
                    </Status>
                    <labelData>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xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5Ec8BAMiPeA4AQH7EcwAA8iOeAwCQH/EcAID8iOcAAORHPAcAID/iOQAA+RHPAQDIj3gOAEB+xHMAAPIjngMAkB/xHACA/IjnAADkRzwHACA/4jkAAPkRzwEAyI94DgBAfsRzAADyI54DAJAf8RwAgPyI5wAA5Ec8BwAgP+I5AAD5VcTzpwIAAKb2dDueAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEjr//9Z0PMKZW5kc3RyZWFtCmVuZG9iago1IDAgb2JqCjw8L0NvbG9yU3BhY2UvRGV2aWNlUkdCL1N1YnR5cGUvSW1hZ2UvSGVpZ2h0IDc1NC9GaWx0ZXIvRmxhdGVEZWNvZGUvVHlwZS9YT2JqZWN0L1dpZHRoIDIwMDAvU01hc2sgNCAwIFIvTGVuZ3RoIDIwNjgwL0JpdHNQZXJDb21wb25lbnQgOD4+c3RyZWFtCnic7NgBjpvaFkXBP/9J56uVVvJCg43NhQW4agTtdfZNJP73PwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAuJtfAAAAAABwU763AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63AwAAAADAdr63c4wjl3Zm9R3Gq4tyhHplO6rTEqsHOF5d9D7qSwbq5LysngzD1FOaV1dhmHpK/6hjjFFXzNThp+oecBb1W6RUr+8s6jvsoo7K7uqJ7ahOS6we4Hh10fuoLxmr87NKPROGqac0r67CGPWOpuoeY9QVM3X4qboHnEX9FinV64vV+Y9QN2a8elOHqmNzqHpuR6gbX159wMuoD/XR6uMzTD2leXUVxqh3NFX3GKOu2KirT9U94ETq50ipXl+jrt6oq7NVvaBYnZ8d1eNq1NWvqr7btdXX+xT1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AAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAAYDvf2wEAAAAA4P/t2DENAAAAwyD/rieiyS6QQefbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAAnW8HAAAAAIDOtwMAAAAAQOfbAQAAAACg8+0AAAAAAND5dgAAAAAA6Hw7AAAAAAB0vh0AAAAAADrfDgAAAAAA3fPbAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgY6TttL8KZW5kc3RyZWFtCmVuZG9iago2IDAgb2JqCjw8L0ZpbHRlci9GbGF0ZURlY29kZS9MZW5ndGggNTE+PnN0cmVhbQp4nCvkcgrhMlAwNTfVMzFWCEnhcg3hCuQqVDBUMABCCJmcq6AfkWao4JKvEMgFAPziClEKZW5kc3RyZWFtCmVuZG9iago4IDAgb2JqCjw8L0NvbnRlbnRzIDYgMCBSL1R5cGUvUGFnZS9SZXNvdXJjZXM8PC9Qcm9jU2V0IFsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXS9YT2JqZWN0PDwvWGYxIDEgMCBSPj4+Pi9QYXJlbnQgNyAwIFIvTWVkaWFCb3hbMCAwIDI5Ny42NCA1NzUuNDNdPj4KZW5kb2JqCjIgMCBvYmoKPDwvU3VidHlwZS9UeXBlMS9UeXBlL0ZvbnQvQmFzZUZvbnQvSGVsdmV0aWNhLUJvbGQvRW5jb2RpbmcvV2luQW5zaUVuY29kaW5nPj4KZW5kb2JqCjMgMCBvYmoKPDwvU3VidHlwZS9UeXBlMS9UeXBlL0ZvbnQvQmFzZUZvbnQvSGVsdmV0aWNhL0VuY29kaW5nL1dpbkFuc2lFbmNvZGluZz4+CmVuZG9iagoxIDAgb2JqCjw8L1N1YnR5cGUvRm9ybS9GaWx0ZXIvRmxhdGVEZWNvZGUvVHlwZS9YT2JqZWN0L01hdHJpeCBbMSAwIDAgMSAwIDBdL0Zvcm1UeXBlIDEvUmVzb3VyY2VzPDwvUHJvY1NldCBbL1BERiAvVGV4dCAvSW1hZ2VCIC9JbWFnZUMgL0ltYWdlSV0vRm9udDw8L0YxIDIgMCBSL0YyIDMgMCBSPj4vWE9iamVjdDw8L2ltZzEgNSAwIFIvaW1nMCA0IDAgUj4+Pj4vQkJveFswIDAgMjk3LjY0IDU3NS40M10vTGVuZ3RoIDI1MTI+PnN0cmVhbQp4nJ2a3XIctxGF7/cp5tKuVKDB7wC+ChXLSmLJJVNMXKk4laLIJSlrubRIqlzlB/ML5FXyIGl0Y9AHS8qRo58SD3m+MzMABmhg9X4zT3GJJvjpmr6cp93GlcWkgF82w25ztflus9/Y6aeNm/5C9h82dp5ebv7xz3k637xnfp5uLzdPTzZPvrKTDSbZ6eSCiPoDO8VscppiDMbH6eR6Y81M/55tPvvyTy+mV0dfPzv5/OQHiqFvPTvZzCamVDxdbear1d/HzzfZxCkGZ3K9ZZeLsX7Vu83r9drJRIeXZsrThX298GyW5Gzma//tZv8FXpYD3FTMEjDA0xUyRTgTnESEknLgiG+eHH16gqOnzpKQyuwtJxz/+5fr7e2b7e3l5Dz9+fS4Wb7Pz+SCSxyXKNdOX92e7t9dfLi9/+S0ULLhsN/PZl6Kld55/uz45dE3f3+QYqeQzfJYSmyNFIwrHPHyr69Pnh0/ch/JhGGIOOdNCUNXBeeK3MjXN/v703f309Gbu+3+fHv7sN8edry1xge6UcpZWjPZRG1c847GnqeHKVNYch2d103R+EqlvgpzHWddvt44Cg5J7atW4JCQQHq+Jfd4S8MpaPwqNX61r1qBQ6I1KH2jDuwHfVLvs7Rh56xzvzJwPxaRqDvb2M8hLjJyj66n7053u8nNS/37G+LizK9/jStpHWsuW+rsp7fb6+3+N2T5aPKyDtySl/z/DdwQWiP974EbDU1NDwduyN7Ud5oHrq3TFw7cZ9c/Xvxnf3kwcuvcFOg9psmyz2hN1459PyWahhe+josm0rVsrD+snW/TdHY9PXl7fWmnL2+mbznM51Tvroc1DaMkmfxgevQ0RILvc1uQue3oze327Gr/YX95t781X9Bzrr9mO4dHGiaY8iA5FVPayPF+HXzH24vt7Xb/M8feXf34r607c3EO5zEHG9J2e3px/sbbTN/yJduLRzshDX0wW0MzoK8v+9oHM7Ucj4XtT2/Pru4fmzIeDKo1J6XWIJbmVk6x07vLT7iPFM0chvvwYfGtQfc/n17tPuk26IUrFm7DmTZx2Sf20anvkU5N9YVoLy3dkLy0r2n6HHq09uU8O+obm/N8ODh9fVUzjCfRMqnF9XH7j5uuPy7exKCGJn3qs+jMI1MTmlYHX0CkXkB/3Dpg4ZdufHTnUi03ZBikUOSFfrF9e392c759cnzz4f7t/rJ+jc/rvUmptkldR643NLHQPN3krklL00dmyeYurzZ0YzkCvdQOVJql0mwGOsy1FTodfO3vTovsdjEjHetKpDRPIEqzVJrNQFOX0pvS6UhDHq4tstvFjDTNnwDT5JgBZqlw9SK71HVAYeriBWCWCrMZ6OSMh/5Kvr4rnRbZ7WJGOtBUBzRNrxFolkqzGelcq6hOL3NdhDotUmk2A70EM8OdL6m+/kqz7HYxI70Yh9cuxuO1WSrNZqDrzOSVzvRvUlpkt4sZ6VBfP6XppYBWE6k0m5GmYW+BXoZWE6k0m4EujmeAlaZS08MoF9ntYkZ6qeWS0sVEuLZIpdkMtKWiK8HFLa0TCWaHpjvR/EOCr19CQqxVAySwhgT2DwnZzAsmFGiQ3aohgf2YYGeDt2B9LXo0QLQGsH3gpQjRgDS0YtMQwP4hgfeVmkB7ooy3IBoS2I8JZC0RE+h1wXYUrQniHxKWoRVcqRsOCGANActBK/gZmo0CaC2I8P42rQHiHxLoRcF2pPVgwXYUDQnsHxKywVsItLV0ECAaAqodeap3Hd4BrQoOn0G0Boh/SKB3BANy3aVAAGsIqHbkaSWJ+Ai00CSYS5rWAPEPCa4WZ5AQhzW3aUhg/5BANQe+UcnWfY4miIYE9mMCrSsuY4KHpXi3ak0Q/5AQaqkICTTiMaBK4Nk98HkoW+zixlYQDQn5oHKxi4dFuybQG4QBVSov7oFfYN2ufKl7KAhgDQnLsLBTQrb12EATslSLPUG0Joh/SIhDEWPrYoIBC1YezT3wvE9RvsxDIdM0JLAfE6jCtdiPJQzVTNOaIP4hYRkKGkuLUsB2FA0Jy0FNU48GIsyNbnYmwVM03YnmHxIClnNrUa4BrCEgjBWdozUIS7p6eIG1TdMQUA6qOkebISxvnA1DfdO0Joh/SEhmuAUa8A4DWENAtSPvZqhqKIC+wDqlaQ0Q/5DgYW2vCQkKvt2qIcEPa39NyMbC7OjqGgIvZdOQwH5M8G4oeJwPw1rdtCaIf0iIQ83jaBOz4FOIhoR4UPM4X+rhiiYEZ2Z8CtGQwH5MoHUHiz4X8lCyNK0J4seEum7Ae+loXRnaQbQmiH9IcEPN4qI3Q0CVwLuDisXROpTxGWgnUyIGLEOF0vyYQOuQxTtIYShZmtYE8Q8JcahZXD1ZwL4UDQnxoGZxtBBFhwllWK+bhgT2Q8LFR7fsgSt9rlHkmDK4djr+/Wdh9t9/7pbEx4O/K2We5/qXfz1yHvPYcUAtwEJeT+ZmK8dCfz7f7uU84MXbs+3+bju92p3eDycCgasmKSjXjXGT68Y4tlNYtq6CdrY0uUdA5V3rKMvVLV5guVJa0SRl0IqK7Gi1Ktm2qStK21CbFBW5usWr7GLhFomlqqEAy3J1ixdYKUo6KxVGZ1l2lr3KZj5Q6myWamVlRa5u8QIr+82VLbOC9HWn2KVUkeKhU/wBkoIsV7d4gZXCobM8vDrKHzWtJDuVrDtED/1a93sRWrjpFWh25BeeK5XnM1vgWSvPduAtn2wqT+vojNcX3XmxIy9Lv/KFZ3/lWSvPduCdrPydd4G3KJ0X3XmxIy9nZspn4xbkWSvPduC9Ndh8nuctxUV3nN1Iy45McTlUU5y14mwHPsjq2vm2v+q86M6LHXk+9wS+mIi9L1p5tgMf5fyr87TG4NOz7LSYkc5mxr5vu5iOi1ae7cAnXiIVT1zOK8664+xGWtbHjtNkhPfOUmE2A037leSQ5gNnwFl3XuzIy8qovOxmlGetPNuBz3IS1fmcjMe2E915sSNfeOfdeZqgZph0mlae7cDTviPje1cK3M9u1Z0Xu/L1E5ECnedmOSRa+aZXoNmR5y2C4om31IqzVry6kZbzH8ULV86Ks1Zc/tuC8lbOkzpvFz7g7LzozosdeDfD09ZK3nKt0nnRnRc78nJ0r/xSSxHgWSvPduBbnd95j4XFbtWdFzvycgKvPJdjwLNWnu3AB89niJ0PVGAhL7rzYkdezr47H8eapGnl2Q58HMsSF7HU2K268/GgMvlozWnrTrZ+DG/s+tH4HOVzol//VKx/jBrDgzqz8CfDNY2q1SD/IeOPN9fXN/vpxemb7W569eL5H+r/eHn64e7tfnt3N726ub0/HT4S/JZ+/xcykiLiCmVuZHN0cmVhbQplbmRvYmoKNyAwIG9iago8PC9LaWRzWzggMCBSXS9UeXBlL1BhZ2VzL0NvdW50IDEvSVRYVCgyLjEuNyk+PgplbmRvYmoKOSAwIG9iago8PC9UeXBlL0NhdGFsb2cvUGFnZXMgNyAwIFI+PgplbmRvYmoKMTAgMCBvYmoKPDwvTW9kRGF0ZShEOjIwMjIwOTA2MTIzNDEyKzAyJzAwJykvQ3JlYXRpb25EYXRlKEQ6MjAyMjA5MDYxMjM0MTIrMDInMDAnKS9Qcm9kdWNlcihpVGV4dCAyLjEuNyBieSAxVDNYVCk+PgplbmRvYmoKeHJlZgowIDExCjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDA0MDg5NSAwMDAwMCBuIAowMDAwMDQwNzE0IDAwMDAwIG4gCjAwMDAwNDA4MDcgMDAwMDAgbiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDE5NTgwIDAwMDAwIG4gCjAwMDAwNDA0MzAgMDAwMDAgbiAKMDAwMDA0MzY3NyAwMDAwMCBuIAowMDAwMDQwNTQ3IDAwMDAwIG4gCjAwMDAwNDM3NDAgMDAwMDAgbiAKMDAwMDA0Mzc4NSAwMDAwMCBuIAp0cmFpbGVyCjw8L0luZm8gMTAgMCBSL0lEIFs8M2MwNjJjY2RmZDdiMzBkNTc5NWM1OGExYzE0ZWQwMWM+PGZlNjk0MTU4MDlmMzMxM2ZhMDI3ZDA5ODc5OGExNzNkPl0vUm9vdCA5IDAgUi9TaXplIDExPj4Kc3RhcnR4cmVmCjQzOTA4CiUlRU9GCg==</labelData>
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
                <minorRelease>4</minorRelease>
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

ShipmentErrorResponse = """<soap:Envelope xmlns:bcs="http://dhl.de/webservices/businesscustomershipping/3.0"
    xmlns:cis="http://dhl.de/webservice/cisbase"
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <soap:Header/>
    <soap:Body>
        <bcs:CreateShipmentOrderResponse>
            <bcs:Version>
                <majorRelease>3</majorRelease>
                <minorRelease>4</minorRelease>
            </bcs:Version>
            <Status>
                <statusCode>1101</statusCode>
                <statusText>Hard validation error occured.</statusText>
            </Status>
            <CreationState>
                <sequenceNumber/>
                <LabelData>
                    <Status>
                        <statusCode>1101</statusCode>
                        <statusText>Hard validation error occured.</statusText>
                        <statusMessage>Bitte geben Sie ein gültiges Sendungsdatum an.</statusMessage>
                        <statusMessage>Bitte geben Sie ein gültiges Sendungsdatum an.</statusMessage>
                    </Status>
                </LabelData>
            </CreationState>
        </bcs:CreateShipmentOrderResponse>
    </soap:Body>
</soap:Envelope>
"""

HTMLErrorResponse = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>Unauthorized</h1>
        <p>This server could not verify that you
            are authorized to access the document
            requested. Either you supplied the wrong
            credentials (e.g., bad password), or your
            browser doesn't understand how to supply
            the credentials required.</p>
    </body>
</html>
"""
