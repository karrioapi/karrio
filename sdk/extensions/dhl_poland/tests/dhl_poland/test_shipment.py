import time
import unittest
from unittest.mock import patch, ANY
import karrio
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from .fixture import gateway


class TestDHLPolandShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)
        self.InternationalShipmentRequest = ShipmentRequest(
            **interantional_shipment_data
        )
        self.VoidShipmentRequest = ShipmentCancelRequest(**void_shipment_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequestXML)

    def test_create_international_shipment_request(self):
        request = gateway.mapper.create_shipment_request(
            self.InternationalShipmentRequest
        )

        self.assertEqual(request.serialize(), InternationalShipmentRequestXML)

    def test_create_void_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.VoidShipmentRequest
        )

        self.assertEqual(request.serialize(), VoidShipmentRequestXML)

    def test_create_shipment(self):
        with patch("karrio.mappers.dhl_poland.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                gateway.settings.server_url,
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"],
                f"{gateway.settings.server_url}#createShipment",
            )

    def test_void_shipment(self):
        with patch("karrio.mappers.dhl_poland.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.cancel(self.VoidShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                gateway.settings.server_url,
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"],
                f"{gateway.settings.server_url}#deleteShipment",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dhl_poland.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_void_shipment_response(self):
        with patch("karrio.mappers.dhl_poland.proxy.lib.request") as mock:
            mock.return_value = VoidShipmentResponseXML
            parsed_response = (
                karrio.Shipment.cancel(self.VoidShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedVoidShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


void_shipment_data = {"shipment_identifier": "10000696"}

shipment_data = {
    "shipper": {
        "company_name": "Janek",
        "person_name": "3e General Partnership",
        "address_line1": "9 Lesna",
        "address_line2": "59",
        "street_number": "9",
        "city": "Wawa",
        "postal_code": "00909",
        "country_code": "PL",
        "phone_number": "123456789",
        "email": "testomir@gmail.pl",
        "residential": True,
    },
    "recipient": {
        "company_name": "Me",
        "person_name": "3e General Partnership",
        "address_line1": "Lesna",
        "address_line2": "59",
        "street_number": "9",
        "city": "Wawa",
        "postal_code": "00001",
        "country_code": "PL",
        "phone_number": "123456789",
        "email": "testomir@gmail.pl",
        "residential": False,
    },
    "parcels": [
        {
            "height": 3,
            "length": 10.0,
            "width": 3,
            "weight": 1.0,
        }
    ],
    "service": "dhl_poland_polska",
    "options": {
        "dhl_poland_proof_of_delivery": True,
    },
}

interantional_shipment_data = {
    **shipment_data,
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "address_line2": "59",
        "street_number": "23",
        "city": "Ottawa",
        "postal_code": "k1k 4t3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
        "phone_number": "1 (450) 823-8432",
        "residential": False,
    },
    "customs": {
        "duty": {"paid_by": "sender", "declared_value": "100.0"},
        "commodities": [{"weight": "10", "title": "test"}],
        "options": {"nip_number": "5218487281"},
    },
}

ParsedShipmentResponse = [
    {
        "carrier_id": "dhl_poland",
        "carrier_name": "dhl_poland",
        "shipment_identifier": "string",
        "tracking_number": "string",
        "docs": {"invoice": "string", "label": ANY},
        "meta": {
            "carrier_tracking_link": "https://www.dhl.com/pl-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=string"
        },
    },
    [],
]

ParsedVoidShipmentResponse = [
    {
        "carrier_id": "dhl_poland",
        "carrier_name": "dhl_poland",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequestXML = f"""<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns="https://dhl24.com.pl/webapi2/provider/service.html?ws=1">
    <soap-env:Body>
        <createShipment>
            <authData>
                <username>username</username>
                <password>password</password>
            </authData>
            <shipment>
                <shipmentInfo>
                    <dropOffType>REGULAR_PICKUP</dropOffType>
                    <serviceType>AH</serviceType>
                    <billing>
                        <shippingPaymentType>SHIPPER</shippingPaymentType>
                        <paymentType>BANK_TRANSFER</paymentType>
                    </billing>
                    <specialServices>
                        <item>
                            <serviceType>POD</serviceType>
                        </item>
                    </specialServices>
                    <shipmentTime>
                        <shipmentDate>{time.strftime("%Y-%m-%d")}</shipmentDate>
                        <shipmentStartHour>10:00</shipmentStartHour>
                        <shipmentEndHour>10:00</shipmentEndHour>
                    </shipmentTime>
                    <labelType>BLP</labelType>
                </shipmentInfo>
                <content>N/A</content>
                <reference></reference>
                <ship>
                    <shipper>
                        <preaviso>
                            <personName>3e General Partnership</personName>
                            <phoneNumber>123456789</phoneNumber>
                            <emailAddress>testomir@gmail.pl</emailAddress>
                        </preaviso>
                        <contact>
                            <personName>3e General Partnership</personName>
                            <phoneNumber>123456789</phoneNumber>
                            <emailAddress>testomir@gmail.pl</emailAddress>
                        </contact>
                        <address>
                            <name>Janek</name>
                            <postalCode>00909</postalCode>
                            <city>Wawa</city>
                            <street>9 Lesna</street>
                            <houseNumber>9</houseNumber>
                            <apartmentNumber>59</apartmentNumber>
                        </address>
                    </shipper>
                    <receiver>
                        <preaviso>
                            <personName>3e General Partnership</personName>
                            <phoneNumber>123456789</phoneNumber>
                            <emailAddress>testomir@gmail.pl</emailAddress>
                        </preaviso>
                        <contact>
                            <personName>3e General Partnership</personName>
                            <phoneNumber>123456789</phoneNumber>
                            <emailAddress>testomir@gmail.pl</emailAddress>
                        </contact>
                        <address>
                            <country>PL</country>
                            <addressType>B</addressType>
                            <name>Me</name>
                            <postalCode>00001</postalCode>
                            <city>Wawa</city>
                            <street>Lesna</street>
                            <houseNumber>9</houseNumber>
                            <apartmentNumber>59</apartmentNumber>
                        </address>
                    </receiver>
                </ship>
                <pieceList>
                    <item>
                        <type>PACKAGE</type>
                        <weight>0</weight>
                        <width>7</width>
                        <height>7</height>
                        <length>25</length>
                        <quantity>1</quantity>
                    </item>
                </pieceList>
            </shipment>
        </createShipment>
    </soap-env:Body>
</soap-env:Envelope>
"""

InternationalShipmentRequestXML = f"""<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns="https://dhl24.com.pl/webapi2/provider/service.html?ws=1">
    <soap-env:Body>
        <createShipment>
            <authData>
                <username>username</username>
                <password>password</password>
            </authData>
            <shipment>
                <shipmentInfo>
                    <dropOffType>REGULAR_PICKUP</dropOffType>
                    <serviceType>AH</serviceType>
                    <billing>
                        <shippingPaymentType>SHIPPER</shippingPaymentType>
                        <paymentType>BANK_TRANSFER</paymentType>
                    </billing>
                    <specialServices>
                        <item>
                            <serviceType>POD</serviceType>
                        </item>
                    </specialServices>
                    <shipmentTime>
                        <shipmentDate>{time.strftime("%Y-%m-%d")}</shipmentDate>
                        <shipmentStartHour>10:00</shipmentStartHour>
                        <shipmentEndHour>10:00</shipmentEndHour>
                    </shipmentTime>
                    <labelType>BLP</labelType>
                </shipmentInfo>
                <content>N/A</content>
                <reference></reference>
                <ship>
                    <shipper>
                        <preaviso>
                            <personName>3e General Partnership</personName>
                            <phoneNumber>123456789</phoneNumber>
                            <emailAddress>testomir@gmail.pl</emailAddress>
                        </preaviso>
                        <contact>
                            <personName>3e General Partnership</personName>
                            <phoneNumber>123456789</phoneNumber>
                            <emailAddress>testomir@gmail.pl</emailAddress>
                        </contact>
                        <address>
                            <name>Janek</name>
                            <postalCode>00909</postalCode>
                            <city>Wawa</city>
                            <street>9 Lesna</street>
                            <houseNumber>9</houseNumber>
                            <apartmentNumber>59</apartmentNumber>
                        </address>
                    </shipper>
                    <receiver>
                        <preaviso>
                            <personName>Jain</personName>
                            <phoneNumber>1 (450) 823-8432</phoneNumber>
                        </preaviso>
                        <contact>
                            <personName>Jain</personName>
                            <phoneNumber>1 (450) 823-8432</phoneNumber>
                        </contact>
                        <address>
                            <country>CA</country>
                            <addressType>B</addressType>
                            <name>CGI</name>
                            <postalCode>k1k 4t3</postalCode>
                            <city>Ottawa</city>
                            <street>23 jardin private</street>
                            <houseNumber>9</houseNumber>
                            <apartmentNumber>59</apartmentNumber>
                        </address>
                    </receiver>
                </ship>
                <pieceList>
                    <item>
                        <type>PACKAGE</type>
                        <weight>0</weight>
                        <width>7</width>
                        <height>7</height>
                        <length>25</length>
                        <quantity>1</quantity>
                    </item>
                </pieceList>
                <customs>
                    <customsType>S</customsType>
                    <firstName>N/A</firstName>
                    <secondaryName>N/A</secondaryName>
                    <costsOfShipment>100.0</costsOfShipment>
                    <nipNr>5218487281</nipNr>
                    <categoryOfItem>9</categoryOfItem>
                    <countryOfOrigin>PL</countryOfOrigin>
                    <grossWeight>0.45</grossWeight>
                    <customsItem>
                        <item>
                            <nameEn>test</nameEn>
                            <namePl>test</namePl>
                            <quantity>1</quantity>
                            <weight>4.54</weight>
                        </item>
                    </customsItem>
                    <customAgreements>
                        <notExceedValue>true</notExceedValue>
                        <notProhibitedGoods>true</notProhibitedGoods>
                        <notRestrictedGoods>true</notRestrictedGoods>
                    </customAgreements>
                </customs>
            </shipment>
        </createShipment>
    </soap-env:Body>
</soap-env:Envelope>
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

VoidShipmentRequestXML = """<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns="https://dhl24.com.pl/webapi2/provider/service.html?ws=1">
    <soap-env:Body>
        <deleteShipment>
            <authData>
                <username>username</username>
                <password>password</password>
            </authData>
            <shipment>
                <shipmentIdentificationNumber>10000696</shipmentIdentificationNumber>
            </shipment>
        </deleteShipment>
    </soap-env:Body>
</soap-env:Envelope>
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
