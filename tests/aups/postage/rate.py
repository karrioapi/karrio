import unittest
from unittest.mock import patch
from gds_helpers import to_dict
from tests.aups.postage.fixture import proxy
from purplship.domain.Types import RateRequest
from pyaups.domestic_letter_postage import ServiceRequest as LetterServiceRequest
from pyaups.international_parcel_postage import ServiceRequest as ParcelServiceRequest


class TestAustraliaPostPostageRate(unittest.TestCase):
    def setUp(self):
        self.LetterServiceRequest = LetterServiceRequest(
            **DOMESTIC_LETTER_POSTAGE_REQUEST
        )
        self.ParcelServiceRequest = ParcelServiceRequest(**INTL_PARCEL_POSTAGE_REQUEST)

    def test_create_rate_request(self):
        payload = RateRequest(**DOMESTIC_LETTER_PAYLOAD)

        shipping_price_request = proxy.mapper.create_quote_request(payload)
        self.assertEqual(
            to_dict(shipping_price_request), to_dict(self.LetterServiceRequest)
        )

    def test_create_intl_rate_request(self):
        payload = RateRequest(**INTL_PARCEL_PAYLOAD)

        shipping_price_request = proxy.mapper.create_quote_request(payload)
        self.assertEqual(
            to_dict(shipping_price_request), to_dict(self.ParcelServiceRequest)
        )

    @patch("purplship.carriers.aups.aups_proxy.http", return_value="{}")
    def test_domestic_letter_get_quotes(self, http_mock):
        proxy.get_quotes(self.LetterServiceRequest)

        req_url = http_mock.call_args[1]["url"]
        self.assertEqual(
            req_url, DOMESTIC_LETTER_POSTAGE_REQUEST_URL
        )

    @patch("purplship.carriers.aups.aups_proxy.http", return_value="{}")
    def test_intl_parcel_get_quotes(self, http_mock):
        proxy.get_quotes(self.ParcelServiceRequest)

        req_url = http_mock.call_args[1]["url"]
        self.assertEqual(
            req_url, INTL_PARCEL_POSTAGE_REQUEST_URL
        )

    def test_parse_domestic_rate_response(self):
        parsed_response = proxy.mapper.parse_quote_response(
            DOMESTIC_POSTAGE_SERVICE_RESPONSE
        )
        self.assertEqual(
            to_dict(parsed_response), PARSED_DOMESTIC_POSTAGE_SERVICE_RESPONSE
        )

    def test_parse_intl_rate_response(self):
        parsed_response = proxy.mapper.parse_quote_response(
            INTL_POSTAGE_SERVICE_RESPONSE
        )
        self.assertEqual(to_dict(parsed_response), PARSED_INTL_POSTAGE_SERVICE_RESPONSE)

    def test_parse_rate_response_errors(self):
        parsed_response = proxy.mapper.parse_quote_response(POSTAGE_RESPONSE_ERROR)
        self.assertEqual(to_dict(parsed_response), PARSED_POSTAGE_RESPONSE_ERROR)

    def test_parse_api_response_errors(self):
        parsed_response = proxy.mapper.parse_quote_response(API_ERROR)
        self.assertEqual(to_dict(parsed_response), PARSED_API_ERROR)


if __name__ == "__main__":
    unittest.main()


DOMESTIC_LETTER_PAYLOAD = {
    "shipper": {"country_code": "AU", "postal_code": "2000"},
    "recipient": {"country_code": "AU", "postal_code": "3000"},
    "shipment": {
        "dimension_unit": "CM",
        "weight_unit": "KG",
        "items": [
            {
                "length": 10.0,
                "width": 10.0,
                "height": 10.0,
                "weight": 1.0,
                "packaging_type": "SM",
            }
        ],
    },
}

INTL_PARCEL_PAYLOAD = {
    "shipper": {"country_code": "AU"},
    "recipient": {"country_code": "US"},
    "shipment": {
        "dimension_unit": "CM",
        "weight_unit": "KG",
        "items": [{"id": "1", "height": 10, "length": 10, "width": 10, "weight": 0.5}],
    },
}

PARSED_INTL_POSTAGE_SERVICE_RESPONSE = [
    [
        {
            "carrier": "AustraliaPost",
            "currency": "AUD",
            "service_name": "Courier",
            "service_type": "INT_PARCEL_COR_OWN_PACKAGING",
            "total_charge": 91.35,
        },
        {
            "carrier": "AustraliaPost",
            "currency": "AUD",
            "service_name": "Express",
            "service_type": "INT_PARCEL_EXP_OWN_PACKAGING",
            "total_charge": 41.35,
        },
        {
            "carrier": "AustraliaPost",
            "currency": "AUD",
            "service_name": "Standard",
            "service_type": "INT_PARCEL_STD_OWN_PACKAGING",
            "total_charge": 24.0,
        },
        {
            "carrier": "AustraliaPost",
            "currency": "AUD",
            "service_name": "Economy Air",
            "service_type": "INT_PARCEL_AIR_OWN_PACKAGING",
            "total_charge": 17.0,
        },
    ],
    [],
]

PARSED_DOMESTIC_POSTAGE_SERVICE_RESPONSE = [
    [
        {
            "carrier": "AustraliaPost",
            "currency": "AUD",
            "service_name": "Express Post",
            "service_type": "AUS_PARCEL_EXPRESS",
            "total_charge": 21.45,
        },
        {
            "carrier": "AustraliaPost",
            "currency": "AUD",
            "service_name": "Small-Medium satchel",
            "service_type": "AUS_PARCEL_EXPRESS_SATCHEL_1KG",
            "total_charge": 14.55,
        },
        {
            "carrier": "AustraliaPost",
            "currency": "AUD",
            "service_name": "Parcel Post",
            "service_type": "AUS_PARCEL_REGULAR",
            "total_charge": 15.05,
        },
        {
            "carrier": "AustraliaPost",
            "currency": "AUD",
            "service_name": "Small-Medium satchel",
            "service_type": "AUS_PARCEL_REGULAR_SATCHEL_1KG",
            "total_charge": 11.55,
        },
    ],
    [],
]

PARSED_POSTAGE_RESPONSE_ERROR = [
    [],
    [{"carrier": "AustraliaPost", "message": "Please enter From postcode."}],
]

PARSED_API_ERROR = [
    [],
    [{"carrier": "AustraliaPost", "code": "404", "message": "Not found"}],
]


INTL_PARCEL_POSTAGE_REQUEST = {"country_code": "US", "weight": 0.5}

INTL_PARCEL_POSTAGE_REQUEST_URL = f"https://digitalapi.auspost.com.au/postage/parcel/international/service.json?country_code=US&weight=0.5"

DOMESTIC_LETTER_POSTAGE_REQUEST = {
    "length": 10.0,
    "thickness": 10.0,
    "weight": 1.0,
    "width": 10.0,
}

DOMESTIC_LETTER_POSTAGE_REQUEST_URL = f"https://digitalapi.auspost.com.au/postage/letter/domestic/service.json?length=10.0&thickness=10.0&weight=1.0&width=10.0"

POSTAGE_RESPONSE_ERROR = {"error": {"errorMessage": "Please enter From postcode."}}

API_ERROR = {"status": "Failed", "errors": [{"code": "404", "message": "Not found"}]}

DOMESTIC_POSTAGE_SERVICE_RESPONSE = {
    "services": {
        "service": [
            {
                "code": "AUS_PARCEL_EXPRESS",
                "name": "Express Post",
                "price": "21.45",
                "max_extra_cover": 500,
                "options": {
                    "option": [
                        {
                            "code": "AUS_SERVICE_OPTION_STANDARD",
                            "name": "Standard Service",
                            "suboptions": {
                                "option": {
                                    "code": "AUS_SERVICE_OPTION_EXTRA_COVER",
                                    "name": "Extra Cover",
                                    "max_extra_cover": 500,
                                }
                            },
                        },
                        {
                            "code": "AUS_SERVICE_OPTION_SIGNATURE_ON_DELIVERY",
                            "name": "Signature on Delivery",
                            "suboptions": {
                                "option": {
                                    "code": "AUS_SERVICE_OPTION_EXTRA_COVER",
                                    "name": "Extra Cover",
                                    "max_extra_cover": 5000,
                                }
                            },
                        },
                    ]
                },
            },
            {
                "code": "AUS_PARCEL_EXPRESS_SATCHEL_1KG",
                "name": "Small-Medium satchel",
                "price": "14.55",
                "max_extra_cover": 500,
                "options": {
                    "option": [
                        {
                            "code": "AUS_SERVICE_OPTION_STANDARD",
                            "name": "Standard Service",
                            "suboptions": {
                                "option": {
                                    "code": "AUS_SERVICE_OPTION_EXTRA_COVER",
                                    "name": "Extra Cover",
                                    "max_extra_cover": 500,
                                }
                            },
                        },
                        {
                            "code": "AUS_SERVICE_OPTION_SIGNATURE_ON_DELIVERY",
                            "name": "Signature on Delivery",
                            "suboptions": {
                                "option": {
                                    "code": "AUS_SERVICE_OPTION_EXTRA_COVER",
                                    "name": "Extra Cover",
                                    "max_extra_cover": 5000,
                                }
                            },
                        },
                    ]
                },
            },
            {
                "code": "AUS_PARCEL_REGULAR",
                "name": "Parcel Post",
                "price": "15.05",
                "max_extra_cover": 500,
                "options": {
                    "option": [
                        {
                            "code": "AUS_SERVICE_OPTION_STANDARD",
                            "name": "Standard Service",
                            "suboptions": {
                                "option": {
                                    "code": "AUS_SERVICE_OPTION_EXTRA_COVER",
                                    "name": "Extra Cover",
                                    "max_extra_cover": 500,
                                }
                            },
                        },
                        {
                            "code": "AUS_SERVICE_OPTION_SIGNATURE_ON_DELIVERY",
                            "name": "Signature on Delivery",
                            "suboptions": {
                                "option": {
                                    "code": "AUS_SERVICE_OPTION_EXTRA_COVER",
                                    "name": "Extra Cover",
                                    "max_extra_cover": 5000,
                                }
                            },
                        },
                    ]
                },
            },
            {
                "code": "AUS_PARCEL_REGULAR_SATCHEL_1KG",
                "name": "Small-Medium satchel",
                "price": "11.55",
                "max_extra_cover": 500,
                "options": {
                    "option": [
                        {
                            "code": "AUS_SERVICE_OPTION_STANDARD",
                            "name": "Standard Service",
                            "suboptions": {
                                "option": {
                                    "code": "AUS_SERVICE_OPTION_EXTRA_COVER",
                                    "name": "Extra Cover",
                                    "max_extra_cover": 500,
                                }
                            },
                        },
                        {
                            "code": "AUS_SERVICE_OPTION_SIGNATURE_ON_DELIVERY",
                            "name": "Signature on Delivery",
                            "suboptions": {
                                "option": {
                                    "code": "AUS_SERVICE_OPTION_EXTRA_COVER",
                                    "name": "Extra Cover",
                                    "max_extra_cover": 5000,
                                }
                            },
                        },
                    ]
                },
            },
        ]
    }
}

INTL_POSTAGE_SERVICE_RESPONSE = {
    "services": {
        "service": [
            {
                "code": "INT_PARCEL_COR_OWN_PACKAGING",
                "name": "Courier",
                "price": "91.35",
                "max_extra_cover": 5000,
                "options": {
                    "option": [
                        {"code": "INT_TRACKING", "name": "Tracking"},
                        {"code": "INT_SMS_TRACK_ADVICE", "name": "SMS track advice"},
                        {"code": "INT_EXTRA_COVER", "name": "Extra Cover"},
                    ]
                },
            },
            {
                "code": "INT_PARCEL_EXP_OWN_PACKAGING",
                "name": "Express",
                "price": "41.35",
                "max_extra_cover": 5000,
                "options": {
                    "option": [
                        {"code": "INT_TRACKING", "name": "Tracking"},
                        {
                            "code": "INT_SIGNATURE_ON_DELIVERY",
                            "name": "Signature on delivery",
                        },
                        {"code": "INT_SMS_TRACK_ADVICE", "name": "SMS track advice"},
                        {"code": "INT_EXTRA_COVER", "name": "Extra Cover"},
                    ]
                },
            },
            {
                "code": "INT_PARCEL_STD_OWN_PACKAGING",
                "name": "Standard",
                "price": "24.00",
                "max_extra_cover": 5000,
                "options": {
                    "option": [
                        {"code": "INT_TRACKING", "name": "Tracking"},
                        {"code": "INT_EXTRA_COVER", "name": "Extra Cover"},
                        {
                            "code": "INT_SIGNATURE_ON_DELIVERY",
                            "name": "Signature on delivery",
                        },
                        {"code": "INT_SMS_TRACK_ADVICE", "name": "SMS track advice"},
                    ]
                },
            },
            {
                "code": "INT_PARCEL_AIR_OWN_PACKAGING",
                "name": "Economy Air",
                "price": "17.00",
                "max_extra_cover": 5000,
                "options": {
                    "option": [
                        {"code": "INT_EXTRA_COVER", "name": "Extra Cover"},
                        {
                            "code": "INT_SIGNATURE_ON_DELIVERY",
                            "name": "Signature on delivery",
                        },
                    ]
                },
            },
        ]
    }
}
