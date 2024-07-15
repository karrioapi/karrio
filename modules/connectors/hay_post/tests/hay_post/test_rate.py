import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestHayPostRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.hay_post.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/Api/Order/CalculateTariff",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.hay_post.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()

RatePayload = {
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
    "services": [
        "sprint_simple"
    ],
    "options": {
        "postmen_delivery_value": True,
        "ordered_packaging": True,
        "shipment_date": "2024-06-24"
    },
}

RateRequest = {
    "additionalServices": [3, 5],
    "currencyId": 1,
    "customerId": 2004381,
    "destinationAddress": {
        "address": "Some address 1",
        "cityVillage": "Yerevan",
        "receiverInfo": {
            "companyName": "asdasd",
            "firstName": "David"
        }
    },
    "returnAddress": {
        "address": "Some address 1",
        "cityVillage": "Yerevan",
        "receiverInfo": {
            "companyName": "HayPost",
            "firstName": "GGer"
        }
    },
    "serviceCategoryDirectionId": 97,
    "totalPrice": 0,
    "weight": 1.0
}

RateResponse = """320"""
ParsedRateResponse = [
    [{
        'carrier_id': 'hay_post',
        'carrier_name': 'hay_post',
        'currency': 'AMD',
        'service': 'sprint_simple',
        'total_charge': 320.0
    }],
    []
]
