import unittest
from unittest.mock import patch, ANY
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models
from .fixture import gateway, LabelResponse


class TestCanadaPostReturnShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ReturnShipmentRequest = models.ShipmentRequest(
            **return_shipment_data
        )

    def test_create_return_shipment_request(self):
        request = gateway.mapper.create_return_shipment_request(
            self.ReturnShipmentRequest
        )

        self.assertEqual(request.serialize(), ReturnShipmentRequestXML)

    def test_create_return_shipment(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.side_effect = [ReturnShipmentResponseXML, LabelResponse]
            karrio.Shipment.create(self.ReturnShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args_list[0][1]["url"],
                f"{gateway.settings.server_url}/rs/{gateway.settings.customer_number}/{gateway.settings.customer_number}/authorizedreturn",
            )

    def test_parse_return_shipment_response(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.side_effect = [ReturnShipmentResponseXML, LabelResponse]
            parsed_response = (
                karrio.Shipment.create(self.ReturnShipmentRequest)
                .from_(gateway)
                .parse()
            )

            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedReturnShipmentResponse
            )

    def test_parse_return_shipment_error_response(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.side_effect = [ReturnShipmentErrorResponseXML, None]
            parsed_response = (
                karrio.Shipment.create(self.ReturnShipmentRequest)
                .from_(gateway)
                .parse()
            )

            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedReturnShipmentErrorResponse
            )


if __name__ == "__main__":
    unittest.main()


return_shipment_data = {
    "service": "canadapost_expedited_parcel",
    "is_return": True,
    "reference": "Return Order 12345",
    "shipper": {
        "person_name": "Customer Name",
        "company_name": "Customer Inc",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "state_code": "QC",
    },
    "recipient": {
        "person_name": "Warehouse Manager",
        "company_name": "Return Center Inc",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "K1K4T3",
        "country_code": "CA",
        "state_code": "ON",
        "email": "returns@example.com",
    },
    "parcels": [
        {
            "weight": 2.0,
            "weight_unit": "KG",
            "height": 10,
            "length": 20,
            "width": 15,
            "dimension_unit": "CM",
        }
    ],
    "payment": {"account_number": "2004381"},
}


ParsedReturnShipmentResponse = [
    {
        "carrier_name": "canadapost",
        "carrier_id": "canadapost",
        "tracking_number": "987654321098",
        "shipment_identifier": "987654321098",
        "label_type": "PDF",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://www.canadapost-postescanada.ca/track-reperage/en#/resultList?searchFor=987654321098",
            "tracking_numbers": ["987654321098"],
            "shipment_identifiers": ["987654321098"],
        },
    },
    [],
]

ParsedReturnShipmentErrorResponse = [
    None,
    [
        {
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "code": "9111",
            "details": {},
            "message": "Postal code is not valid for province.",
        }
    ],
]

ReturnShipmentRequestXML = """<authorized-return xmlns="http://www.canadapost.ca/ws/authreturn-v2">
    <service-code>DOM.EP</service-code>
    <returner>
        <name>Customer Name</name>
        <company>Customer Inc</company>
        <domestic-address>
            <address-line-1>502 MAIN ST N</address-line-1>
            <city>MONTREAL</city>
            <province>QC</province>
            <postal-code>H2B1A0</postal-code>
        </domestic-address>
    </returner>
    <receiver>
        <name>Warehouse Manager</name>
        <company>Return Center Inc</company>
        <email>returns@example.com</email>
        <domestic-address>
            <address-line-1>23 jardin private</address-line-1>
            <city>Ottawa</city>
            <province>ON</province>
            <postal-code>K1K4T3</postal-code>
        </domestic-address>
    </receiver>
    <parcel-characteristics>
        <weight>2</weight>
        <dimensions>
            <length>20.0</length>
            <width>15.0</width>
            <height>10.0</height>
        </dimensions>
    </parcel-characteristics>
    <print-preferences>
        <output-format>4x6</output-format>
        <encoding>PDF</encoding>
    </print-preferences>
    <settlement-info>
        <paid-by-customer>2004381</paid-by-customer>
        <contract-id>42708517</contract-id>
    </settlement-info>
    <references>
        <customer-ref-1>Return Order 12345</customer-ref-1>
    </references>
</authorized-return>
"""

ReturnShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<authorized-return-info xmlns="http://www.canadapost.ca/ws/authreturn-v2">
    <tracking-pin>987654321098</tracking-pin>
    <links>
        <link rel="label" href="https://ct.soa-gw.canadapost.ca/rs/artifact/return/label/987654321098" media-type="application/pdf" index="0"/>
    </links>
</authorized-return-info>
"""

ReturnShipmentErrorResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<messages xmlns="http://www.canadapost.ca/ws/messages">
    <message>
        <code>9111</code>
        <description>Postal code is not valid for province.</description>
    </message>
</messages>
"""
