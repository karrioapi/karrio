import unittest
from unittest.mock import patch
import purplship
from purplship.core.utils import DP
from purplship.core.models import ShipmentRequest, ShipmentCancelRequest
from tests.carrier.fixture import gateway


class TestCarrierShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)
        self.VoidShipmentRequest = ShipmentCancelRequest(**void_shipment_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), VoidShipmentRequestXML)

    def test_create_void_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.VoidShipmentRequest
        )

        self.assertEqual(request.serialize(), VoidShipmentRequestXML)

    def test_create_shipment(self):
        with patch("purplship.mappers.[carrier].proxy.http") as mocks:
            mocks.side_effect = [
                ShipmentResponseXML,
            ]
            purplship.Shipment.create(self.ShipmentRequest).from_(gateway)

            process_shipment_call, *_ = mocks.call_args_list

            self.assertEqual(
                process_shipment_call[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_void_shipment(self):
        with patch("purplship.mappers.[carrier].proxy.http") as mock:
            mock.return_value = "<a></a>"
            purplship.Shipment.cancel(self.VoidShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("purplship.mappers.[carrier].proxy.http") as mocks:
            mocks.side_effect = [
                ShipmentResponseXML,
            ]
            parsed_response = (
                purplship.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(ParsedShipmentResponse))

    def test_parse_void_shipment_response(self):
        with patch("purplship.mappers.[carrier].proxy.http") as mock:
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
    "service": "carrier_ground",
}

ParsedShipmentResponse = [
    {},
    [],
]

ParsedVoidShipmentResponse = [
    {
        "carrier_id": "carrier",
        "carrier_name": "carrier",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequestXML = """
"""

ShipmentLabelRequestXML = """
"""

ShipmentResponseXML = """
"""

ShipmentLabelResponseXML = """
"""

VoidShipmentRequestXML = """
"""

VoidShipmentResponseXML = """
"""
