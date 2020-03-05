import unittest
from unittest.mock import patch
from tests.sendle.fixture import proxy
from gds_helpers import to_dict
from purplship.core.models import RateRequest
from pysendle.quotes import DomesticParcelQuote, InternationalParcelQuote


class TestSendleQuote(unittest.TestCase):
    def setUp(self):
        self.DomesticParcelQuote = DomesticParcelQuote(**DOMESTIC_PARCEL_QUOTE)
        self.InternationalParcelQuote = InternationalParcelQuote(
            **INTERNATIONAL_PARCEL_QUOTE
        )

    def test_create_domestic_quote_request(self):
        payload = RateRequest(**DOMESTIC_QUOTE_PAYLOAD)

        parcel_quote = proxy.mapper.create_quote_request(payload)
        self.assertEqual(to_dict(parcel_quote), to_dict(self.DomesticParcelQuote))

    def test_create_international_quote_request(self):
        payload = RateRequest(**INTERNATIONAL_QUOTE_PAYLOAD)

        parcel_quote = proxy.mapper.create_quote_request(payload)
        self.assertEqual(to_dict(parcel_quote), to_dict(self.InternationalParcelQuote))

    @patch("purplship.carriers.sendle.sendle_proxy.http", return_value="{}")
    def test_get_domestic_quotes(self, http_mock):
        proxy.get_quotes(self.DomesticParcelQuote)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, DOMESTIC_PARCEL_QUOTE_QUERY_STR)

    @patch("purplship.carriers.sendle.sendle_proxy.http", return_value="{}")
    def test_get_domestic_quotes(self, http_mock):
        proxy.get_quotes(self.InternationalParcelQuote)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, INTERNATIONAL_PARCEL_QUOTE_QUERY_STR)

    def test_parse_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(PARCEL_QUOTE_RESPONSE)
        self.assertEqual(to_dict(parsed_response), PARSED_PARCEL_QUOTE_RESPONSE)

    def test_parse_quote_response_errors(self):
        parsed_response = proxy.mapper.parse_quote_response(ERROR)
        self.assertEqual(to_dict(parsed_response), PARSED_ERRORS)


if __name__ == "__main__":
    unittest.main()


DOMESTIC_QUOTE_PAYLOAD = {
    "shipper": {"address_lines": ["Camberwell North"], "postal_code": "3124"},
    "recipient": {"address_lines": ["Barangaroo"], "postal_code": "2000"},
    "shipment": {"total_weight": 2.0, "extra": {"cubic_metre_volume": 0.01}},
}

INTERNATIONAL_QUOTE_PAYLOAD = {
    "shipper": {"address_lines": ["Sydney"], "postal_code": "2000"},
    "recipient": {"country_code": "NZ"},
    "shipment": {"total_weight": 5},
}


PARSED_PARCEL_QUOTE_RESPONSE = [
    [
        {
            "base_charge": 14.95,
            "carrier": "Sendle",
            "currency": "AUD",
            "delivery_date": "2018-02-19",
            "duties_and_taxes": 1.36,
            "service_name": "Easy",
            "service_type": "Easy",
            "total_charge": 13.59,
        },
        {
            "base_charge": 13.95,
            "carrier": "Sendle",
            "currency": "AUD",
            "delivery_date": "2018-02-19",
            "duties_and_taxes": 1.27,
            "service_name": "Premium",
            "service_type": "Premium",
            "total_charge": 12.68,
        },
        {
            "base_charge": 13.95,
            "carrier": "Sendle",
            "currency": "AUD",
            "delivery_date": "2018-02-14",
            "duties_and_taxes": 1.27,
            "service_name": "Pro",
            "service_type": "Pro",
            "total_charge": 12.68,
        },
    ],
    [],
]

PARSED_ERRORS = [
    [],
    [
        {
            "carrier": "Sendle",
            "code": "unprocessable_entity",
            "details": {
                "pickup_date": [
                    "must be a business day and at least one business day in the future."
                ]
            },
            "message": "The data you supplied is invalid. Error messages are in the messages section. Please fix those fields and try again.",
        }
    ],
]


"""Tests Fixtures"""

PARCEL_QUOTE_RESPONSE = [
    {
        "quote": {
            "gross": {"amount": 14.95, "currency": "AUD"},
            "net": {"amount": 13.59, "currency": "AUD"},
            "tax": {"amount": 1.36, "currency": "AUD"},
        },
        "plan_name": "Easy",
        "eta": {
            "days_range": [2, 4],
            "date_range": ["2018-02-15", "2018-02-19"],
            "for_pickup_date": "2018-02-13",
        },
    },
    {
        "quote": {
            "gross": {"amount": 13.95, "currency": "AUD"},
            "net": {"amount": 12.68, "currency": "AUD"},
            "tax": {"amount": 1.27, "currency": "AUD"},
        },
        "plan_name": "Premium",
        "eta": {
            "days_range": [0, 4],
            "date_range": ["2018-02-13", "2018-02-19"],
            "for_pickup_date": "2018-02-13",
        },
    },
    {
        "quote": {
            "gross": {"amount": 13.95, "currency": "AUD"},
            "net": {"amount": 12.68, "currency": "AUD"},
            "tax": {"amount": 1.27, "currency": "AUD"},
        },
        "plan_name": "Pro",
        "eta": {
            "days_range": [1],
            "date_range": ["2018-02-14"],
            "for_pickup_date": "2018-02-13",
        },
    },
]

DOMESTIC_PARCEL_QUOTE_QUERY_STR = f"{proxy.client.server_url}/quote?pickup_suburb=Camberwell North&pickup_postcode=3124&delivery_suburb=Barangaroo&delivery_postcode=2000&kilogram_weight=2.0&cubic_metre_volume=0.01"

DOMESTIC_PARCEL_QUOTE = {
    "pickup_suburb": "Camberwell North",
    "pickup_postcode": "3124",
    "delivery_suburb": "Barangaroo",
    "delivery_postcode": "2000",
    "kilogram_weight": 2.0,
    "cubic_metre_volume": 0.01,
}

INTERNATIONAL_PARCEL_QUOTE_QUERY_STR = f"{proxy.client.server_url}/quote?delivery_country=NZ&kilogram_weight=5&pickup_postcode=2000&pickup_suburb=Sydney"

INTERNATIONAL_PARCEL_QUOTE = {
    "pickup_suburb": "Sydney",
    "pickup_postcode": "2000",
    "delivery_country": "NZ",
    "kilogram_weight": 5,
}

ERROR = {
    "messages": {
        "pickup_date": [
            "must be a business day and at least one business day in the future."
        ]
    },
    "error": "unprocessable_entity",
    "error_description": "The data you supplied is invalid. Error messages are in the messages section. Please fix those fields and try again.",
}
