import unittest
from unittest.mock import patch
import purplship
from purplship.core.utils import DP
from purplship.core.models import AddressValidationRequest
from tests.carrier.fixture import gateway


class TestCarrierAddressValidation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = AddressValidationRequest(
            **AddressValidationPayload
        )

    def test_create_address_validation_request(self):
        request = gateway.mapper.create_address_validation_request(
            self.AddressValidationRequest
        )

        self.assertEqual(
            request.serialize(),
            AddressValidationRequestXML,
        )

    def test_validate_address(self):
        with patch("purplship.mappers.[carrier].proxy.http") as mock:
            mock.return_value = "<a></a>"
            purplship.Address.validate(self.AddressValidationRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_address_validation_response(self):
        with patch("purplship.mappers.[carrier].proxy.http") as mock:
            mock.return_value = AddressValidationResponseXML
            parsed_response = (
                purplship.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedAddressValidationResponse)
            )


if __name__ == "__main__":
    unittest.main()


AddressValidationPayload = {
    "address": {
        "address_line1": "Suit 333",
        "address_line2": "333 Twin",
        "postal_code": "V5E4H9",
        "city": "Burnaby",
        "country_code": "CA",
        "state_code": "BC",
    }
}

ParsedAddressValidationResponse = [
    {
        "carrier_id": "carrier",
        "carrier_name": "carrier",
        "complete_address": {
            "address_line1": "565 SHERBOURNE ST",
            "city": "TORONTO",
            "country_code": "CA",
            "postal_code": "M4X1W7",
            "residential": False,
            "state_code": "ON",
        },
        "success": True,
    },
    [],
]


AddressValidationRequestXML = """
"""

AddressValidationResponseXML = """
"""
