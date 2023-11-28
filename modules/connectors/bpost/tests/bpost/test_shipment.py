import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestBelgianPostShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.IntlShipmentRequest = models.ShipmentRequest(**IntlShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_intl_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.IntlShipmentRequest)

        self.assertEqual(request.serialize(), IntlShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.bpost.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse]
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args_list[0][1]["url"],
                f"{gateway.settings.server_url}/123456/orders/",
            )
            self.assertEqual(
                mock.call_args_list[1][1]["url"],
                f"{gateway.settings.server_url}/123456/orders/TEST_20131202_036/labels/A4",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.bpost.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/123456/orders/323212345659900357663030",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.bpost.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.bpost.proxy.lib.request") as mock:
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
        with patch("karrio.mappers.bpost.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "bpack_24h_pro",
    "shipper": {
        "company_name": "bpost - bpack",
        "person_name": "Business Solutions Team",
        "street_number": "1",
        "address_line1": "Muntcentrum",
        "city": "Brussel",
        "postal_code": "1000",
        "country_code": "BE",
        "email": "esolutions@bpost.be",
        "phone_number": "0032499123456",
    },
    "recipient": {
        "company_name": "Vandenborre",
        "person_name": "Reception Desk",
        "street_number": "105",
        "address_line1": "Bruul",
        "city": "Mechelen",
        "postal_code": "2800",
        "country_code": "BE",
        "email": "test@provider.be",
        "phone_number": "0032499123456",
    },
    "parcels": [
        {
            "weight": 2.0,
            "weight_unit": "KG",
            "reference_number": "TEST_20131202_036",
            "items": [
                {"description": "Earphones", "quantity": 10},
                {"description": "Ipad 5", "quantity": 20},
            ],
        }
    ],
    "label_type": "PDF",
    "reference": "bpack@home VAS 036",
    "options": {
        "bpost_signed": True,
        "bpost_info_next_day": "tester@test.com",
    },
}

IntlShipmentPayload = {
    "service": "bpack_bpost_international",
    "shipper": {
        "company_name": "SENDER_COMPANY",
        "person_name": "SENDER_NAME",
        "street_number": "1",
        "address_line1": "sender_street_name",
        "city": "sender_city",
        "postal_code": "1000",
        "country_code": "BE",
        "email": "sender@test.be",
        "phone_number": "0032123456789",
    },
    "recipient": {
        "company_name": "company_name",
        "person_name": "name_of_final_receiver",
        "street_number": "7",
        "address_line1": "street_name_of_final_receiver",
        "city": "city_of_final_receiver",
        "postal_code": "4811 ZG",
        "country_code": "FR",
        "email": "finalreceiver@test.be",
        "phone_number": "0033123456789",
    },
    "parcels": [
        {
            "weight": 2.0,
            "weight_unit": "KG",
            "reference_number": "customer reference xxxx08",
            "items": [
                {"description": "Product 1", "quantity": 1},
            ],
        }
    ],
    "label_type": "PDF",
    "reference": "Reference that can be used for cross-referencing",
    "options": {
        "bpost_keep_me_informed": "sender@test.be",
        "bpost_parcel_return_instructions": "RTS",
        "bpost_pugo_id": "163372",
        "bpost_pugo_name": "name_of_delivery_point",
        "bpost_pugo_address": {
            "street_number": "89",
            "address_line1": "street_of_delivery_point",
            "city": "city_of_delivery_point",
            "postal_code": "75009",
            "country_code": "FR",
        },
    },
    "customs": {
        "commodities": [{"description": "Product 1", "quantity": 1}],
        "duty": {"declared_value": 1000},
        "content_description": "Test description",
        "content_type": "GOODS",
    },
}

ShipmentCancelPayload = {
    "shipment_identifier": "323212345659900357663030",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "bpost",
        "carrier_name": "bpost",
        "docs": {"label": ANY},
        "label_type": "PNG",
        "shipment_identifier": "TEST_20131202_036",
        "tracking_number": "323212345659900357663030",
        "meta": {
            "carrier_tracking_url": "https://track.bpost.cloud/btr/web/#/search?itemCode=323212345659900357663030&lang=EN",
            "shipment_identifiers": ["TEST_20131202_036"],
            "tracking_numbers": [
                "323212345659900357663030",
                "323212345659900357664050",
            ],
        },
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "bpost",
        "carrier_name": "bpost",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "bpost",
            "carrier_name": "bpost",
            "code": 409,
            "details": {},
            "message": "The order is in CANCELLED state and cannot be modified anymore.",
        }
    ],
]


ShipmentRequest = """<tns:order xmlns="http://schema.post.be/shm/deepintegration/v5/national" xmlns:common="http://schema.post.be/shm/deepintegration/v5/common" xmlns:tns="http://schema.post.be/shm/deepintegration/v5/" xmlns:international="http://schema.post.be/shm/deepintegration/v5/international" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://schema.post.be/shm/deepintegration/v5/">
    <tns:accountId>123456</tns:accountId>
    <tns:reference>TEST_20131202_036</tns:reference>
    <tns:costCenter>Cost Center</tns:costCenter>
    <tns:orderLine>
        <tns:text>Earphones</tns:text>
        <tns:nbOfItems>10</tns:nbOfItems>
    </tns:orderLine>
    <tns:orderLine>
        <tns:text>Ipad 5</tns:text>
        <tns:nbOfItems>20</tns:nbOfItems>
    </tns:orderLine>
    <tns:box>
        <tns:sender>
            <common:name>Business Solutions Team</common:name>
            <common:company>bpost - bpack</common:company>
            <common:address>
                <common:streetName>Muntcentrum</common:streetName>
                <common:number>1</common:number>
                <common:postalCode>1000</common:postalCode>
                <common:locality>Brussel</common:locality>
                <common:countryCode>BE</common:countryCode>
            </common:address>
            <common:emailAddress>esolutions@bpost.be</common:emailAddress>
            <common:phoneNumber>0032499123456</common:phoneNumber>
        </tns:sender>
        <tns:nationalBox>
            <atHome>
                <product>bpack 24h Pro</product>
                <options>
                    <common:infoNextDay language="EN">
                        <common:emailAddress>tester@test.com</common:emailAddress>
                    </common:infoNextDay>
                    <common:keepMeInformed language="EN">
                        <common:emailAddress>test@provider.be</common:emailAddress>
                    </common:keepMeInformed>
                    <common:signed/>
                </options>
                <weight>2000</weight>
                <receiver>
                    <common:name>Reception Desk</common:name>
                    <common:company>Vandenborre</common:company>
                    <common:address>
                        <common:streetName>Bruul</common:streetName>
                        <common:number>105</common:number>
                        <common:postalCode>2800</common:postalCode>
                        <common:locality>Mechelen</common:locality>
                        <common:countryCode>BE</common:countryCode>
                    </common:address>
                    <common:emailAddress>test@provider.be</common:emailAddress>
                    <common:phoneNumber>0032499123456</common:phoneNumber>
                </receiver>
            </atHome>
        </tns:nationalBox>
        <tns:remark>bpack@home VAS 036</tns:remark>
    </tns:box>
</tns:order>
"""

IntlShipmentRequest = """<tns:order xmlns="http://schema.post.be/shm/deepintegration/v5/national" xmlns:common="http://schema.post.be/shm/deepintegration/v5/common" xmlns:tns="http://schema.post.be/shm/deepintegration/v5/" xmlns:international="http://schema.post.be/shm/deepintegration/v5/international" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://schema.post.be/shm/deepintegration/v5/">
    <tns:accountId>123456</tns:accountId>
    <tns:reference>customer reference xxxx08</tns:reference>
    <tns:costCenter>Cost Center</tns:costCenter>
    <tns:orderLine>
        <tns:text>Product 1</tns:text>
        <tns:nbOfItems>1</tns:nbOfItems>
    </tns:orderLine>
    <tns:box>
        <tns:sender>
            <common:name>SENDER_NAME</common:name>
            <common:company>SENDER_COMPANY</common:company>
            <common:address>
                <common:streetName>sender_street_name</common:streetName>
                <common:number>1</common:number>
                <common:postalCode>1000</common:postalCode>
                <common:locality>sender_city</common:locality>
                <common:countryCode>BE</common:countryCode>
            </common:address>
            <common:emailAddress>sender@test.be</common:emailAddress>
            <common:phoneNumber>0032123456789</common:phoneNumber>
        </tns:sender>
        <tns:internationalBox>
            <international:atIntlPugo>
                <international:product>bpack@bpost international</international:product>
                <international:options>
                    <common:keepMeInformed language="EN">
                        <common:emailAddress>sender@test.be</common:emailAddress>
                    </common:keepMeInformed>
                </international:options>
                <international:receiver>
                    <common:name>name_of_final_receiver</common:name>
                    <common:company>company_name</common:company>
                    <common:address>
                        <common:streetName>street_name_of_final_receiver</common:streetName>
                        <common:number>7</common:number>
                        <common:postalCode>4811 ZG</common:postalCode>
                        <common:locality>city_of_final_receiver</common:locality>
                        <common:countryCode>FR</common:countryCode>
                    </common:address>
                    <common:emailAddress>finalreceiver@test.be</common:emailAddress>
                    <common:phoneNumber>0033123456789</common:phoneNumber>
                </international:receiver>
                <international:parcelWeight>2000</international:parcelWeight>
                <international:customsInfo>
                    <international:parcelValue>1000</international:parcelValue>
                    <international:contentDescription>Test description</international:contentDescription>
                    <international:shipmentType>GOODS</international:shipmentType>
                    <international:parcelReturnInstructions>RTS</international:parcelReturnInstructions>
                    <international:privateAddress>false</international:privateAddress>
                </international:customsInfo>
                <international:parcelContents>
                    <international:parcelContent>
                        <international:numberOfItemType>1</international:numberOfItemType>
                        <international:itemDescription>Product 1</international:itemDescription>
                    </international:parcelContent>
                </international:parcelContents>
                <international:pugoId>163372</international:pugoId>
                <international:pugoName>name_of_delivery_point</international:pugoName>
                <international:pugoAddress>
                    <common:streetName>street_of_delivery_point</common:streetName>
                    <common:number>89</common:number>
                    <common:postalCode>75009</common:postalCode>
                    <common:locality>city_of_delivery_point</common:locality>
                    <common:countryCode>FR</common:countryCode>
                </international:pugoAddress>
            </international:atIntlPugo>
        </tns:internationalBox>
        <tns:remark>Reference that can be used for cross-referencing</tns:remark>
    </tns:box>
</tns:order>
"""

ShipmentCancelRequest = """<orderUpdate xmlns="http://schema.post.be/shm/deepintegration/v3/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://schema.post.be/shm/deepintegration/v3/">
    <common:status>CANCELLED</common:status>
</orderUpdate>
"""

ShipmentResponse = ""

LabelResponse = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<labels xmlns="http://schema.post.be/shm/deepintegration/v5/"
    xmlns:ns2="http://schema.post.be/shm/deepintegration/v5/common"
    xmlns:ns3="http://schema.post.be/shm/deepintegration/v5/national"
    xmlns:ns4="http://schema.post.be/shm/deepintegration/v5/international">
    <label>
        <barcode>323212345659900357663030</barcode>
        <barcode>323212345659900357664050</barcode>
        <mimeType>image/png</mimeType>
        <bytes>iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8z8BQz0AEYBxVSF+FABJADveWkH6oAAAAAElFTkSuQmCC</bytes>
    </label>
</labels>
"""

ShipmentCancelResponse = ""

ErrorResponse = """<ns2:businessException xmlns="http://schema.post.be/common/exception/v1/"
    xmlns:ns2="http://schema.post.be/api/shm/v1/">
    <code>409</code>
    <message>The order is in CANCELLED state and cannot be modified anymore.</message>
</ns2:businessException>
"""
