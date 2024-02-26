import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAustraliaPostRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v1/prices/items",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "city": "MELBOURNE",
        "state_code": "VIC",
        "postal_code": "3000",
        "country_code": "AU",
    },
    "recipient": {
        "city": "SYDNEY",
        "state_code": "NSW",
        "postal_code": "2000",
        "country_code": "AU",
    },
    "parcels": [
        {
            "length": 5,
            "height": 1,
            "width": 10,
            "weight": 2,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "packaging_type": "BOX",
            "options": {
                "insurance": 1000,
            },
        }
    ],
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "currency": "AUD",
            "extra_charges": [
                {"amount": 38.82, "currency": "AUD", "name": "base charge"},
                {"amount": 3.88, "currency": "AUD", "name": "GST"},
            ],
            "meta": {"service_name": "EXPRESS POST"},
            "service": "australiapost_express_post",
            "total_charge": 42.7,
        },
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "currency": "AUD",
            "extra_charges": [
                {"amount": 8.18, "currency": "AUD", "name": "base charge"},
                {"amount": 0.82, "currency": "AUD", "name": "GST"},
            ],
            "meta": {"service_name": "PARCEL POST + SIGNATURE"},
            "service": "T28S",
            "total_charge": 9.0,
        },
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "currency": "AUD",
            "extra_charges": [{"amount": 3.18, "currency": "AUD", "name": "GST"}],
            "meta": {"service_name": "EXPRESS POST + SIGNATURE"},
            "service": "E34S",
            "total_charge": 34.94,
        },
    ],
    [
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "code": "43003",
            "details": {},
            "message": "The service T28V1N0 is not available based upon the submitted "
            "weight of 5 kg.",
        },
        {
            "carrier_id": "australiapost",
            "carrier_name": "australiapost",
            "code": "42002",
            "details": {},
            "message": "The service T28V1N0 is not available based upon the information "
            "submitted.",
        },
    ],
]


RateRequest = {
    "items": [
        {
            "features": {"TRANSIT_COVER": {"attributes": {"cover_amount": 1000.0}}},
            "height": 1.0,
            "item_reference": "1",
            "length": 5.0,
            "packaging_type": "BOX",
            "weight": 2.0,
            "width": 10.0,
        }
    ],
    "from": {"country": "AU", "postcode": "3000"},
    "to": {"country": "AU", "postcode": "2000"},
}

RateResponse = """{
    "items": [
        {
            "weight": 5,
            "height": 5,
            "length": 5,
            "width": 5,
            "prices": [
                {
                    "product_id": "E34",
                    "product_type": "EXPRESS POST",
                    "options": {
                        "signature_on_delivery_option": false,
                        "authority_to_leave_option": true
                    },
                    "calculated_price": 42.7,
                    "calculated_price_ex_gst": 38.82,
                    "calculated_gst": 3.88,
                    "bundled_price": 37.45,
                    "bundled_price_ex_gst": 34.05,
                    "bundled_gst": 3.4,
                    "features": {
                        "feature": {
                            "type": "TRANSIT_COVER",
                            "attributes": {
                                "rate": 1.5,
                                "maximum_cover": 5000,
                                "cover_amount": 3000,
                                "included_cover": 200
                            },
                            "price": {
                                "calculated_price": 210.00,
                                "calculated_price_ex_gst": 189.99,
                                "calculated_gst": 20.01
                            },
                            "bundled": false
                        }
                    }
                },
                {
                    "product_id": "T28S",
                    "product_type": "PARCEL POST + SIGNATURE",
                    "options": {
                        "signature_on_delivery_option": true,
                        "authority_to_leave_option": true
                    },
                    "calculated_price": 9,
                    "calculated_price_ex_gst": 8.18,
                    "calculated_gst": 0.82,
                    "bundled_price": 8,
                    "bundled_price_ex_gst": 7.27,
                    "bundled_gst": 0.73
                },
                {
                    "product_id": "E34S",
                    "product_type": "EXPRESS POST + SIGNATURE",
                    "options": {
                        "signature_on_delivery_option": true,
                        "authority_to_leave_option": true
                    },
                    "calculated_price": 34.94,
                    "calculated_gst_ex_gst": 31.76,
                    "calculated_gst": 3.18,
                    "bundled_price": 29.68,
                    "bundled_price_ex_gst": 26.98,
                    "bundled_gst": 2.7
                }
            ],
            "errors": [],
            "warnings": [
                {
                    "code": "43003",
                    "name": "NO_PRICE_SCALE_FOUND_FOR_QUANTITY",
                    "message": "The service T28V1N0 is not available based upon the submitted weight of 5 kg.",
                    "context": []
                },
                {
                    "code": "42002",
                    "name": "NO_PRICES_FOR_PRODUCT",
                    "message": "The service T28V1N0 is not available based upon the information submitted.",
                    "context": []
                }
            ]
        }
    ]
}
"""
