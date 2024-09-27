import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTNTConnectItalyShipping(unittest.TestCase):
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
        with patch("karrio.mappers.tnt_it.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.tnt_it.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.tnt_it.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.tnt_it.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
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


ShipmentPayload = {
    "shipper": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "person_name": "TEST USER",
        "state_code": "WA",
        "email": "test@gmail.com",
        "phone_number": "(07) 3114 1499",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "k1k 4t3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "parcels": [
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "service": "carrier_service",
    "options": {
        "signature_required": True,
    },
    "reference": "#Order 11111",
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = []

ParsedCancelShipmentResponse = ParsedCancelShipmentResponse = [
    {
        "carrier_id": "tnt_it",
        "carrier_name": "tnt_it",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = """<shipment xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="W:ExpressLabel\Internazionale\routinglabel.xsd">
    <software>
        <application>MYRTL</application>
        <version>1.0</version>
    </software>
    <security>
        <customer>string</customer>
        <user>string</user>
        <password>string</password>
        <langid>IT</langid>
    </security>
    <labelType>T</labelType>
    <consignment action="I" cashondelivery="N" hazardous="N" highvalue="N" insurance="N"
        international="Y" specialgoods="N">
        <laroseDepot />
        <senderAccId>string</senderAccId>
        <consignmentno>test1</consignmentno>
        <consignmenttype>C</consignmenttype>
        <actualweight>00010500</actualweight>
        <actualvolume />
        <totalpackages>1</totalpackages>
        <packagetype>C</packagetype>
        <division>D</division>
        <product>NC</product>
        <vehicle />
        <insurancevalue>0000000010000</insurancevalue>
        <insurancecurrency>EUR</insurancecurrency>
        <packingdesc>BOX</packingdesc>
        <reference>DDT1</reference>
        <collectiondate>26062012</collectiondate>
        <collectiontime />
        <invoicevalue />
        <invoicecurrency />
        <specialinstructions>Attenzione consegnare sempre dopo le
            12:00</specialinstructions>
        <options>
            <option />
            <option />
            <option />
        </options>
        <termsofpayment>S</termsofpayment>
        <systemcode>RL</systemcode>
        <systemversion>1.0</systemversion>
        <codfvalue>0000000015000</codfvalue>
        <codfcurrency>EUR</codfcurrency>
        <goodsdesc>ABBIGLIAMENTO</goodsdesc>
        <eomenclosure />
        <eomofferno />
        <eomdivision />
        <eomunification />
        <dropoffpoint />
        <addresses>
            <address>
                <addressType>S</addressType>
                <vatno />
                <addrline1>via Roma 1</addrline1>
                <addrline2 />
                <addrline3 />
                <postcode>10100</postcode>
                <phone1>011</phone1>
                <phone2>2226111</phone2>
                <name>TEST SPA</name>
                <country>IT</country>
                <town>Torino</town>
                <contactname>Mario Rossi</contactname>
                <province>TO</province>
                <custcountry />
            </address>
            <address>
                <addressType>R</addressType>
                <vatno />
                <addrline1>Via Torino 1</addrline1>
                <addrline2 />
                <addrline3 />
                <postcode>00100</postcode>
                <phone1>06</phone1>
                <phone2>111112222</phone2>
                <name>Bianchi SRL</name>
                <country>IT</country>
                <town>Roma</town>
                <contactname>Mario Bianchi</contactname>
                <province>RO</province>
                <custcountry />
            </address>
            <address>
                <addressType>C</addressType>
                <vatno />
                <addrline1 />
                <addrline2 />
                <addrline3 />
                <postcode />
                <phone1 />
                <phone2 />
                <name />
                <country />
                <town />
                <contactname />
                <province />
                <custcountry />
            </address>
            <address>
                <addressType>D</addressType>
                <vatno />
                <addrline1 />
                <addrline2 />
                <addrline3 />
                <postcode />
                <phone1 />
                <phone2 />
                <name />
                <country />
                <town />
                <contactname />
                <province />
                <custcountry />
            </address>
        </addresses>
        <dimensions itemaction="I">
            <itemsequenceno>1</itemsequenceno>
            <itemtype>C</itemtype>
            <itemreference>0123456789</itemreference>
            <volume />
            <weight>0010000</weight>
            <length />
            <height />
            <width />
            <quantity />
        </dimensions>
        <articles>
            <tariff />
            <origcountry>IT</origcountry>
        </articles>
    </consignment>
</shipment>
"""

ShipmentCancelRequest = """<a></a>
"""

ShipmentResponse = """<a></a>
"""

ShipmentCancelResponse = """<a></a>
"""
