import unittest
from unittest.mock import patch
from tests.aups.logistic.fixture import gateway
from purplship.core.utils.helpers import jsonify, to_dict
from purplship.core.models import RateRequest
from purplship.package import rating


class TestAustraliaPostLogisticRate(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RATE_PAYLOAD)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(to_dict(request.serialize()), to_dict(SHIPPING_PRICE_REQUEST))

    @patch("purplship.package.mappers.aups.proxy.http", return_value="{}")
    def test_get_rates(self, http_mock):
        rating.fetch(self.RateRequest).from_(gateway)

        reqUrl = http_mock.call_args[1]["url"]
        self.assertEqual(
            reqUrl, f"{gateway.settings.server_url}/shipping/v1/prices/shipments"
        )

    def test_parse_rate_response(self):
        with patch("purplship.package.mappers.aups.proxy.http") as mock:
            mock.return_value = jsonify(SHIPPING_PRICE_RESPONSE)
            parsed_response = rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(
                to_dict(parsed_response), to_dict(PARSED_SHIPPING_PRICE_RESPONSE)
            )

    def test_parse_rate_response_errors(self):
        with patch("purplship.package.mappers.aups.proxy.http") as mock:
            mock.return_value = jsonify(ERRORS)
            parsed_response = rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(to_dict(parsed_response), to_dict(PARSED_ERRORS))


if __name__ == "__main__":
    unittest.main()


RATE_PAYLOAD = {
    "shipper": {
        "person_name": "John Citizen",
        "address_line1": "1 Main Street",
        "state_code": "VIC",
        "postal_code": "3000",
        "phone_number": "0401234567",
        "email": "john.citizen@citizen.com",
        "suburb": "MELBOURNE",
    },
    "recipient": {
        "person_name": "Jane Smith",
        "company_name": "Smith Pty Ltd",
        "address_line1": "123 Centre Road",
        "state_code": "NSW",
        "postal_code": "2000",
        "phone_number": "0412345678",
        "email": "jane.smith@smith.com",
        "suburb": "Sydney",
    },
    "parcel": {
        "id": "T28S",
        "reference": "XYZ-001-01",
        "length": 10,
        "height": 10,
        "width": 10,
        "weight": 1,
    },
}


PARSED_SHIPPING_PRICE_RESPONSE = [
    [
        {
            "base_charge": 58.74,
            "carrier": "aups",
            "carrier_name": "Australia Post Shipping",
            "currency": "AUD",
            "duties_and_taxes": 5.87,
            "extra_charges": [
                {"amount": 4.51, "currency": "AUD", "name": "Fuel"},
                {"amount": 8.25, "currency": "AUD", "name": "Transit Cover"},
                {"amount": 45.98, "currency": "AUD", "name": "Freight Charge"},
            ],
            "total_charge": 64.61,
        }
    ],
    [],
]

PARSED_ERRORS = [
    [],
    [
        {
            "carrier": "aups",
            "carrier_name": "Australia Post Shipping",
            "code": "44003",
            "message": "The product T28S specified in an item has indicated that dangerous goods will be included in the parcel, however, the product does not allow dangerous goods to be sent using the service.  Please choose a product that allows dangerous goods to be included within the parcel to be sent.",
        }
    ],
]


SHIPPING_PRICE_RESPONSE = {
    "shipments": [
        {
            "shipment_reference": "XYZ-001-01",
            "from": {
                "type": "MERCHANT_LOCATION",
                "lines": ["1 Main Street"],
                "suburb": "MELBOURNE",
                "postcode": "3000",
                "state": "VIC",
                "name": "John Citizen",
                "country": "AU",
                "email": "john.citizen@citizen.com",
                "phone": "0401234567",
            },
            "to": {
                "lines": ["123 Centre Road"],
                "suburb": "Sydney",
                "postcode": "2000",
                "state": "NSW",
                "name": "Jane Smith",
                "business_name": "Smith Pty Ltd",
                "country": "AU",
                "email": "jane.smith@smith.com",
                "phone": "0412345678",
            },
            "items": [
                {"weight": 1, "height": 10, "length": 10, "width": 10},
                {"weight": 1, "height": 10, "length": 10, "width": 10},
                {"weight": 1, "height": 10, "length": 10, "width": 10},
            ],
            "shipment_summary": {
                "total_cost": 64.61,
                "total_cost_ex_gst": 58.74,
                "freight_charge": 45.98,
                "transit_cover": 8.25,
                "fuel_surcharge": 4.51,
                "total_gst": 5.87,
                "tracking_summary": {},
                "number_of_items": 4,
            },
        }
    ]
}

SHIPPING_PRICE_REQUEST = {
    "shipments": [
        {
            "shipment_reference": "XYZ-001-01",
            "email_tracking_enabled": True,
            "from_": {
                "name": "John Citizen",
                "lines": ["1 Main Street", ""],
                "suburb": "MELBOURNE",
                "state": "VIC",
                "postcode": "3000",
                "phone": "0401234567",
                "email": "john.citizen@citizen.com",
            },
            "to": {
                "name": "Jane Smith",
                "business_name": "Smith Pty Ltd",
                "lines": ["123 Centre Road", ""],
                "suburb": "Sydney",
                "state": "NSW",
                "postcode": "2000",
                "phone": "0412345678",
                "email": "jane.smith@smith.com",
            },
            "items": [
                {
                    "item_reference": "XYZ-001-01",
                    "product_id": "T28S",
                    "length": 10,
                    "height": 10,
                    "width": 10,
                    "weight": 1,
                    "authority_to_leave": False,
                    "allow_partial_delivery": True,
                }
            ],
        }
    ]
}

ERRORS = {
    "errors": [
        {
            "code": "44003",
            "name": "DANGEROUS_GOODS_NOT_SUPPORTED_BY_PRODUCT_ERROR",
            "message": "The product T28S specified in an item has indicated that dangerous goods will be included in the parcel, however, the product does not allow dangerous goods to be sent using the service.  Please choose a product that allows dangerous goods to be included within the parcel to be sent.",
        }
    ]
}
