import unittest
from unittest.mock import patch
import purplship
from purplship.core.utils.helpers import to_dict
from purplship.core.models import ShipmentRequest
from tests.canpar.fixture import gateway


class TestCanparShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)


if __name__ == "__main__":
    unittest.main()

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
            "height": 9,
            "length": 6,
            "width": 12,
            "weight": 20.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "service": "canadapost_expedited_parcel",
    "options": {
        "canadapost_signature": True,
        "cash_on_delivery": {"amount": 10.5},
        "insurance": {"amount": 70.0},
    },
}

ParsedShipmentResponse = []

ShipmentRequestXML = """
"""

ShipmentRequestWithPackagePresetXML = """
"""

ShipmentResponseXML = """
"""
