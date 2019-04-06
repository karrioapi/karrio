import unittest
from gds_helpers import to_dict
from tests.aups.postage.fixture import proxy


class TestAustraliaPostPostageRate(unittest.TestCase):
    def test_parse_rate_response_errors(self):
        parsed_response = proxy.mapper.parse_quote_response(POSTAGE_RESPONSE_ERROR)
        self.assertEqual(to_dict(parsed_response), PARSED_POSTAGE_RESPONSE_ERROR)

    def test_parse_api_response_errors(self):
        parsed_response = proxy.mapper.parse_quote_response(API_ERROR)
        self.assertEqual(to_dict(parsed_response), PARSED_API_ERROR)


if __name__ == "__main__":
    unittest.main()


PARSED_POSTAGE_RESPONSE_ERROR = [
    [],
    [{"carrier": "AustraliaPost", "message": "Please enter From postcode."}],
]

PARSED_API_ERROR = [
    [],
    [{"carrier": "AustraliaPost", "code": "404", "message": "Not found"}],
]


POSTAGE_RESPONSE_ERROR = {"error": {"errorMessage": "Please enter From postcode."}}

API_ERROR = {"status": "Failed", "errors": [{"code": "404", "message": "Not found"}]}
