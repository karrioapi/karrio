import re
import unittest
import time
from unittest.mock import patch
import purplship
from purplship.core.utils import DP
from purplship.core.models import ShipmentRequest, ShipmentCancelRequest
from tests.dhl_parcel_pl.fixture import gateway


class TestCanparShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)
        self.VoidShipmentRequest = ShipmentCancelRequest(**void_shipment_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        pipeline = request.serialize()
        process_shipment_request = pipeline["process"]()
        get_label_request = pipeline["get_label"](ShipmentResponseXML)

        serialized_process_shipment_request = re.sub(
            "<shipping_date>[^>]+</shipping_date>",
            "",
            process_shipment_request.data.serialize(),
        )

        self.assertEqual(serialized_process_shipment_request, ShipmentRequestXML)
        self.assertEqual(get_label_request.data.serialize(), ShipmentLabelRequestXML)

    def test_create_void_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.VoidShipmentRequest
        )

        self.assertEqual(request.serialize(), VoidShipmentRequestXML)

    def test_create_shipment(self):
        with patch("purplship.mappers.dhl_parcel_pl.proxy.http") as mocks:
            mocks.side_effect = [
                ShipmentResponseXML,
                ShipmentLabelResponseXML,
            ]
            purplship.Shipment.create(self.ShipmentRequest).from_(gateway)

            process_shipment_call, get_label_call = mocks.call_args_list

            self.assertEqual(
                process_shipment_call[1]["url"],
                f"{gateway.settings.server_url}/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                process_shipment_call[1]["headers"]["soapaction"], "urn:processShipment"
            )
            self.assertEqual(
                get_label_call[1]["url"],
                f"{gateway.settings.server_url}/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                get_label_call[1]["headers"]["soapaction"], "urn:getLabels"
            )

    def test_void_shipment(self):
        with patch("purplship.mappers.dhl_parcel_pl.proxy.http") as mock:
            mock.return_value = "<a></a>"
            purplship.Shipment.cancel(self.VoidShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"], "urn:voidShipment"
            )

    def test_parse_shipment_response(self):
        with patch("purplship.mappers.dhl_parcel_pl.proxy.http") as mocks:
            mocks.side_effect = [
                ShipmentResponseXML,
                ShipmentLabelResponseXML,
            ]
            parsed_response = (
                purplship.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedShipmentResponse)
            )

    def test_parse_void_shipment_response(self):
        with patch("purplship.mappers.dhl_parcel_pl.proxy.http") as mock:
            mock.return_value = VoidShipmentResponseXML
            parsed_response = (
                purplship.Shipment.cancel(self.VoidShipmentRequest)
                .from_(gateway)
                .parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedVoidShipmentResponse)
            )


if __name__ == "__main__":
    unittest.main()


void_shipment_data = {"shipment_identifier": "10000696"}

shipment_data = {
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
        "residential": False,
    },
    "recipient": {
        "address_line1": "1 TEST ST",
        "city": "TORONTO",
        "company_name": "TEST ADDRESS",
        "phone_number": "4161234567",
        "postal_code": "M4X1W7",
        "state_code": "ON",
        "residential": False,
    },
    "parcels": [
        {
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 1.0,
        }
    ],
    "service": "dhl_parcel_pl_ground",
    "options": {
        "dhl_parcel_pl_extra_care": True,
    },
}

ParsedShipmentResponse = [
    {
        "carrier_id": "dhl_parcel_pl",
        "carrier_name": "dhl_parcel_pl",
        "label": "...ENCODED INFORMATION...",
        "selected_rate": {
            "base_charge": 7.57,
            "carrier_id": "dhl_parcel_pl",
            "carrier_name": "dhl_parcel_pl",
            "currency": "CAD",
            "duties_and_taxes": 1.34,
            "extra_charges": [
                {"amount": 7.57, "currency": "CAD", "name": "Freight Charge"},
                {
                    "amount": 2.75,
                    "currency": "CAD",
                    "name": "Residential Address Surcharge",
                },
                {"amount": 1.34, "currency": "CAD", "name": "ONHST Tax Charge"},
            ],
            "meta": {"service_name": "dhl_parcel_pl_ground"},
            "service": "dhl_parcel_pl_ground",
            "total_charge": 11.66,
            "transit_days": 1,
        },
        "tracking_number": "D999999990000000461001",
        "shipment_identifier": "10000696",
    },
    [],
]

ParsedVoidShipmentResponse = [
    {
        "carrier_id": "dhl_parcel_pl",
        "carrier_name": "dhl_parcel_pl",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequestXML = f"""<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
    <soap-env:Body>
        <ns0:createShipment>
            <authData>
                <username>test</username>
                <password>123456789</password>
            </authData>
            <shipment>
                <shipmentInfo>
                    <dropOffType>REQUEST COURIER</dropOffType>
                    <serviceType>AH</serviceType>
                    <billing>
                        <shippingPaymentType>SHIPPER</shippingPaymentType>
                        <billingAccountNumber>1204663</billingAccountNumber>
                        <paymentType>BANK_TRANSFER</paymentType>
                        <costsCenter>ABC1235</costsCenter>
                    </billing>
                    <specialServices>
                        <item>
                            <serviceType>ODB</serviceType>
                        </item>
                        <item>
                            <serviceType>UBEZP</serviceType>
                            <serviceValue>20000</serviceValue>
                        </item>
                    </specialServices>
                    <shipmentTime>
                        <shipmentDate>2012—10—23</shipmentDate>
                        <shipmentStartHour>12:00</shipmentStartHour>
                        <shipmentEndHour>15:00</shipmentEndHour>
                    </shipmentTime>
                    <labelType>BLP</labelType>
                </shipmentInfo>
                <content>Gra komputerowa</content>
                <comment>ostroznie</comment>
                <ship>
                    <shipper>
                        <preaviso>
                            <personName>Thomas Test</personName>
                            <phoneNumber>123456789</phoneNumber>
                            <emailAddress>thomas@test.com</emailAddress>
                        </preaviso>
                        <contact>
                            <personName>Thomas Test</personName>
                            <phoneNumber>l23456789</phoneNumber>
                            <emailAddress>thomas0test.com</emailAddress>
                        </contact>
                        <address>
                            <name>Thomas Test</name>
                            <postalCode>02823</postalCode>
                            <city>Warszawa</city>
                            <street>Osmahska</street>
                            <houseNumber>2</houseNumber>
                            <apartmentNumber></apartmentNumber>
                        </address>
                    </shipper>
                    <receiver>
                        <preaviso>
                            <personName>Receiver</personName>
                            <phoneNumber>123456789</phoneNumber>
                            <emailAddress>receiverNgmail.com</emailAddress>
                        </preaviso>
                        <contact>
                            <personName>Receiver</personName>
                            <phoneNumber>123456789</phoneNumber>
                            <emailAddress>receiver@gmail.com</emailAddress>
                        </contact>
                        <address>
                            <country>PL</country>
                            <name>Receiver</name>
                            <addressType>C</addressType>
                            <postalCode>30001</postalCode>
                            <city>Krakow</city>
                            <street>Jasnogorska</street>
                            <houseNumber>44</houseNumber>
                            <apartmentNumber>55</apartmentNumber>
                        </address>
                    </receiver>
                </ship>
                <pieceList>
                    <item>
                        <type>ENVELOPE</type>
                        <quantity>1</quantity>
                    </item>
                    <item>
                        <type>PACKAGE</type>
                        <weight>20</weight>
                        <width>60</width>
                        <height>40</height>
                        <length>40</length>
                        <quantity>1</quantity>
                    </item>
                </pieceList>
                <customs>
                    <customsType>U</customsType>
                    <costsOfShipment>l0</costsOfShipment>
                    <currency>PLN</currency>
                    <nipNr>5218487281</nipNr>
                    <categoryOfItem>Inne</categoryOfItem>
                    <countryOfOrigin>PL</countryOfOrigin>
                    <customAgreements>
                        <notExceedValue>T</notExceedValue>
                        <notProhibitedGoods>T</notProhibitedGoods>
                        <notRestrictedGoods>T</notRestrictedGoods>
                    </customAgreements>
                    <customsItem>
                        <item>
                            <nameEn>test</nameEn>
                            <namePl>test</namePl>
                            <quantity>2</quantity>
                            <weight>2.0</weight>
                            <value>l00</value>
                            <tariffCode>001</tariffCode>
                        </item>
                    </customsItem>
                    <firstName>Testomir</firstName>
                    <secondaryName>Testalski</secondaryName>
                </customs>
            </shipment>
        </ns0:createShipment>
    </soap-env:Body>
</soap-env:Envelope>
"""

ShipmentLabelRequestXML = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"  xmlns:ws="http://ws.onlinerating.canshipws.dhl_parcel_pl.com" xmlns:xsd="http://ws.dto.canshipws.dhl_parcel_pl.com/xsd" >
    <soap:Header/>
    <soap:Body>
        <ws:getLabelsAdvanced>
            <ws:request>
                <xsd:horizontal>false</xsd:horizontal>
                <xsd:id>10000696</xsd:id>
                <xsd:password>password</xsd:password>
                <xsd:thermal>false</xsd:thermal>
                <xsd:user_id>user_id</xsd:user_id>
            </ws:request>
        </ws:getLabelsAdvanced>
    </soap:Body>
</soap:Envelope>
"""

ShipmentResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<createShipmentResponse xmlns="https://dhl24.com.pl/webapi2/provider/service.html?ws=1" xsi:schemaLocation="https://dhl24.com.pl/webapi2/provider/service.html?ws=1 schema.xsd"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <createShipmentResult>
        <shipmentNotificationNumber>string</shipmentNotificationNumber>
        <shipmentTrackingNumber>string</shipmentTrackingNumber>
        <packagesTrackingNumbers>string</packagesTrackingNumbers>
        <dispatchNotificationNumber>string</dispatchNotificationNumber>
        <label>
            <labelType>string</labelType>
            <labelFormat>string</labelFormat>
            <labelContent>string</labelContent>
            <cn23Content>string</cn23Content>
            <cn23MimeType>string</cn23MimeType>
            <fvProformaContent>string</fvProformaContent>
            <fvProformaMimeType>string</fvProformaMimeType>
            <fvProformaNumer>string</fvProformaNumer>
        </label>
    </createShipmentResult>
</createShipmentResponse>
"""

ShipmentLabelResponseXML = """<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
    <soapenv:Body>
        <ns:getLabelsResponse xmlns:ns="http://ws.business.canshipws.dhl_parcel_pl.com">
            <ns:return xmlns:ax211="http://dto.canshipws.dhl_parcel_pl.com/xsd"
                xmlns:ax29="http://ws.dto.canshipws.dhl_parcel_pl.com/xsd"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax29:GetLabelsRs">
                <ax29:error xsi:nil="true"/>
                <ax29:labels>...ENCODED INFORMATION...</ax29:labels>
            </ns:return>
        </ns:getLabelsResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

VoidShipmentRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ser="https://sandbox.dhl24.com.pl/webapi2/provider/service.html?ws=1">
    <soapenv:Header/>
    <soapenv:Body>
        <ser:deleteShipment>
            <authData>
                <username>?</username>
                <password>?</password>
            </authData>
            <shipment>
                <shipmentIdentificationNumber>?</shipmentIdentificationNumber>
            </shipment>
        </ser:deleteShipment>
    </soapenv:Body>
</soapenv:Envelope>
"""

VoidShipmentResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<deleteShipmentResponse xmlns="https://dhl24.com.pl/webapi2/provider/service.html?ws=1" xsi:schemaLocation="https://dhl24.com.pl/webapi2/provider/service.html?ws=1 schema.xsd"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <deleteShipmentResult>
        <id>string</id>
        <result>0</result>
        <error>string</error>
    </deleteShipmentResult>
</deleteShipmentResponse>
"""
