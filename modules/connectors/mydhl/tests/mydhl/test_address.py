"""MyDHL carrier address validation tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)

class TestMyDHLAddress(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = models.AddressValidationRequest(**AddressValidationPayload)

    def test_create_address_validation_request(self):
        request = gateway.mapper.create_address_validation_request(self.AddressValidationRequest)
        self.assertEqual(lib.to_dict(request.serialize()), AddressValidationRequest)

    def test_validate_address(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Address.validate(self.AddressValidationRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/address/validate"
            )

    def test_parse_address_validation_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = AddressValidationResponse
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedAddressValidationResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


AddressValidationPayload = {
    "address": {
        "address_line1": "123 Main St",
        "city": "City Name",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
    }
}

AddressValidationRequest = {
  "streetAddress": "123 Main St",
  "cityLocality": "City Name",
  "postalCode": "12345",
  "countryCode": "US",
  "stateProvince": "CA"
}

AddressValidationResponse = """{
  "isValid": true,
  "normalizedAddress": {
    "streetAddress": "123 MAIN ST",
    "cityLocality": "CITY NAME",
    "postalCode": "12345",
    "countryCode": "US",
    "stateProvince": "CA"
  },
  "validationMessages": [
    {
      "message": "Address is valid",
      "code": "SUCCESS"
    }
  ]
}"""

ErrorResponse = """{
  "error": {
    "code": "address_error",
    "message": "Unable to validate address",
    "details": "Invalid address information provided"
  }
}"""

ParsedAddressValidationResponse = [
    {
        "carrier_id": "mydhl",
        "carrier_name": "mydhl",
        "success": True
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "code": "address_error",
            "message": "Unable to validate address",
            "details": {
                "details": "Invalid address information provided"
            }
        }
    ]
]