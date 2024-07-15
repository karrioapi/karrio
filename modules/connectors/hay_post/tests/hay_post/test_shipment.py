import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestHayPostShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.hay_post.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/Api/Order/CreateOrderByCustomerShort",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.hay_post.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)


if __name__ == "__main__":
    unittest.main()

ShipmentPayload = {
    "parcels": [
        {
            "dimension_unit": "CM",
            "height": 18.2,
            "is_document": False,
            "length": 10,
            "packaging_type": "your_packaging",
            "weight": 1,
            "weight_unit": "KG",
            "width": 160
        }
    ],
    "service": "56a1sd65a1sd",
    "recipient": {
        "address_line1": "Some address 1",
        "address_line2": "Some address 2",
        "city": "Yerevan",
        "company_name": "asdasd",
        "country_code": "AM",
        "person_name": "David"
    },
    "shipper": {
        "address_line1": "Some address 1",
        "city": "Yerevan",
        "company_name": "HayPost",
        "country_code": "AM",
        "person_name": "GGer"
    },
    "options": {
        "postmen_delivery_value": True,
        "ordered_packaging": True,
        "shipment_date": "2024-06-24"
    },
    "payment": {
        "paid_by": "sender",
        "currency": None,
        "account_number": None
    },
    "billing_address": {
        "address_line1": "Some address 1",
        "address_line2": "Some address 2",
        "city": "Yerevan",
        "company_name": "asdasd",
        "country_code": "AM",
        "person_name": "David"
    }
}

ShipmentRequest = {
    "additionalServices": [3, 5],
    "customerId": 2004381,
    "weight": 1.0,
    "destinationAddress": {
        "cityVillage": "Yerevan",
        "countryId": 11,
        "receiverInfo": {
            "companyName": "asdasd",
            "firstName": "David"
        },
        "street": "1 Some address"
    },
    "returnAddress": {
        "cityVillage": "Yerevan",
        "countryId": 11,
        "receiverInfo": {
            "companyName": "HayPost",
            "firstName": "GGer"
        },
        "street": "1 Some address"
    },
}

ShipmentResponse = """{
    "id": 15022783,
    "barcode": "PAS105759416AM",
    "revertOrderId": 15022784,
    "revertBarcode": "APAS105759416AM",
    "postalcode": null
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "hay_post",
        "carrier_name": "hay_post",
        "docs": {
            "label": "No label..."
        },
        "meta": {
            "revertBarcode": "APAS105759416AM",
            "revertOrderId": 15022784
        },
        "shipment_identifier": "15022783",
        "tracking_number": "PAS105759416AM"
    },
    []
]
