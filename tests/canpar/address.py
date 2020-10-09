import unittest
import logging
from unittest.mock import patch
import purplship
from purplship.core.utils.helpers import to_dict
from purplship.core.models import AddressValidationRequest
from tests.canpar.fixture import gateway


class TestCanparAddressValidation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = AddressValidationRequest(
            **AddressValidationPayload
        )

    # def test_create_address_validation_request(self):
    #     request = gateway.mapper.create_address_validation_request(
    #         self.AddressValidationRequest
    #     )
    #
    #     self.assertEqual(
    #         request.serialize(),
    #         AddressValidationRequestXML,
    #     )
    #
    # def test_validate_address(self):
    #     with patch("purplship.mappers.canpar.proxy.http") as mock:
    #         mock.return_value = "<a></a>"
    #         purplship.Address.validate(self.AddressValidationRequest).from_(gateway)
    #
    #         self.assertEqual(
    #             mock.call_args[1]["url"],
    #             f"{gateway.settings.server_url}/EWS/V2/ServiceAvailability/ServiceAvailabilityService.asmx",
    #         )
    #
    # def test_parse_address_validation_response(self):
    #     with patch("purplship.mappers.canpar.proxy.http") as mock:
    #         mock.return_value = AddressValidationResponseXML
    #         parsed_response = (
    #             purplship.Address.validate(self.AddressValidationRequest)
    #             .from_(gateway)
    #             .parse()
    #         )
    #
    #         self.assertEqual(
    #             to_dict(parsed_response), to_dict(ParsedAddressValidationResponse)
    #         )


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

ParsedAddressValidationResponse = []


AddressValidationRequestXML = """
"""

AddressValidationResponseXML = """
"""
