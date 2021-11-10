import unittest
from unittest.mock import patch
import purplship
from purplship.core.utils import DP
from purplship.core.models import AddressValidationRequest
from tests.ups.fixture import gateway


class TestUPSAddressValidation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = AddressValidationRequest(
            **AddressValidationPayload
        )

    def test_create_address_validation_request(self):
        request = gateway.mapper.create_address_validation_request(
            self.AddressValidationRequest
        )

        self.assertEqual(request.serialize(), AddressValidationRequestXML)

    def test_validate_address(self):
        with patch("purplship.mappers.ups.proxy.http") as mock:
            mock.return_value = "<a></a>"
            purplship.Address.validate(self.AddressValidationRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/webservices/AV",
            )

    def test_parse_address_validation_response(self):
        with patch("purplship.mappers.ups.proxy.http") as mock:
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
        "postal_code": "94089",
        "city": "North Dakhota",
        "country_code": "US",
        "state_code": "CA",
    }
}

ParsedAddressValidationResponse = [
    {
        "carrier_id": "ups",
        "carrier_name": "ups",
        "success": True,
    },
    [],
]


AddressValidationRequestXML = """<AddressValidationRequest xml:lang="en-US">
    <Request>
        <RequestAction>AV</RequestAction>
    </Request>
    <Address>
        <City>North Dakhota</City>
        <StateProvinceCode>CA</StateProvinceCode>
        <CountryCode>US</CountryCode>
        <PostalCode>94089</PostalCode>
    </Address>
</AddressValidationRequest>
"""

AddressValidationResponseXML = """<?xml version="1.0"?>
<AddressValidationResponse>
   <Response>
      <TransactionReference>
         <XpciVersion>1.0001</XpciVersion>
      </TransactionReference>
      <ResponseStatusCode>1</ResponseStatusCode>
      <ResponseStatusDescription>Success</ResponseStatusDescription>
   </Response>
   <AddressValidationResult>
      <Rank>1</Rank>
      <Quality>1.0</Quality>
      <Address>
         <City>TIMONIUM</City>
         <StateProvinceCode>MD</StateProvinceCode>
      </Address>
      <PostalCodeLowEnd>21093</PostalCodeLowEnd>
      <PostalCodeHighEnd>21094</PostalCodeHighEnd>
   </AddressValidationResult>
</AddressValidationResponse>
"""
