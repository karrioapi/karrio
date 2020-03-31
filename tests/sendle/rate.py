import unittest
import urllib.parse
from unittest.mock import patch
from tests.sendle.fixture import gateway
from purplship.core.utils.helpers import to_dict, jsonify
from purplship.core.errors import RequiredFieldError
from purplship.core.models import RateRequest
from purplship.package import rating


class TestSendleQuote(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.DomesticRateRequest = RateRequest(**DOMESTIC_RATE_PAYLOAD)
        self.InternationalRateRequest = RateRequest(**INTERNATIONAL_RATE_PAYLOAD)

    def test_create_domestic_rate_request(self):
        request = gateway.mapper.create_rate_request(self.DomesticRateRequest)
        self.assertEqual(request.serialize(), to_dict(DOMESTIC_PARCEL_RATE))

    def test_create_international_rate_request(self):
        request = gateway.mapper.create_rate_request(self.InternationalRateRequest)
        self.assertEqual(request.serialize(), to_dict(INTERNATIONAL_PARCEL_RATE))

    def test_create_domestic_rate_with_package_preset_request(self):
        request = gateway.mapper.create_rate_request(
            RateRequest(**DOMESTIC_RATE_WITH_PACKAGE_PRESET_PAYLOAD)
        )
        self.assertEqual(
            request.serialize(), to_dict(DOMESTIC_PARCEL_WITH_PACKAGE_REQUEST_RATE)
        )

    def test_create_international_with_package_rate_request(self):
        request = gateway.mapper.create_rate_request(
            RateRequest(**INTERNATIONAL_RATE_WITH_PACKAGE_PRESET_PAYLOAD)
        )
        self.assertEqual(
            request.serialize(), to_dict(INTERNATIONAL_PARCEL_WITH_PACKAGE_REQUEST_RATE)
        )

    def test_create_domestic_rate_missing_weight_request(self):
        with self.assertRaises(RequiredFieldError):
            gateway.mapper.create_rate_request(
                RateRequest(**DOMESTIC_RATE_MISSING_WEIGHT_PAYLOAD)
            )

    def test_create_international_rate_missing_weight_request(self):
        with self.assertRaises(RequiredFieldError):
            gateway.mapper.create_rate_request(
                RateRequest(**INTERNATIONAL_RATE_MISSING_WEIGHT_PAYLOAD)
            )

    @patch("purplship.package.mappers.sendle.proxy.http", return_value="{}")
    def test_get_domestic_rates(self, http_mock):
        rating.fetch(self.DomesticRateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, DOMESTIC_PARCEL_RATE_QUERY_STR)

    @patch("purplship.package.mappers.sendle.proxy.http", return_value="{}")
    def test_get_international_rates(self, http_mock):
        rating.fetch(self.InternationalRateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, INTERNATIONAL_PARCEL_RATE_QUERY_STR)

    def test_parse_rate_response(self):
        with patch("purplship.package.mappers.sendle.proxy.http") as mock:
            mock.return_value = jsonify(PARCEL_QUOTE_RESPONSE)
            parsed_response = (
                rating.fetch(self.DomesticRateRequest).from_(gateway).parse()
            )

            self.assertEqual(
                to_dict(parsed_response), to_dict(PARSED_PARCEL_RATE_RESPONSE)
            )

    def test_parse_rate_response_errors(self):
        with patch("purplship.package.mappers.sendle.proxy.http") as mock:
            mock.return_value = jsonify(ERROR)
            parsed_response = (
                rating.fetch(self.DomesticRateRequest).from_(gateway).parse()
            )
            self.assertEqual(to_dict(parsed_response), to_dict(PARSED_ERRORS))


if __name__ == "__main__":
    unittest.main()


DOMESTIC_RATE_PAYLOAD = {
    "shipper": {"address_line1": "Camberwell North", "postal_code": "3124"},
    "recipient": {"address_line1": "Barangaroo", "postal_code": "2000"},
    "parcel": {"weight": 2.0, "weight_unit": "KG"},
}

INTERNATIONAL_RATE_PAYLOAD = {
    "shipper": {"address_line1": "Sydney", "postal_code": "2000"},
    "recipient": {"country_code": "NZ"},
    "parcel": {"weight": 5, "weight_unit": "KG"},
}

DOMESTIC_RATE_WITH_PACKAGE_PRESET_PAYLOAD = {
    "shipper": {"address_line1": "Camberwell North", "postal_code": "3124"},
    "recipient": {"address_line1": "Barangaroo", "postal_code": "2000"},
    "parcel": {"package_preset": "sendle_shoebox"},
}

INTERNATIONAL_RATE_WITH_PACKAGE_PRESET_PAYLOAD = {
    "shipper": {"address_line1": "Sydney", "postal_code": "2000"},
    "recipient": {"country_code": "NZ"},
    "parcel": {"package_preset": "sendle_carry_on"},
}

DOMESTIC_RATE_MISSING_WEIGHT_PAYLOAD = {
    "shipper": {"address_line1": "Camberwell North", "postal_code": "3124"},
    "recipient": {"address_line1": "Barangaroo", "postal_code": "2000"},
    "parcel": {"reference": "testing request"},
}

INTERNATIONAL_RATE_MISSING_WEIGHT_PAYLOAD = {
    "shipper": {"address_line1": "Sydney", "postal_code": "2000"},
    "recipient": {"country_code": "NZ"},
    "parcel": {"reference": "testing request"},
}


PARSED_PARCEL_RATE_RESPONSE = [
    [
        {
            "base_charge": 14.95,
            "carrier": "sendle",
            "carrier_name": "Sendle",
            "currency": "AUD",
            "duties_and_taxes": 1.36,
            "estimated_delivery": "2018-02-19",
            "service": "sendle_easy",
            "total_charge": 13.59,
        },
        {
            "base_charge": 13.95,
            "carrier": "sendle",
            "carrier_name": "Sendle",
            "currency": "AUD",
            "duties_and_taxes": 1.27,
            "estimated_delivery": "2018-02-19",
            "service": "sendle_premium",
            "total_charge": 12.68,
        },
        {
            "base_charge": 13.95,
            "carrier": "sendle",
            "carrier_name": "Sendle",
            "currency": "AUD",
            "duties_and_taxes": 1.27,
            "estimated_delivery": "2018-02-14",
            "service": "sendle_pro",
            "total_charge": 12.68,
        },
    ],
    [],
]


PARSED_ERRORS = [
    [],
    [
        {
            "carrier": "sendle",
            "carrier_name": "Sendle",
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

DOMESTIC_PARCEL_RATE = {
    "pickup_suburb": "Camberwell North",
    "pickup_postcode": "3124",
    "delivery_suburb": "Barangaroo",
    "delivery_postcode": "2000",
    "kilogram_weight": "2.0",
}

DOMESTIC_PARCEL_RATE_QUERY_STR = f"{gateway.settings.server_url}/quote?{urllib.parse.urlencode(to_dict(DOMESTIC_PARCEL_RATE))}"

DOMESTIC_PARCEL_WITH_PACKAGE_REQUEST_RATE = {
    "pickup_suburb": "Camberwell North",
    "pickup_postcode": "3124",
    "delivery_suburb": "Barangaroo",
    "delivery_postcode": "2000",
    "kilogram_weight": "0.907184",
}


INTERNATIONAL_PARCEL_RATE = {
    "pickup_suburb": "Sydney",
    "pickup_postcode": "2000",
    "delivery_country": "NZ",
    "kilogram_weight": "5.0",
}

INTERNATIONAL_PARCEL_RATE_QUERY_STR = f"{gateway.settings.server_url}/quote?{urllib.parse.urlencode(to_dict(INTERNATIONAL_PARCEL_RATE))}"


INTERNATIONAL_PARCEL_WITH_PACKAGE_REQUEST_RATE = {
    "pickup_suburb": "Sydney",
    "pickup_postcode": "2000",
    "delivery_country": "NZ",
    "kilogram_weight": "4.53592",
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
