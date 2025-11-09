"""MyDHL carrier address validation tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestMyDHLAddress(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = models.AddressValidationRequest(**AddressValidationPayload)

    def test_create_address_validation_request(self):
        request = gateway.mapper.create_address_validation_request(self.AddressValidationRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), AddressValidationRequest)

    def test_validate_address(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Address.validate(self.AddressValidationRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/address/validate"
            )

    def test_parse_address_validation_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = AddressValidationResponse
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest).from_(gateway).parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedAddressValidationResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest).from_(gateway).parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


AddressValidationPayload = {
    "address": {
        "address_line1": "123 Main Street",
        "city": "Los Angeles",
        "postal_code": "90001",
        "country_code": "US",
        "state_code": "CA",
    }
}

AddressValidationRequest = {
    "streetAddress": "123 Main Street",
    "cityLocality": "Los Angeles",
    "postalCode": "90001",
    "countryCode": "US",
    "stateProvince": "CA"
}

AddressValidationResponse = """{
  "warnings": [],
  "address": [
    {
      "postalCode": 90001,
      "cityName": "LOS ANGELES",
      "countryCode": "US",
      "countyName": "CA",
      "serviceArea": {
        "code": "LAX",
        "description": "LOS ANGELES - USA",
        "facilityCode": "LAX",
        "inboundSortCode": "LAX"
      }
    }
  ]
}"""

ErrorResponse = """{
  "status": 400,
  "title": "Bad Request",
  "detail": "Invalid address validation request - missing required field",
  "instance": "/address/validate"
}"""

ParsedAddressValidationResponse = [
    {
        "carrier_id": "mydhl",
        "carrier_name": "mydhl",
        "success": True,
        "complete_address": {
            "postal_code": "90001",
            "city": "LOS ANGELES",
            "country_code": "US",
            "state_code": "CA"
        },
        "meta": {
            "warnings": [],
            "service_area": {
                "code": "LAX",
                "description": "LOS ANGELES - USA",
                "facilityCode": "LAX",
                "inboundSortCode": "LAX"
            }
        }
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "code": "400",
            "message": "Invalid address validation request - missing required field",
            "details": {
                "instance": "/address/validate",
                "title": "Bad Request"
            }
        }
    ]
]