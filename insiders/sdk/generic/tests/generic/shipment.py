import unittest
import karrio
from unittest.mock import ANY
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest
from tests.generic.fixture import gateway


class TestGenericShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_request_data)

    def test_parse_rate_response(self):
        parsed_response = (
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
        )

        self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)


if __name__ == "__main__":
    unittest.main()


shipment_request_data = {
    "service": "carrier_premium",
    "label_type": "ZPL",
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "K1K4T3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "parcels": [
        {
            "height": 3.0,
            "length": 5.0,
            "width": 3.0,
            "weight": 4.0,
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "reference_number": "2975565",
            "items": [
                {
                    "weight": 1.0,
                    "weight_unit": "LB",
                    "quantity": 1,
                    "description": "Item 1",
                    "sku": "SKU-1",
                    "metadata": {
                        "RFF_CN": "037-2332855",
                        "BGM": "040000000000016256",
                        "RFF_ON": "5424560",
                        "DEPT": "DBR128",
                        "CTL": "11253678",
                        "XXNC": "138039C01",
                        "NAD_UD": "570162",
                        "RFF_AJY": "907",
                        "RFF_AEM": "3901L",
                    },
                },
            ],
        }
    ],
}


ParsedShipmentResponse = [
    {
        "carrier_id": "custom-carrier",
        "carrier_name": "custom_carrier",
        "label_type": "ZPL",
        "docs": {"label": ANY},
        "meta": {"service_name": "carrier_premium"},
        "shipment_identifier": "2975565",
        "tracking_number": "2975565",
    },
    [],
]
