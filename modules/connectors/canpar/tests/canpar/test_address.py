import unittest
import logging
from unittest.mock import patch
import karrio
from karrio.core.utils import DP
from karrio.core.models import AddressValidationRequest
from .fixture import gateway


class TestCanparAddressValidation(unittest.TestCase):
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
        with patch("karrio.mappers.canpar.proxy.http") as mock:
            mock.return_value = "<a></a>"
            karrio.Address.validate(self.AddressValidationRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/CanparRatingService.CanparRatingServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"], "urn:searchCanadaPost"
            )

    def test_parse_address_validation_response(self):
        with patch("karrio.mappers.canpar.proxy.http") as mock:
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
        "address_line1": "333 Twin",
        "address_line2": "Suit 333",
        "postal_code": "V5E4H9",
        "city": "Burnaby",
        "country_code": "CA",
        "state_code": "BC",
    }
}

ParsedAddressValidationResponse = [
    {
        "carrier_id": "canpar",
        "carrier_name": "canpar",
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


AddressValidationRequestXML = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"  xmlns:ws="http://ws.onlinerating.canshipws.canpar.com" xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd" >
    <soap:Header/>
    <soap:Body>
        <ws:searchCanadaPost>
            <ws:request>
                <xsd:city>Burnaby</xsd:city>
                <xsd:password>password</xsd:password>
                <xsd:postal_code>V5E4H9</xsd:postal_code>
                <xsd:province>BC</xsd:province>
                <xsd:street_direction></xsd:street_direction>
                <xsd:street_name>Twin</xsd:street_name>
                <xsd:street_num>333</xsd:street_num>
                <xsd:street_type></xsd:street_type>
                <xsd:user_id>user_id</xsd:user_id>
                <xsd:validate_only>true</xsd:validate_only>
            </ws:request>
        </ws:searchCanadaPost>
    </soap:Body>
</soap:Envelope>
"""

AddressValidationResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
    <soapenv:Body>
        <ns:searchCanadaPostResponse xmlns:ns="http://ws.onlinerating.canshipws.canpar.com">
            <ns:return xmlns:ax25="http://ws.dto.canshipws.canpar.com/xsd" xmlns:ax27="http://dto.canshipws.canpar.com/xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax25:SearchCanadaPostRs">
                <ax25:address xsi:type="ax27:Address">
                    <ax27:address_id />
                    <ax27:address_line_1>565 SHERBOURNE ST</ax27:address_line_1>
                    <ax27:address_line_2 />
                    <ax27:address_line_3 />
                    <ax27:attention />
                    <ax27:city>TORONTO</ax27:city>
                    <ax27:country>CA</ax27:country>
                    <ax27:email />
                    <ax27:extension />
                    <ax27:id>-1</ax27:id>
                    <ax27:inserted_on>2012-06-15T15:42:40.044Z</ax27:inserted_on>
                    <ax27:name />
                    <ax27:phone />
                    <ax27:postal_code>M4X1W7</ax27:postal_code>
                    <ax27:province>ON</ax27:province>
                    <ax27:residential>false</ax27:residential>
                    <ax27:updated_on>2012-06-15T15:42:40.044Z</ax27:updated_on>
                </ax25:address>
                <ax25:error xsi:nil="true" />
            </ns:return>
        </ns:searchCanadaPostResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""
