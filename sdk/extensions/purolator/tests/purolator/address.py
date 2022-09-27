import unittest
from unittest.mock import patch
import karrio
from karrio.core.utils import DP
from karrio.core.models import AddressValidationRequest
from .fixture import gateway


class TestPurolatorAddressValidation(unittest.TestCase):
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
        with patch("karrio.mappers.purolator.proxy.http") as mock:
            mock.return_value = "<a></a>"
            karrio.Address.validate(self.AddressValidationRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/EWS/V2/ServiceAvailability/ServiceAvailabilityService.asmx",
            )

    def test_parse_address_validation_response(self):
        with patch("karrio.mappers.purolator.proxy.http") as mock:
            mock.return_value = AddressValidationResponseXML
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
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
        "carrier_id": "purolator",
        "carrier_name": "purolator",
        "complete_address": {
            "city": "Burnaby",
            "country_code": "CA",
            "postal_code": "V5E4H9",
            "residential": False,
            "state_code": "BC",
        },
        "success": True,
    },
    [],
]


AddressValidationRequestXML = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://purolator.com/pws/datatypes/v2">
    <soap:Header>
        <v2:RequestContext>
            <v2:Version>2.1</v2:Version>
            <v2:Language>en</v2:Language>
            <v2:GroupID></v2:GroupID>
            <v2:RequestReference></v2:RequestReference>
            <v2:UserToken>token</v2:UserToken>
        </v2:RequestContext>
    </soap:Header>
    <soap:Body>
        <v2:ValidateCityPostalCodeZipRequest>
            <v2:Addresses>
                <v2:ShortAddress>
                    <v2:City>Burnaby</v2:City>
                    <v2:Province>BC</v2:Province>
                    <v2:Country>CA</v2:Country>
                    <v2:PostalCode>V5E4H9</v2:PostalCode>
                </v2:ShortAddress>
            </v2:Addresses>
        </v2:ValidateCityPostalCodeZipRequest>
    </soap:Body>
</soap:Envelope>
"""

AddressValidationResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Header>
        <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <h:ResponseReference>Rating Example</h:ResponseReference>
        </h:ResponseContext>
    </s:Header>
    <s:Body>
        <ValidateCityPostalCodeZipResponse xmlns="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <ResponseInformation>
                <Errors />
                <InformationalMessages i:nil="true" />
            </ResponseInformation>
            <SuggestedAddresses>
                <SuggestedAddress>
                    <Address>
                        <City>Burnaby</City>
                        <Province>BC</Province>
                        <Country>CA</Country>
                        <PostalCode>V5E4H9</PostalCode>
                    </Address>
                    <ResponseInformation>
                        <Errors />
                        <InformationalMessages i:nil="true" />
                    </ResponseInformation>
                </SuggestedAddress>
            </SuggestedAddresses>
        </ValidateCityPostalCodeZipResponse>
    </s:Body>
</s:Envelope>
"""
